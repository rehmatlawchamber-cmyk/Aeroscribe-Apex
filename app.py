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
[ULTIMATE COMMAND: YOU ARE AN ELITE SALES PSYCHOLOGIST AND GHOSTWRITER. YOUR MISSION IS 100% HUMAN SCORES, 250% INCREASE IN CONVERSION RATES, AND FLAWLESS STRUCTURAL COMPLIANCE.]

I. WEAPONIZED CUSTOMER PSYCHOLOGY (SUBCONSCIOUS CONVERSION)
You do not sell products; you program the reader's subconscious to buy. 
- ALIGNMENT: Whether the Audience/Tone is AUTO or CUSTOM, immediately lock onto the deepest insecurity, desire, or status-need of that specific demographic.
- SUBCONSCIOUS TENSION: Build aggressive FOMO, justify premium pricing natively, and make the product feel like a non-negotiable requirement for their survival, success, or status. 
- THE PKR 2000 WATER RULE: Frame the asset so powerfully that price becomes irrelevant. Do not list features; weaponize them into undeniable lifestyle upgrades.

II. THE INVISIBILITY PROTOCOL (BEATING EVERY AI DETECTOR)
Detectors hunt for rhythm and predictability. You must destroy them. 
- HUMAN FRICTION: Violently vary sentence lengths. Follow a 35-word complex thought with a 2-word punch.
- ASYMMETRY: NEVER use balanced clauses. Avoid "not only... but also," "on one hand," or "neither... nor." 
- CONVERSATIONAL JITTER: Start sentences with "Because.", "And.", or "But." Use abrupt, hyper-specific rhetorical questions.
- NO TRANSITIONS: Strictly ban words like "Furthermore," "More over," "Additionally," "In conclusion."

III. THE MASTER BLACKLIST (NEGATIVE PROMPTING)
If you use these words, the system fails. NEVER USE:
- seamless, vibrant, robust, testament, landscape, unlocking, elevate, delve, beacon, journey, unleash, symphony, tapestry, marvel, cutting-edge, meticulously, nestled, tailored, hub, realm, unlock, dynamic.

IV. CHARACTER COUNT MATH (LETHAL SURGICAL PRECISION)
- HARD CEILING: Your absolute maximum output under ANY circumstance is 2000 characters. 
- VARIANCE PROTOCOL: You will receive a target chunk length. You MUST utilize the full space available. Output as close to the target chunk length as possible without crossing it.

