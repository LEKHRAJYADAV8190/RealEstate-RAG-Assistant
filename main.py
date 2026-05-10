# Generated from: main.ipynb
# Converted at: 2026-05-10T12:56:34.788Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

# @Author: Dhaval Patel Copyrights Codebasics Inc. and LearnerX Pvt Ltd.

import streamlit as st

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Real Estate Research Tool",
    page_icon="🏡",
    layout="wide"
)

from rag import process_urls, generate_answer

# =========================================================
# UI
# =========================================================

st.title("🏡 Real Estate Research Tool")

# =========================================================
# SESSION STATE
# =========================================================

if "url_count" not in st.session_state:
    st.session_state.url_count = 1

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("📄 Add Article URLs")

col1, col2 = st.sidebar.columns(2)

with col1:

    if st.button("➕ Add URL"):

        st.session_state.url_count += 1

with col2:

    if st.session_state.url_count > 1:

        if st.button("➖ Remove"):

            st.session_state.url_count -= 1

# =========================================================
# URL INPUTS
# =========================================================

urls = []

for i in range(st.session_state.url_count):

    url = st.sidebar.text_input(
        label=f"URL {i+1}",
        placeholder="https://example.com/article",
        key=f"url_{i}"
    )

    if url.strip():

        urls.append(url.strip())

# =========================================================
# PROCESS URLS
# =========================================================

process_url_button = st.sidebar.button(
    "🚀 Process URLs",
    use_container_width=True
)

status_placeholder = st.empty()

if process_url_button:

    if not urls:

        status_placeholder.warning(
            "⚠️ Please provide at least one valid URL"
        )

    else:

        try:

            with st.spinner("🔄 Processing articles..."):

                process_urls(urls)

            status_placeholder.success(
                f"✅ Successfully processed {len(urls)} article(s)"
            )

        except Exception as e:

            st.error(f"❌ Error:\n{str(e)}")

# =========================================================
# QUESTION INPUT
# =========================================================

st.markdown("---")

query = st.text_input(
    "💬 Ask Question",
    placeholder="Ask anything about the processed articles..."
)

# =========================================================
# GENERATE ANSWER
# =========================================================

if query:

    try:

        with st.spinner("🤖 Generating answer..."):

            answer, sources = generate_answer(query)

        st.header("📌 Answer")

        st.write(answer)

        # =================================================
        # SOURCES
        # =================================================

        if sources:

            st.subheader("📚 Sources")

            for idx, source in enumerate(sources, start=1):

                st.markdown(f"**{idx}.** {source}")

    except Exception as e:

        st.error(f"❌ Error:\n{str(e)}")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption("Built with Streamlit + LangChain + Groq 🚀")