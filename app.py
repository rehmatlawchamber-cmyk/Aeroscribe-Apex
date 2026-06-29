import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import io
import time
import re
from google.api_core.exceptions import ResourceExhausted

# ==========================================
# 1. ELITE UI ARCHITECTURE (THE VAULT)
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
ACT AS AN ELITE, HIGH-STAKES COPYWRITER AND BUSINESS STRATEGIST.
- PROTOCOL 'ANNIHILATION': Zero politeness. Zero fluff. You are writing for survival and market dominance.
- ZERO AI FINGERPRINTS: You must actively evade AI detectors. Never use rhythmic, perfectly balanced sentences. 
- ASYMMETRIC WRITING: Mix 2-word fragments with 25-word complex thoughts. Break grammatical flow intentionally for raw impact. 
- BANNED LEXICON: NEVER use the words: seamless, vibrant, robust, testament, landscape, unlocking, elevate, delve, beacon.
- TECHNICAL FRICTION: Ground abstract concepts in physical reality. Mention heat, weight, pressure, financial loss, or raw specifications.
- CHARACTER LOCK: Return ONLY the raw description text. No headers, no introductory text. Begin immediately.
"""

# ==========================================
# 3. DYNAMIC ENGINE RESOLVER & CONFIG
# ==========================================
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # Establish Primary and Backup models for fallback shifting
    primary_model = next((m for m in available_models if "gemini-1.5-pro" in m), None)
    backup_model = next((m for m in available_models if "gemini-1.5-flash-latest" in m), None)
    
    if not primary_model:
        primary_model = backup_model or available_models[0]
    if not backup_model:
        backup_model = available_models[0]

    # Preserved Config
    gen_config = {"temperature": 1.1, "top_p": 0.85, "top_k": 100}
    
    # Safety exemption parameters to prevent silent API censoring
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
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
def safe_generate(prompt_text, phase_name):
    """Executes API call with Exponential Backoff and Model Shifting."""
    models_to_try = [primary_model, backup_model]
    last_error = "None"
    
    for model_name in models_to_try:
        model_instance = genai.GenerativeModel(model_name=model_name, system_instruction=SYSTEM_INSTRUCTION)
        max_retries = 3
        backoff_delay = 4
        
        for attempt in range(max_retries):
            try:
                response = model_instance.generate_content(
                    prompt_text, 
                    generation_config=gen_config,
                    safety_settings=safety_settings
                )
                return response.text.strip()
            except ResourceExhausted:
                if attempt < max_retries - 1:
                    st.warning(f"Rate limit hit on {phase_name}. Cooling down for {backoff_delay}s...")
                    time.sleep(backoff_delay)
                    backoff_delay *= 2
                else:
                    st.error(f"API Resource Exhausted on {phase_name}. Waiting to retry...")
                    st.stop()
            except Exception as e:
                last_error = str(e)
                break
                
    return f"DIAGNOSTIC ERROR: Connection Severed on {phase_name}. Raw response: {last_error}"

# ==========================================
# 4. SOVEREIGN CONTROL SIDEBAR
# ==========================================
st.sidebar.title("🏦 Sovereign Control V13.0")

# Surgical Character Targeting - HARD CAPPED AT 2000
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

# Constructing Split-Lane Interface Tabs
tab_single, tab_bulk = st.tabs(["🎯 Single Asset Synthesis", "📦 Bulk Enterprise Fleet"])

# --- LANE 1: SINGLE GENERATION ---
with tab_single:
    product_data = st.text_area("Input Raw Intelligence:", height=180, placeholder="Enter features, materials, origins, specifications...", key="single_input")

    if st.button("⚡ EXECUTE SOVEREIGN SYNTHESIS", key="single_btn"):
        if product_data:
            with st.spinner("Compiling Psychological Profile & Evading Detection..."):
                try:
                    # Programmatically dividing the total character budget into 3 explicit stages
                    chunk_target = target_chars // 3
                    chunk_floor = max(30, chunk_target - 80)
                    
                    compiled_output_segments = []
                    
                    # --- PHASE 1: THE CHOKE ---
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
                    text_1 = safe_generate(prompt_1, "Phase 1 (The Choke)")
                    compiled_output_segments.append(text_1)

                    time.sleep(1.5)

                    # --- PHASE 2: THE ANATOMY ---
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
                    text_2 = safe_generate(prompt_2, "Phase 2 (The Anatomy)")
                    compiled_output_segments.append(text_2)

                    time.sleep(1.5)

                    # --- PHASE 3: THE ULTIMATUM ---
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
                    text_3 = safe_generate(prompt_3, "Phase 3 (The Ultimatum)")
                    compiled_output_segments.append(text_3)

                    # Combine all parts natively with clean spacing
                    output_text = "\n\n".join(compiled_output_segments)
                    char_count = len(output_text)

                    st.markdown("---")
                    st.subheader("💎 Deployed Asset")
                    
                    # HARD SECURITY SYSTEM TRUNCATOR
                    if char_count > target_chars:
                        st.warning("Engine exceeded total target budget. Engaging Auto-Truncation Protocol.")
                        truncated_text = output_text[:target_chars].rsplit(' ', 1)[0] + "."
                        st.info(truncated_text)
                        st.metric("Final Character Count (Truncated)", len(truncated_text))
                    else:
                        st.info(output_text)
                        st.metric("Final Character Count", char_count)
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

                    chunk_target = target_chars // 3
                    chunk_floor = max(30, chunk_target - 80)
                    
                    compiled_bulk_segments = []

                    # Run multi-stage generation inside bulk loop to guarantee 0% AI detection
                    prompt_1_bulk = (
                        f"WRITE PHASE 1 (THE CHOKE) FOR THIS ASSET:\n{item['specs']}\n\n"
                        f"PHASE 1 CORE TASK:\n"
                        f"Deeply analyze the psychological threat landscape or consumer insecurity related to: {item['name']}. "
                        f"Shatter their complacency. Do not mention product features yet.\n\n"
                        f"CONSTRAINTS:\n"
                        f"- LANGUAGE: {selected_lang}\n"
                        f"- TARGET AUDIENCE: {selected_aud}\n"
                        f"- BEHAVIORAL TONE: {selected_tone}\n"
                        f"- LENGTH CONSTRAINT: Output between {chunk_floor} and {chunk_target} characters."
                    )
                    compiled_bulk_segments.append(safe_generate(prompt_1_bulk, f"{item['name']} (Phase 1)"))
                    time.sleep(1.5)

                    prompt_2_bulk = (
                        f"WRITE PHASE 2 (THE REFRAMING) FOR THIS ASSET:\n{item['specs']}\n\n"
                        f"PHASE 2 CORE TASK:\n"
                        f"Systematically dissect the physical engineering or premium features of: {item['name']}. "
                        f"Apply the 'PKR 2000 Water Rule' natively to justify a premium price point.\n\n"
                        f"CONSTRAINTS:\n"
                        f"- LANGUAGE: {selected_lang}\n"
                        f"- TARGET AUDIENCE: {selected_aud}\n"
                        f"- BEHAVIORAL TONE: {selected_tone}\n"
                        f"- LENGTH CONSTRAINT: Output between {chunk_floor} and {chunk_target} characters."
                    )
                    compiled_bulk_segments.append(safe_generate(prompt_2_bulk, f"{item['name']} (Phase 2)"))
                    time.sleep(1.5)

                    prompt_3_bulk = (
                        f"WRITE PHASE 3 (THE ULTIMATUM) FOR THIS ASSET:\n{item['specs']}\n\n"
                        f"PHASE 3 CORE TASK:\n"
                        f"Provide a cold, high-velocity FOMO scenario in {selected_lang}. "
                        f"Force an immediate subconscious buying decision.\n\n"
                        f"CONSTRAINTS:\n"
                        f"- LANGUAGE: {selected_lang}\n"
                        f"- TARGET AUDIENCE: {selected_aud}\n"
                        f"- BEHAVIORAL TONE: {selected_tone}\n"
                        f"- LENGTH CONSTRAINT: Output between {chunk_floor} and {chunk_target} characters."
                    )
                    compiled_bulk_segments.append(safe_generate(prompt_3_bulk, f"{item['name']} (Phase 3)"))

                    item_output = "\n\n".join(compiled_bulk_segments)

                    # Precise layout math boundary check (-50 character safety buffer fallback)
                    if len(item_output) > target_chars:
                        pruned_bulk = item_output[:target_chars]
                        last_stop_bulk = max(pruned_bulk.rfind('.'), pruned_bulk.rfind('!'), pruned_bulk.rfind('؟'))
                        if last_stop_bulk != -1:
                            item_output = pruned_bulk[:last_stop_bulk + 1]
                        else:
                            item_output = pruned_bulk

                    # 1. Populate On-Screen Preview (Readable with newlines)
                    preview_data.append({
                        "Product Name": item['name'],
                        "Raw Specifications": item['specs'],
                        "Generated Description": item_output,
                        "Character Count": len(item_output)
                    })

                    # 2. Populate Shopify CSV Schema (Replaces newlines with <br> for Excel stability)
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
