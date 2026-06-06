import streamlit as st
import re
import math

# Page Setup - Gourav Smart UPVC Ultra-Premium VIP Dark Matrix Engine
st.set_page_config(page_title="Gourav Smart UPVC", page_icon="🪟", layout="wide")

# --- 🎨 VIP SHARP CARBON BLACK DARK THEME ---
st.markdown("""
    <style>
    /* Premium Dark Mode Background */
    .main { background-color: #0d0f12 !important; color: #e2e8f0 !important; }
    
    /* Neon Sharp Headings */
    h1, h2, h3, h4 { color: #00ecff !important; font-weight: bold !important; font-family: 'Courier New', monospace !important; text-shadow: 0px 0px 8px rgba(0,236,255,0.3) !important; }
    
    /* Electric Cyan Buttons */
    .stButton>button { background-color: #00ecff !important; color: #0d0f12 !important; font-weight: bold !important; border-radius: 4px !important; height: 45px !important; border: none !important; box-shadow: 0px 0px 15px rgba(0,236,255,0.4) !important; font-size: 16px !important; }
    .stButton>button:hover { background-color: #00b9cc !important; color: #ffffff !important; box-shadow: 0px 0px 25px rgba(0,236,255,0.7) !important; }
    
    /* Dark Input Boxes with Cyan Border */
    input { background-color: #1a1f26 !important; color: #00ecff !important; font-weight: bold !important; border: 1px solid #00ecff !important; border-radius: 4px !important; }
    select { background-color: #1a1f26 !important; color: #00ecff !important; font-weight: bold !important; border: 1px solid #00ecff !important; border-radius: 4px !important; }
    
    /* Glassmorphism Expander Panels */
    div[data-testid="stExpander"] { background-color: #151922 !important; border: 1px solid #00ecff !important; border-radius: 6px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] div { color: #ffffff !important; }
    
    /* Matrix Style Grid Containers */
    div[data-testid="stBlock"] { background-color: #11151d !important; padding: 12px !important; border-radius: 6px !important; border: 1px solid #242f41 !important; margin-bottom: 5px !important; }
    .stNumberInput, .stSelectbox { margin-bottom: 0px !important; padding-bottom: 0px !important; }
    
    /* Success & Error Alert Adjustments */
    .stAlert { background-color: #1a1f26 !important; border-radius: 4px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪟 GOURAV SMART UPVC | MASTER DEEP OPTIMIZER")
st.write("Production Status: Ultra Powerful Core Mode Enabled.")

BLADE_THICKNESS = 3  
ALUM_BAR_12FT = 3650  

def evaluate_custom_formula(formula_str, w_val, h_val):
    try:
        c_str = formula_str.lower().replace(' ', '').replace('width', str(w_val)).replace('w', str(w_val)).replace('height', str(h_val)).replace('h', str(h_val))
        if not re.match(r'^[\d\+\-\*\/\(\)\.]+$', c_str): return "Error"
        return int(round(eval(c_str)))
    except: return "Error"

# --- 🧠 BRUTE-FORCE MASTER PACKING ENGINE (Aapke Dimaag Ki Tarah Mixed Jodi Optimization) ---
def mistri_brain_cut_optimizer(stock_length, pieces, kerf):
    rem_pieces = list(pieces)
    all_bars = []
    
    while rem_pieces:
        best_combo = []
        best_waste = stock_length + 1
        
        def find_best_fit(current_idx, current_combo, current_length):
            nonlocal best_combo, best_waste
            num_cuts = len(current_combo)
            total_needed = current_length + (num_cuts * kerf)
            
            if total_needed > stock_length: return
            
            waste = stock_length - total_needed
            if waste < best_waste:
                best_waste = waste
                best_combo = list(current_combo)
                
            if best_waste <= 3: return  # 3mm tak perfect combo milte hi stop

            for i in range(current_idx, len(rem_pieces)):
                current_combo.append(rem_pieces[i])
                find_best_fit(i + 1, current_combo, current_length + rem_pieces[i])
                current_combo.pop()

        rem_pieces.sort(reverse=True)
        find_best_fit(0, [], 0)
        
        for p in best_combo: rem_pieces.remove(p)
        all_bars.append(best_combo)
        
    return all_bars

# =========================================================================
# ⚙️ 1. MASTER SETTINGS & BAR LENGTH SELECTOR
# =========================================================================
st.header("⚡ 1. MASTER CONFIGURATION")
with st.container():
    col_f1, col_f2, col_f3 = st.columns([3, 3, 2])
    with col_f1: custom_w_formula = st.text_input("Sash WIDTH Formula:", value="(W - 52 - 52 - 5 + 58 + 16) / 2 + 5")
    with col_f2: custom_h_formula = st.text_input("Sash HEIGHT Formula:", value="H - 50")
    with col_f3: chosen_bar_length = st.selectbox("Select Bar Stock Length:", [5800, 5900], index=0)
    
    st.write("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    
    st.markdown("#### Test Size On-The-Spot:")
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1: test_w = st.number_input("Enter Outer Width (W) in mm:", min_value=0, value=None, key="test_width", placeholder="W dalein...")
    with col_in2: test_h = st.number_input("Enter Outer Height (H) in mm:", min_value=0, value=None, key="test_height", placeholder="H dalein...")
    with col_in3:
        st.write("<div style='padding-top:25px;'></div>", unsafe_allow_html=True)
        if test_w and test_h:
            res_w = evaluate_custom_formula(custom_w_formula, test_w, test_h)
            res_h = evaluate_custom_formula(custom_h_formula, test_w, test_h)
            if res_w != "Error" and res_h != "Error":
                st.success(f"🎯 Sash Size: {res_w} x {res_h} mm")
            else: st.error("⚠️ Formula Check Karein!")

# =========================================================================
# 🏢 2. COMPACT ESTIMATOR TABLE
# =========================================================================
st.markdown("---")
st.header("⚡ 2. COMPACT SITE ESTIMATOR")

if 'bulk_rows' not in st.session_state: st.session_state.bulk_rows = 1

with st.container():
    col_t1, col_t2 = st.columns([2, 4])
    with col_t1: site_track = st.selectbox("Select Site Track Type:", ["2 Track", "2.5 Track", "3 Track"])

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
        with c1: w = st.number_input(f"Width #{i+1}", min_value=0, value=None, key=f"win_w_{i}", placeholder="Width mm...", label_visibility="collapsed")
        with c2: h = st.number_input(f"Height #{i+1}", min_value=0, value=None, key=f"win_h_{i}", placeholder="Height mm...", label_visibility="collapsed")
        with c3: q = st.number_input(f"Qty #{i+1}", min_value=1, value=1, step=1, key=f"win_q_{i}", label_visibility="collapsed")
        if w and h and w > 0 and h > 0: window_entries.append({"id": i+1, "width": w, "height": h, "qty": q})

if st.button("➕ Add More Window Row"):
    st.session_state.bulk_rows += 1
    st.rerun()

st.write("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# =========================================================================
# 🔴 BAREEK CALCULATION ENGINE WITH ASLI EXPERT UPVC RULES
# =========================================================================
if st.button("🔴 GENERATE FULL SITE LAYOUT & POWERFUL BILL", type="primary", use_container_width=True):
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
        total_gasket_meters = 0
        total_wool_pile_meters = 0
        
        # Hardware Counters
        hw_normal_rollers = 0
        hw_mesh_rollers = 0
        hw_adjustable_rollers = 0  
        hw_touch_locks = 0
        hw_espag_handles = 0       
        hw_espag_rods = 0          
        hw_bump_stoppers = 0       
        
        all_frame_2t_pieces = []
        all_frame_3t_pieces = []
        all_sash_pieces = []
        all_mesh_pieces = []
        all_alum_pieces = []  
        all_interlock_pieces = [] # <--- New Interlock Cut List
        
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
            
            # --- 🛠️ INDUSTRY STANDARD CALCULATIONS ---
            if site_track == "2 Track":
                num_glass_sash = 2
                num_mesh_sash = 0
                num_interlock_pieces = 2 # <--- 2 Khade Interlock Fixed!
                
                total_frame_2t_mm += ((w * 2) + (h * 2)) * qty
                all_frame_2t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_alum_track_mm += (w * 2) * qty
                all_alum_pieces.extend([int(w), int(w)] * qty)
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_glass_sash * qty
                
                hw_normal_rollers += 4 * qty
                hw_touch_locks += 2 * qty
                hw_bump_stoppers += 2 * qty  
                
                sash_display_list.append(f"🔹 Line {idx} ({site_track}): Glass Sash = `{sash_w} x {sash_h} mm` | Qty: {num_glass_sash * qty} Palles")
                
            elif site_track == "2.5 Track":
                num_glass_sash = 2
                num_mesh_sash = 1
                num_interlock_pieces = 2 # <--- Glass pallo ke beech me 2 khade pieces
                
                total_frame_3t_mm += ((w * 2) + (h * 2)) * qty
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_alum_track_mm += (w * 3) * qty
                all_alum_pieces.extend([int(w), int(w), int(w)] * qty)
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_glass_sash * qty
                total_mesh_area += (sash_w / 304.8) * (sash_h / 304.8) * num_mesh_sash * qty
                
                hw_normal_rollers += 4 * qty
                hw_mesh_rollers += 2 * qty
                hw_touch_locks += 3 * qty  
                hw_bump_stoppers += 2 * qty  
                
                sash_display_list.append(f"🔹 Line {idx} ({site_track}): Glass Sash = `{sash_w} x {sash_h} mm` ({num_glass_sash * qty} Pcs) | Jaali Sash = `{sash_w} x {sash_h} mm` ({num_mesh_sash * qty} Pcs)")
                
            elif site_track == "3 Track":
                num_glass_sash = 3  
                num_mesh_sash = 0
                num_interlock_pieces = 4 # <--- 🧠 MISTRI BRAIN CORE FIXED: 4 KHADE INTERLOCK PIECES PIECE-TO-PIECE!
                
                total_frame_3t_mm += ((w * 2) + (h * 2)) * qty
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_alum_track_mm += (w * 3) * qty
                all_alum_pieces.extend([int(w), int(w), int(w)] * qty)
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_glass_sash * qty
                
                hw_adjustable_rollers += 6 * qty  
                hw_espag_handles += 3 * qty       
                hw_espag_rods += 3 * qty          
                hw_bump_stoppers += 4 * qty  
                
                sash_display_list.append(f"🔹 Line {idx} ({site_track}): Glass Sash = `{sash_w} x {sash_h} mm` | Qty: {num_glass_sash * qty} Palles")

            # Cut lists bundles
            all_sash_pieces.extend([int(sash_w)] * (2 * num_glass_sash * qty))
            all_sash_pieces.extend([int(sash_h)] * (2 * num_glass_sash * qty))
            total_sash_mm += ((sash_w * 2) + (sash_h * 2)) * num_glass_sash * qty
            
            if num_mesh_sash > 0:
                all_mesh_pieces.extend([int(sash_w)] * (2 * num_mesh_sash * qty))
                all_mesh_pieces.extend([int(sash_h)] * (2 * num_mesh_sash * qty))
                total_mesh_sash_mm += ((sash_w * 2) + (sash_h * 2)) * num_mesh_sash * qty
            
            # Interlock bundle according to precise pieces rule
            all_interlock_pieces.extend([int(sash_h)] * (num_interlock_pieces * qty))
            total_interlock_mm += (sash_h * num_interlock_pieces) * qty
            
            total_gasket_meters += (((sash_w * 2) + (sash_h * 2)) * 2 * num_glass_sash * qty) / 1000
            total_wool_pile_meters += ((((sash_w * 2) + (sash_h * 2)) * (num_glass_sash + num_mesh_sash) * qty) / 1000)

        if error_found: st.error("⚠️ Formula format check karein!")
        else:
            st.write("---")
            st.header("📐 SITE SINGLE SASH CUTTING SIZES")
            for display_text in sash_display_list: st.write(display_text)

            # Optimizations via Brute Force Mixed-Jodi Algorithm
            bars_2t_plan = mistri_brain_cut_optimizer(chosen_bar_length, all_frame_2t_pieces, BLADE_THICKNESS) if all_frame_2t_pieces else []
            bars_3t_plan = mistri_brain_cut_optimizer(chosen_bar_length, all_frame_3t_pieces, BLADE_THICKNESS) if all_frame_3t_pieces else []
            bars_sash_plan = mistri_brain_cut_optimizer(chosen_bar_length, all_sash_pieces, BLADE_THICKNESS) if all_sash_pieces else []
            bars_mesh_plan = mistri_brain_cut_optimizer(chosen_bar_length, all_mesh_pieces, BLADE_THICKNESS) if all_mesh_pieces else []
            bars_interlock_plan = mistri_brain_cut_optimizer(chosen_bar_length, all_interlock_pieces, BLADE_THICKNESS) if all_interlock_pieces else []
            bars_alum_plan = mistri_brain_cut_optimizer(3650, all_alum_pieces, 2) if all_alum_pieces else []

            st.write("---")
            st.header(f"🏢 MASTER MATERIAL & HARDWARE CHECKLIST ({chosen_bar_length}mm)")
            
            bm1, bm2, bm3 = st.columns(3)
            with bm1:
                st.markdown("#### 🪵 Profiles Required")
                if total_frame_2t_mm > 0: st.write(f"🔹 **2-Track Outer Frame:** `{total_frame_2t_mm/1000:.1f} Mtrs` ➔ 📦 **{len(bars_2t_plan)} Pcs**")
                if total_frame_3t_mm > 0: st.write(f"🔸 **3-Track Outer Frame:** `{total_frame_3t_mm/1000:.1f} Mtrs` ➔ 📦 **{len(bars_3t_plan)} Pcs**")
                st.write(f"🟩 **Glass Sash Profile:** `{total_sash_mm/1000:.1f} Mtrs` ➔ 📦 **{len(bars_sash_plan)} Pcs**")
                if total_mesh_sash_mm > 0: st.write(f"🕸️ **Jaali (Mesh) Profile:** `{total_mesh_sash_mm/1000:.1f} Mtrs` ➔ 📦 **{len(bars_mesh_plan)} Pcs**")
                st.write(f"⛓️ **Interlock Profile:** `{total_interlock_mm/1000:.1f} Mtrs` ➔ 📦 **{len(bars_interlock_plan)} Pcs**")
                st.write(f"⚙️ **Aluminum Sliding Track:** `{total_alum_track_mm/1000:.1f} Mtrs` ➔ 💿 **{len(bars_alum_plan)} Pcs (12ft)**")
                
            with bm2:
                st.markdown("#### 🪟 Glass & Jaali Sheet")
                st.write(f"⬛ **Pure Glass Area:** `{total_glass_area:.2f} Sq.Ft.`")
                if total_mesh_area > 0: st.write(f"🕸️ **Wire Mesh (Jaali):** `{total_mesh_area:.2f} Sq.Ft.`")
                
            with bm3:
                st.markdown("#### 📦 Accurate Accessories Checklist")
                if hw_normal_rollers > 0: st.write(f"🛞 Standard Glass Rollers: **{hw_normal_rollers} Pcs**")
                if hw_mesh_rollers > 0: st.write(f"🦟 Mosquito Mesh Rollers: **{hw_mesh_rollers} Pcs**")
                if hw_adjustable_rollers > 0: st.write(f"🚀 Heavy Adjustable Rollers: **{hw_adjustable_rollers} Pcs**")
                if hw_touch_locks > 0: st.write(f"🔒 Standard Touch Locks: **{hw_touch_locks} Pcs**")
                if hw_espag_handles > 0: st.write(f"🔑 Premium Espag Handles: **{hw_espag_handles} Pcs**")
                if hw_espag_rods > 0: st.write(f"⛓️ Multi-Point Espag Rods: **{hw_espag_rods} Pcs**")
                if hw_bump_stoppers > 0: st.write(f"🛑 Rubber Bump Stoppers: **{hw_bump_stoppers} Pcs**") 
                st.write(f"⚫ Weather Gasket Rubber: **{total_gasket_meters:.1f} Mtrs**")
                st.write(f"💨 Dust Wool Pile: **{total_wool_pile_meters:.1f} Mtrs**")

            # Cutting plans
            st.write("---")
            st.header(f"📐 DEEP MISTRI-BRAIN COMBINATION PLANS ({chosen_bar_length}mm Stock)")
            
            if bars_2t_plan:
                st.subheader("🖼️ 2-Track Outer Frame Cutting")
                for idx, bar in enumerate(bars_2t_plan, 1):
                    waste = chosen_bar_length - sum(bar) - (len(bar)*BLADE_THICKNESS)
                    st.write(f"BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Waste: `{max(0, waste)}` mm)")

            if bars_3t_plan:
                st.subheader("🖼️ 3-Track Outer Frame Cutting")
                for idx, bar in enumerate(bars_3t_plan, 1):
                    waste = chosen_bar_length - sum(bar) - (len(bar)*BLADE_THICKNESS)
                    st.write(f"BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Waste: `{max(0, waste)}` mm)")

            if bars_sash_plan:
                st.subheader("🪟 Glass Sash Profile Cutting")
                for idx, bar in enumerate(bars_sash_plan, 1):
                    waste = chosen_bar_length - sum(bar) - (len(bar)*BLADE_THICKNESS)
                    st.write(f"BAR #{idx} ➔ Kaato Mixed Combos: `{bar}` mm | (🎯 Waste: `{max(0, waste)}` mm)")

            if bars_mesh_plan:
                st.subheader("🕸️ Jaali (Mesh) Sash Profile Cutting")
                for idx, bar in enumerate(bars_mesh_plan, 1):
                    waste = chosen_bar_length - sum(bar) - (len(bar)*BLADE_THICKNESS)
                    st.write(f"BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Waste: `{max(0, waste)}` mm)")

            if bars_interlock_plan:
                st.subheader("⛓️ Interlock Profile Cutting")
                for idx, bar in enumerate(bars_interlock_plan, 1):
                    waste = chosen_bar_length - sum(bar) - (len(bar)*BLADE_THICKNESS)
                    st.write(f"BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Waste: `{max(0, waste)}` mm)")

            if bars_alum_plan:
                st.subheader("⚙️ Aluminum Sliding Track Cutting (12ft/3650mm)")
                for idx, bar in enumerate(bars_alum_plan, 1):
                    waste = 3650 - sum(bar) - (len(bar)*2)
                    st.write(f"ALUM BAR #{idx} ➔ Kaato Pieces: `{bar}` mm | (Waste: `{max(0, waste)}` mm)")
