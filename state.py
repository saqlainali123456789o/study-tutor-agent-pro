def init_state(st):
    defaults = {
        "messages": [], "documents": [], "vector_store": None, "mastery": {}, "last_route": None,
        "study_level": "Intermediate", "subject": "General", "learning_goal": "Understand concepts deeply",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def record_mastery(st, concept: str, score: float):
    old = st.session_state.mastery.get(concept, {"attempts": 0, "score": 0.0})
    attempts = old["attempts"] + 1
    avg = ((old["score"] * old["attempts"]) + score) / attempts
    st.session_state.mastery[concept] = {"attempts": attempts, "score": round(avg, 3)}
