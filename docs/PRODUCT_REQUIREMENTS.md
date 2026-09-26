# Product Requirements — Study Tutor Agent

## Goal
Create a professional agent-based tutor that supports deep learning rather than simple conversational Q&A.

## User journey
1. Student selects subject, level, and goal.
2. Student optionally uploads study material.
3. Manager identifies the learning need.
4. Specialist agent executes the workflow.
5. Learner receives explanation, evidence, questions, or feedback.
6. Mastery state is updated when assessment occurs.
7. System recommends revision or the next concept.

## Functional requirements

- Deep concept teaching
- Prerequisite identification
- Definition-first explanations
- Everyday and academic examples
- Case-study learning
- Uploaded-document grounding
- Semantic + keyword retrieval
- Current web research when needed
- Source display
- Practice generation
- Answer evaluation
- Adaptive revision
- Study planning
- Notes
- Flashcards
- Exam preparation
- Socratic mode
- Quantitative calculation
- Session memory
- Mastery tracking

## Non-functional requirements

- Cloud-first deployment
- Secrets outside source control
- Modular architecture
- Clear agent responsibilities
- Deterministic calculation where possible
- Grounded document answers
- Error messages that are actionable
- No requirement for local execution

## Acceptance criteria

The deployed app must:

1. Start successfully on Streamlit Community Cloud.
2. Load Gemini credentials from Streamlit Secrets.
3. Display the professional tutor UI.
4. Route requests through the Manager Agent.
5. Execute a specialist agent workflow.
6. Accept supported study documents.
7. Build an in-memory FAISS knowledge base.
8. Show retrieved source context when document grounding is used.
9. Generate practice and evaluate learner responses.
10. Avoid committing secrets or local runtime artifacts.
