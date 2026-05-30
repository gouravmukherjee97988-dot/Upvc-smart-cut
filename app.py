import streamlit as st
import re

# Page Setup - Gourav Smart UPVC
st.set_page_config(page_title="Gourav Smart UPVC", page_icon="🪟", layout="wide")

st.markdown("""
    <style>
    /* Background and Global Colors */
    .main { background-color: #f4f7f6 !important; color: #000000 !important; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: bold !important; margin-bottom: 5px !important; }
    
    /* Premium Blue Buttons */
    .stButton>button { background-color: #0056b3 !important; color: #ffffff !important; font-weight: bold !important; border-radius: 6px !important; height: 42px !important; border: 2px solid #002244 !important; }
    .stButton>button:hover { background-color: #002244 !important; }
    
    /* Input Box Visibility */
    input { color: #000000 !important; font-weight: bold !important; }
    select { color: #000000 !important; font-weight: bold !important; }
    
    /* Output Box Content Styling */
    div[data-testid="stExpander"] { background-color: #eef4fc !important; border: 2px solid #003366 !important; border-radius: 6px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] div { color: #000000 !important; font-weight: bold !important; }
    
    /* Grid Box Container */
    div[data-testid="stBlock"] { background-color: #ffffff !important; padding: 10px !important; border-radius: 6px !important; border: 1px solid #ccd1d9 !important; margin-bottom: 5px !important; }
    
    /* Super Tight Layout for Mobile Excel Feel */
    .stNumberInput, .stSelectbox { margin-bottom: 0px !important; padding-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪟 Gourav Smart UPVC | Core Estimator")

# --- PARAMETERS ---
STANDARD_BAR = 5800  # 5.8 Meter
BLADE_THICKNESS = 3  # 3mm blade cutoff

# --- FORMULA EVALUATOR ---
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

# --- SCRAP MINIMIZER ENGINE ---
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
        if not placed:
            bars_used.append([piece])
    return bars_used


# =========================================================================
# ⚙️ 1. MASTER FORMULA SETTING (Alag Section)
# =========================================================================
st.header("⚙️ 1. DEDICATED SASH FORMULA")
with st.container():
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        custom_w_formula = st.text_input("Sash WIDTH Formula:", value="(W - 52 - 52 - 5 + 58 + 16) / 2 + 5")
    with col_f2:
        custom_h_formula = st.text_input("Sash HEIGHT Formula:", value="H - 50")


# =========================================================================
# 🏢 2. COMPACT ESTIMATOR TABLE (Default 1 Row, Smart Track)
# =========================================================================
st.markdown("---")
st.header("🏢 2. COMPACT SITE ESTIMATOR")

# Master Track Selection in First Row Look
if 'bulk_rows' not in st.session_state:
    st.session_state.bulk_rows = 1

with st.container():
    col_t1, col_t2 = st.columns([2, 4])
    with col_t1:
        site_track = st.selectbox("Select Site Track Type:", ["2 Track", "2.5 Track", "3 Track"])

st.write("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# Grid Header
with st.container():
    ch1, ch2, ch3 = st.columns(3)
    ch1.markdown("**Width (mm)**")
    ch2.markdown("**Height (mm)**")
    ch3.markdown("**Quantity (Pcs)**")

window_entries = []

# Excel Grid (Default 1 Row, Adds on button click)
for i in range(st.session_state.bulk_rows):
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            w = st.number_input(f"Width #{i+1}", min_value=0, value=None, key=f"win_w_{i}", placeholder="Width dalein...", label_visibility="collapsed")
        with c2:
            h = st.number_input(f"Height #{i+1}", min_value=0, value=None, key=f"win_h_{i}", placeholder="Height dalein...", label_visibility="collapsed")
        with c3:
            q = st.number_input(f"Qty #{i+1}", min_value=1, value=1, step=1, key=f"win_q_{i}", label_visibility="collapsed")
            
        if w and h and w > 0 and h > 0:
            window_entries.append({"id": i+1, "width": w, "height": h, "qty": q})

# Add Row Button
if st.button("➕ Add More Window Row"):
    st.session_state.bulk_rows += 1
    st.rerun()

st.write("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)


# =========================================================================
# 🔴 BAREEK CALCULATION ENGINE & OUTPUT
# =========================================================================
if st.button("🔴 GENERATE FULL SITE LAYOUT & BAREEK MATERIAL BILL", type="primary", use_container_width=True):
    if not window_entries:
        st.error("⚠️ Kripya table me kam se kam ek window ka Width aur Height bharein!")
    else:
        # Counters for Bareek Material Bill
        total_glass_area = 0.0
        total_mesh_area = 0.0
        
        total_frame_2t_mm = 0
        total_frame_3t_mm = 0
        total_sash_mm = 0
        total_mesh_sash_mm = 0
        total_interlock_mm = 0
        
        total_glass_rollers = 0
        total_mesh_rollers = 0
        total_touch_locks = 0
        total_gasket_meters = 0
        total_wool_pile_meters = 0
        
        # Cutting Stock Lists
        all_frame_2t_pieces = []
        all_frame_3t_pieces = []
        all_sash_pieces = []
        all_mesh_pieces = []
        
        sash_display_list = []
        error_found = False
        
        for win in window_entries:
            w = win["width"]
            h = win["height"]
            qty = win["qty"]
            idx = win["id"]
            
            sash_w = evaluate_custom_formula(custom_w_formula, w, h)
            sash_h = evaluate_custom_formula(custom_h_formula, w, h)
            
            if sash_w == "Error" or sash_h == "Error":
                error_found = True
                break
            
            # --- DETAILED TRACK WISE LOGIC (BAREEK HISAB) ---
            if site_track == "2 Track":
                # 2 Palle Glass ke
                num_glass_sash = 2
                num_mesh_sash = 0
                
                # Profiles Length (2T Outer Frame Horizontal=2, Vertical=2)
                total_frame_2t_mm += ((w * 2) + (h * 2)) * qty
                all_frame_2t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                
                # Glass Area (Sq.Ft)
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_glass_sash * qty
                
                # Hardware Bareek Calculation
                total_glass_rollers += 4 * qty
                total_touch_locks += 2 * qty
                
                # Interlock (Har window me 2 interlock khade lagte hain)
                total_interlock_mm += (sash_h * 2) * qty
                
                sash_display_list.append(f"🔹 **Line {idx} ({site_track}):** Glass Sash = **`{sash_w} x {sash_h} mm`** | Qty: {num_glass_sash * qty} Palles")
                
            elif site_track == "2.5 Track":
                # 2 Palle Glass ke + 1 Palla Jaali (Mesh) ka
                num_glass_sash = 2
                num_mesh_sash = 1
                
                # Profiles Length (3T Outer Frame lagta hai isme)
                total_frame_3t_mm += ((w * 2) + (h * 2)) * qty
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                
                # Glass & Mesh Area (Sq.Ft)
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_glass_sash * qty
                total_mesh_area += (sash_w / 304.8) * (sash_h / 304.8) * num_mesh_sash * qty
                
                # Hardware Bareek Calculation
                total_glass_rollers += 4 * qty
                total_mesh_rollers += 2 * qty
                total_touch_locks += 3 * qty  
                
                # Interlock (Glass pallo ke liye 2 interlock)
                total_interlock_mm += (sash_h * 2) * qty
                
                sash_display_list.append(f"🔹 **Line {idx} ({site_track}):** Glass Sash = **`{sash_w} x {sash_h} mm`** ({num_glass_sash * qty} Pcs) | Jaali Sash = **`{sash_w} x {sash_h} mm`** ({num_mesh_sash * qty} Pcs)")
                
            elif site_track == "3 Track":
                # 3 Palle Poore Glass ke (No Jaali)
                num_glass_sash = 3
                num_mesh_sash = 0
                
                # Profiles Length (3T Outer Frame)
                total_frame_3t_mm += ((w * 2) + (h * 2)) * qty
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                
                # Glass Area (Sq.Ft)
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_glass_sash * qty
                
                # Hardware Bareek Calculation
                total_glass_rollers += 6 * qty  # Har palle me 2 roller = 3*2 = 6
                total_touch_locks += 3 * qty   # Har palle par 1 lock = 3
                
                # Interlock (3-track me 4 interlock khade lagte hain overlap ke liye)
                total_interlock_mm += (sash_h * 4) * qty
                
                sash_display_list.append(f"🔹 **Line {idx} ({site_track}):** Glass Sash = **`{sash_w} x {sash_h} mm`** | Qty: {num_glass_sash * qty} Palles")

            # --- SASH CUTTING PIECES BUNDLE (Width=2, Height=2 per sash) ---
            # Glass Sash Cut Stock List
            all_sash_pieces.extend([int(sash_w)] * (2 * num_glass_sash * qty))
            all_sash_pieces.extend([int(sash_h)] * (2 * num_glass_sash * qty))
            total_sash_mm += ((sash_w * 2) + (sash_h * 2)) * num_glass_sash * qty
            
            # Jaali (Mesh) Sash Cut Stock List
            if num_mesh_sash > 0:
                all_mesh_pieces.extend([int(sash_w)] * (2 * num_mesh_sash * qty))
                all_mesh_pieces.extend([int(sash_h)] * (2 * num_mesh_sash * qty))
                total_mesh_sash_mm += ((sash_w * 2) + (sash_h * 2)) * num_mesh_sash * qty
            
            # --- GASKET & WOOL PILE BAREEK LOGIC ---
            # Gasket hamesha kanch ke pallo ke charo taraf double lagta hai (Inner + Outer glass binding)
            total_gasket_meters += (((sash_w * 2) + (sash_h * 2)) * 2 * num_glass_sash * qty) / 1000
            
            # Wool pile frame aur sash dono me lagta hai fitting tight karne ke liye
            # Bareek estimation rule: Pure sash perimeter ka running total
            total_wool_pile_meters += ((((sash_w * 2) + (sash_h * 2)) * (num_glass_sash + num_mesh_sash) * qty) / 1000)

        if error_found:
            st.error("⚠️ Formula text format sahi nahi hai! Sirf W, H, +, -, *, /, aur brackets daalein.")
        else:
            # =================== DISPLAY RESULTS ===================
            st.write("---")
            st.header("📐 SITE SINGLE SASH CUTTING SIZES")
            for display_text in sash_display_list:
                st.write(display_text)

            st.write("---")
            st.header("🏢 MASTER MATERIAL & BAREEK HARDWARE BILL")
            
            bm1, bm2, bm3 = st.columns(3)
            with bm1:
                st.markdown("### 🪵 Profiles Required")
                if total_frame_2t_mm > 0: st.write(f"🔹 **2-Track Outer Frame:** `{total_frame_2t_mm/1000:.2f} Mtrs`")
                if total_frame_3t_mm > 0: st.write(f"🔸 **3-Track Outer Frame:** `{total_frame_3t_mm/1000:.2f} Mtrs`")
                st.write(f"🟩 **Glass Sash Profile:** `{total_sash_mm/1000:.2f} Mtrs`")
                if total_mesh_sash_mm > 0: st.write(f"🕸️ **Jaali Sash Profile:** `{total_mesh_sash_mm/1000:.2f} Mtrs`")
                st.write(f"⛓️ **Interlock Profile:** `{total_interlock_mm/1000:.2f} Mtrs`")
                
            with bm2:
                st.markdown("### 🪟 Glass & Jaali Sheet")
                st.write(f"⬛ **Pure Glass Area:** `{total_glass_area:.2f} Sq.Ft.`")
                if total_mesh_area > 0: st.write(f"🕸️ **Wire Mesh (Jaali):** `{total_mesh_area:.2f} Sq.Ft.`")
                
            with bm3:
                st.markdown("### 📦 Accurate Accessories")
                st.write(f"🛞 Glass Palla Rollers: **{total_glass_rollers} Pcs**")
                if total_mesh_rollers > 0: st.write(f"🛞 Jaali Palla Rollers: **{total_mesh_rollers} Pcs**")
                st.write(f"🔒 Premium Touch Locks: **{total_touch_locks} Pcs**")
                st.write(f"⚫ Weather Gasket Rubber: **{total_gasket_meters:.1f} Mtrs**")
                st.write(f"💨 Dust Wool Pile: **{total_wool_pile_meters:.1f} Mtrs**")

            # =================== CUTTING STOCK OPTIMIZATION ===================
            st.write("---")
            st.header("📐 MINIMUM WASTAGE PROFILE CUTTING PLANS (5.8m Bar)")
            st.info("Niche bataya gaya hai ki 5800mm ke khade bar me se kaun-kaun se size kaatne hain taaki kachra na bache:")

            if all_frame_2t_pieces:
                st.subheader("🖼️ 2-Track Outer Frame Cutting Plan")
                bars = cutting_stock_1d(STANDARD_BAR, all_frame_2t_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"FRAME BAR #{idx} ➔ Kaato pieces: {bar}"): st.write(f"➔ `{bar}` mm")

            if all_frame_3t_pieces:
                st.subheader("🖼️ 3-Track Outer Frame Cutting Plan")
                bars = cutting_stock_1d(STANDARD_BAR, all_frame_3t_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"3-TRACK FRAME BAR #{idx} ➔ Kaato pieces: {bar}"): st.write(f"➔ `{bar}` mm")

            if all_sash_pieces:
                st.subheader("🪟 Glass Sash Profile Cutting Plan")
                bars = cutting_stock_1d(STANDARD_BAR, all_sash_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"SASH BAR #{idx} ➔ Kaato pieces: {bar}"): st.write(f"➔ `{bar}` mm")

            if all_mesh_pieces:
                st.subheader("🕸️ Jaali (Mesh) Sash Profile Cutting Plan")
                bars = cutting_stock_1d(STANDARD_BAR, all_mesh_pieces, BLADE_THICKNESS)
                for idx, bar in enumerate(bars, 1):
                    with st.expander(f"JAALI SASH BAR #{idx} ➔ Kaato pieces: {bar}"): st.write(f"➔ `{bar}` mm")
d
