import streamlit as st
import re

# Custom CSS for Forceful High-Contrast Visibility - "Gourav Smart UPVC"
st.set_page_config(page_title="Gourav Smart UPVC", page_icon="🪟", layout="wide")

st.markdown("""
    <style>
    /* Global Page Background */
    .main { background-color: #f4f7f6 !important; color: #000000 !important; }
    
    /* Headings Styling */
    h1, h2, h3, h4 { color: #003366 !important; font-weight: bold !important; }
    
    /* Buttons Custom Style */
    .stButton>button { background-color: #0056b3 !important; color: #ffffff !important; font-weight: bold !important; border-radius: 8px !important; height: 55px !important; font-size: 20px !important; border: 2px solid #002244 !important; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .stButton>button:hover { background-color: #002244 !important; }
    
    /* Force Input Texts to be Pure Black and Bold */
    input { color: #000000 !important; font-weight: bold !important; font-size: 16px !important; }
    select { color: #000000 !important; font-weight: bold !important; }
    
    /* Expander Text Visibility (No Whiteout) */
    div[data-testid="stExpander"] { background-color: #eef4fc !important; border: 2px solid #003366 !important; border-radius: 8px !important; margin-bottom: 5px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] div, div[data-testid="stExpander"] label { color: #000000 !important; font-weight: bold !important; font-size: 16px !important; }
    
    /* Section Separation Containers */
    div[data-testid="stBlock"] { background-color: #ffffff !important; padding: 15px !important; border-radius: 8px !important; border: 1px solid #ccd1d9 !important; margin-bottom: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪟 Gourav Smart UPVC | All-in-One Master Engine")
st.write("Workshop Special - Apna formula dalein aur poori site ki 15 windows ka automatic calculation payein.")

# --- CONFIGURATION ---
STANDARD_BAR = 5800  # 5.8m
BLADE_THICKNESS = 3  # 3mm

# --- SMART MATH EVALUATOR ---
def evaluate_custom_formula(formula_str, w_val, h_val):
    try:
        c_str = formula_str.lower().replace(' ', '')
        c_str = c_str.replace('width', str(w_val)).replace('w', str(w_val))
        c_str = c_str.replace('height', str(h_val)).replace('h', str(h_val))
        
        if not re.match(r'^[\d\+\-\*\/\(\)\.]+$', c_str):
            return "Error"
        
        return int(round(eval(c_str)))
    except:
        return "Error"

# --- OPTIMIZATION ENGINE ---
def cutting_stock_1d(stock_length, pieces, kerf):
    pieces.sort(reverse=True)
    bars_used = []
    for piece in pieces:
        placed = False
        for bar in bars_used:
            remaining_space = stock_length - sum(bar) - (len(bar) * kerf)
            if remaining_space >= piece:
                bar.append(piece)
                placed = True
                break
        if not placed:
            bars_used.append([piece])
    return bars_used


# =========================================================================
# ⚙️ 1. MASTER FORMULA BOX (Sab Kuch Isi Par Chalega)
# =========================================================================
st.header("⚙️ 1. MASTER FORMULA INPUT")
st.write("Aapke dukan ke profile brand ke hisab se sash ka lamba jod-ghatav yahan set karein (W = Width, H = Height):")

with st.container():
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        # Bracket standard lagakar default formula set kiya hai
        custom_w_formula = st.text_input("Sash WIDTH Ka Formula Likhein:", value="(W - 52 - 52 - 5 + 58 + 16) / 2 + 5")
    with col_f2:
        custom_h_formula = st.text_input("Sash HEIGHT Ka Formula Likhein:", value="H - 50")


# =========================================================================
# 📝 2. POORI SITE KI LIST (Line Se 15 Rows - Ekdum Khali Bina Zero Ke)
# =========================================================================
st.write("")
st.header("📝 2. SITE WINDOW SIZES (Jitna chahe utna bharein, baki khali chodh dein)")

window_list = []

# Ek baar me line se 15 rows bina zero ke khulengi
for i in range(15):
    with st.container():
        c1, c2, c3, c4 = st.columns([1.5, 2, 2, 1.5])
        with c1:
            track_type = st.selectbox(f"Track", ["2 Track", "2.5 Track", "3 Track"], key=f"track_{i}")
        with c2:
            # value=None karne se dabba ekdum blank rehta hai, koi zero nahi dikhta
            w = st.number_input(f"Width (mm) #{i+1}", min_value=0, value=None, step=10, key=f"w_{i}", placeholder="Type Width...")
        with c3:
            h = st.number_input(f"Height (mm) #{i+1}", min_value=0, value=None, step=10, key=f"h_{i}", placeholder="Type Height...")
        with c4:
            q = st.number_input(f"Quantity #{i+1}", min_value=1, value=1, step=1, key=f"q_{i}")
            
        if w is not None and h is not None and w > 0 and h > 0:
            window_list.append({"id": i+1, "track": track_type, "width": w, "height": h, "qty": q})

st.write("")

# =========================================================================
# 🔴 GENERATE ALL CALCULATION BUTTON
# =========================================================================
if st.button("🔴 GENERATE FULL SITE LAYOUT, MATERIAL BILL & SIZES", type="primary"):
    if not window_list:
        st.error("⚠️ Kripya kam se kam ek window ka sahi Width aur Height dalein!")
    else:
        total_glass_area = 0
        total_mesh_area = 0
        total_frame_2t_m = 0
        total_frame_3t_m = 0
        total_sash_m = 0
        total_rollers = 0
        total_mesh_rollers = 0
        total_locks = 0
        total_gasket = 0
        total_wool_pile = 0
        
        all_frame_2t_pieces = []
        all_frame_3t_pieces = []
        all_sash_pieces = []
        all_mesh_pieces = []
        sash_sizes_display = []
        formula_error_triggered = False
        
        for win in window_list:
            t = win["track"]
            w = win["width"]
            h = win["height"]
            qty = win["qty"]
            idx = win["id"]
            
            # RUN USER'S CUSTOM FORMULA DYNAMICALLY
            sash_w = evaluate_custom_formula(custom_w_formula, w, h)
            sash_h = evaluate_custom_formula(custom_h_formula, w, h)
            
            if sash_w == "Error" or sash_h == "Error":
                formula_error_triggered = True
                break
                
            if t == "2 Track":
                num_sash = 2
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_2t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_2t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_rollers += 4 * qty
                total_locks += 2 * qty
                sash_sizes_display.append(f"🔹 **Window No. {idx} ({t}):** Single Sash Size = **`{sash_w} mm` (W) x `{sash_h} mm` (H)** | Total {num_sash * qty} Sashes")
                
            elif t == "2.5 Track":
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * 2 * qty
                total_mesh_area += (sash_w / 304.8) * (sash_h / 304.8) * 1 * qty
                total_frame_3t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                all_sash_pieces.extend([int(sash_w)] * (4 * qty))
                all_sash_pieces.extend([int(sash_h)] * (4 * qty))
                all_mesh_pieces.extend([int(sash_w)] * (2 * qty))
                all_mesh_pieces.extend([int(sash_h)] * (2 * qty))
                total_rollers += 4 * qty
                total_mesh_rollers += 2 * qty
                total_locks += 3 * qty
                sash_sizes_display.append(f"🔹 **Window No. {idx} ({t}):** Glass Sash = **`{sash_w}x{sash_h} mm`** ({2*qty} Pcs) | Mesh Sash = **`{sash_w}x{sash_h} mm`** ({qty} Pcs)")
                
            elif t == "3 Track":
                num_sash = 3
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_3t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_rollers += 6 * qty
                total_locks += 3 * qty
                sash_sizes_display.append(f"🔹 **Window No. {idx} ({t}):** Single Sash Size = **`{sash_w} mm` (W) x `{sash_h} mm` (H)** | Total {num_sash * qty} Sashes")

            if t != "2.5 Track":
                all_sash_pieces.extend([int(sash_w)] * (2 * num_sash * qty))
                all_sash_pieces.extend([int(sash_h)] * (2 * num_sash * qty))
            
            # Consumables
            current_sash_total_mm = ((sash_w * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2)) + (sash_h * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2))) * qty
            total_sash_m += current_sash_total_mm / 1000
            total_gasket += (current_sash_total_mm * 2) / 1000
            total_wool_pile += ((sash_h * 4) + (sash_w * 2)) * qty / 1000

        if formula_error_triggered:
            st.error("⚠️ Upar diye gaye Formula me koi galti hai! Kripya check karein (Sirf numbers, +, -, *, /, W, H aur brackets lagayein).")
        else:
            # --- 1. SASH SIZES DISPLAY ---
            st.write("---")
            st.header("📐 AAPKE FORMULA SE NIKLA EXACT SASH SIZE (Palle Ka Naap)")
            for size_info in sash_sizes_display:
                st.write(size_info)

            # --- 2. MATERIAL BILL ---
            st.write("---")
            st.header("🏢 POORI SITE KA TOTAL MATERIAL BILL (BOM)")
            c_m1, c_m2, c_m3 = st.columns(3)
            with c_m1:
                st.write(f"⬛ **Total Glass Area:** **`{total_glass_area:.2f} Sq.Ft.`**")
                if total_mesh_area > 0:
                    st.write(f"🕸️ **Wire Mesh (Jaali):** **`{total_mesh_area:.2f} Sq.Ft.`**")
            with c_m2:
                if total_frame_2t_m > 0:
                    st.write(f"🔹 **2-Track Outer Frame Profile:** **`{total_frame_2t_m:.2f} Meters`**")
                if total_frame_3t_m > 0:
                    st.write(f"🔸 **3-Track Outer Frame Profile:** **`{total_frame_3t_m:.2f} Meters`**")
            with c_m3:
                st.write(f"🟩 **Total Sash Profile Needed:** **`{total_sash_m:.2f} Meters`**")

            st.subheader("📦 Hardware, Locks & Consumables Summary:")
            st.write(f"🛞 Heavy Rollers: **`{total_rollers} Pcs`** | 🕸️ Mesh Rollers: **`{total_mesh_rollers} Pcs`** | 🔒 Touch Locks: **`{total_locks} Pcs`**")
            st.write(f"⚫ Gasket (Rubber): **`{total_gasket:.1f} Mtrs`** | 💨 Wool Pile (Strips): **`{total_wool_pile:.1f} Mtrs`**")
            
            # --- 3. CUTTING LAYOUT OPTIMIZER ---
            st.write("---")
            if all_frame_2t_pieces:
                st.header("📐 1. 2-TRACK OUTER FRAME CUTTING PLAN")
                bars = cutting_stock_1d(STANDARD_BAR, all_frame_2t_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"🖼️ 2-TRACK FRAME BAR {idx} -> Pieces: {bar}"):
                        st.write(f"➔ **Is Bar Me Se Kaato:** `{bar}`")

            if all_frame_3t_pieces:
                st.header("📐 2. 3-TRACK OUTER FRAME CUTTING PLAN")
                bars = cutting_stock_1d(STANDARD_BAR, all_frame_3t_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"🖼️ 3-TRACK FRAME BAR {idx} -> Pieces: {bar}"):
                        st.write(f"➔ **Is Bar Me Se Kaato:** `{bar}`")

            if all_sash_pieces:
                st.header("⚡ 3. GLASS SASH PROFILE CUTTING PLAN")
                bars = cutting_stock_1d(STANDARD_BAR, all_sash_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"🪟 SASH BAR {idx} -> Pieces: {bar}"):
                        st.write(f"➔ **Is Bar Me Se Kaato:** `{bar}`")

            if all_mesh_pieces:
                st.header("🕸️ 4. MESH SASH (JAALI) CUTTING PLAN")
                bars = cutting_stock_1d(STANDARD_BAR, all_mesh_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"🕸️ MESH BAR {idx} -> Pieces: {bar}"):
                        st.write(f"➔ **Is Bar Me Se Kaato:** `{bar}`")
