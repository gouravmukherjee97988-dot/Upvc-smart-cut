import streamlit as st
import re
import google.generativeai as genai
from PIL import Image
import json

# Page Config
st.set_page_config(page_title="Gourav Smart UPVC", page_icon="🪟", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6 !important; color: #000000 !important; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: bold !important; }
    .stButton>button { background-color: #0056b3 !important; color: #ffffff !important; font-weight: bold !important; border-radius: 8px !important; height: 50px !important; font-size: 18px !important; border: 2px solid #002244 !important; }
    input { color: #000000 !important; font-weight: bold !important; }
    select { color: #000000 !important; font-weight: bold !important; }
    div[data-testid="stExpander"] { background-color: #eef4fc !important; border: 2px solid #003366 !important; border-radius: 8px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] div { color: #000000 !important; font-weight: bold !important; }
    div[data-testid="stBlock"] { background-color: #ffffff !important; padding: 20px !important; border-radius: 8px !important; border: 1px solid #ccd1d9 !important; margin-bottom: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪟 Gourav Smart UPVC | AI Photo Optimizer")
st.write("Workshop Special - Secure Cloud Production Mode.")

STANDARD_BAR = 5800  
BLADE_THICKNESS = 3  

# Secrets se key safely uthane ke liye
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        API_KEY = st.secrets["gemini_api_key"]
except Exception:
    API_KEY = None

st.header("⚙️ 1. MASTER FORMULA SETTING")
with st.container():
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        custom_w_formula = st.text_input("Sash WIDTH Formula:", value="(W - 52 - 52 - 5 + 58 + 16) / 2 + 5")
    with col_f2:
        custom_h_formula = st.text_input("Sash HEIGHT Formula:", value="H - 50")

def evaluate_custom_formula(formula_str, w_val, h_val):
    try:
        c_str = formula_str.lower().replace(' ', '').replace('width', str(w_val)).replace('w', str(w_val)).replace('height', str(h_val)).replace('h', str(h_val))
        if not re.match(r'^[\d\+\-\*\/\(\)\.]+$', c_str): return "Error"
        return int(round(eval(c_str)))
    except: return "Error"

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

st.markdown("---")
st.header("📸 2. UPLOAD OR TAKE PHOTO")
uploaded_file = st.file_uploader("Parchi ki photo chunein...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Aapki Upload Ki Hui Photo", width=300)
    
    if not API_KEY:
        st.error("⚠️ Streamlit Secrets me API Key nahi mili! Settings me jaakar Secrets me key dalein.")
    else:
        if st.button("🔍 AI SCAN START KAREIN"):
            with st.spinner("AI photo se size padh raha hai..."):
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = """
                    Look at this image of a window size list or bill. Extract all window entries with width, height, track type, and quantity.
                    Identify if the track is 2 Track, 2.5 Track, or 3 Track. If not specified, default to '2 Track'.
                    Provide the output STRICTLY as a valid JSON array of objects, with keys: "track", "width", "height", "qty". 
                    Example format: [{"track": "2 Track", "width": 1200, "height": 1500, "qty": 2}]
                    Do not write any markdown code blocks, just raw JSON text.
                    """
                    response = model.generate_content([prompt, img])
                    clean_txt = response.text.replace("```json", "").replace("```", "").strip()
                    st.session_state.scanned_windows = json.loads(clean_txt)
                    st.success("🎯 AI ne saare size ek baar me padh liye hain! Niche report dekhein.")
                except Exception as e:
                    st.error(f"❌ AI Scan me galti hui: {str(e)}")

if 'scanned_windows' in st.session_state and st.session_state.scanned_windows:
    window_list = st.session_state.scanned_windows
    st.markdown("---")
    st.subheader("📋 AI Ne Jo Size Padhe:")
    for idx, win in enumerate(window_list, 1):
        st.write(f"Line {idx} ➔ **{win.get('track', '2 Track')}** | Width: `{win.get('width')} mm` | Height: `{win.get('height')} mm` | Qty: `{win.get('qty', 1)} Pcs`")

    st.write("")
    if st.button("🔴 GENERATE FULL SITE LAYOUT & MATERIAL BILL (From Photo)", type="primary"):
        total_glass_area, total_mesh_area = 0, 0
        total_frame_2t_m, total_frame_3t_m, total_sash_m = 0, 0, 0
        total_rollers, total_locks, total_gasket, total_wool_pile = 0, 0, 0, 0
        all_frame_2t_pieces, all_frame_3t_pieces, all_sash_pieces = [], [], []
        sash_sizes_display = []
        
        for idx, win in enumerate(window_list, 1):
            t = win.get("track", "2 Track")
            w = int(win.get("width", 0))
            h = int(win.get("height", 0))
            qty = int(win.get("qty", 1))
            
            if w == 0 or h == 0: continue
            
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
                total_rollers += 4 * qty
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

        st.header("🏢 FINAL MATERIAL BILL SUMMARY")
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            st.write(f"⬛ **Glass:** `{total_glass_area:.2f} Sq.Ft.`")
            if total_mesh_area > 0: st.write(f"🕸️ **Mesh:** `{total_mesh_area:.2f} Sq.Ft.`")
        with c_m2:
            if total_frame_2t_m > 0: st.write(f"🔹 **2-Track Frame:** `{total_frame_2t_m:.2f} Mtrs`")
            if total_frame_3t_m > 0: st.write(f"🔸 **3-Track Frame:** `{total_frame_3t_m:.2f} Mtrs`")
        with c_m3:
            st.write(f"🟩 **Total Sash Profile:** `{total_sash_m:.2f} Mtrs`")
            st.write(f"🛞 Rollers: **{total_rollers} Pcs** | 🔒 Locks: **{total_locks} Pcs**")
