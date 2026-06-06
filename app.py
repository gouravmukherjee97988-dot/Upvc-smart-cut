import streamlit as st
import re
import math

# Page Setup - Gourav Smart UPVC Premium Engine
st.set_page_config(page_title="Gourav Smart UPVC", page_icon="🪟", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6 !important; color: #000000 !important; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: bold !important; margin-bottom: 5px !important; }
    .stButton>button { background-color: #0056b3 !important; color: #ffffff !important; font-weight: bold !important; border-radius: 6px !important; height: 42px !important; border: 2px solid #002244 !important; }
    .stButton>button:hover { background-color: #002244 !important; }
    input { color: #000000 !important; font-weight: bold !important; }
    select { color: #000000 !important; font-weight: bold !important; }
    div[data-testid="stExpander"] { background-color: #eef4fc !important; border: 2px solid #003366 !important; border-radius: 6px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] div { color: #000000 !important; font-weight: bold !important; }
    div[data-testid="stBlock"] { background-color: #ffffff !important; padding: 10px !important; border-radius: 6px !important; border: 1px solid #ccd1d9 !important; margin-bottom: 5px !important; }
    .stNumberInput, .stSelectbox { margin-bottom: 0px !important; padding-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪟 Gourav Smart UPVC | Zero Wastage Optimizer")

STANDARD_BAR = 5800  # 5.8 Meter UPVC Bar
ALUM_BAR_12FT = 3650  # 12 Foot Aluminum Track
BLADE_THICKNESS = 3  # 3mm katayi blade motai

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

# --- 🚀 MISTRI STYLE SMART COMBINATION CUTTING ENGINE (BEST-FIT) ---
def smart_cutting_stock(stock_length, pieces, kerf):
    # Pehle saare pieces ko bade se chote me arrange karo
    remaining_pieces = sorted(pieces, reverse=True)
    bars_used = []
    
    while remaining_pieces:
        current_bar = []
        # Pehla sabse bada piece uthao
        first_piece = remaining_pieces.pop(0)
        current_bar.append(first_piece)
        
        # Ab check karo baaki bache pieces me se kaun sa sabse sateek jodi bana raha hai
        # Taaki wastage ekdum na ke barabar bache
        continue_filling = True
        while continue_filling:
            space_left = stock_length - sum(current_bar) - (len(current_bar) * kerf)
            best_idx = -1
            min_waste_left = space_left + 1
            
            for idx, piece in enumerate(remaining_pieces):
                if piece <= space_left:
                    waste_after_cut = space_left - piece
                    # Jis piece ko rakhne se sabse kam space bache, use chun lo (Best Fit)
                    if waste_after_cut < min_waste_left:
                        min_waste_left = waste_after_cut
                        best_idx = idx
            
            if best_idx != -1:
                current_bar.append(remaining_pieces.pop(best_idx))
            else:
                continue_filling = False
                
        bars_used.append(current_bar)
        
    return bars_used

# =========================================================================
# ⚙️ 1. MASTER FORMULA SETTING
# =========================================================================
st.header("⚙️ 1. DEDICATED SASH FORMULA")
with st.container():
    st.markdown("#### Set Master Formula Rules:")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        custom_w_formula = st.text_input("Sash WIDTH Formula:", value="(W - 52 - 52 - 5 + 58 + 16) / 2 + 5")
    with col_f2:
        custom_h_formula = st.text_input("Sash HEIGHT Formula:", value="H - 50")
    
    st.write("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    
    st.markdown("#### Test Size On-The-Spot:")
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        test_w = st.number_input("Enter Outer Width (W) in mm:", min_value=0, value=None, key="test_width", placeholder="W dalein...")
    with col_in2:
        test_h = st.number_input("Enter Outer Height (H) in mm:", min_value=0, value=None, key="test_height", placeholder="H dalein...")
    with col_in3:
        st.write("<div style='padding-top:25px;'></div>", unsafe_allow_html=True)
        if test_w and test_h:
            res_w = evaluate_custom_formula(custom_w_formula, test_w, test_h)
            res_h = evaluate_custom_formula(custom_h_formula, test_w, test_h)
            if res_w != "Error" and res_h != "Error":
                st.success(f"🎯 **Sash Size:** `{res_w} x {res_h} mm`")
            else:
                st.error("⚠️ Formula Check Karein!")
        else:
            st.info("💡 Size likhte hi palles ka size yahan dikhega.")

# =========================================================================
# 🏢 2. COMPACT ESTIMATOR TABLE
# =========================================================================
st.markdown("---")
st.header("🏢 2. COMPACT SITE ESTIMATOR")

if 'bulk_rows' not in st.session_state:
    st.session_state.bulk_rows = 1

with st.container():
    col_t1, col_t2 = st.columns([2, 4])
    with col_t1:
        site_track = st.selectbox("Select Site Track Type:", ["2 Track", "2.5 Track", "3 Track"])

st.write("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

with st.container():
    ch1, ch2, ch3 = st.columns(3)
    ch1.markdown("**Width (mm)**")
    ch2.markdown("**Height (mm)**")
    ch3.markdown("**Quantity (Pcs)**")

window_entries = []

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

if st.button("➕ Add More Window Row"):
    st.session_state.bulk_rows += 1
    st.rerun()

st.write("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# =========================================================================
# 🔴 BAREEK CALCULATION ENGINE
# =========================================================================
if st.button("🔴 GENERATE FULL SITE LAYOUT & BAREEK MATERIAL BILL", type="primary", use_container_width=True):
    if not window_entries:
        st.error("⚠️ Kripya table me kam se kam ek window ka Width aur Height bharein!")
    else:
        total_glass_area = 0.0
        total_mesh_area = 0.0
        
        total_frame_2t_mm = 0
        total_frame_3t_mm = 0
        total_sash_mm = 0
        total_mesh_sash_mm = 0
        total_interlock_mm = 0
        total_alum_track_mm = 0  
        
        total_glass_rollers = 0
        total_mesh_rollers = 0  
        total_touch_locks = 0
        total_gasket_meters = 0
        total_wool_pile_meters = 0
        
        all_frame_2t_pieces = []
        all_frame_3t_pieces = []
        all_sash_pieces = []
        all_mesh_pieces = []
        all_alum_pieces = []  
        
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
            
            # --- TRACK LOGIC ---
            if site_track == "2 Track":
                num_glass_sash = 2
                num_mesh_sash = 0
                
                total_frame_2t_mm += ((w * 2) + (h * 2)) * qty
                all_frame_2t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_alum_track_mm += (w * 2) * qty
                all_alum_pieces.extend([int(w), int(w)] * qty)
                
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_glass_sash * qty
                total_glass_rollers += 4 * qty
                total_touch_locks += 2 * qty
                total_interlock_mm += (sash_h * 2) * qty
                
                sash_display_list.append(f"🔹 **Line {idx} ({site_track}):** Glass Sash = **`{sash_w} x {sash_h} mm`** | Qty: {num_glass_sash * qty} Palles")
                
            elif site_track == "2.5 Track":
                num_glass_sash = 2
                num_mesh_sash = 1
                
                total_frame_3t_mm += ((w * 2) + (h * 2)) * qty
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_alum_track_mm += (w * 3) * qty
                all_alum_pieces.extend([int(w), int(w), int(w)] * qty)
                
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_glass_sash * qty
                total_mesh_area += (sash_w / 304.8) * (sash_h / 304.8) * num_mesh_sash * qty
                
                total_glass_rollers += 4 * qty
                total_mesh_rollers += 2 * qty
                total_touch_locks += 3 * qty  
                total_interlock_mm += (sash_h * 2) * qty
                
                sash_display_list.append(f"🔹 **Line {idx} ({site_track}):** Glass Sash = **`{sash_w} x {sash_h} mm`** ({num_glass_sash * qty} Pcs) | Jaali Sash = **`{sash_w} x {sash_h} mm`** ({num_mesh_sash * qty} Pcs)")
                
            elif site_track == "3 Track":
                num_glass_sash = 3  
                num_mesh_sash = 0
                
                total_frame_3t_mm += ((w * 2) + (h * 2)) * qty
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_alum_track_mm += (w * 3) * qty
                all_alum_pieces.extend([int(w), int(w), int(w)] * qty)
                
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_glass_sash * qty
                total_glass_rollers += 6 * qty  
                total_touch_locks += 3 * qty   
                total_interlock_mm += (sash_h * 4) * qty
                
                sash_display_list.append(f"🔹 **Line {idx} ({site_track}):** Glass Sash = **`{sash_w} x {sash_h} mm`** | Qty: {num_glass_sash * qty} Palles")

            all_sash_pieces.extend([int(sash_w)] * (2 * num_glass_sash * qty))
            all_sash_pieces.extend([int(sash_h)] * (2 * num_glass_sash * qty))
            total_sash_mm += ((sash_w * 2) + (sash_h * 2)) * num_glass_sash * qty
            
            if num_mesh_sash > 0:
                all_mesh_pieces.extend([int(sash_w)] * (2 * num_mesh_sash * qty))
                all_mesh_pieces.extend([int(sash_h)] * (2 * num_mesh_sash * qty))
                total_mesh_sash_mm += ((sash_w * 2) + (sash_h * 2)) * num_mesh_sash * qty
            
            total_gasket_meters += (((sash_w * 2) + (sash_h * 2)) * 2 * num_glass_sash * qty) / 1000
            total_wool_pile_meters += ((((sash_w * 2) + (sash_h * 2)) * (num_glass_sash + num_mesh_sash) * qty) / 1000)

        if error_found:
            st.error("⚠️ Formula text format sahi nahi hai!")
        else:
            st.write("---")
            st.header("📐 SITE SINGLE SASH CUTTING SIZES")
            for display_text in sash_display_list: st.write(display_text)

            # --- SMART SMART COMBINATION EXECUTION (Zero Wastage Plan) ---
            bars_2t_plan = smart_cutting_stock(STANDARD_BAR, all_frame_2t_pieces, BLADE_THICKNESS) if all_frame_2t_pieces else []
            bars_3t_plan = smart_cutting_stock(STANDARD_BAR, all_frame_3t_pieces, BLADE_THICKNESS) if all_frame_3t_pieces else []
            bars_sash_plan = smart_cutting_stock(STANDARD_BAR, all_sash_pieces, BLADE_THICKNESS) if all_sash_pieces else []
            bars_mesh_plan = smart_cutting_stock(STANDARD_BAR, all_mesh_pieces, BLADE_THICKNESS) if all_mesh_pieces else []
            bars_alum_plan = smart_cutting_stock(ALUM_BAR_12FT, all_alum_pieces, 2) if all_alum_pieces else []
            
            bars_interlock = math.ceil(total_interlock_mm / STANDARD_BAR) if total_interlock_mm > 0 else 0

            st.write("---")
            st.header("🏢 MASTER MATERIAL & BAREEK HARDWARE BILL")
            
            bm1, bm2, bm3 = st.columns(3)
            with bm1:
                st.markdown("### 🪵 Profiles Required")
                if total_frame_2t_mm > 0: st.write(f"🔹 **2-Track Outer Frame:** `{total_frame_2t_mm/1000:.1f} Mtrs` ➔ 📦 **{len(bars_2t_plan)} Pcs (5.8m)**")
                if total_frame_3t_mm > 0: st.write(f"🔸 **3-Track Outer Frame:** `{total_frame_3t_mm/1000:.1f} Mtrs` ➔ 📦 **{len(bars_3t_plan)} Pcs (5.8m)**")
                st.write(f"🟩 **Glass Sash Profile:** `{total_sash_mm/1000:.1f} Mtrs` ➔ 📦 **{len(bars_sash_plan)} Pcs (5.8m)**")
                if total_mesh_sash_mm > 0: st.write(f"🕸️ **Jaali Sash Profile:** `{total_mesh_sash_mm/1000:.1f} Mtrs` ➔ 📦 **{len(bars_mesh_plan)} Pcs (5.8m)**")
                if total_interlock_mm > 0: st.write(f"⛓️ **Interlock Profile:** `{total_interlock_mm/1000:.1f} Mtrs` ➔ 📦 **{bars_interlock} Pcs (5.8m)**")
                st.write(f"⚙️ **Aluminum Sliding Track:** `{total_alum_track_mm/1000:.1f} Mtrs` ➔ 💿 **{len(bars_alum_plan)} Pcs (12ft)**")
                
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

            # --- CLEAN MIXED COMBINATION DISPLAY ---
            st.write("---")
            st.header("📐 ZERO-WASTAGE MIXED CUTTING PLANS")
            st.info("Mistri dhyan dein! Niche diye gaye tarike se pieces ko mila-jula kar kaatein, wastage ekdum zero girega:")
            
            if bars_2t_plan:
                st.subheader("🖼️ 2-Track Outer Frame Cutting")
                for idx, bar in enumerate(bars_2t_plan, 1):
                    waste = STANDARD_BAR - sum(bar) - (len(bar)*BLADE_THICKNESS)
                    st.write(f"BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Bacha kachra: `{max(0, waste)}` mm)")

            if bars_3t_plan:
                st.subheader("🖼️ 3-Track Outer Frame Cutting")
                for idx, bar in enumerate(bars_3t_plan, 1):
                    waste = STANDARD_BAR - sum(bar) - (len(bar)*BLADE_THICKNESS)
                    st.write(f"BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Bacha kachra: `{max(0, waste)}` mm)")

            if bars_sash_plan:
                st.subheader("🪟 Glass Sash Profile Cutting")
                for idx, bar in enumerate(bars_sash_plan, 1):
                    waste = STANDARD_BAR - sum(bar) - (len(bar)*BLADE_THICKNESS)
                    st.write(f"BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Bacha kachra: `{max(0, waste)}` mm)")

            if bars_mesh_plan:
                st.subheader("🕸️ Jaali (Mesh) Sash Profile Cutting")
                for idx, bar in enumerate(bars_mesh_plan, 1):
                    waste = STANDARD_BAR - sum(bar) - (len(bar)*BLADE_THICKNESS)
                    st.write(f"BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Bacha kachra: `{max(0, waste)}` mm)")

            if bars_alum_plan:
                st.subheader("⚙️ Aluminum Sliding Track Cutting (12ft Bars)")
                for idx, bar in enumerate(bars_alum_plan, 1):
                    waste = ALUM_BAR_12FT - sum(bar) - (len(bar)*2)
                    st.write(f"ALUM BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Bacha kachra: `{max(0, waste)}` mm)")
