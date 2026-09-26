from crewai import Agent, LLM
from ..prompts import *
from ..tools.calculator import CalculatorTool
from ..tools.web_search import WebSearchTool


def build_llm(api_key: str, model: str) -> LLM:
    return LLM(model=f"gemini/{model}", api_key=api_key, temperature=0.2, max_tokens=5000)


def build_agents(llm: LLM) -> dict[str, Agent]:
    return {
        "manager": Agent(role="Study Tutor Manager", goal="Route each learner request to the right specialist workflow.", backstory=MANAGER_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "teacher": Agent(role="Expert Teacher", goal="Teach concepts deeply and clearly using a structured pedagogy.", backstory=TEACHER_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "research": Agent(role="Research Analyst", goal="Find and synthesize trustworthy external evidence when needed.", backstory=RESEARCH_SYSTEM, llm=llm, tools=[WebSearchTool()], allow_delegation=False, verbose=False),
        "assessment": Agent(role="Assessment Designer", goal="Generate high-quality learning assessments.", backstory=ASSESSMENT_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "evaluator": Agent(role="Learning Evaluator", goal="Diagnose understanding, missing knowledge, and misconceptions.", backstory=EVALUATOR_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "revision": Agent(role="Revision Coach", goal="Create targeted revision from weak areas.", backstory=REVISION_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "planner": Agent(role="Learning Planner", goal="Create adaptive study sequences and schedules.", backstory=PLANNER_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "case": Agent(role="Case Study Tutor", goal="Apply theory to realistic cases and scenarios.", backstory=CASE_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "socratic": Agent(role="Socratic Tutor", goal="Guide learners through reasoning with purposeful questions.", backstory=SOCRATIC_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "notes": Agent(role="Study Notes Specialist", goal="Create structured notes for learning and revision.", backstory=NOTES_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "flashcards": Agent(role="Flashcard Specialist", goal="Create active-recall flashcards.", backstory=FLASHCARD_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "exam": Agent(role="Exam Preparation Agent", goal="Coordinate diagnosis, revision, practice, and mock assessment.", backstory=EXAM_SYSTEM, llm=llm, allow_delegation=False, verbose=False),
        "calculator": Agent(role="Quantitative Tutor", goal="Explain quantitative solutions using deterministic calculations.", backstory="Solve quantitative learning problems carefully and explain each step. Use the calculator tool for arithmetic.", llm=llm, tools=[CalculatorTool()], allow_delegation=False, verbose=False),
    }
