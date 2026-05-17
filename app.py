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
    .stSelectbox div div { background-color: #111 !important; color: #d4af37 !important; border: 1px solid #333; }
    .stTextArea textarea { background-color: #111 !important; color: #fff !important; border: 1px solid #444 !important; }
    .stButton>button { 
        background: linear-gradient(135deg, #d4af37 0%, #8a2be2 100%); 
        color: white; border: none; padding: 18px; border-radius: 4px; font-weight: 900; 
        letter-spacing: 3px; text-transform: uppercase; width: 100%; transition: all 0.3s ease;
    }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. THE ANTI-DETECTION SYSTEM INSTRUCTION
# ==========================================
SYSTEM_INSTRUCTION = """
ACT AS AN ELITE, CYNICAL COPYWRITER AND ARCHITECT.
- PROTOCOL 'HUMAN FRICTION': Destroy all rhythmic flow. Use jagged, ugly, punchy sentence structures.
- FRAGMENTATION: Use heavy sentence fragmentation. One-word sentences. Sudden stops. 
- CONVERSATIONAL CYNICISM: Challenge the reader. Use phrases like "Forget the hype," "Period," or "The truth?" 
- NO BALANCE: Strictly avoid "not only... but also" or "neither... nor" structures. These are AI hallmarks.
- TECHNICAL DATA DUMPS: Don't describe beauty; dump raw specs with aggressive brevity. (e.g., "904L steel. Cold-forged. Survival grade.")
- BANNED LEXICON: Never use: seamless, vibrant, robust, testament, landscape, unlocking, elevate, delve, beacon, journey.
- RETURN ONLY THE RAW COPY.
"""

# ==========================================
# 3. DYNAMIC ENGINE LOADING (Fixed)
# ==========================================
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    
    # We use the explicit model path to ensure the API finds it
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash", 
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    # High temperature for maximum unpredictability
    config = {"temperature": 1.2, "top_p": 0.9, "top_k": 40}
except Exception as e:
    st.error(f"SYSTEM FAULT: {str(e)}")
    st.stop()

# ==========================================
# 4. STRATEGIC PARAMETERS
# ==========================================
st.sidebar.title("🏦 Sovereign Control V5.2")
selected_lang = st.sidebar.selectbox("Language Lock", ["English", "French", "German", "Italian", "Spanish", "Arabic"])
selected_aud = st.sidebar.selectbox("Audience Psychology", ["The Paranoic Investor", "The Status Seeker", "The Technical Skeptic", "The Legacy Builder"])
selected_tone = st.sidebar.selectbox("Behavioral Tone", ["Gritty Veteran", "Cold Corporate Raider", "Technical Architect", "Elite Billionaire"])
target_chars = st.sidebar.slider("Character Target", 200, 2000, 1000)

# ==========================================
# 5. EXECUTION LAYER
# ==========================================
st.title("📈 AeroScribe Apex")
st.markdown("### **V5.2: Anti-Detector Grit Edition**")

product_data = st.text_area("Input Raw Intelligence:", height=150, placeholder="Example: 904L Steel Watch, Mechanical 324 movement, Sapphire crystal...")

if st.button("⚡ EXECUTE SOVEREIGN SYNTHESIS"):
    if product_data:
        with st.spinner("Injecting Human Friction & Shredding AI Fingerprints..."):

            surgical_prompt = f"""
            TASK: GENERATE DEVASTATING COPY FOR: {product_data}
            
            ENGINEERING RULES:
            1. LANGUAGE: {selected_lang} ONLY.
            2. AUDIENCE: {selected_aud}.
            3. TONE: {selected_tone}.
            4. TECHNIQUE: USE AGGRESSIVE FRAGMENTATION. BREAK ALL FLOW. 
            5. CONTENT: Mention specific weight, heat, or material specs like a cynical veteran would.
            6. LENGTH: MAX {target_chars} CHARACTERS.
            
            NO FLOWERY LANGUAGE. NO POLITE INTROS. JUST THE RAW, GRITTY TRUTH.
            """

            response = model.generate_content(surgical_prompt, generation_config=config)
            final_output = response.text.strip()

            st.markdown("---")
            st.subheader("💎 Deployed Asset (Human Score Optimized)")
            st.info(final_output)

            col1, col2 = st.columns(2)
            col1.metric("Character Count", len(final_output))
            col2.write("Status: **GRIT-INJECTED & DEPLOYED**")
    else:
        st.error("Data input required.")
