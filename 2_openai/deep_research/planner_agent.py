from agents import Agent
from schemas import WebSearchPlan
from models import openrouter_model
from config import settings
from guardrail import soccer_only_guardrail

INSTRUCTIONS = (
    f"You are a helpful research assistant. Given a query, come up with a set of web searches "
    f"to perform to best answer the query. Output {settings.max_searches} terms to query for."
)

planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model=openrouter_model,
    output_type=WebSearchPlan,
    input_guardrails=[soccer_only_guardrail],
)
