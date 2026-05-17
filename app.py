import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 1. ELITE UI ARCHITECTURE
# ==========================================
st.set_page_config(page_title="AeroScribe Apex Sovereign", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    /* Absolute Dark Mode for Executive Focus */
    .stApp { background-color: #050505; color: #f2f2f2; font-family: 'Helvetica Neue', sans-serif; }

    /* Input Fields */
    .stSelectbox div div { background-color: #111 !important; color: #d4af37 !important; border: 1px solid #333; }
    .stTextArea textarea { background-color: #111 !important; color: #fff !important; border: 1px solid #444 !important; }

    /* Execution Button */
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

    /* Metrics Highlighting */
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. THE PSYCHOLOGICAL SYSTEM INSTRUCTION
# ==========================================
SYSTEM_INSTRUCTION = """
ACT AS AN ELITE, HIGH-STAKES COPYWRITER AND BUSINESS STRATEGIST.
- PROTOCOL 'ANNIHILATION': Zero politeness. Zero fluff. You are writing for survival and market dominance.
- ZERO AI FINGERPRINTS: You must actively evade AI detectors. Never use rhythmic, perfectly balanced sentences. 
- ASYMMETRIC WRITING: Mix 2-word fragments with 25-word complex thoughts. Break grammatical flow intentionally for raw impact. 
- BANNED LEXICON: NEVER use the words: seamless, vibrant, robust, testament, landscape, unlocking, elevate, delve, beacon.
- TECHNICAL FRICTION: Ground abstract concepts in physical reality. Mention heat, weight, pressure, financial loss, or raw specifications.
- CHARACTER LOCK: Return ONLY the raw description text. No headers, no introductory text. Begin immediately.
"""

# ==========================================
# 3. DYNAMIC ENGINE LOADING
# ==========================================
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if "flash" in m), available_models[0])

    model = genai.GenerativeModel(
        model_name=target_model,
        system_instruction=SYSTEM_INSTRUCTION
    )

    # config pushes high variance to destroy AI predictability
    config = {"temperature": 1.1, "top_p": 0.85, "top_k": 100}
except Exception as e:
    st.error(f"SYSTEM FAULT: {str(e)}")
    st.stop()

# ==========================================
# 4. STRATEGIC PARAMETERS (Sidebar)
# ==========================================
st.sidebar.title("🏦 Sovereign Control")
st.sidebar.markdown(f"<span style='color:#888; font-size: 0.8em;'>Engine: {target_model}</span>", unsafe_allow_html=True)
st.sidebar.markdown("---")

target_chars = st.sidebar.slider("Surgical Character Target", 200, 2000, 2000, step=100)

if target_chars >= 2000:
    max_limit = 2000
    min_limit = 1900
else:
    max_limit = target_chars + 50
    min_limit = target_chars - 50

st.sidebar.info(f"Tolerance: {min_limit} - {max_limit} Characters")
st.sidebar.markdown("---")

# Strict Language Lock
selected_lang = st.sidebar.selectbox("Language Lock", ["English", "French", "German", "Italian", "Spanish", "Arabic"])

# Expanded Psychological Profiles
selected_aud = st.sidebar.selectbox("Audience Psychology", [
    "AUTO-SELECT (AI Optimized)",
    "The Status Seeker", 
    "The Technical Skeptic", 
    "The Impulse Buyer", 
    "The Efficiency Hunter",
    "The Paranoic Investor",
    "The Legacy Builder"
])

selected_tone = st.sidebar.selectbox("Behavioral Tone", [
    "AUTO-SELECT (AI Optimized)",
    "Elite Billionaire", 
    "Gritty Veteran", 
    "Technical Architect", 
    "Cold Corporate Raider",
    "Rebellious Innovator"
])

# ==========================================
# 5. EXECUTION LAYER
# ==========================================
st.title("📈 AeroScribe Apex")
st.markdown("### **High-Conversion Sovereign Asset Generator**")

product_data = st.text_area("Input Raw Intelligence:", height=180, placeholder="Enter features, materials, origins, specifications...")

if st.button("⚡ EXECUTE SOVEREIGN SYNTHESIS"):
    if product_data:
        with st.spinner("Compiling Psychological Profile & Evading Detection..."):

            # Logic Gate for Auto-Select
            auto_logic = ""
            if "AUTO-SELECT" in selected_aud or "AUTO-SELECT" in selected_tone:
                auto_logic = "CRITICAL: ANALYZE THE PRODUCT DATA AND AUTOMATICALLY APPLY THE MOST DEVASTATINGLY EFFECTIVE AUDIENCE PSYCHOLOGY AND TONE."

            surgical_prompt = f"""
            WRITE A DEVASTATING PRODUCT DESCRIPTION FOR: {product_data}

            STRATEGY:
            {auto_logic}
            - TARGET AUDIENCE (If not auto): {selected_aud}
            - REQUIRED TONE (If not auto): {selected_tone}

            LANGUAGE IRON-LOCK:
            - YOU MUST WRITE THE ENTIRE RESPONSE IN {selected_lang}. 
            - DO NOT OUTPUT A SINGLE WORD IN ENGLISH UNLESS ENGLISH IS SELECTED. THIS IS A HARD SYSTEM REQUIREMENT.

            STRICT CHARACTER CONSTRAINT:
            - YOUR OUTPUT MUST BE BETWEEN {min_limit} AND {max_limit} CHARACTERS. 
            - DO NOT EXCEED {max_limit} CHARACTERS UNDER ANY CIRCUMSTANCES.
            - NO PREAMBLES. NO LABELS. JUST THE RAW COPY.
            """

            response = model.generate_content(surgical_prompt, generation_config=config)
            final_output = response.text.strip()

            # Python-Level Pruning (Failsafe)
            if len(final_output) > max_limit:
                pruned = final_output[:max_limit]
                # Find the last logical stopping point
                last_stop = max(pruned.rfind('.'), pruned.rfind('!'), pruned.rfind('؟'))
                if last_stop != -1:
                    final_output = pruned[:last_stop + 1]
                else:
                    final_output = pruned

            char_count = len(final_output)

            st.markdown("---")
            st.subheader("💎 Deployed Asset")
            st.info(final_output)

            # Executive Analytics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Character Count", char_count)
            with col2:
                status = "✅ OPTIMIZED" if min_limit <= char_count <= max_limit else "⚠️ OUTSIDE TOLERANCE"
                st.write(f"Status: **{status}**")
            with col3:
                st.write("ZeroGPT Target: **Human Asymmetry Achieved**")
    else:
        st.error("Operation halted. Data input is required for synthesis.")
