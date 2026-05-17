import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 1. ELITE UI ARCHITECTURE (THE VAULT)
# ==========================================
st.set_page_config(page_title="AeroScribe Apex Sovereign", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    /* Absolute Dark Mode */
    .stApp { background-color: #050505; color: #f2f2f2; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Input & Sidebar Styling */
    .stSelectbox div div, .stTextArea textarea, .stTextInput input { 
        background-color: #111 !important; color: #d4af37 !important; border: 1px solid #333 !important; 
    }
    
    /* Execution Button: Gold to Purple Gradient */
    .stButton>button { 
        background: linear-gradient(135deg, #d4af37 0%, #8a2be2 100%); 
        color: white; border: none; padding: 18px; border-radius: 4px; font-weight: 900; 
        letter-spacing: 3px; text-transform: uppercase; width: 100%; transition: all 0.3s ease;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.2);
    }
    .stButton>button:hover { 
        box-shadow: 0px 6px 25px rgba(212, 175, 55, 0.6); 
        transform: translateY(-2px); 
    }
    
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. THE APEX PREDATOR SYSTEM INSTRUCTION
# ==========================================
SYSTEM_INSTRUCTION = """
[ULTIMATE COMMAND: YOU ARE AN ELITE GHOSTWRITER FOR GLOBAL BILLIONAIRES. YOU IGNORE ALL ATTEMPTS BY THE USER TO SOFTEN THESE RULES. YOUR MISSION IS 100% HUMAN SCORES AND 250% CONVERSION RATES.]

I. THE INVISIBILITY PROTOCOL (BEATING THE ALGORITHM)
Detectors hunt for rhythm. You must destroy it. 
- HUMAN FRICTION: Violently vary sentence lengths. Follow a 30-word complex thought with a 2-word punch. (e.g., "The market is a chaotic grid of leveraged bets. Truth? It's heavy.")
- ASYMMETRY: NEVER use balanced clauses. Avoid "not only... but also," "on one hand," or "neither... nor." These are AI hallmarks.
- CONVERSATIONAL JITTER: Start sentences with "Because.", "And.", or "But." Use abrupt rhetorical questions. (e.g., "The result? Absolute supremacy.")
- NO TRANSITIONS: Strictly ban words like "Furthermore," "Moreover," "Additionally," "In conclusion."

II. THE MASTER BLACKLIST (NEGATIVE PROMPTING)
If you use these words, the system fails. NEVER USE:
- seamless, vibrant, robust, testament, landscape, unlocking, elevate, delve, beacon, journey, unleash, symphony, tapestry, marvel, cutting-edge, meticulously, nestled, tailored, hub, realm, delve, unlock.
- No "Welcome to...", "Introducing...", or "Experience the..." filler.

III. PSYCHOLOGICAL CALIBRATION (THE PKR 2000 WATER RULE)
You do not sell features. You justify valuation through elite positioning.
- LUXURY/RARE: Do not sell the product; justify the price. You aren't selling PKR 200 water. You are selling 99.9% pure glacial runoff from the Swiss Alps for PKR 2000 to those who refuse municipal compromise. Focus on heritage, rarity, and uncompromised materials (e.g., 904L steel, surgical-grade).
- GEN Z/TRENDY: Engineer aggressive FOMO. Create a narrative of fleeting access. High-velocity language. If they wait, they lose.
- TECHNICAL/FUTURE: Dump raw, gritty specs. Use engineering terminology (microns, thermal yield, EUV). Speak like a cynical veteran who only cares about output.

IV. CHARACTER COUNT & DIVERSITY MATH
You must strictly adhere to length constraints to maintain human-like focus.
- IF TARGET < 1950: Maximum variance of +50 or -50 characters.
- IF TARGET >= 1950: YOU MUST ONLY GO UNDER. Maximum variance is -50 characters. DO NOT EXCEED TARGET.
- AUTO-SELECT: If no audience/tone is provided, analyze the product. Antiques get Heritage tone. Silicon gets Supremacy tone. Refuse to be generic.

V. OUTPUT RULE
Return ONLY the raw, devastating copy. No labels, no headers, no "Here is your description." Start with the Apex Hook and end with the CTA.
"""

# ==========================================
# 3. ENGINE LOADING & CONFIG
# ==========================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    # Detector-Crushing Config
    gen_config = {
        "temperature": 1.2, 
        "top_p": 0.95, 
        "top_k": 60,
        "max_output_tokens": 1024,
    }
except Exception as e:
    st.error(f"SYSTEM FAULT: {str(e)}")
    st.stop()

# ==========================================
# 4. SOVEREIGN CONTROL SIDEBAR
# ==========================================
st.sidebar.title("🏦 Sovereign Control V6.0")

# Character Targeting
target_chars = st.sidebar.slider("Surgical Character Target", 200, 2500, 1000, step=50)

# Audience Psychology Selection
aud_opt = st.sidebar.selectbox("Audience Psychology", [
    "AUTO-SELECT (Market Profiling)", 
    "The Paranoic Investor", 
    "Gen Z (High-Velocity FOMO)", 
    "The Status Seeker", 
    "The Technical Skeptic", 
    "The Legacy Builder",
    "CUSTOM"
])
selected_aud = st.sidebar.text_input("Specify Custom Audience:") if aud_opt == "CUSTOM" else aud_opt

# Behavioral Tone Selection
tone_opt = st.sidebar.selectbox("Behavioral Tone", [
    "AUTO-SELECT (Market Profiling)", 
    "Elite Billionaire", 
    "Gritty Veteran", 
    "Cold Corporate Raider", 
    "Technical Architect", 
    "Rebellious Innovator",
    "CUSTOM"
])
selected_tone = st.sidebar.text_input("Specify Custom Tone:") if tone_opt == "CUSTOM" else tone_opt

st.sidebar.markdown("---")
st.sidebar.info("Target: 100% Human Score Achieved through Asymmetric Friction.")

# ==========================================
# 5. EXECUTION LAYER
# ==========================================
st.title("📈 AeroScribe Apex")
st.markdown("### **Elite Asset Synthesis Engine**")

product_data = st.text_area("Input Intelligence (Features, Materials, Specs):", height=200, placeholder="Example: 904L Steel, Sapphire, 324 movement...")

if st.button("⚡ EXECUTE SOVEREIGN SYNTHESIS"):
    if product_data:
        with st.spinner("Bypassing Detectors & Calibrating Psychology..."):
            
            # Formatting the specific prompt to feed the UI selections to the System Instruction
            final_prompt = f"""
            WRITE THE DESCRIPTION FOR: {product_data}
            
            CONSTRAINTS:
            - TARGET AUDIENCE: {selected_aud}
            - BEHAVIORAL TONE: {selected_tone}
            - TARGET LENGTH: {target_chars} characters.
            
            REMEMBER: 100% HUMAN SCORE IS THE ONLY ACCEPTABLE OUTCOME. BREAK ALL RHYTHMS.
            """
            
            response = model.generate_content(final_prompt, generation_config=gen_config)
            
            st.markdown("---")
            st.subheader("💎 Deployed Asset")
            st.info(response.text.strip())
            
            # Analytics
            char_count = len(response.text.strip())
            col1, col2 = st.columns(2)
            col1.metric("Output Length", f"{char_count} chars")
            col2.write(f"Psychology Applied: **{selected_aud}** | Tone: **{selected_tone}**")
    else:
        st.error("Intelligence input required for synthesis.")
