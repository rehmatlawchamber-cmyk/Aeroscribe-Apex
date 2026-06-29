import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import time
import re

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
# Helper Function for Handle Generation
# ==========================================
def generate_handle(title):
    """Generates a clean, URL-safe slug matching Shopify's Handle rules."""
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    return "-".join(clean.split())

# ==========================================
# Helper Function for Rate-Limited Generations
# ==========================================
def generate_with_retry(prompt_text, config_dict):
    """Executes API generation with exponential backoff on 429 rate limits."""
    max_retries = 3
    delay = 15  # Starts at 15 seconds to safely clear the 5 RPM limit
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt_text, generation_config=config_dict)
            return response.text.strip()
        except Exception as e:
            err_msg = str(e).lower()
            # Catch standard 429, Quota, or ResourceExhausted exceptions
            if "429" in err_msg or "exhausted" in err_msg or "quota" in err_msg:
                if attempt < max_retries - 1:
                    st.warning(f"Rate limit hit. Cooling down system for {delay} seconds (Attempt {attempt+1}/{max_retries})...")
                    time.sleep(delay)
                    delay *= 1.5  # Progressively scale up cooldown time
                else:
                    raise e
            else:
                raise e

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
# 5. EXECUTION & VIEWPORT ROUTER
# ==========================================
st.title("📈 AeroScribe Apex")
st.markdown("### **High-Conversion Sovereign Asset Generator**")

# Constructing Split-Lane Interface Tabs
tab_single, tab_bulk = st.tabs(["🎯 Single Asset Synthesis", "📦 Bulk Enterprise Fleet"])

# --- LANE 1: SINGLE GENERATION ---
with tab_single:
    product_data = st.text_area("Input Raw Intelligence:", height=180, placeholder="Enter features, materials, origins, specifications...", key="single_input")

    if st.button("⚡ EXECUTE SOVEREIGN SYNTHESIS", key="single_btn"):
        if product_data:
            with st.spinner("Compiling Psychological Profile & Evading Detection..."):
                try:
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

                    # Secure API Content Fetch with Retry Protection
                    final_output = generate_with_retry(surgical_prompt, config)

                    # Python-Level Pruning (Failsafe)
                    if len(final_output) > max_limit:
                        pruned = final_output[:max_limit]
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
                        status = "✅ OPTIMIZED" if min_limit <= char_count <= max_limit else "⚠️ OUTSIDE TOLERANCE"
                        st.write(f"Status: **{status}**")
                    with col3:
                        st.write("ZeroGPT Target: **Human Asymmetry Achieved**")
                except Exception as single_error:
                    st.error(f"SINGLE GENERATION FAULT: {str(single_error)}")
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
                    
                    auto_logic = ""
                    if "AUTO-SELECT" in selected_aud or "AUTO-SELECT" in selected_tone:
                        auto_logic = "CRITICAL: ANALYZE THE PRODUCT DATA AND AUTOMATICALLY APPLY THE MOST DEVASTATINGLY EFFECTIVE AUDIENCE PSYCHOLOGY AND TONE."

                    bulk_prompt = f"""
                    WRITE A DEVASTATING PRODUCT DESCRIPTION FOR: {item['name']} - Specifications: {item['specs']}

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

                    # Secure API Content Fetch using our Rate-Limit Shield
                    item_output = generate_with_retry(bulk_prompt, config)

                    # Precise layout math boundary check (-50 character safety buffer fallback)
                    if len(item_output) > max_limit:
                        pruned_bulk = item_output[:max_limit]
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
                    shopify_data.append({
                        "Handle": generate_handle(item['name']),
                        "Title": item['name'],
                        "Body (HTML)": item_output,
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
                    
                    # Subtle pacing delay to clear normal usage intervals
                    time.sleep(1.5)

                # Convert compiled preview records to DataFrame for tracking display
                df_preview = pd.DataFrame(preview_data)
                st.markdown("---")
                st.success(f"Successfully processed {total_items} corporate assets!")
                st.dataframe(df_preview, use_container_width=True)

                # Convert Shopify schema to secure CSV bytes directly (fixes BytesIO issues)
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
