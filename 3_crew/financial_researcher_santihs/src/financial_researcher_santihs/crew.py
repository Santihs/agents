from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

@CrewBase
class FinancialResearcherSantihs():
    """FinancialResearcherSantihs crew"""

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'], verbose=True, tools=[SerperDevTool(), ScrapeWebsiteTool()])

    @agent
    def analyst(self) -> Agent:
        return Agent(config=self.agents_config['analyst'], verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def analyst_task(self) -> Task:
        return Task(config=self.tasks_config['analyst_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )