from crewai import Crew, Process, Task
from .agents.agents import build_agents

ROUTES = {
    "TEACH": "teacher", "KNOWLEDGE": "teacher", "RESEARCH": "research", "PRACTICE": "assessment",
    "EVALUATE": "evaluator", "REVISION": "revision", "PLAN": "planner", "CASE_STUDY": "case",
    "SOCRATIC": "socratic", "NOTES": "notes", "FLASHCARDS": "flashcards", "EXAM": "exam", "CALCULATE": "calculator",
}


def _task_for(route: str, agent, request: str, context: str, learner: str, level: str) -> Task:
    instructions = f"""
Student level: {level}
Learner profile: {learner}
Student request: {request}
Grounded study context, if available:
{context}

Complete the task for route {route}. Keep the response useful and structured. If the source context does not contain the requested fact, do not pretend it does.
"""
    return Task(description=instructions, expected_output="A clear, educational response suitable for the learner.", agent=agent)


def run_route(route: str, api_key: str, model: str, request: str, context: str = "", learner: str = "", level: str = "Intermediate") -> str:
    agents = build_agents(__import__("study_tutor_agent.agents.agents", fromlist=["build_llm"]).build_llm(api_key, model))
    key = ROUTES.get(route, "teacher")
    task = _task_for(route, agents[key], request, context, learner, level)
    crew = Crew(agents=[agents[key]], tasks=[task], process=Process.sequential, verbose=False)
    result = crew.kickoff()
    return getattr(result, "raw", str(result))


def choose_route(api_key: str, model: str, request: str, context_hint: str = "") -> str:
    agents = build_agents(__import__("study_tutor_agent.agents.agents", fromlist=["build_llm"]).build_llm(api_key, model))
    task = Task(description=f"Student request: {request}\nUploaded material available: {bool(context_hint)}\nReturn only one route token.", expected_output="One route token.", agent=agents["manager"])
    crew = Crew(agents=[agents["manager"]], tasks=[task], process=Process.sequential, verbose=False)
    result = crew.kickoff()
    route = getattr(result, "raw", str(result)).strip().upper().split()[0]
    return route if route in ROUTES else "TEACH"
