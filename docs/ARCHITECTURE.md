# Study Tutor Agent — Architecture

## Product definition

Study Tutor Agent is a multi-agent learning system that plans, teaches, retrieves study material, researches when needed, generates assessments, evaluates learner understanding, tracks mastery, adapts difficulty, and recommends the next learning activity.

## Runtime flow

Student → Streamlit UI → Manager/Orchestrator → selected specialist agent → tools/RAG → response → progress state → next activity.

## Agent responsibilities

### Manager / Orchestrator
Determines the learner's immediate need and selects the smallest useful workflow.

### Teacher
Provides structured teaching from prerequisites through definitions, deep explanation, examples, applications, misconceptions, checks, and next concepts.

### Knowledge / RAG
Retrieves relevant passages from uploaded study material. Metadata includes source and page where available.

### Research
Searches the public web for current/external information and synthesizes evidence.

### Assessment
Creates MCQs, short answers, long answers, true/false, numerical, scenario, and case questions.

### Evaluator
Diagnoses correct understanding, missing knowledge, and misconceptions.

### Revision
Builds targeted revision from weak areas.

### Planner
Creates study sequences and schedules based on goals, level, time, and weak areas.

### Case Study
Connects theory to realistic scenarios and decision-making.

### Socratic
Uses guided questioning to develop reasoning instead of immediately revealing the answer.

### Notes
Creates structured study notes.

### Flashcards
Creates active-recall cards.

### Exam
Coordinates diagnostic assessment, targeted learning, practice, mock assessment, evaluation, and revision.

### Calculator
Uses deterministic arithmetic for quantitative subjects.

## RAG design

Documents are extracted in memory. Chunks use overlap. Gemini embeddings are generated through the API. FAISS runs in memory for the active session. Hybrid scoring combines semantic similarity and keyword overlap.

## Memory design

The MVP uses Streamlit session state for conversation and mastery. No local database is required. Persistent cross-device memory is a future integration with an external database.

## Model design

CrewAI orchestrates specialist agents. Gemini is the primary model. The model identifier is configurable through Streamlit Secrets.
