import streamlit as st
from google import genai
from PIL import Image
import io

# --- INITIALIZATION ---
st.set_page_config(page_title="NSS Media Engine", page_icon="🦅", layout="centered")

# Mobile-First UI Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #1a73e8;
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTextArea textarea { border-radius: 12px; border: 1px solid #dfe1e5; }
    [data-testid="stFileUploader"] {
        border: 2px dashed #1a73e8;
        border-radius: 12px;
        padding: 15px;
        background: white;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #ffffff;
        border-radius: 8px 8px 0 0;
        border: 1px solid #dfe1e5;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API CLIENT SETUP ---
try:
    # Using the new google-genai SDK structure
    client = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    MODEL_ID = "gemini-2.5-flash-preview-09-2025"
except Exception as e:
    st.error("Credential Error: Ensure 'GEMINI_KEY' is set in Streamlit Secrets.")
    st.stop()

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are the Lead Media Strategist for NSS XIM University. 
Target: Convert raw field data into content that builds brand authority and attracts corporate sponsors.

Draft 3 pieces:
1. LinkedIn: ROI-driven, professional, focus on scale/logistics/impact.
2. Instagram: High-energy, hype, student-centric, visual storytelling.
3. Media/FB: Trustworthy narrative, community-focused, journalistic.

Rules:
- Fact-check against provided text (no hallucinations).
- Dignity-first portrayal of beneficiaries.
- Use #NSSXIM #XIMUniversity #SocialImpact.
"""

st.title("🦅 NSS Content Engine")
st.caption("One-tap media production for the restless builder.")

# --- INPUT SECTION ---
uploaded_files = st.file_uploader("📸 Batch Upload Photos", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
raw_text = st.text_area("📝 Field Notes / Brochure Context", 
                        placeholder="Bullet points or raw text from the site...",
                        height=130)

if st.button("⚡ GENERATE CONTENT"):
    if not uploaded_files or not raw_text:
        st.warning("Needs fuel: Add photos and notes.")
    else:
        try:
            # Prepare multimodal content for the new SDK
            content_list = [SYSTEM_PROMPT, f"FIELD DATA: {raw_text}"]
            
            for f in uploaded_files:
                img = Image.open(f)
                content_list.append(img)

            with st.status("🏗️ Architecting posts...", expanded=False) as status:
                # New SDK call format
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=content_list
                )
                status.update(label="🚀 Strategy Finalized!", state="complete")

            # --- MOBILE OUTPUT DISPLAY ---
            raw_output = response.text
            tabs = st.tabs(["🔗 LinkedIn", "📸 Instagram", "📰 Press"])

            # Logic to slice output into readable chunks for mobile
            def split_content(text, marker):
                parts = text.split(marker)
                if len(parts) > 1:
                    return parts[1].split("2." if "1." in marker else ("3." if "2." in marker else "###"))[0].strip()
                return text

            with tabs[0]:
                st.subheader("Corporate/LinkedIn")
                st.code(split_content(raw_output, "1."), language=None)
                
            with tabs[1]:
                st.subheader("Campus/Instagram")
                st.code(split_content(raw_output, "2."), language=None)
                
            with tabs[2]:
                st.subheader("Regional/Press")
                st.code(split_content(raw_output, "3."), language=None)

            st.success("Drafts generated. Tap to copy.")

        except Exception as e:
            st.error(f"SDK Error: {str(e)}")

st.divider()
st.caption("v2.0 | Optimized for google-genai & Mobile")
