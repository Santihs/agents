import asyncio
import logging

from pydantic import BaseModel
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput
from models import ollama_guardrail_model
from config import settings

logger = logging.getLogger(__name__)


class TopicCheckOutput(BaseModel):
    is_on_topic: bool
    reason: str


# Runs locally via Ollama — fast, free, offline
_topic_checker = Agent(
    name="Topic checker",
    instructions=(
        "Your only job is to decide if the user's research query is about music. "
        "This includes: artists, bands, albums, songs, genres, concerts, music history, "
        "music theory, instruments, record labels, music industry, streaming, lyrics, composers. "
        "Set is_on_topic=True ONLY if the query is clearly about music. "
        "Everything else — sports, science, politics, technology, cooking — must be False."
    ),
    output_type=TopicCheckOutput,
    model=ollama_guardrail_model,
)

_FAIL_OPEN = GuardrailFunctionOutput(
    output_info={"reason": "guardrail skipped — failing open"},
    tripwire_triggered=False,
)


@input_guardrail
async def soccer_only_guardrail(ctx, agent, message):
    """Block any research query that is not about soccer/football.

    Fails open on timeout or error — guardrail must never become a hard dependency.
    """
    try:
        result = await asyncio.wait_for(
            Runner.run(_topic_checker, message, context=ctx.context),
            timeout=settings.guardrail_timeout,
        )
    except asyncio.TimeoutError:
        logger.warning("Guardrail timed out after %.1fs — failing open", settings.guardrail_timeout)
        return _FAIL_OPEN
    except Exception as e:
        logger.warning("Guardrail error: %s — failing open", e)
        return _FAIL_OPEN

    output = result.final_output
    logger.info(
        "Guardrail: is_on_topic=%s reason=%r",
        output.is_on_topic,
        output.reason,
    )

    return GuardrailFunctionOutput(
        output_info={"reason": output.reason},
        tripwire_triggered=not output.is_on_topic,
    )
