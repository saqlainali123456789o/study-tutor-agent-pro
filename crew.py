from crewai import Crew, Process, Task

from agents.agents import build_agents
from config import get_gemini_api_key, get_gemini_model


ROUTES = {
    "TEACH": "teacher",
    "KNOWLEDGE": "teacher",
    "RESEARCH": "research",
    "PRACTICE": "assessment",
    "EVALUATE": "evaluator",
    "REVISION": "revision",
    "PLAN": "planner",
    "CASE_STUDY": "case",
    "SOCRATIC": "socratic",
    "NOTES": "notes",
    "FLASHCARDS": "flashcards",
    "EXAM": "exam",
    "CALCULATE": "calculator",
}


def choose_route(
    api_key: str,
    model: str,
    request: str,
    context: str = "",
) -> str:
    """
    Select the appropriate learning workflow.

    This deterministic router handles obvious requests first.
    """

    text = request.lower().strip()

    if any(word in text for word in [
        "calculate",
        "calculation",
        "solve",
        "equation",
        "algebra",
        "statistics",
        "statistic",
        "finance",
        "accounting",
        "percentage",
        "percent",
        "formula",
    ]):
        return "CALCULATE"

    if any(word in text for word in [
        "flashcard",
        "flash cards",
        "flash-cards",
    ]):
        return "FLASHCARDS"

    if any(word in text for word in [
        "mock exam",
        "mock test",
        "exam preparation",
        "exam prep",
        "prepare for exam",
    ]):
        return "EXAM"

    if any(word in text for word in [
        "socratic",
        "guide me with questions",
        "don't give me the answer",
        "do not give me the answer",
    ]):
        return "SOCRATIC"

    if any(word in text for word in [
        "case study",
        "business scenario",
        "real world scenario",
        "real-world scenario",
        "scenario",
    ]):
        return "CASE_STUDY"

    if any(word in text for word in [
        "study plan",
        "study schedule",
        "learning plan",
        "schedule my study",
        "study roadmap",
    ]):
        return "PLAN"

    if any(word in text for word in [
        "revise",
        "revision",
        "review this weak",
        "weak concept",
        "help me review",
    ]):
        return "REVISION"

    if any(word in text for word in [
        "check my answer",
        "check my solution",
        "is my answer correct",
        "evaluate my answer",
        "evaluate this answer",
    ]):
        return "EVALUATE"

    if any(word in text for word in [
        "practice questions",
        "practice question",
        "give me questions",
        "generate questions",
        "quiz me",
        "practice",
    ]):
        return "PRACTICE"

    if any(word in text for word in [
        "notes",
        "make notes",
        "study notes",
        "summary",
        "summarize",
    ]):
        return "NOTES"

    if any(word in text for word in [
        "research",
        "latest",
        "recent",
        "current",
        "academic sources",
        "research paper",
        "recent studies",
    ]):
        return "RESEARCH"

    if context.strip():
        return "KNOWLEDGE"

    return "TEACH"


def _task_for(
    route: str,
    agent,
    request: str,
    context: str,
    learner: str,
    level: str,
) -> Task:

    instructions = f"""
Student level:
{level}

Learner profile:
{learner}

Student request:
{request}

Grounded study context:
{context}

Workflow:
{route}

Complete the student's learning task using the workflow above.

Important requirements:
- Be accurate.
- Explain clearly.
- Adapt to the student's level.
- Use the supplied study context when it is relevant.
- Do not invent information from the supplied context.
- If the supplied context does not contain a requested fact,
  clearly distinguish that from general knowledge.
"""

    return Task(
        description=instructions,
        expected_output=(
            "A clear, accurate, structured educational response "
            "appropriate for the student's level."
        ),
        agent=agent,
    )


def run_route(
    route: str,
    api_key: str,
    model: str,
    request: str,
    context: str,
    learner: str,
    level: str,
) -> str:

    route = route.upper().strip()

    if route not in ROUTES:
        route = "TEACH"

    agents = build_agents(
        __import__("agents.agents", fromlist=["build_llm"])
        .build_llm(api_key, model)
    )

    agent_name = ROUTES[route]
    agent = agents[agent_name]

    task = _task_for(
        route=route,
        agent=agent,
        request=request,
        context=context,
        learner=learner,
        level=level,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)
