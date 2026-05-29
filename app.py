import streamlit as st
import re

# Custom CSS for Full Visibility and High Contrast - "Gourav Smart UPVC"
st.set_page_config(page_title="Gourav Smart UPVC", page_icon="🪟", layout="wide")

st.markdown("""
    <style>
    /* Global Page Background */
    .main { background-color: #f4f7f6 !important; color: #000000 !important; }
    
    /* Headings Styling */
    h1, h2, h3, h4 { color: #003366 !important; font-weight: bold !important; }
    
    /* Buttons Custom Style */
    .stButton>button { background-color: #0056b3 !important; color: #ffffff !important; font-weight: bold !important; border-radius: 8px !important; height: 48px !important; border: 2px solid #002244 !important; }
    .stButton>button:hover { background-color: #002244 !important; }
    
    /* Force Input Texts to be Pure Black */
    input { color: #000000 !important; font-weight: bold !important; font-size: 16px !important; }
    select { color: #000000 !important; font-weight: bold !important; }
    
    /* CRITICAL FIX: Expander Text Visibility (No Whiteout) */
    div[data-testid="stExpander"] { background-color: #eef4fc !important; border: 2px solid #003366 !important; border-radius: 8px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] div, div[data-testid="stExpander"] label { color: #000000 !important; font-weight: bold !important; font-size: 16px !important; }
    
    /* Section Separation Containers */
    .block-container { padding-top: 2rem !important; }
    div[data-testid="stBlock"] { background-color: #ffffff !important; padding: 20px !important; border-radius: 8px !important; border: 1px solid #ccd1d9 !important; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪟 Gourav Smart UPVC | Advanced Workshop Engine")
st.write("Workshop Special - Custom Formula Tester aur Purana Site Cutting Optimizer.")

# --- CONFIGURATION ---
STANDARD_BAR = 5800  # 5.8m
BLADE_THICKNESS = 3  # 3mm

# --- SAFE MATH EVALUATOR ---
def evaluate_custom_formula(formula_str, w_val, h_val):
    try:
        # Clean spacing and handle lower/uppercase W and H
        c_str = formula_str.lower().replace(' ', '')
        c_str = c_str.replace('width', str(w_val)).replace('w', str(w_val))
        c_str = c_str.replace('height', str(h_val)).replace('h', str(h_val))
        
        # Security check: only allow numbers and basic math characters
        if not re.match(r'^[\d\+\-\*\/\(\)\.]+$', c_str):
            return "Invalid Symbols"
        
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
# 🧮 SECTION 1: MASTER CUSTOM FORMULA BOX (Sirf Checking Ke Liye)
# =========================================================================
st.markdown("---")
st.header("🧮 SECTION 1: DYNAMIC SASH SIZE CALCULATOR")
st.write("Yahan aap apna koi bhi naya ya lamba formula daal kar on-the-spot size check kar sakte hain:")

with st.container():
    col_x1, col_x2 = st.columns(2)
    with col_x1:
        input_w = st.number_input("Window Ka Total Width (mm)", min_value=0, value=1200, step=10)
        input_h = st.number_input("Window Ka Total Height (mm)", min_value=0, value=1500, step=10)
        st.info("💡 **Formula Likhne Ka Tarika:**\n\nWidth ke liye **W** aur Height ke liye **H** ka use karein. \n\n*Example:* `W - 52 - 52 - 5 + 58 + 16 / 2 + 5`")

    with col_x2:
        custom_w_formula = st.text_input("Sash WIDTH Ka Pura Formula Type Karein:", value="W - 52 - 52 - 5 + 58 + 16 / 2 + 5")
        custom_h_formula = st.text_input("Sash HEIGHT Ka Pura Formula Type Karein:", value="H - 50")
        
    st.write("")
    if st.button("🔍 CHECK SASH CUTTING SIZE NOW", type="secondary"):
        res_w = evaluate_custom_formula(custom_w_formula, input_w, input_h)
        res_h = evaluate_custom_formula(custom_h_formula, input_w, input_h)
        
        if res_w in ["Error", "Invalid Symbols"] or res_h in ["Error", "Invalid Symbols"]:
            st.error("⚠️ Formula check karein! Kripya sirf numbers, +, -, *, /, W aur H ka use karein.")
        else:
            st.markdown("### 🎯 Aapke Formula Ke Hisab Se Sash Size:")
            st.success(f"🟩 **Sash Width (Chaurai):** `{res_w} mm`   |   🟩 **Sash Height (Unchai):** `{res_h} mm`")

st.markdown("---")


# =========================================================================
# 🏢 SECTION 2: PURANA SITE BULK OPTIMIZER (Bilkul Pehle Jaisa Same To Same)
# =========================================================================
st.header("🏢 SECTION 2: FULL SITE BULK CALCULATOR & OPTIMIZER")
st.write("Poori site ki windows ki entry ek sath yahan karein. Iska cutting plan standard calculation par chalega:")

if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 4

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("➕ Ek aur Window Jodein (Add Row)"):
        st.session_state.num_rows += 1
with col_btn2:
    if st.button("➖ Ek Row Kam Karein (Remove Row)") and st.session_state.num_rows > 1:
        st.session_state.num_rows -= 1

window_list = []
for i in range(st.session_state.num_rows):
    st.markdown(f"#### 🪟 Window No. {i+1}")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        track_type = st.selectbox(f"Track Type #{i+1}", ["2 Track", "2.5 Track", "3 Track"], key=f"track_{i}")
    with c2:
        w = st.number_input(f"Width (mm) #{i+1}", min_value=0, value=0, step=10, key=f"w_{i}")
    with c3:
        h = st.number_input(f"Height (mm) #{i+1}", min_value=0, value=0, step=10, key=f"h_{i}")
    with c4:
        q = st.number_input(f"Quantity #{i+1}", min_value=1, value=1, step=1, key=f"q_{i}")
    
    if w > 0 and h > 0:
        window_list.append({"track": track_type, "width": w, "height": h, "qty": q})

st.write("---")

if st.button("🔴 GENERATE FULL SITE LAYOUT & TRACK BILL", type="primary"):
    if not window_list:
        st.error("⚠️ Kripya size aur quantity sahi se bharein!")
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
        
        for idx, win in enumerate(window_list, 1):
            t = win["track"]
            w = win["width"]
            h = win["height"]
            qty = win["qty"]
            
            # Pure standard deductions (Jo pehle perfect chal raha tha)
            if t == "2 Track":
                sash_w = (w / 2) + 25
                sash_h = h - 50
                num_sash = 2
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_2t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_2t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_rollers += 4 * qty
                total_locks += 2 * qty
                sash_sizes_display.append(f"🔹 **Window {idx} ({t}):** Sash Size = `{int(sash_w)}x{int(sash_h)} mm` | Total {num_sash * qty} Palles")
                
            elif t == "2.5 Track":
                sash_w = (w / 2) + 25
                sash_h = h - 50
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
                sash_sizes_display.append(f"🔹 **Window {idx} ({t}):** Glass Sash = `{int(sash_w)}x{int(sash_h)} mm` | Mesh Sash = `{int(sash_w)}x{int(sash_h)} mm`")
                
            elif t == "3 Track":
                sash_w = (w / 3) + 30
                sash_h = h - 50
                num_sash = 3
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_3t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_rollers += 6 * qty
                total_locks += 3 * qty
                sash_sizes_display.append(f"🔹 **Window {idx} ({t}):** Sash Size = `{int(sash_w)}x{int(sash_h)} mm` | Total {num_sash * qty} Palles")

            if t != "2.5 Track":
                all_sash_pieces.extend([int(sash_w)] * (2 * num_sash * qty))
                all_sash_pieces.extend([int(sash_h)] * (2 * num_sash * qty))
            
            current_sash_total_mm = ((sash_w * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2)) + (sash_h * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2))) * qty
            total_sash_m += current_sash_total_mm / 1000
            total_gasket += (current_sash_total_mm * 2) / 1000
            total_wool_pile += ((sash_h * 4) + (sash_w * 2)) * qty / 1000

        # --- FINAL DISPLAY WITH FORCE BLACK TEXT ---
        st.header("🏢 FINAL SITE MATERIAL BILL (BOM)")
        
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            st.write(f"⬛ **Total Glass Area:** {total_glass_area:.2f} Sq.Ft.")
            if total_mesh_area > 0:
                st.write(f"🕸️ **Wire Mesh (Jaali):** {total_mesh_area:.2f} Sq.Ft.")
        with c_m2:
            if total_frame_2t_m > 0:
                st.write(f"🔹 **2-Track Outer Frame:** {total_frame_2t_m:.2f} Meters")
            if total_frame_3t_m > 0:
                st.write(f"🔸 **3-Track Outer Frame:** {total_frame_3t_m:.2f} Meters")
        with c_m3:
            st.write(f"🟩 **Total Sash Profile:** {total_sash_m:.2f} Meters")

        st.subheader("📦 Hardware & Locks Breakdown:")
        st.write(f"🛞 Rollers: **{total_rollers} Pcs** | 🕸️ Mesh Rollers: **{total_mesh_rollers} Pcs** | 🔒 Touch Locks: **{total_locks} Pcs**")
        st.write(f"⚫ Gasket: **{total_gasket:.1f} Mtrs** | 💨 Wool Pile: **{total_wool_pile:.1f} Mtrs**")
        
        st.write("---")
        st.header("📐 SINGLE SASH CUTTING SIZES")
        for size_info in sash_sizes_display:
            st.write(size_info)
        
        st.write("---")

        # --- HIGH CONTRAST OPTIMIZATION PLANS ---
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
