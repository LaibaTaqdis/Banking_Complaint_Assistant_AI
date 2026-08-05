import streamlit as st
import os
import re
import random
import string
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Banking Complaint Assistant",
    page_icon="🛡️",
    layout="wide"
)

# ==================== DESIGN SYSTEM ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --navy: #0f172a;
        --navy-soft: #1e293b;
        --emerald: #0e7c66;
        --emerald-light: #e3f4ee;
        --coral: #c2410c;
        --bg: #f4f6f9;
        --card: #ffffff;
        --border: #e4e8ee;
        --text: #1a2233;
        --muted: #64748b;
    }

    .stApp { background: var(--bg); }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--text); }

    .stDeployButton { display: none !important; }

    .hero {
        background: linear-gradient(120deg, var(--navy) 0%, #16213d 60%, var(--navy-soft) 100%);
        border-radius: 20px;
        padding: 30px 35px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 30px -12px rgba(15, 23, 42, 0.45);
    }
    .hero::before {
        content: "";
        position: absolute;
        top: -60px; right: -60px;
        width: 200px; height: 200px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(14,124,102,0.3), transparent 70%);
    }
    .hero-inner {
        display: flex;
        align-items: center;
        gap: 18px;
        position: relative;
        z-index: 1;
    }
    .hero-icon {
        width: 50px; height: 50px;
        border-radius: 14px;
        background: rgba(14,124,102,0.25);
        border: 1px solid rgba(14,124,102,0.5);
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .hero p {
        font-size: 14px;
        color: #b8c2d4;
        margin: 4px 0 0 0;
    }
    .hero-badges {
        margin-top: 14px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    .hero-badge {
        font-size: 12px;
        font-weight: 500;
        color: #dce6f0;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        padding: 5px 14px;
        border-radius: 20px;
    }

    .panel {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 2px 10px rgba(15,23,42,0.04);
    }
    .panel-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: var(--navy);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .tips-panel {
        background: linear-gradient(160deg, var(--emerald-light), #ffffff);
        border: 1px solid #cfe9df;
        border-radius: 14px;
        padding: 20px 22px;
        height: 100%;
    }
    .tips-panel ul { margin: 0; padding-left: 18px; font-size: 13.5px; line-height: 2; color: var(--text); }
    .tips-panel li::marker { color: var(--emerald); }

    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 1.5px solid var(--border);
        padding: 14px;
        font-size: 15px;
        background: #fbfcfe;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: var(--emerald);
        box-shadow: 0 0 0 4px rgba(14,124,102,0.12);
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--emerald), #0a5f4f);
        color: #ffffff;
        border: none;
        padding: 12px 35px;
        font-size: 15px;
        font-weight: 600;
        border-radius: 12px;
        width: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 6px 16px -4px rgba(14,124,102,0.45);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px -4px rgba(14,124,102,0.55);
    }

    .meter-row { display: flex; align-items: center; gap: 14px; margin: 6px 0 18px 0; }
    .meter-track { flex: 1; height: 8px; border-radius: 6px; background: #e7ebf1; overflow: hidden; }
    .meter-fill { height: 100%; border-radius: 6px; }
    .meter-label { font-size: 13px; font-weight: 600; color: var(--navy); min-width: 80px; }

    .result-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 10px rgba(15,23,42,0.04);
    }
    .result-card.analysis { border-top: 4px solid var(--navy); }
    .result-card.improved { border-top: 4px solid var(--emerald); }
    .result-card.response { border-top: 4px solid #c2410c; }
    .result-card h4 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 16px;
        font-weight: 600;
        margin: 0 0 10px 0;
        color: var(--navy);
    }
    .result-card p { font-size: 14px; line-height: 1.7; color: #2a3142; margin: 0 0 8px 0; }
    .result-card ul { margin: 0 0 8px 0; padding-left: 20px; }
    .result-card li { font-size: 14px; line-height: 1.7; color: #2a3142; }

    .status-banner {
        background: var(--emerald-light);
        border: 1px solid #b8dfd0;
        border-radius: 12px;
        padding: 12px 18px;
        font-size: 14px;
        font-weight: 600;
        color: var(--emerald);
        margin: 20px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .badge-fraud { background: #dc3545; color: white; padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
    .badge-transaction { background: #ffc107; color: #1a2233; padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
    .badge-card { background: #17a2b8; color: white; padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
    .badge-other { background: #6c757d; color: white; padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }

    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] { 
        background: var(--navy); 
    }
    section[data-testid="stSidebar"] * { 
        color: #ffffff !important; 
    }
    .sb-brand { 
        font-family: 'Space Grotesk', sans-serif; 
        font-size: 20px; 
        font-weight: 700; 
        color: #ffffff !important; 
    }
    .sb-sub { 
        font-size: 12px; 
        color: #8fa2bd !important; 
        margin-bottom: 16px; 
        letter-spacing: 0.5px; 
    }
    .sb-title { 
        font-size: 11px; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        color: #5f7594 !important; 
        margin: 16px 0 6px 0; 
        font-weight: 600; 
    }
    .sb-line { 
        font-size: 13px; 
        line-height: 1.9; 
        color: #dce6f0 !important; 
    }
    .sb-chip {
        display: inline-block;
        background: rgba(14,124,102,0.25);
        border: 1px solid rgba(14,124,102,0.5);
        color: #a8e0cd !important;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 3px 4px 3px 0;
    }
    .sb-note {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 12px;
        margin-top: 10px;
        color: #b8c2d4 !important;
    }

    .footer {
        text-align: center;
        color: var(--muted);
        padding: 16px 0;
        margin-top: 30px;
        font-size: 12px;
    }

    /* Simple inline control row above a results section */
    .section-toggle-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 4px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if "case_ref" not in st.session_state:
    suffix = "".join(random.choices(string.digits, k=5))
    st.session_state.case_ref = f"ABC-{datetime.now().strftime('%Y%m')}-{suffix}"

if "processed_result" not in st.session_state:
    st.session_state.processed_result = None

if "complaint_submitted" not in st.session_state:
    st.session_state.complaint_submitted = False

if "complaint_history" not in st.session_state:
    st.session_state.complaint_history = []

# Default ON: most people want to see the response immediately.
if "show_response" not in st.session_state:
    st.session_state.show_response = True

SHIELD_ICON = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 2L4 5v6c0 5 3.4 8.7 8 10 4.6-1.3 8-5 8-10V5l-8-3z" stroke="#4fd6b3" stroke-width="1.6" stroke-linejoin="round"/>
<path d="M8.5 12l2.3 2.3L15.5 9.5" stroke="#4fd6b3" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div class="sb-brand">ABC Bank</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">COMPLAINT INTELLIGENCE</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-title">How it works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-line">
    1&nbsp;&nbsp;Submit your complaint<br>
    2&nbsp;&nbsp;AI classifies category &amp; urgency<br>
    3&nbsp;&nbsp;Complaint restated clearly<br>
    4&nbsp;&nbsp;Draft response generated
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-title">Capabilities</div>', unsafe_allow_html=True)
    st.markdown("""
    <span class="sb-chip">Banking domain</span>
    <span class="sb-chip">Roman Urdu</span>
    <span class="sb-chip">Groq · Llama 3.3</span>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="sb-note">Complaints are processed for this session only and are not stored.</div>',
        unsafe_allow_html=True
    )

    # History lives in the sidebar since it's a simple reference list, not a
    # result to review in depth.
    if st.session_state.complaint_history:
        st.markdown('<div class="sb-title">Past complaints (this session)</div>', unsafe_allow_html=True)
        show_history = st.checkbox("Show past complaints", value=False)
        if show_history:
            for i, item in enumerate(st.session_state.complaint_history[-3:]):
                st.caption(f"{i+1}. {item[:50]}...")

    st.markdown("---")
    st.caption("Build 1.1 · Summer 2026")

# ==================== HERO ====================
st.markdown(f"""
<div class="hero">
    <div class="hero-inner">
        <div class="hero-icon">{SHIELD_ICON}</div>
        <div>
            <h1>Banking Complaint Assistant</h1>
            <p>AI-powered analysis, requirement clarity, and response drafting</p>
        </div>
    </div>
    <div class="hero-badges">
        <span class="hero-badge">Case {st.session_state.case_ref}</span>
        <span class="hero-badge">{datetime.now().strftime('%d %b %Y, %H:%M')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN INPUT ====================
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">✏️ Describe the complaint</div>', unsafe_allow_html=True)
    complaint = st.text_area(
        "Complaint",
        height=130,
        placeholder="e.g. Meray sath 50000 ka fraud hogya ha",
        help="Write in English or Roman Urdu",
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown("""
    <div class="tips-panel">
        <div class="panel-title" style="color:#0e7c66;">💡 Tips</div>
        <ul>
            <li>Be specific</li>
            <li>Include amount</li>
            <li>Mention date</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== BUTTON ====================
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    submit = st.button("🚀 Process Complaint", use_container_width=True)

# ==================== HELPERS ====================

def get_category_badge(category_text):
    category_lower = category_text.lower()
    if "fraud" in category_lower:
        return '<span class="badge-fraud">🚨 Fraud</span>'
    elif "transaction" in category_lower:
        return '<span class="badge-transaction">💰 Transaction</span>'
    elif "card" in category_lower:
        return '<span class="badge-card">💳 Card</span>'
    else:
        return '<span class="badge-other">📌 Other</span>'

def inline_md_to_html(text):
    text = text.strip().lstrip("-•*").strip()
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    return text

def content_lines_to_html(content_lines):
    parts = []
    bullet_buffer = []

    def flush_bullets():
        if bullet_buffer:
            items = "".join(f"<li>{inline_md_to_html(b)}</li>" for b in bullet_buffer)
            parts.append(f"<ul>{items}</ul>")
            bullet_buffer.clear()

    for line in content_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("-", "•", "*")):
            bullet_buffer.append(stripped)
        else:
            flush_bullets()
            parts.append(f"<p>{inline_md_to_html(stripped)}</p>")
    flush_bullets()
    return "".join(parts)

def render_card(section_key, content_lines):
    title_map = {
        "analysis": "📊 Analysis",
        "improved": "📝 Improved Complaint",
        "response": "✉️ Professional Response",
    }
    title = title_map.get(section_key, "Result")
    css_class = section_key if section_key in ("analysis", "improved", "response") else "analysis"
    body_html = content_lines_to_html(content_lines)

    if section_key == "analysis":
        category_match = re.search(r'category:?\s*(\w+)', body_html, re.IGNORECASE)
        if category_match:
            badge = get_category_badge(category_match.group(1))
            body_html = badge + "<br><br>" + body_html

    card_html = f'<div class="result-card {css_class}"><h4>{title}</h4>{body_html}</div>'
    st.markdown(card_html, unsafe_allow_html=True)

def parse_result(result):
    lines = result.split("\n")
    current_section = None
    section_content = []
    all_sections = {"analysis": [], "improved": [], "response": []}

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("1.") or "ANALYSIS" in stripped.upper():
            if section_content and current_section:
                all_sections[current_section] = section_content.copy()
                section_content = []
            current_section = "analysis"
            if stripped.startswith("1."):
                continue
        elif stripped.startswith("2.") or "IMPROVED" in stripped.upper():
            if section_content and current_section:
                all_sections[current_section] = section_content.copy()
                section_content = []
            current_section = "improved"
            if stripped.startswith("2."):
                continue
        elif stripped.startswith("3.") or "PROFESSIONAL" in stripped.upper() or "RESPONSE" in stripped.upper():
            if section_content and current_section:
                all_sections[current_section] = section_content.copy()
                section_content = []
            current_section = "response"
            if stripped.startswith("3."):
                continue
        else:
            if stripped and not stripped.startswith("###"):
                section_content.append(line)

    if section_content and current_section:
        all_sections[current_section] = section_content.copy()
    return all_sections

def display_results(all_sections):
    if all_sections["analysis"]:
        render_card("analysis", all_sections["analysis"])
    if all_sections["improved"]:
        render_card("improved", all_sections["improved"])

    # Toggle now sits right above the section it controls, and defaults on.
    st.markdown("---")
    show_response = st.checkbox(
        "Show bank's reply",
        value=st.session_state.show_response,
        help="The formal draft reply to this complaint"
    )
    st.session_state.show_response = show_response

    if show_response:
        if all_sections["response"]:
            render_card("response", all_sections["response"])
            st.download_button(
                label="📥 Download Response",
                data="\n\n".join(all_sections["response"]),
                file_name=f"response_{st.session_state.case_ref}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("ℹ️ No professional response generated.")

# ==================== PROCESS COMPLAINT ====================
if submit:
    complaint_text = complaint.strip()
    if not complaint_text:
        st.warning("⚠️ Please enter a complaint before submitting.")
    elif len(complaint_text) < 5:
        st.warning("⚠️ Please enter at least 5 characters.")
    else:
        # Single, honest loading state instead of a fake typing animation
        # stacked on top of a progress bar.
        with st.spinner("Analyzing complaint and drafting a response..."):
            try:
                client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

                system_prompt = """
                You are a Banking Complaint Processing Assistant.

                Process this complaint and provide:

                1. ANALYSIS:
                   - Category: (fraud/transaction/card/other)
                   - Urgency: (low/medium/high)
                   - Emotion: (angry/frustrated/neutral/urgent)

                2. IMPROVED COMPLAINT:
                   Rewrite clearly with specific details (amount, date, account).

                3. PROFESSIONAL RESPONSE:
                   Formal banking reply with apology, action plan, timeline, contact.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Customer Complaint: {complaint_text}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.5,
                    max_completion_tokens=1024,
                )

                result = chat_completion.choices[0].message.content

                st.session_state.processed_result = result
                st.session_state.complaint_submitted = True
                st.session_state.complaint_history.append(complaint_text)

            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.session_state.processed_result = None
                st.session_state.complaint_submitted = False

    if st.session_state.complaint_submitted and st.session_state.processed_result:
        result = st.session_state.processed_result

        st.markdown("---")
        st.markdown(
            f'<div class="status-banner">✅ Case {st.session_state.case_ref} processed successfully</div>',
            unsafe_allow_html=True
        )

        urgency = "medium"
        lower_result = result.lower()
        if "urgency: high" in lower_result or "urgent" in lower_result:
            urgency = "high"
        elif "urgency: low" in lower_result:
            urgency = "low"

        urgency_map = {
            "low": (33, "#0e7c66", "Low"),
            "medium": (66, "#c2410c", "Medium"),
            "high": (100, "#b91c1c", "High"),
        }
        pct, color, label = urgency_map[urgency]

        st.markdown(f"""
        <div class="meter-row">
            <span class="meter-label">Urgency</span>
            <div class="meter-track"><div class="meter-fill" style="width:{pct}%; background:{color};"></div></div>
            <span class="meter-label" style="color:{color};">{label}</span>
        </div>
        """, unsafe_allow_html=True)

        all_sections = parse_result(result)
        display_results(all_sections)

# ==================== DISPLAY STORED RESULTS (on rerun, e.g. toggling checkbox) ====================
elif st.session_state.complaint_submitted and st.session_state.processed_result:
    result = st.session_state.processed_result

    st.markdown("---")
    st.markdown(
        f'<div class="status-banner">✅ Case {st.session_state.case_ref} processed successfully</div>',
        unsafe_allow_html=True
    )

    urgency = "medium"
    lower_result = result.lower()
    if "urgency: high" in lower_result or "urgent" in lower_result:
        urgency = "high"
    elif "urgency: low" in lower_result:
        urgency = "low"

    urgency_map = {
        "low": (33, "#0e7c66", "Low"),
        "medium": (66, "#c2410c", "Medium"),
        "high": (100, "#b91c1c", "High"),
    }
    pct, color, label = urgency_map[urgency]

    st.markdown(f"""
    <div class="meter-row">
        <span class="meter-label">Urgency</span>
        <div class="meter-track"><div class="meter-fill" style="width:{pct}%; background:{color};"></div></div>
        <span class="meter-label" style="color:{color};">{label}</span>
    </div>
    """, unsafe_allow_html=True)

    all_sections = parse_result(result)
    display_results(all_sections)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    ABC Bank · Complaint Intelligence · Powered by Groq Cloud<br>
    © 2026 ABC Bank
</div>
""", unsafe_allow_html=True)