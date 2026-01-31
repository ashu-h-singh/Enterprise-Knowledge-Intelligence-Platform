import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# Config
# -----------------------------
API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="EKIP | Enterprise Knowledge Intelligence Platform",
    layout="centered"
)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <h1 style="margin-bottom: 0;">EKIP</h1>
    <p style="color: gray; margin-top: 0;">
        Enterprise Knowledge Intelligence Platform
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Sidebar – User Context (RBAC)
# -----------------------------
with st.sidebar:
    st.header("User Context")

    username = st.text_input(
        "Username",
        value="ashu_user"
    )

    role = st.selectbox(
        "Role",
        options=["user", "admin"]
    )

    st.caption(
        "Access control is enforced at retrieval time.\n"
        "The LLM never sees unauthorized documents."
    )

user_context = {
    "username": username,
    "role": role
}

# -----------------------------
# Main – Question Input
# -----------------------------
st.subheader("Ask a Question")

question = st.text_area(
    label="",
    placeholder="Example: What is the password rotation policy?",
    height=100
)

ask_clicked = st.button("Ask", type="primary")

# -----------------------------
# API Call
# -----------------------------
if ask_clicked:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        payload = {
            "question": question,
            "user": user_context
        }

        with st.spinner("Retrieving knowledge and generating answer..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=120)
                response.raise_for_status()
                data = response.json()

                # -----------------------------
                # Answer
                # -----------------------------
                st.subheader("Answer")
                st.write(data["answer"])

                # -----------------------------
                # Sources
                # -----------------------------
                if data.get("sources"):
                    st.subheader("Sources")
                    for src in data["sources"]:
                        st.markdown(f"- `{src}`")

                # -----------------------------
                # Metadata
                # -----------------------------
                st.caption(
                    f"Answered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                    f"| Role: {role}"
                )

            except requests.exceptions.Timeout:
                st.error("The request timed out. The model may still be generating.")
            except requests.exceptions.RequestException as e:
                st.error(f"Backend error: {e}")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(
    "Powered by FastAPI, FAISS, Ollama (LLaMA-3), and Streamlit • "
    "Secure RAG with RBAC & hallucination control"
)
