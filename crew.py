from crewai import Crew, Process, Task

from agents.agents import build_agents, build_llm


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
- Use supplied study context when relevant.
- Do not invent information from supplied context.
- If context does not contain a requested fact,
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


def _run_with_model(
    model: str,
    api_key: str,
    route: str,
    request: str,
    context: str,
    learner: str,
    level: str,
) -> str:

    llm = build_llm(api_key, model)

    agents = build_agents(llm)

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

    # Primary model
    models = [
        model,
        "gemini-2.5-flash-lite",
    ]

    # Remove duplicates while preserving order
    models = list(dict.fromkeys(models))

    errors = []

    for current_model in models:

        try:

            return _run_with_model(
                model=current_model,
                api_key=api_key,
                route=route,
                request=request,
                context=context,
                learner=learner,
                level=level,
            )

        except Exception as exc:

            error_text = str(exc)

            errors.append(
                f"{current_model}: {error_text}"
            )

            # Continue to fallback model
            continue

    raise RuntimeError(
        "All configured Gemini models were unavailable.\n\n"
        + "\n\n".join(errors)
    )
