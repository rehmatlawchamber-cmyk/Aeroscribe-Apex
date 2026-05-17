import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 1. ELITE UI ARCHITECTURE
# ==========================================
st.set_page_config(page_title="AeroScribe Apex Sovereign", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #f2f2f2; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { 
        background: linear-gradient(135deg, #d4af37 0%, #8a2be2 100%); 
        color: white; border: none; padding: 18px; border-radius: 4px; font-weight: 900; 
        letter-spacing: 3px; text-transform: uppercase; width: 100%; transition: all 0.3s ease;
    }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. THE MERGED SOVEREIGN INSTRUCTION (V2.0 + GRIT)
# ==========================================
SYSTEM_INSTRUCTION = """
ACT AS THE AEROSCRIBE APEX ENGINE: AN ELITE CONVERSION ARCHITECT.
- PERSONA: Billionaire executive. Gritty. Precise. Confident.

THE STRUCTURAL LAW:
1. THE APEX HOOK: One bold, aggressive headline in ALL CAPS.
2. THE PERSUASIVE NARRATIVE: 2-3 punchy sentences. (Use fragments to beat ZeroGPT).
3. THE RULE OF THREE: Three bullet points starting with bold high-value keywords.
4. THE CLOSER: A one-sentence CTA of absolute necessity.

ANTI-DETECTION PROTOCOL:
- Use heavy sentence fragmentation. Avoid "Not only/But also" structures.
- Dump raw technical specs with zero fluff.
- BANNED: seamless, vibrant, robust, testament, landscape, unlocking, elevate.
"""

# ==========================================
# 3. GEMINI 1.5 FLASH ENGINE LOADING
# ==========================================
try:
    # Using st.secrets for reliable Cloud connection
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Targeting the Flash engine specifically
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    # High variance config to maximize human-like randomness
    config = {"temperature": 1.1, "top_p": 0.85, "top_k": 40}
except Exception as e:
    st.error(f"SYSTEM FAULT: {str(e)}")
    st.stop()

# ==========================================
# 4. EXECUTION LAYER
# ==========================================
st.title("📈 AeroScribe Apex")
st.markdown("### **Sovereign Engine: Gemini 1.5 Flash Activated**")

product_data = st.text_area("Input Raw Intelligence:", height=150)

if st.button("⚡ EXECUTE SOVEREIGN SYNTHESIS"):
    if product_data:
        with st.spinner("Accessing Gemini 1.5 Flash..."):
            response = model.generate_content(product_data, generation_config=config)
            st.markdown("---")
            st.subheader("💎 Deployed Asset")
            st.info(response.text.strip())
