import asyncio

from ddgs import DDGS
from agents import Agent, function_tool, ModelSettings
from models import groq_model


def _ddgs_search(query: str) -> list[dict]:
    """Sync DDGS call — must be run in a thread to avoid blocking the event loop."""
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=5))


@function_tool
async def web_search(query: str) -> str:
    """Search the web for the given query and return summarized results."""
    results = await asyncio.to_thread(_ddgs_search, query)
    return "\n\n".join(
        f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}"
        for r in results
    )


INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[web_search],
    model=groq_model,
    model_settings=ModelSettings(tool_choice="required"),
)
