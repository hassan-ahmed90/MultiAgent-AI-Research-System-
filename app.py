import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multiagent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.35em;
    color: #6ef0c8;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2rem, 5vw, 3.6rem);
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 30%, #6ef0c8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem;
}
.hero-sub {
    font-size: 1rem;
    color: #888;
    font-weight: 400;
}

/* ── Divider ── */
.h-divider {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 0.5rem 0 2rem;
}

/* ── Input card ── */
.input-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
}

/* ── Step indicators ── */
.steps-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.step-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 999px;
    padding: 0.45rem 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #555;
    transition: all 0.3s ease;
}
.step-chip.active {
    border-color: #6ef0c8;
    color: #6ef0c8;
    box-shadow: 0 0 12px rgba(110, 240, 200, 0.2);
}
.step-chip.done {
    border-color: #2a2a3e;
    color: #6ef0c8;
    background: #0d1a15;
}
.step-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: currentColor;
}

/* ── Result cards ── */
.result-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.result-card.search::before  { background: linear-gradient(90deg, #6ef0c8, #3bb8f0); }
.result-card.scraped::before { background: linear-gradient(90deg, #f0c86e, #f07a6e); }
.result-card.report::before  { background: linear-gradient(90deg, #c86ef0, #6ef0c8); }
.result-card.critic::before  { background: linear-gradient(90deg, #f06e6e, #f0c86e); }

.card-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    border: 1px solid;
}
.badge-search  { color: #6ef0c8; border-color: #6ef0c8; background: rgba(110,240,200,0.07); }
.badge-scraped { color: #f0c86e; border-color: #f0c86e; background: rgba(240,200,110,0.07); }
.badge-report  { color: #c86ef0; border-color: #c86ef0; background: rgba(200,110,240,0.07); }
.badge-critic  { color: #f07a6e; border-color: #f07a6e; background: rgba(240,122,110,0.07); }

.card-content {
    font-size: 0.9rem;
    line-height: 1.75;
    color: #c8c8d8;
    white-space: pre-wrap;
    font-family: 'Space Mono', monospace;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
    background: #0d0d14 !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #6ef0c8 !important;
    box-shadow: 0 0 0 2px rgba(110,240,200,0.15) !important;
}
.stTextInput > label {
    color: #888 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em;
}

.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #6ef0c8, #3bb8f0) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2.5rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
    letter-spacing: 0.05em;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active, .stDownloadButton > button:active {
    transform: translateY(0) !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #6ef0c8, #3bb8f0) !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #6ef0c8 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #111118 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 10px !important;
    color: #888 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* Alerts */
.stAlert {
    background: #111118 !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-label">⬡ Research Suite</div>
  <h1 class="hero-title">Multiagent Research<br>System</h1>
  <p class="hero-sub">Search → Scrape → Write → Critique — fully automated.</p>
</div>
<hr class="h-divider"/>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
col_in, col_btn = st.columns([4, 1], vertical_alignment="bottom")

with col_in:
    topic = st.text_input(
        "RESEARCH TOPIC",
        placeholder="e.g.  Agentic AI in 2025 — latest breakthroughs",
        key="topic_input",
    )

with col_btn:
    run_btn = st.button("Run Pipeline →", use_container_width=True)


# ── Pipeline execution ────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
        st.stop()

    steps = [
        ("🔍", "Search Agent"),
        ("📄", "Reader Agent"),
        ("✍️",  "Writer Chain"),
        ("🧠", "Critic Chain"),
    ]

    # Step indicator row (all idle at start)
    step_placeholder = st.empty()

    def render_steps(active_idx: int, done_up_to: int):
        html = '<div class="steps-row">'
        for i, (icon, label) in enumerate(steps):
            cls = "done" if i < done_up_to else ("active" if i == active_idx else "")
            html += f'<div class="step-chip {cls}"><span class="step-dot"></span>{icon} {label}</div>'
        html += "</div>"
        step_placeholder.markdown(html, unsafe_allow_html=True)

    render_steps(0, 0)

    progress = st.progress(0, text="Starting pipeline…")
    state = {}

    try:
        # ── Step 1: Search ──────────────────────────────────────────────────
        render_steps(0, 0)
        progress.progress(10, text="Step 1 — Search Agent is working…")

        from agents import build_search_agent
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state['search_results'] = search_result['messages'][-1].content
        render_steps(1, 1)
        progress.progress(30, text="Step 1 complete ✓")

        # ── Step 2: Reader ──────────────────────────────────────────────────
        render_steps(1, 1)
        progress.progress(40, text="Step 2 — Reader Agent scraping content…")

        from agents import build_reader_agent
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state['scraped_content'] = reader_result['messages'][-1].content
        render_steps(2, 2)
        progress.progress(55, text="Step 2 complete ✓")

        # ── Step 3: Writer ──────────────────────────────────────────────────
        render_steps(2, 2)
        progress.progress(65, text="Step 3 — Writer drafting report…")

        from agents import writer_chain
        research_combined = (
            f"Search Results:\n{state['search_results']}\n\n"
            f"Detailed Scraped Content:\n{state['scraped_content']}"
        )
        state['report'] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })
        render_steps(3, 3)
        progress.progress(80, text="Step 3 complete ✓")

        # ── Step 4: Critic ──────────────────────────────────────────────────
        render_steps(3, 3)
        progress.progress(90, text="Step 4 — Critic evaluating report…")

        from agents import critic_chain
        state['feedback'] = critic_chain.invoke({
            "report": state['report']
        })
        render_steps(4, 4)
        progress.progress(100, text="Pipeline complete ✓")
        render_steps(-1, 4)

    except Exception as e:
        progress.empty()
        st.error(f"Pipeline error: {e}")
        st.stop()

    time.sleep(0.4)
    progress.empty()

    # ── Results ───────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Results")
    st.markdown("<hr class='h-divider'/>", unsafe_allow_html=True)

    # Search Results
    with st.expander("🔍  Search Results", expanded=False):
        st.markdown(f"""
        <div class="result-card search">
            <div class="card-badge badge-search">● Search Agent Output</div>
            <div class="card-content">{state.get('search_results', 'No results.')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Scraped Content
    with st.expander("📄  Scraped Web Content", expanded=False):
        st.markdown(f"""
        <div class="result-card scraped">
            <div class="card-badge badge-scraped">● Reader Agent Output</div>
            <div class="card-content">{state.get('scraped_content', 'No content scraped.')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Final Report — prominent
    st.markdown(f"""
    <div class="result-card report">
        <div class="card-badge badge-report">● Final Research Report</div>
        <div class="card-content">{state.get('report', 'No report generated.')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Critic Feedback
    st.markdown(f"""
    <div class="result-card critic">
        <div class="card-badge badge-critic">● Critic Evaluation</div>
        <div class="card-content">{state.get('feedback', 'No feedback generated.')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Download button
    full_output = (
        f"RESEARCH TOPIC: {topic}\n\n"
        f"{'='*60}\nSEARCH RESULTS\n{'='*60}\n{state.get('search_results','')}\n\n"
        f"{'='*60}\nSCRAPED CONTENT\n{'='*60}\n{state.get('scraped_content','')}\n\n"
        f"{'='*60}\nFINAL REPORT\n{'='*60}\n{state.get('report','')}\n\n"
        f"{'='*60}\nCRITIC FEEDBACK\n{'='*60}\n{state.get('feedback','')}\n"
    )
    st.download_button(
        label="⬇  Download Full Report (.txt)",
        data=full_output,
        file_name=f"research_{topic[:30].replace(' ','_')}.txt",
        mime="text/plain",
    )

else:
    # Idle state hint
    st.markdown("""
    <div style="text-align:center; padding: 4rem 1rem; color: #333;">
        <div style="font-size:3rem; margin-bottom:1rem;">🔬</div>
        <div style="font-family:'Space Mono',monospace; font-size:0.8rem; letter-spacing:0.15em;">
            ENTER A TOPIC AND PRESS RUN PIPELINE
        </div>
    </div>
    """, unsafe_allow_html=True)