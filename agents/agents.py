from crewai import Agent, LLM

from prompts import *
from tools.calculator import CalculatorTool
from tools.web_search import WebSearchTool


def build_llm(api_key: str, model: str):
    return LLM(
        model=f"gemini/{model}",
        api_key=api_key,
        temperature=0.2,
        max_tokens=5000,
    )


def build_agents(llm):

    calculator = CalculatorTool()
    web_search = WebSearchTool()

    agents = {

        "manager": Agent(
            role="Study Tutor Manager / Orchestrator",
            goal=(
                "Understand the student's learning need and route "
                "the task to the appropriate specialist."
            ),
            backstory=MANAGER_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "teacher": Agent(
            role="Expert Teacher",
            goal="Teach concepts deeply and clearly.",
            backstory=TEACHER_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "research": Agent(
            role="Academic Research Agent",
            goal="Find and explain reliable external information.",
            backstory=RESEARCH_SYSTEM,
            tools=[web_search],
            llm=llm,
            verbose=False,
        ),

        "assessment": Agent(
            role="Assessment Designer",
            goal="Create useful educational practice questions.",
            backstory=ASSESSMENT_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "evaluator": Agent(
            role="Student Answer Evaluator",
            goal="Evaluate student answers and identify misconceptions.",
            backstory=EVALUATOR_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "revision": Agent(
            role="Revision Specialist",
            goal="Help students strengthen weak concepts.",
            backstory=REVISION_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "planner": Agent(
            role="Learning Planner",
            goal="Create realistic personalized learning plans.",
            backstory=PLANNER_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "case": Agent(
            role="Case Study Instructor",
            goal="Connect theory with realistic cases.",
            backstory=CASE_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "socratic": Agent(
            role="Socratic Tutor",
            goal="Guide students through reasoning using questions.",
            backstory=SOCRATIC_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "notes": Agent(
            role="Study Notes Specialist",
            goal="Create structured and useful study notes.",
            backstory=NOTES_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "flashcards": Agent(
            role="Flashcard Specialist",
            goal="Create high-quality active-recall flashcards.",
            backstory=FLASHCARD_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "exam": Agent(
            role="Exam Preparation Specialist",
            goal="Prepare students through diagnosis, practice and evaluation.",
            backstory=EXAM_SYSTEM,
            llm=llm,
            verbose=False,
        ),

        "calculator": Agent(
            role="Educational Calculator",
            goal="Perform accurate mathematical calculations.",
            backstory=(
                "You are a precise educational calculator. "
                "Use the calculator tool for mathematical operations. "
                "Show the reasoning clearly when appropriate."
            ),
            tools=[calculator],
            llm=llm,
            verbose=False,
        ),
    }

    return agents
