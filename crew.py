from crewai import Crew, Process, Task
from agents.agents import build_agents


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


def _task_for(
    route: str,
    agent,
    request: str,
    context: str,
    learner: str,
    level: str,
) -> Task:

    instructions = f"""
Student level: {level}

Learner profile:
{learner}

Student request:
{request}

Grounded study context, if available:
{context}

Complete the task for route {route}.

Keep the response useful, structured, accurate, and educational.

If the source context does not contain the requested fact,
do not pretend that it does.
"""

    return Task(
        description=instructions,
        expected_output="A clear, accurate, structured educational response.",
        agent=agent,
    )
