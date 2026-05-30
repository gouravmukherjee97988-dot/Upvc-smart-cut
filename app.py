import streamlit as st
import re
import google.generativeai as genai
from PIL import Image
import json

# Custom CSS for Branded Layout - "Gourav Smart UPVC"
st.set_page_config(page_title="Gourav Smart UPVC", page_icon="🪟", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6 !important; color: #000000 !important; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: bold !important; }
    .stButton>button { background-color: #0056b3 !important; color: #ffffff !important; font-weight: bold !important; border-radius: 8px !important; height: 50px !important; font-size: 18px !important; border: 2px solid #002244 !important; }
    input { color: #000000 !important; font-weight: bold !important; }
    div[data-testid="stExpander"] { background-color: #eef4fc !important; border: 2px solid #003366 !important; border-radius: 8px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] div { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪟 Gourav Smart UPVC | AI Photo Scanner")
st.write("Workshop Special - Parchi ki photo kheechein aur poora cutting bill auto-generate karein.")

# --- CONFIGURATION ---
STANDARD_BAR = 5800  
BLADE_THICKNESS = 3  

# =========================================================================
# ⚙️ 1. API KEY & FORMULA SETTING
# =========================================================================
st.header("⚙️ 1. AI & FORMULA SETTING")
with st.container():
    c_set1, c_set2, c_set3 = st.columns(3)
    with c_set1:
        # FREE API KEY daalne ki jagah
        api_key = st.text_input("Apni FREE Gemini API Key Dalein:", type="password", placeholder="Yahan API key paste karein...")
    with c_set2:
        custom_w_formula = st.text_input("Sash WIDTH Formula:", value="(W - 52 - 52 - 5 + 58 + 16) / 2 + 5")
    with c_set3:
        custom_h_formula = st.text_input("Sash HEIGHT Formula:", value="H - 50")

# --- MATH EVALUATOR ---
def evaluate_custom_formula(formula_str, w_val, h_val):
    try:
        c_str = formula_str.lower().replace(' ', '').replace('width', str(w_val)).replace('w', str(w_val)).replace('height', str(h_val)).replace('h', str(h_val))
        if not re.match(r'^[\d\+\-\*\/\(\)\.]+$', c_str): return "Error"
        return int(round(eval(c_str)))
    except: return "Error"

# --- CUTTING STOCK OPTIMIZER ---
def cutting_stock_1d(stock_length, pieces, kerf):
    pieces.sort(reverse=True)
    bars_used = []
    for piece in pieces:
        placed = False
        for bar in bars_used:
            if (stock_length - sum(bar) - (len(bar) * kerf)) >= piece:
                bar.append(piece)
                placed = True
                break
        if not placed: bars_used.append([piece])
    return bars_used

# =========================================================================
# 📸 2. AI PHOTO UPLOAD & SCAN SECTION
# =========================================================================
st.markdown("---")
st.header("📸 2. UPLOAD OR TAKE PHOTO")
st.write("Site par likhi hui naap ki parchi ki photo yahan upload karein:")

uploaded_file = st.file_uploader("Parchi ya Excel sheet ki photo chunein...", type=["jpg", "jpeg", "png"])

window_list = []

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Aapki Upload Ki Hui Photo", width=300)
    
    if not api_key:
        st.warning("⚠️ AI Scan chalane ke liye upar apni FREE Gemini API Key dalein!")
    else:
        if st.button("🔍 AI SCAN START KAREIN"):
            with st.spinner("AI photo se size padh raha hai, thoda rukiye..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = """
                    Look at this image of a window size list or bill. Extract all window entries with width, height, track type, and quantity.
                    Identify if the track is 2 Track, 2.5 Track, or 3 Track. If not specified, default to '2 Track'.
                    Provide the output STRICTLY as a valid JSON array of objects, with keys: "track", "width", "height", "qty". 
                    Example format: [{"track": "2 Track", "width": 1200, "height": 1500, "qty": 2}]
                    Do not write any markdown code blocks, just raw JSON text.
                    """
                    
                    response = model.generate_content([prompt, img])
                    
                    # Clean response text
                    clean_txt = response.text.replace("```json", "").replace("
```", "").strip()
                    parsed_data = json.loads(clean_txt)
                    st.session_state.scanned_windows = parsed_data
                    st.success("🎯 AI ne saare size ek baar me padh liye hain! Niche report dekhein.")
                except Exception as e:
                    st.error(f"❌ AI Scan me galti hui: {str(e)}")

# Check if data was scanned successfully
if 'scanned_windows' in st.session_state and st.session_state.scanned_windows:
    window_list = st.session_state.scanned_windows
    
    st.markdown("---")
    st.subheader("📋 AI Ne Jo Size Padhe (Confirmation Grid):")
    for idx, win in enumerate(window_list, 1):
        st.write(f"Line {idx} ➔ **{win['track']}** | Width: `{win['width']} mm` | Height: `{win['height']} mm` | Qty: `{win['qty']} Pcs`")

    # =========================================================================
    # 🔴 CALCULATE OUTPUT ON SCANNED DATA
    # =========================================================================
    st.write("")
    if st.button("🔴 GENERATE FULL SITE LAYOUT & MATERIAL BILL (From Photo)", type="primary"):
        total_glass_area, total_mesh_area = 0, 0
        total_frame_2t_m, total_frame_3t_m, total_sash_m = 0, 0, 0
        total_rollers, total_mesh_rollers, total_locks, total_gasket, total_wool_pile = 0, 0, 0, 0, 0
        all_frame_2t_pieces, all_frame_3t_pieces, all_sash_pieces, all_mesh_pieces = [], [], [], []
        sash_sizes_display = []
        
        for idx, win in enumerate(window_list, 1):
            t = win["track"]
            w = int(win["width"])
            h = int(win["height"])
            qty = int(win["qty"])
            
            sash_w = evaluate_custom_formula(custom_w_formula, w, h)
            sash_h = evaluate_custom_formula(custom_h_formula, w, h)
            
            if t == "2 Track":
                num_sash = 2
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_2t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_2t_pieces.extend([w, w, h, h] * qty)
                total_rollers += 4 * qty
                total_locks += 2 * qty
                sash_sizes_display.append(f"🔹 **Window No. {idx} ({t}):** Sash = `{sash_w}x{sash_h} mm` | Qty: {num_sash * qty} Palles")
                
            elif t == "2.5 Track":
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * 2 * qty
                total_mesh_area += (sash_w / 304.8) * (sash_h / 304.8) * 1 * qty
                total_frame_3t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_3t_pieces.extend([w, w, h, h] * qty)
                all_sash_pieces.extend([sash_w] * (4 * qty))
                all_sash_pieces.extend([sash_h] * (4 * qty))
                all_mesh_pieces.extend([sash_w] * (2 * qty))
                all_mesh_pieces.extend([sash_h] * (2 * qty))
                total_rollers += 4 * qty
                total_mesh_rollers += 2 * qty
                total_locks += 3 * qty
                sash_sizes_display.append(f"🔹 **Window No. {idx} ({t}):** Glass Sash = `{sash_w}x{sash_h} mm` | Mesh = `{sash_w}x{sash_h} mm`")
                
            elif t == "3 Track":
                num_sash = 3
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_3t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_3t_pieces.extend([w, w, h, h] * qty)
                total_rollers += 6 * qty
                total_locks += 3 * qty
                sash_sizes_display.append(f"🔹 **Window No. {idx} ({t}):** Sash = `{sash_w}x{sash_h} mm` | Qty: {num_sash * qty} Palles")

            if t != "2.5 Track":
                all_sash_pieces.extend([sash_w] * (2 * num_sash * qty))
                all_sash_pieces.extend([sash_h] * (2 * num_sash * qty))
            
            current_sash_total_mm = ((sash_w * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2)) + (sash_h * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2))) * qty
            total_sash_m += current_sash_total_mm / 1000
            total_gasket += (current_sash_total_mm * 2) / 1000
            total_wool_pile += ((sash_h * 4) + (sash_w * 2)) * qty / 1000

        # --- OUTPUT ---
        st.header("🏢 FINAL MATERIAL BILL SUMMARY")
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            st.write(f"⬛ **Glass:** `{total_glass_area:.2f} Sq.Ft.`")
            if total_mesh_area > 0: st.write(f"🕸️ **Mesh (Jaali):** `{total_mesh_area:.2f} Sq.Ft.`")
        with c_m2:
            if total_frame_2t_m > 0: st.write(f"🔹 **2-Track Frame:** `{total_frame_2t_m:.2f} Mtrs`")
            if total_frame_3t_m > 0: st.write(f"🔸 **3-Track Frame:** `{total_frame_3t_m:.2f} Mtrs`")
        with c_m3:
            st.write(f"🟩 **Total Sash Profile:** `{total_sash_m:.2f} Mtrs`")

        st.subheader("📦 Accessories Breakdown:")
        st.write(f"🛞 Rollers: **{total_rollers} Pcs** | 🔒 Locks: **{total_locks} Pcs** | ⚫ Gasket: **{total_gasket:.1f} Mtrs**")
        
        st.write("---")
        st.header("📐 SINGLE SASH SIZES FROM PHOTO")
        for size_info in sash_sizes_display: st.write(size_info)
        
        st.write("---")
        st.header("📐 BAR OPTIMIZED CUTTING PLANS")
        
        if all_frame_2t_pieces:
            st.subheader("🖼️ 2-Track Frame Plan")
            bars = cutting_stock_1d(STANDARD_BAR, all_frame_2t_pieces, BLADE_THICKNESS)
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"FRAME BAR {idx} -> Kaato: {bar}"): st.write(f"➔ `{bar}`")

        if all_frame_3t_pieces:
            st.subheader("🖼️ 3-Track Frame Plan")
            bars = cutting_stock_1d(STANDARD_BAR, all_frame_3t_pieces, BLADE_THICKNESS)
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"3-TRACK BAR {idx} -> Kaato: {bar}"): st.write(f"➔ `{bar}`")

        if all_sash_pieces:
            st.subheader("🪟 Glass Sash Profile Plan")
            bars = cutting_stock_1d(STANDARD_BAR, all_sash_pieces, BLADE_THICKNESS)
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"SASH BAR {idx} -> Kaato: {bar}"): st.write(f"➔ `{bar}`")
