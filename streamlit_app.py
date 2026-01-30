import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- INITIALIZATION ---
st.set_page_config(page_title="NSS Media Engine", page_icon="📲", layout="centered")

# Custom CSS for high-velocity mobile use
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        box-shadow: 0px 4px 10px rgba(0, 123, 255, 0.3);
    }
    .stTextArea textarea {
        border-radius: 12px;
    }
    [data-testid="stFileUploader"] {
        border: 2px dashed #007bff;
        border-radius: 12px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0px 0px;
        gap: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API CONFIGURATION ---
try:
    # Reference secrets for production deployment
    GEMINI_API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.error("Missing GEMINI_KEY in Secrets. Please add it to your Streamlit Dashboard.")
    st.stop()

# --- SYSTEM PROMPT (The "Media Authority" Strategist) ---
SYSTEM_PROMPT = """
You are the Chief Communications Officer for NSS XIM University.
Objective: Convert raw field inputs into high-authority media content that attracts big-ticket sponsors.

1. LinkedIn (ROI & Systems): Focus on man-hours, volunteer scale, logistics, and university prestige. Use a professional, 'Economics' slant.
2. Instagram (FOMO & Energy): High-energy, student-centric, punchy sentences, and localized hashtags (#NSSXIM #XIMB #Bhubaneswar).
3. Facebook/Press (Trust & Story): Journalistic narrative. Who, What, Where, When. Focus on community transformation.

Strict Guardrails:
- Zero data hallucinations.
- Maintain 'Dignity-First' reporting.
- Ensure the copy makes NSS XIM look like a professional, high-impact organization worthy of corporate sponsorship.
"""

st.title("🦅 NSS Content Engine")
st.caption("Field Data to Media Authority in < 60s.")

# --- MOBILE INPUT SECTION ---
uploaded_files = st.file_uploader("📸 Capture/Upload Photos", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
raw_text = st.text_area("📝 Raw Field Notes / Brochure Text", 
                        placeholder="Ex: 40 volunteers, Slum cleanliness drive at X. 300kgs waste collected. Ward Councillor joined.",
                        height=120)

if st.button("🚀 GENERATE DRAFTS"):
    if not uploaded_files or not raw_text:
        st.warning("Input required: Upload photos and add event notes.")
    else:
        try:
            # Using the high-velocity multimodal model
            model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
            
            # Process Images
            images = [Image.open(f) for f in uploaded_files]
            
            with st.status("🛠️ AI Editor drafting...", expanded=False) as status:
                prompt = f"{SYSTEM_PROMPT}\n\nRAW INPUT:\n{raw_text}"
                response = model.generate_content([prompt] + images)
                status.update(label="✅ Content Ready!", state="complete")

            # --- OUTPUT TABS ---
            output = response.text
            tabs = st.tabs(["🔗 LinkedIn", "📸 Instagram", "📰 Press Kit"])
            
            # Helper to split text into platform chunks
            def get_chunk(text, start_marker, end_marker=None):
                try:
                    start = text.find(start_marker)
                    if start == -1: return text
                    sub = text[start:]
                    if end_marker:
                        end = sub.find(end_marker, len(start_marker))
                        return sub[:end].strip() if end != -1 else sub.strip()
                    return sub.strip()
                except:
                    return text

            with tabs[0]:
                st.subheader("Professional ROI Draft")
                st.code(get_chunk(output, "1.", "2."), language=None)
                
            with tabs[1]:
                st.subheader("Student Energy Draft")
                st.code(get_chunk(output, "2.", "3."), language=None)
                
            with tabs[2]:
                st.subheader("Local Media Narrative")
                st.code(get_chunk(output, "3."), language=None)

            st.success("Tap the code blocks to copy instantly!")

        except Exception as e:
            st.error(f"System Error: {str(e)}")

st.divider()
st.caption("Optimized for XIM Media Authority | 2026")
