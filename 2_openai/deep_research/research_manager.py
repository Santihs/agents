import asyncio
import logging
from typing import AsyncGenerator

from agents import Runner, trace, gen_trace_id
from agents.exceptions import InputGuardrailTripwireTriggered
from tenacity import AsyncRetrying, wait_exponential, stop_after_attempt

from search_agent import search_agent
from planner_agent import planner_agent
from writer_agent import writer_agent
from email_agent import email_agent
from schemas import WebSearchItem, WebSearchPlan, ReportData
from config import settings

logger = logging.getLogger(__name__)


class ResearchManager:

    async def run(self, query: str, deliver: bool = True) -> AsyncGenerator[str, None]:
        """Run the deep research pipeline, yielding status updates then the final report."""
        if deliver and not settings.sendgrid_api_key:
            yield "Email delivery requested but SENDGRID_API_KEY is not configured. Disabling delivery."
            deliver = False

        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield "Starting research..."

            try:
                search_plan = await self.plan_searches(query)
            except InputGuardrailTripwireTriggered:
                yield "Blocked: this tool only researches music topics. Please try a music-related query."
                return

            yield f"Searches planned ({len(search_plan.searches)}), starting to search..."

            search_results = await self.perform_searches(search_plan)
            yield f"Searches complete ({len(search_results)} results), writing report..."

            try:
                report = await self.write_report(query, search_results)
            except Exception:
                yield "Failed to generate the report. The writer agent encountered an error — please try again."
                return

            if deliver:
                yield "Report written, sending email..."
                await self._deliver(report)
                yield "Email sent, research complete"
            else:
                yield "Report written"

            yield _format_report(report)

    async def plan_searches(self, query: str) -> WebSearchPlan:
        logger.info("Planning searches for query=%r", query)
        result = await Runner.run(planner_agent, f"Query: {query}")
        plan = result.final_output_as(WebSearchPlan)
        logger.info("Planned %d searches", len(plan.searches))
        return plan

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        sem = asyncio.Semaphore(settings.max_concurrent_searches)

        async def bounded_search(item: WebSearchItem) -> str | None:
            async with sem:
                return await self.search(item)

        tasks = [asyncio.create_task(bounded_search(item)) for item in search_plan.searches]
        results: list[str] = []
        num_completed = 0

        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            logger.info("Search progress: %d/%d", num_completed, len(tasks))

        logger.info("Searches done: %d/%d succeeded", len(results), len(tasks))
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            async for attempt in AsyncRetrying(
                wait=wait_exponential(
                    multiplier=1,
                    min=settings.search_retry_min_wait,
                    max=settings.search_retry_max_wait,
                ),
                stop=stop_after_attempt(settings.search_max_retries),
            ):
                with attempt:
                    result = await Runner.run(search_agent, input_text)
                    return str(result.final_output)
        except Exception:
            logger.warning("Search exhausted retries for query=%r", item.query, exc_info=True)
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        logger.info("Writing report...")
        input_text = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input_text)
        logger.info("Report written")
        return result.final_output_as(ReportData)

    async def _deliver(self, report: ReportData) -> None:
        logger.info("Sending email...")
        await Runner.run(email_agent, report.markdown_report)
        logger.info("Email sent")


def _format_report(report: ReportData) -> str:
    """Assemble all ReportData fields into a single markdown string for display."""
    followups = "\n".join(f"- {q}" for q in report.follow_up_questions)
    return (
        f"> {report.short_summary}\n\n"
        f"---\n\n"
        f"{report.markdown_report}\n\n"
        f"---\n\n"
        f"## Suggested Follow-up Topics\n\n"
        f"{followups}"
    )
