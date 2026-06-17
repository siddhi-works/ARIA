import streamlit as st
from aria_researcher import INITIAL_PROMPT, graph, config
from langchain_core.messages import AIMessage
import logging
import time
import os
import re
from pathlib import Path

# ==========================
# LOGGING
# ==========================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Research AI Workstation",
    page_icon="⚡",
    layout="wide"
)

#Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================
# THEME
# ==========================

st.markdown("""
<style>

.stApp {
    background: #F8FAFC;
}

header {
    visibility: hidden;
}

html, body {
    color: #0F172A;
}

/* MAIN TITLE */

.main-title {
    text-align: center;
    font-size: 120px;
    font-weight: 800;
    letter-spacing: -4px;
    color: #0F172A;
    margin-bottom: 0px;
}

/* AGENT NAME */

.agent-title {
    text-align: center;
    font-size: 26px;
    color: #0F172A;
    margin-top: -10px;
    margin-bottom: 20px;
}

/* DISCOVER ANALYZE SYNTHESIZE */

.tagline {
    text-align: center;
    font-size: 22px;
    font-weight: 600;
    color: #0F172A;
    margin-top: 25px;
}

/* SUBTITLE */

.subline {
    text-align: center;
    font-size: 18px;
    color: #64748B;
    margin-top: 10px;
    margin-bottom: 20px;
}

/* STATUS */

.statusline {
    text-align: center;
    color: #64748B;
    font-size: 16px;
    margin-bottom: 40px;
}

/* CHAT CARDS */

.stChatMessage {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

/* CHAT INPUT */

[data-testid="stChatInput"] {
    background: white;
    border-radius: 20px;
    min-height: 40px;
}

.stChatMessage,
.stChatMessage p,
.stChatMessage li,
.stChatMessage span,
.stChatMessage div {
            color: #0F172A !important;
            }
            
/* DOWNLOAD BUTTON */

.stDownloadButton button {
    width: 100%;
    border-radius: 14px;
}

[data-testid="stChatMessageContent"] {
    color: #0F172A !important;
}

[data-testid="stChatMessageContent"] * {
    color: #0F172A !important;
}

.stMarkdown {
    color: #0F172A !important;
}

p {
    color: #0F172A !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# HEADER
# ==========================

st.markdown("""
<div class="main-title">
ARIA
</div>

<div class="agent-title">
Automated Research & Intelligence Agent
</div>

<div class="tagline">
Discover. Analyze. Synthesize.
</div>

<div class="subline">
Transform academic literature into actionable research insights.
</div>

<div class="statusline">
✦ Gemini Flash &nbsp;&nbsp; | &nbsp;&nbsp; 🟢 Research Mode: Active
</div>
            
<hr style="
width:220px;
margin:auto;
margin-top:20px;
margin-bottom:30px;
border:none;
border-top:1px solid #CBD5E1;
">
""", unsafe_allow_html=True)

_, center, _ = st.columns([1.5, 4, 1.5])

with center:
    # DISPLAY OLD CHAT
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    if not st.session_state.chat_history:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# CHAT INPUT
user_input = st.chat_input("Enter research topic...")

with center:
    # PROCESS MESSAGE
    if user_input and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            chat_input = {
                "messages": [{"role": "system","content": INITIAL_PROMPT}] + st.session_state.chat_history }
            start_time = time.time()
            full_response = ""
        
        with st.chat_message("assistant"):
            
            placeholder = st.empty()
            
            try:
                
                for s in graph.stream(chat_input,config,stream_mode="values"):
                    
                    message = s["messages"][-1]
                    
                    if isinstance(message, AIMessage):
                        content = message.content

                        if content is None:
                            continue
                        
                        if isinstance(content, list):
                            extracted_text = ""
                            for item in content:
                                if isinstance(item,dict):
                                    extracted_text += item.get("text", "")
                                else:
                                    extracted_text += str(item)
                                
                            content = extracted_text

                        if content:
                            
                            full_response += str(content)
                            
                            placeholder.markdown(
                                full_response + "",
                                unsafe_allow_html=True
                            )
                placeholder.markdown(full_response)

                # PDF DOWNLOAD BUTTON

                elapsed = round(time.time() - start_time,2)

                st.caption(f"Generated in {elapsed}s")

                pdf_dir = Path("output")
                if pdf_dir.exists():
                    pdf_files = sorted( 
                        pdf_dir.glob("*.pdf"),
                        key=lambda f: f.stat().st_mtime,
                        reverse=True )
                    if pdf_files:
                        latest_pdf = pdf_files[0]
                        with open(latest_pdf, "rb") as pdf_file:
                            st.download_button(
                                label="Download Research Paper PDF",
                                data=pdf_file.read(),
                                file_name=latest_pdf.name,
                                mime="application/pdf")

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": full_response
                })
                
            except Exception as e:
                error_text = str(e).lower()
                if (
                    "rate limit" in error_text
                    or "resource exhausted" in error_text
                    or "429" in error_text ):
                    st.warning("Model rate limit reached. Please wait a minute and try again.")
                else:
                    st.error(f"Error: {str(e)}")
    


# ==========================
# SESSION STATE
# ==========================

# ==========================
# DISPLAY OLD CHAT
# ==========================

# ==========================
# CHAT INPUT
# ==========================

# ==========================
# PROCESS MESSAGE
# ==========================