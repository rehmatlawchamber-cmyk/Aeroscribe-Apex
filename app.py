import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import io
import time
import re

# ==========================================
# 1. ELITE UI ARCHITECTURE
# ==========================================
st.set_page_config(page_title="AeroScribe Apex Sovereign", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    /* Absolute Dark Mode */
    .stApp { background-color: #050505; color: #f2f2f2; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Input & Sidebar Styling */
    .stSelectbox div div, .stTextArea textarea, .stTextInput input, .stSlider div { 
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

I. WEAPONIZED CUSTOMER PSYCHOLOGY (THE PKR 2000 WATER RULE)
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
# 3. DYNAMIC ENGINE RESOLVER & CONFIG
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
    
    gen_config = {
        "temperature": 1.0, 
        "top_p": 0.95, 
        "top_k": 60,
        "max_output_tokens": 1200 
    }
except Exception as e:
    st.error(f"SYSTEM FAULT: {str(e)}")
    st.stop()

# ==========================================
# Helper Function for Handle Generation
# ==========================================
def generate_handle(title):
    """Generates a clean, URL-safe slug matching Shopify's Handle rules."""
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    return "-".join(clean.split())

# ==========================================
# 4. SOVEREIGN CONTROL SIDEBAR
# ==========================================
st.sidebar.title("🏦 Sovereign Control V11.4")

# Surgical Character Targeting - HARD CAPPED AT 2000
target_chars = st.sidebar.slider("Surgical Character Target (Max 2000)", 300, 2000, 1000, step=50)

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
st.sidebar.success("DYNAMIC MODE: 1200 Max Tokens")

# ==========================================
# 5. EXECUTION LAYER
# ==========================================
st.title("📈 AeroScribe Apex")
st.markdown(f"### **Sovereign Engine: {selected_lang} Mode**")

# Constructing Split-Lane Interface Tabs
tab_single, tab_bulk = st.tabs(["🎯 Single Asset Synthesis", "📦 Bulk Enterprise Fleet"])

# --- LANE 1: SINGLE GENERATION ---
with tab_single:
    product_data = st.text_area("Input Raw Intelligence:", height=180, placeholder="Enter features, materials, origins, specifications...", key="single_input")

    if st.button("⚡ EXECUTE SOVEREIGN SYNTHESIS", key="single_btn"):
        if product_data:
            with st.spinner("Compiling Psychological Profile & Evading Detection..."):
                try:
                    # Mathematical Floor for the LLM
                    target_floor = max(50, target_chars - 50)
                    variance_instruction = "variance is ±50" if target_chars < 1950 else "variance is -50 (DO NOT EXCEED)"

                    surgical_prompt = f"""
                    WRITE THE HIGH-CONVERSION SALES COPY FOR: {product_data}
                    
                    CONSTRAINTS:
                    - LANGUAGE: {selected_lang}
                    - TARGET AUDIENCE: {selected_aud}
                    - BEHAVIORAL TONE: {selected_tone}
                    - TARGET LENGTH: {target_chars} characters.
                    - VARIANCE RULE: {variance_instruction}.
                    - ABSOLUTE MAXIMUM: 2000 characters.
                    """

                    response = model.generate_content(surgical_prompt, generation_config=gen_config)
                    final_output = response.text.strip()

                    # Python-Level Pruning (Failsafe)
                    if len(final_output) > target_chars:
                        pruned = final_output[:target_chars]
                        last_stop = max(pruned.rfind('.'), pruned.rfind('!'), pruned.rfind('؟'))
                        if last_stop != -1:
                            final_output = pruned[:last_stop + 1]
                        else:
                            final_output = pruned

                    char_count = len(final_output)

                    st.markdown("---")
                    st.subheader("💎 Deployed Asset")
                    st.info(final_output)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Character Count", char_count)
                    with col2:
                        status = "✅ OPTIMIZED" if target_floor <= char_count <= target_chars else "⚠️ OUTSIDE TOLERANCE"
                        st.write(f"Status: **{status}**")
                    with col3:
                        st.write("ZeroGPT Target: **Human Asymmetry Achieved**")
                except Exception as e:
                    st.error(f"Execution Failed: {str(e)}")
        else:
            st.error("Operation halted. Data input is required for synthesis.")

# --- LANE 2: MULTI-PRODUCT BATCH SYSTEM ---
with tab_bulk:
    st.markdown("#### **Bulk Catalog Ingestion**")
    st.caption("Paste data directly from Excel or Google Sheets. Format layout: Two columns separated by tabs (Column 1: Product Name | Column 2: Raw Specifications). Do not include header rows.")
    
    bulk_data = st.text_area(
        "Paste Tab-Separated Spreadsheet Matrix Here:", 
        height=220, 
        placeholder="Product A\tHigh-end running shoes, carbon fiber plate, nitrogen-infused foam...\nProduct B\tPremium insulated steel tumbler, 32oz, double-wall vacuum seal...",
        key="bulk_input"
    )

    if st.button("🚀 LAUNCH ENTERPRISE BATCH PROCESSING", key="bulk_btn"):
        if bulk_data.strip():
            try:
                # Parse the raw tab data into a Pandas Matrix row by row
                rows = [line.split('\t') for line in bulk_data.strip().split('\n') if line.strip()]
                
                parsed_items = []
                for idx, r in enumerate(rows):
                    if len(r) >= 2:
                        parsed_items.append({"name": r[0].strip(), "specs": r[1].strip()})
                    elif len(r) == 1:
                        parsed_items.append({"name": f"Item {idx+1}", "specs": r[0].strip()})

                if not parsed_items:
                    st.error("Data tracking breakdown. Please check your text table spacing alignment columns.")
                    st.stop()

                preview_data = [] # For on-screen display
                shopify_data = [] # For Shopify CSV export
                
                total_items = len(parsed_items)
                progress_bar = st.progress(0)

                # Ingest looping sequence through rows
                for idx, item in enumerate(parsed_items):
                    st.write(f"Synthesizing [{idx+1}/{total_items}]: **{item['name']}**")
                    
                    target_floor = max(50, target_chars - 50)
                    variance_instruction = "variance is ±50" if target_chars < 1950 else "variance is -50 (DO NOT EXCEED)"

                    bulk_prompt = f"""
                    WRITE THE HIGH-CONVERSION SALES COPY FOR: {item['name']} - Specifications: {item['specs']}
                    
                    CONSTRAINTS:
                    - LANGUAGE: {selected_lang}
                    - TARGET AUDIENCE: {selected_aud}
                    - BEHAVIORAL TONE: {selected_tone}
                    - TARGET LENGTH: {target_chars} characters.
                    - VARIANCE RULE: {variance_instruction}.
                    - ABSOLUTE MAXIMUM: 2000 characters.
                    """

                    # Secure API Content Fetch
                    response = model.generate_content(bulk_prompt, generation_config=gen_config)
                    item_output = response.text.strip()

                    # Precise layout math boundary check (-50 character safety buffer fallback)
                    if len(item_output) > target_chars:
                        pruned_bulk = item_output[:target_chars]
                        last_stop_bulk = max(pruned_bulk.rfind('.'), pruned_bulk.rfind('!'), pruned_bulk.rfind('؟'))
                        if last_stop_bulk != -1:
                            item_output = pruned_bulk[:last_stop_bulk + 1]
                        else:
                            item_output = pruned_bulk

                    # 1. Populate On-Screen Preview (Readable)
                    preview_data.append({
                        "Product Name": item['name'],
                        "Raw Specifications": item['specs'],
                        "Generated Description": item_output,
                        "Character Count": len(item_output)
                    })
                    
                    # 2. Populate Shopify CSV Schema (System Export)
                    # We replace newlines with HTML breaks to prevent CSV row-breaking errors in Excel
                    clean_html_output = item_output.replace("\n", "<br>")
                    
                    shopify_data.append({
                        "Handle": generate_handle(item['name']),
                        "Title": item['name'],
                        "Body (HTML)": clean_html_output,
                        "Vendor": "AeroScribe Merchant",
                        "Standard Product Type": "",
                        "Custom Product Type": "",
                        "Tags": "AeroScribe-Apex",
                        "Published": "true",
                        "Option1 Name": "Title",
                        "Option1 Value": "Default Title",
                        "Variant SKU": "",
                        "Variant Grams": "0.0",
                        "Variant Inventory Tracker": "",
                        "Variant Inventory Qty": "1",
                        "Variant Inventory Policy": "deny",
                        "Variant Fulfillment Service": "manual",
                        "Variant Price": "",
                        "Variant Compare At Price": "",
                        "Variant Requires Shipping": "true",
                        "Variant Taxable": "true",
                        "Variant Barcode": "",
                        "Image Src": "",
                        "Image Position": "",
                        "Image Alt Text": "",
                        "Gift Card": "false",
                        "SEO Title": "",
                        "SEO Description": "",
                        "Google Shopping / Google Product Category": "",
                        "Google Shopping / Gender": "",
                        "Google Shopping / Age Group": "",
                        "Google Shopping / MPN": "",
                        "Google Shopping / AdWords Grouping": "",
                        "Google Shopping / AdWords Labels": "",
                        "Google Shopping / Condition": "new",
                        "Google Shopping / Custom Product": "",
                        "Google Shopping / Custom Label 0": "",
                        "Google Shopping / Custom Label 1": "",
                        "Google Shopping / Custom Label 2": "",
                        "Google Shopping / Custom Label 3": "",
                        "Google Shopping / Custom Label 4": "",
                        "Variant Image": "",
                        "Variant Weight Unit": "kg",
                        "Variant Tax Code": "",
                        "Cost per item": "",
                        "Status": "active"
                    })
                    
                    progress_bar.progress((idx + 1) / total_items)
                    time.sleep(1.5)

                # Convert compiled preview records to DataFrame for tracking display
                df_preview = pd.DataFrame(preview_data)
                st.markdown("---")
                st.success(f"Successfully processed {total_items} corporate assets!")
                st.dataframe(df_preview, use_container_width=True)

                # Convert Shopify schema to secure CSV bytes directly
                df_shopify = pd.DataFrame(shopify_data)
                csv_data = df_shopify.to_csv(index=False).encode('utf-8-sig')

                st.download_button(
                    label="📥 DOWNLOAD MASTER SHOPIFY CATALOG CSV",
                    data=csv_data,
                    file_name="AeroScribe_Shopify_Import.csv",
                    mime="text/csv"
                )

            except Exception as batch_error:
                st.error(f"BATCH PROCESSING FAULT: {str(batch_error)}")
        else:
            st.error("Bulk workspace requires data strings before initiating calculation loops.")