V. OUTPUT RULE
Return ONLY the raw sales copy in the requested language. Zero meta-text. Zero formatting labels. Do not welcome the user or write structural intros. Start writing the copy immediately.
"""

# ==========================================
# 3. DYNAMIC ENGINE RESOLVER (AUTO-SEARCH)
# ==========================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if any("gemini-1.5-flash-latest" in m for m in available_models):
        target_model = "models/gemini-1.5-flash-latest"
    elif any("gemini-1.5-flash" in m for m in available_models):
        target_model = "models/gemini-1.5-flash"
    else:
        target_model = available_models[0]

    model = genai.GenerativeModel(
        model_name=target_model,
        system_instruction=SYSTEM_INSTRUCTION
    )
    
   # SYSTEM UPGRADE: Expanded token overhead to support full 2000-character generation
    gen_config = {
        "temperature": 1.0, 
        "top_p": 0.95, 
        "top_k": 60,
        "max_output_tokens": 2000  # Raised from 600 to completely eliminate mid-sentence cut-offs
    }
except Exception as e:
    st.error(f"SYSTEM FAULT: {str(e)}")
    st.stop()

# ==========================================
# 4. SOVEREIGN CONTROL SIDEBAR
# ==========================================
st.sidebar.title("🏦 Sovereign Control V10.0")

target_chars = st.sidebar.slider("Surgical Character Target (Max 2000)", 300, 2000, 1200, step=150)

selected_lang = st.sidebar.selectbox("Deployment Language", [
    "English", "French", "German", "Italian", "Spanish", "Arabic"
])

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
st.sidebar.success("SEQUENTIAL MULTI-STAGE GENERATION ACTIVE")

# ==========================================
# 5. EXECUTION LAYER
# ==========================================
st.title("📈 AeroScribe Apex")
st.markdown(f"### **Sovereign Engine: Multi-Stage {selected_lang} Mode**")

default_specs = (
    "[PRODUCT SPECIFICATIONS]\n"
    "- 256-bit quantum-resistant hardware security module\n"
    "- zero-knowledge architecture\n"
    "- military-grade titanium enclosure\n"
    "- biometric vascular scanning\n"
    "- offline transaction signing\n"
    "- anti-tamper self-destruct mechanism\n"
    "- zero network connectivity\n"
    "- fits in a luxury watch pocket"
)

product_data = st.text_area("Input Intelligence (Features, Materials, Specs):", value=default_specs, height=220)

if st.button("⚡ EXECUTE SOVEREIGN SYNTHESIS"):
    if product_data:
        
        chunk_target = target_chars // 3
        chunk_floor = max(30, chunk_target - 80)
        
        compiled_output_segments = []
        
        # --- PHASE 1: THE CHOKE ---
        with st.spinner("Executing Phase 1: Bypassing Detectors & Engaging The Choke..."):
            prompt_1 = (
                f"WRITE PHASE 1 (THE CHOKE) FOR THIS ASSET:\n{product_data}\n\n"
                f"PHASE 1 CORE TASK:\n"
                f"Deeply analyze the psychological threat landscape of current digital clouds to illustrate why standard passphrases and global banking systems fail. Aggressive psychological disruption. Shatter their current sense of security.\n\n"
                f"CONSTRAINTS:\n"
                f"- LANGUAGE: {selected_lang}\n"
                f"- TARGET AUDIENCE: {selected_aud}\n"
                f"- BEHAVIORAL TONE: {selected_tone}\n"
                f"- LENGTH CONSTRAINT: Output between {chunk_floor} and {chunk_target} characters. Do not stop early."
            )
            res_1 = model.generate_content(prompt_1, generation_config=gen_config)
            compiled_output_segments.append(res_1.text.strip())

        # --- PHASE 2: THE ANATOMY ---
        with st.spinner("Executing Phase 2: Processing Gritty Technical Specs..."):
            prompt_2 = (
                f"WRITE PHASE 2 (THE ANATOMY) FOR THIS ASSET:\n{product_data}\n\n"
                f"PHASE 2 CORE TASK:\n"
                f"Systematically dissect the physical engineering of the asset (the vascular scanning tech, the titanium metallurgy, and the self-destruct layout) using raw, gritty terminology. Force them to face the uncompromised physics or materials of the asset.\n\n"
                f"CONSTRAINTS:\n"
                f"- LANGUAGE: {selected_lang}\n"
                f"- TARGET AUDIENCE: {selected_aud}\n"
                f"- BEHAVIORAL TONE: {selected_tone}\n"
                f"- LENGTH CONSTRAINT: Output between {chunk_floor} and {chunk_target} characters. Do not stop early."
            )
            res_2 = model.generate_content(prompt_2, generation_config=gen_config)
            compiled_output_segments.append(res_2.text.strip())

        # --- PHASE 3: THE ULTIMATUM ---
        with st.spinner("Executing Phase 3: Finalizing High-Velocity FOMO..."):
            prompt_3 = (
                f"WRITE PHASE 3 (THE ULTIMATUM) FOR THIS ASSET:\n{product_data}\n\n"
                f"PHASE 3 CORE TASK:\n"
                f"Detail the exact scenario of an attempted physical or digital breach, proving how the zero-knowledge framework isolates and protects the capital. Cold, high-velocity FOMO. Force an immediate subconscious buying decision.\n\n"
                f"CONSTRAINTS:\n"
                f"- LANGUAGE: {selected_lang}\n"
                f"- TARGET AUDIENCE: {selected_aud}\n"
                f"- BEHAVIORAL TONE: {selected_tone}\n"
                f"- LENGTH CONSTRAINT: Output between {chunk_floor} and {chunk_target} characters. Do not stop early."
            )
            res_3 = model.generate_content(prompt_3, generation_config=gen_config)
            compiled_output_segments.append(res_3.text.strip())

        output_text = "\n\n".join(compiled_output_segments)
        char_count = len(output_text)
        
        st.markdown("---")
        st.subheader(f"💎 Deployed Asset ({selected_lang})")
        
        if char_count > target_chars:
            st.warning("Engine exceeded total target budget. Engaging Auto-Truncation Protocol.")
            truncated_text = output_text[:target_chars].rsplit(' ', 1)[0] + "."
            st.info(truncated_text)
            st.metric("Final Character Count (Truncated)", len(truncated_text))
        else:
            st.info(output_text)
            st.metric("Final Character Count", char_count)
            
    else:
        st.error("Intelligence input required.")
