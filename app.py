import streamlit as st
from config import APP_NAME, APP_VERSION, get_gemini_api_key, get_gemini_model, get_embedding_model, validate_configuration
from state import init_state
from ui.styles import inject_css
from rag.ingest import build_chunks
from rag.vector_store import GeminiVectorStore
from crew import choose_route, run_route

st.set_page_config(page_title=APP_NAME, page_icon="🎓", layout="wide")
init_state(st)
inject_css()

st.markdown(f"""
<div class='hero'>
<h1>🎓 {APP_NAME}</h1>
<p>A multi-agent learning system that plans, teaches, researches, assesses, evaluates, and adapts.</p>
<div class='pill'>● Agent Orchestrator Connected · v{APP_VERSION}</div>
</div>
""", unsafe_allow_html=True)

ok, message = validate_configuration()
if not ok:
    st.error(message)
    st.stop()

api_key = get_gemini_api_key()
model = get_gemini_model()

with st.sidebar:
    st.header("Study Setup")
    st.session_state.subject = st.text_input("Subject", st.session_state.subject)
    st.session_state.study_level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"], index=["Beginner","Intermediate","Advanced"].index(st.session_state.study_level))
    st.session_state.learning_goal = st.text_area("Learning goal", st.session_state.learning_goal)
    st.divider()
    st.subheader("Knowledge Base")
    uploads = st.file_uploader("Upload study material", type=["pdf", "docx", "txt", "md"], accept_multiple_files=True)
    if uploads:
        if st.button("Build Knowledge Base", use_container_width=True):
            with st.spinner("Extracting, chunking and embedding documents..."):
                store = GeminiVectorStore(api_key, get_embedding_model())
                total = 0
                for f in uploads:
                    chunks = build_chunks(f.name, f.getvalue())
                    store.add(chunks)
                    st.session_state.documents.append({"name": f.name, "chunks": len(chunks)})
                    total += len(chunks)
                st.session_state.vector_store = store
            st.success(f"Knowledge Base ready · {total} chunks")
    if st.session_state.documents:
        st.caption("Uploaded in this Streamlit session; not stored in GitHub.")
        for d in st.session_state.documents:
            st.write(f"• {d['name']} — {d['chunks']} chunks")
    st.divider()
    st.subheader("Learning Modes")
    st.caption("The Manager Agent selects the workflow automatically, or you can mention: practice, evaluate, revise, plan, case study, Socratic, notes, flashcards, or exam.")

left, right = st.columns([2.2, 1])
with right:
    st.markdown("### Agent Status")
    for label in ["Manager / Orchestrator", "Teacher", "Knowledge", "Research", "Assessment", "Evaluator", "Revision", "Planner", "Case Study", "Socratic", "Notes", "Flashcards", "Exam"]:
        st.markdown(f"<div class='card'>🟢 {label}</div>", unsafe_allow_html=True)
    st.markdown("### Progress")
    if st.session_state.mastery:
        for concept, data in st.session_state.mastery.items():
            st.progress(min(1.0, data["score"]), text=f"{concept}: {data['score']:.0%}")
    else:
        st.caption("No mastery data yet.")

with left:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("What do you want to learn or practice today?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        context = ""
        store = st.session_state.vector_store
        if store:
            context = store.context(prompt, 6)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Manager Agent is routing your request..."):
                    route = choose_route(api_key, model, prompt, context)
                st.session_state.last_route = route
                st.caption(f"Workflow: {route}")
                with st.spinner("Specialist agent is working..."):
                    answer = run_route(route, api_key, model, prompt, context, st.session_state.learning_goal, st.session_state.study_level)
                st.markdown(answer)
                if context and route in {"KNOWLEDGE", "TEACH", "NOTES", "REVISION", "CASE_STUDY"}:
                    with st.expander("📚 Retrieved study sources"):
                        st.text(context)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as exc:
                st.error(f"The agent workflow could not complete: {exc}")
                st.info("Check the Streamlit Secrets and deployment logs. The app does not require a local environment.")
