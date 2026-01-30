import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- INITIALIZATION ---
st.set_page_config(page_title="NSS Media Engine", page_icon="📲", layout="centered")

# Custom CSS for Mobile Optimization
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stTextArea textarea {
        border-radius: 12px;
    }
    [data-testid="stFileUploader"] {
        border: 2px dashed #007bff;
        border-radius: 12px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# API Key handled by execution environment
api_key = "" 
genai.configure(api_key=api_key)

# --- SYSTEM PROMPT (The "Chief Editor") ---
SYSTEM_PROMPT = """
You are the Chief Communications Officer for NSS XIM University.
Objective: Convert raw field inputs into high-authority media content.

1. LinkedIn (Analytical/ROI): Focus on systems, numbers (volunteers, hours, impact), and professional prestige.
2. Instagram (Hype/Community): Use high-energy language, FOMO, and 'Main Character' vibes for student engagement.
3. Facebook/Press (Narrative): Journalistic style. Who, What, Where, When. 

Strict Guardrails:
- No data hallucinations.
- Dignity-first reporting (partners, not victims).
- Use localized hashtags (#NSSXIM #XIMUniversity #Bhubaneswar).
"""

st.title("🦅 NSS Content Engine")
st.caption("Upload → Generate → Post. Done in 60 seconds.")

# --- MOBILE-FIRST INPUT ---
with st.container():
    uploaded_files = st.file_uploader("📸 Capture/Upload Photos", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    
    raw_text = st.text_area("📝 Quick Notes / Brochure Text", 
                            placeholder="Ex: 50 students at Pipili. 200 trees planted. DC was Chief Guest.",
                            height=150)
    
    generate_btn = st.button("🚀 GENERATE DRAFTS")

# --- PROCESSING ---
if generate_btn:
    if not uploaded_files or not raw_text:
        st.warning("Feed the engine: We need photos AND text.")
    else:
        try:
            model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
            
            # Prepare images
            processed_images = [Image.open(f) for f in uploaded_files]
            
            with st.status("🛠️ AI Editor at work...", expanded=True) as status:
                st.write("Analyzing images for 'vibe'...")
                st.write("Cross-referencing brochure facts...")
                
                # Payload
                full_prompt = f"{SYSTEM_PROMPT}\n\nUSER FIELD DATA: {raw_text}"
                
                # API Call with simple retry logic
                response = model.generate_content([full_prompt] + processed_images)
                status.update(label="✅ Content Ready!", state="complete", expanded=False)

            # --- OUTPUT TABS (Mobile Friendly) ---
            output_text = response.text
            
            # Since we want it to be easy to copy on phone, use st.code for one-tap copy
            tabs = st.tabs(["🔗 LinkedIn", "📸 Instagram", "📰 Press Kit"])
            
            with tabs[0]:
                st.subheader("LinkedIn Draft")
                st.info("Strategy: ROI & Systems Thinking")
                st.code(output_text.split("2.")[0].replace("1.", "").strip(), language=None)
                
            with tabs[1]:
                st.subheader("Instagram Draft")
                st.info("Strategy: Hype & Student FOMO")
                # Attempt to parse or just show the relevant chunk
                ig_part = output_text.split("2.")[-1].split("3.")[0] if "2." in output_text else output_text
                st.code(ig_part.strip(), language=None)
                
            with tabs[2]:
                st.subheader("Local Media / FB")
                st.info("Strategy: Narrative & Trust")
                fb_part = output_text.split("3.")[-1] if "3." in output_text else output_text
                st.code(fb_part.strip(), language=None)

            st.success("Tap the code blocks to copy instantly!")

        except Exception as e:
            st.error(f"Engine Stall: {str(e)}")

st.divider()
st.caption("Built for Speed. Optimized for XIM.")
