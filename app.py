import streamlit as st
import re

# Custom CSS for Forceful High-Contrast Visibility & Compact Excel Layout
st.set_page_config(page_title="Gourav Smart UPVC", page_icon="🪟", layout="wide")

st.markdown("""
    <style>
    /* Page Background */
    .main { background-color: #f4f7f6 !important; color: #000000 !important; }
    
    /* Headings */
    h1, h2, h3, h4 { color: #003366 !important; font-weight: bold !important; margin-bottom: 5px !important; }
    
    /* Action Buttons */
    .stButton>button { background-color: #0056b3 !important; color: #ffffff !important; font-weight: bold !important; border-radius: 6px !important; height: 45px !important; border: 2px solid #002244 !important; }
    .stButton>button:hover { background-color: #002244 !important; }
    
    /* Force Input Texts to be Pure Black */
    input { color: #000000 !important; font-weight: bold !important; }
    select { color: #000000 !important; font-weight: bold !important; }
    
    /* Expander Text Visibility */
    div[data-testid="stExpander"] { background-color: #eef4fc !important; border: 2px solid #003366 !important; border-radius: 6px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] div { color: #000000 !important; font-weight: bold !important; }
    
    /* Compact Container Styling */
    div[data-testid="stBlock"] { background-color: #ffffff !important; padding: 12px !important; border-radius: 8px !important; border: 1px solid #ccd1d9 !important; margin-bottom: 8px !important; }
    
    /* Tight layout for Excel table look */
    .stNumberInput, .stSelectbox { margin-bottom: 0px !important; padding-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪟 Gourav Smart UPVC | Workshop Premium Tool")

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
# ⚙️ 1. MASTER FORMULA SETTING
# =========================================================================
st.header("⚙️ 1. MASTER FORMULA SETTING")
with st.container():
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        custom_w_formula = st.text_input("Sash WIDTH Formula:", value="(W - 52 - 52 - 5 + 58 + 16) / 2 + 5")
    with col_f2:
        custom_h_formula = st.text_input("Sash HEIGHT Formula:", value="H - 50")


# =========================================================================
# 🔥 NEW FEATURE: QUICK SINGLE SASH CHECKER (Sirf Size Nikalna Hai To)
# =========================================================================
st.markdown("---")
st.header("🔍 QUICK SINGLE SASH CHECKER")
st.write("Agar kisi customer ke liye sirf on-the-spot ek window ka size nikalna hai, toh yahan daalein:")

with st.container():
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        q_w = st.number_input("Width (mm)", min_value=0, value=None, key="quick_w", placeholder="Width dalein...")
    with col_q2:
        q_h = st.number_input("Height (mm)", min_value=0, value=None, key="quick_h", placeholder="Height dalein...")
    with col_q3:
        st.write("<div style='padding-top:25px;'></div>", unsafe_allow_html=True)
        if q_w and q_h:
            res_quick_w = evaluate_custom_formula(custom_w_formula, q_w, q_h)
            res_quick_h = evaluate_custom_formula(custom_h_formula, q_w, q_h)
            if res_quick_w != "Error" and res_quick_h != "Error":
                st.success(f"🎯 **Sash Size:** `{res_quick_w} x {res_quick_h} mm`")
            else:
                st.error("⚠️ Formula check karein!")
        else:
            st.info("💡 Size likhte hi upar result aa jayega.")


# =========================================================================
# 🏢 2. FULL SITE BULK CALCULATOR (Excel Table Layout with Row Plus Button)
# =========================================================================
st.markdown("---")
st.header("🏢 2. FULL SITE BULK ESTIMATOR (Excel Table)")
st.write("Poori site ka cutting plan aur bill nikalne ke liye niche table bharein:")

# Session state to handle dynamic row counts (Default 5 rows)
if 'rows_count' not in st.session_state:
    st.session_state.rows_count = 5

# Table Header Row
with st.container():
    ch1, ch2, ch3, ch4 = st.columns([1.5, 2, 2, 1.5])
    ch1.markdown("**Track Type**")
    ch2.markdown("**Width (mm)**")
    ch3.markdown("**Height (mm)**")
    ch4.markdown("**Qty (Pcs)**")

window_list = []

# Dynamic Excel-like Table Grid
for i in range(st.session_state.rows_count):
    with st.container():
        c1, c2, c3, c4 = st.columns([1.5, 2, 2, 1.5])
        with c1:
            track_type = st.selectbox(f"Track #{i+1}", ["2 Track", "2.5 Track", "3 Track"], key=f"t_{i}", label_visibility="collapsed")
        with c2:
            w = st.number_input(f"W #{i+1}", min_value=0, value=None, key=f"w_{i}", placeholder="Blank", label_visibility="collapsed")
        with c3:
            h = st.number_input(f"H #{i+1}", min_value=0, value=None, key=f"h_{i}", placeholder="Blank", label_visibility="collapsed")
        with c4:
            q = st.number_input(f"Q #{i+1}", min_value=1, value=1, step=1, key=f"q_{i}", label_visibility="collapsed")
            
        if w is not None and h is not None and w > 0 and h > 0:
            window_list.append({"id": i+1, "track": track_type, "width": w, "height": h, "qty": q})

# Excel-style Row Controls (Plus Button)
col_p1, col_p2 = st.columns([2, 10])
with col_p1:
    if st.button("➕ Add More Rows", use_container_width=True):
        st.session_state.rows_count += 3
        st.rerun()

st.write("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# =========================================================================
# 🔴 GENERATE ALL CALCULATION BUTTON (Now close to the table)
# =========================================================================
if st.button("🔴 GENERATE FULL SITE LAYOUT & MATERIAL BILL", type="primary", use_container_width=True):
    if not window_list:
        st.error("⚠️ Kripya niche table me kam se kam ek window ka Width aur Height dalein!")
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
                sash_sizes_display.append(f"🔹 **Window Line {idx} ({t}):** Sash = **`{sash_w}x{sash_h} mm`** | Total {num_sash * qty} Palles")
                
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
                sash_sizes_display.append(f"🔹 **Window Line {idx} ({t}):** Glass Sash = **`{sash_w}x{sash_h} mm`** | Mesh = **`{sash_w}x{sash_h} mm`**")
                
            elif t == "3 Track":
                num_sash = 3
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_3t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_rollers += 6 * qty
                total_locks += 3 * qty
                sash_sizes_display.append(f"🔹 **Window Line {idx} ({t}):** Sash = **`{sash_w}x{sash_h} mm`** | Total {num_sash * qty} Palles")

            if t != "2.5 Track":
                all_sash_pieces.extend([int(sash_w)] * (2 * num_sash * qty))
                all_sash_pieces.extend([int(sash_h)] * (2 * num_sash * qty))
            
            current_sash_total_mm = ((sash_w * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2)) + (sash_h * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2))) * qty
            total_sash_m += current_sash_total_mm / 1000
            total_gasket += (current_sash_total_mm * 2) / 1000
            total_wool_pile += ((sash_h * 4) + (sash_w * 2)) * qty / 1000

        if formula_error_triggered:
            st.error("⚠️ Formula Check Karein! Sirf W, H, numbers aur brackets allow hain.")
        else:
            # --- RESULTS OUTPUT ---
            st.write("---")
            st.header("📐 SITE BULK SASH CUTTING SIZES")
            for size_info in sash_sizes_display:
                st.write(size_info)

            st.write("---")
            st.header("🏢 SITE MATERIAL BILL SUMMARY")
            c_m1, c_m2, c_m3 = st.columns(3)
            with c_m1:
                st.write(f"⬛ **Glass:** `{total_glass_area:.2f} Sq.Ft.`")
                if total_mesh_area > 0:
                    st.write(f"🕸️ **Mesh (Jaali):** `{total_mesh_area:.2f} Sq.Ft.`")
            with c_m2:
                if total_frame_2t_m > 0:
                    st.write(f"🔹 **2-Track Frame:** `{total_frame_2t_m:.2f} Mtrs`")
                if total_frame_3t_m > 0:
                    st.write(f"🔸 **3-Track Frame:** `{total_frame_3t_m:.2f} Mtrs`")
            with c_m3:
                st.write(f"🟩 **Total Sash Profile:** `{total_sash_m:.2f} Mtrs`")

            st.subheader("📦 Accessories:")
            st.write(f"🛞 Rollers: `{total_rollers} Pcs` | 🕸️ Mesh Rollers: `{total_mesh_rollers} Pcs` | 🔒 Locks: `{total_locks} Pcs`")
            st.write(f"⚫ Gasket: `{total_gasket:.1f} Mtrs` | 💨 Wool Pile: `{total_wool_pile:.1f} Mtrs`")
            
            st.write("---")
            # --- CUTTING PLANS ---
            if all_frame_2t_pieces:
                st.header("📐 1. 2-TRACK OUTER FRAME CUTTING PLAN")
                bars = cutting_stock_1d(STANDARD_BAR, all_frame_2t_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"🖼️ BAR {idx} -> Pieces: {bar}"):
                        st.write(f"➔ **Kaato:** `{bar}`")

            if all_frame_3t_pieces:
                st.header("📐 2. 3-TRACK OUTER FRAME CUTTING PLAN")
                bars = cutting_stock_1d(STANDARD_BAR, all_frame_3t_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"🖼️ BAR {idx} -> Pieces: {bar}"):
                        st.write(f"➔ **Kaato:** `{bar}`")

            if all_sash_pieces:
                st.header("⚡ 3. GLASS SASH PROFILE CUTTING PLAN")
                bars = cutting_stock_1d(STANDARD_BAR, all_sash_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"🪟 BAR {idx} -> Pieces: {bar}"):
                        st.write(f"➔ **Kaato:** `{bar}`")

            if all_mesh_pieces:
                st.header("🕸️ 4. MESH SASH (JAALI) CUTTING PLAN")
                bars = cutting_stock_1d(STANDARD_BAR, all_mesh_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"🕸️ BAR {idx} -> Pieces: {bar}"):
                        st.write(f"➔ **Kaato:** `{bar}`")
