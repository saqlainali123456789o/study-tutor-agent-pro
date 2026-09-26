import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    .hero{padding:1.4rem 1.6rem;border-radius:20px;background:linear-gradient(135deg,#182848,#4b6cb7);color:white;margin-bottom:1rem}
    .hero h1{margin:0;font-size:2.2rem}.hero p{margin:.45rem 0 0;opacity:.9}
    .pill{display:inline-block;padding:.3rem .7rem;border-radius:999px;background:rgba(255,255,255,.16);font-size:.85rem;margin-top:.7rem}
    .card{padding:1rem;border:1px solid rgba(128,128,128,.25);border-radius:16px;margin:.5rem 0}
    .small{font-size:.82rem;opacity:.75}
    </style>
    """, unsafe_allow_html=True)
