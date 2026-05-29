import streamlit as st

# Custom CSS for Professional Clean Layout - "Gourav Smart UPVC"
st.set_page_config(page_title="Gourav Smart UPVC", page_icon="🪟", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; color: #212529; }
    h1, h2, h3, h4 { color: #0056b3 !important; }
    .stButton>button { background-color: #0056b3; color: #ffffff; font-weight: bold; border-radius: 8px; width: 100%; height: 50px; font-size: 18px; border: none; }
    .stButton>button:hover { background-color: #004085; color: #ffffff; }
    div[data-testid="stExpander"] { background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    select { background-color: #ffffff; color: #212529; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪟 Gourav Smart UPVC | Intelligent Multi-Track Optimizer")
st.write("Workshop Special - Custom Formula Engine, Material Bill aur Cutting Layout.")

# --- CONFIGURATION ---
STANDARD_BAR = 5800  # 5.8m
BLADE_THICKNESS = 3  # 3mm

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
# 🔥 NEW SECTION: CUSTOM SASH FORMULA CALCULATOR (Aapka Naya Idea)
# =========================================================================
st.markdown("---")
st.header("🧮 SECTION 1: CUSTOM SASH SIZE CALCULATOR")
st.write("Agar aapko kisi alag brand ke hisab se apna khud ka formula daal kar sash size check karna hai, toh yahan karein:")

with st.container():
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        f_track = st.selectbox("Track Chunien", ["2 Track", "2.5 Track", "3 Track"], key="f_track_select")
        f_width = st.number_input("Window Width (mm)", min_value=0, value=1200, step=10, key="f_w_in")
    
    with col_f2:
        # User khud apna deduction mm me daal sakta hai
        if f_track == "3 Track":
            st.write("**Overlap Formula:** (Width / 3) + Overlap")
            f_overlap = st.number_input("Overlap Plus (mm)", min_value=0, value=30, key="f_over_in")
        else:
            st.write("**Overlap Formula:** (Width / 2) + Overlap")
            f_overlap = st.number_input("Overlap Plus (mm)", min_value=0, value=25, key="f_over_in")
            
        f_height = st.number_input("Window Height (mm)", min_value=0, value=1500, step=10, key="f_h_in")
        
    with col_f3:
        st.write("**Height Deduction Formula:** Height - Minus")
        f_minus = st.number_input("Height Minus (mm)", min_value=0, value=50, key="f_min_in")

    if st.button("🧮 CALCUTE CUSTOM SASH SIZE", type="secondary"):
        if f_width > 0 and f_height > 0:
            # Formula Calculation based on user input
            if f_track == "3 Track":
                calc_sash_w = (f_width / 3) + f_overlap
            else:
                calc_sash_w = (f_width / 2) + f_overlap
                
            calc_sash_h = f_height - f_minus
            
            st.markdown("### 🎯 Aapka Custom Sash Size:")
            if f_track == "2.5 Track":
                st.success(f"🟢 **Glass Sash Size:** `{int(calc_sash_w)} mm` (W) x `{int(calc_sash_h)} mm` (H)\n\n🟢 **Mesh Sash (Jaali) Size:** `{int(calc_sash_w)} mm` (W) x `{int(calc_sash_h)} mm` (H)")
            elif f_track == "3 Track":
                st.success(f"🟢 **3-Track Sash Size (3 Palles):** `{int(calc_sash_w)} mm` (W) x `{int(calc_sash_h)} mm` (H)")
            else:
                st.success(f"🟢 **2-Track Sash Size (2 Palles):** `{int(calc_sash_w)} mm` (W) x `{int(calc_sash_h)} mm` (H)")
        else:
            st.error("Kripya sahi Width aur Height dalein!")

st.markdown("---")


# =========================================================================
# 🏢 SECTION 2: BULK SITE ESTIMATOR & OPTIMIZER (Purana Section)
# =========================================================================
st.header("🏢 SECTION 2: FULL SITE BULK CALCULATOR & OPTIMIZER")
st.write("Poori site ki 10-15 windows ki entry ek sath karne ke liye is section ka use karein:")

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
        # Total Variables for Site BOM
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
            
            if t == "2 Track":
                sash_w = (w / 2) + 25
                sash_h = h - 50
                num_sash = 2
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_2t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_2t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_rollers += 4 * qty
                total_locks += 2 * qty
                sash_sizes_display.append(f"🔹 **Window {idx} ({t}):** Single Sash Size = `{int(sash_w)} mm` (W) x `{int(sash_h)} mm` (H) | Total {num_sash * qty} Palles")
                
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
                sash_sizes_display.append(f"🔹 **Window {idx} ({t}):** Glass Sash = `{int(sash_w)}x{int(sash_h)} mm` ({2*qty} Pcs) | Mesh Sash = `{int(sash_w)}x{int(sash_h)} mm` ({qty} Pcs)")
                
            elif t == "3 Track":
                sash_w = (w / 3) + 30
                sash_h = h - 50
                num_sash = 3
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_3t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                total_rollers += 6 * qty
                total_locks += 3 * qty
                sash_sizes_display.append(f"🔹 **Window {idx} ({t}):** Single Sash Size = `{int(sash_w)} mm` (W) x `{int(sash_h)} mm` (H) | Total {num_sash * qty} Palles")

            if t != "2.5 Track":
                all_sash_pieces.extend([int(sash_w)] * (2 * num_sash * qty))
                all_sash_pieces.extend([int(sash_h)] * (2 * num_sash * qty))
            
            current_sash_total_mm = ((sash_w * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2)) + (sash_h * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2))) * qty
            total_sash_m += current_sash_total_mm / 1000
            total_gasket += (current_sash_total_mm * 2) / 1000
            total_wool_pile += ((sash_h * 4) + (sash_w * 2)) * qty / 1000

        # --- PRINT MATERIAL BILL ---
        st.header("🏢 FINAL SITE MATERIAL BILL (BOM)")
        
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            st.metric("Total Glass Area", f"{total_glass_area:.2f} Sq.Ft.")
            if total_mesh_area > 0:
                st.write(f"🕸️ **Wire Mesh (Jaali):** `{total_mesh_area:.2f} Sq.Ft.`")
        with c_m2:
            if total_frame_2t_m > 0:
                st.write(f"🔹 **2-Track Outer Frame:** `{total_frame_2t_m:.2f} Meters`")
            if total_frame_3t_m > 0:
                st.write(f"🔸 **3-Track Outer Frame:** `{total_frame_3t_m:.2f} Meters`")
        with c_m3:
            st.metric("Total Sash Profile", f"{total_sash_m:.2f} Meters")

        st.subheader("📦 Hardware & Locks Breakdown:")
        st.write(f"🛞 Heavy Rollers: `{total_rollers} Pcs` | 🕸️ Mesh Rollers: `{total_mesh_rollers} Pcs` | 🔒 Touch Locks: `{total_locks} Pcs`")
        st.write(f"⬛ Gasket (Rubber): `{total_gasket:.1f} Meters` | 💨 Wool Pile (Strips): `{total_wool_pile:.1f} Meters`")
        
        st.write("---")
        st.header("📐 SINGLE SASH CUTTING SIZES (Palle Ka Naap)")
        for size_info in sash_sizes_display:
            st.write(size_info)
        
        st.write("---")

        # --- OPTIMIZATION LAYOUTS ---
        if all_frame_2t_pieces:
            st.header("📐 1. 2-TRACK OUTER FRAME CUTTING PLAN")
            bars = cutting_stock_1d(STANDARD_BAR, all_frame_2t_pieces, BLADE_THICKNESS)
            st.subheader(f"Total 2-Track Frame Bars (5.8m): {len(bars)} Pcs")
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"🖼️ 2-TRACK FRAME BAR {idx} -> Pieces: {bar}"):
                    st.progress(int((sum(bar)/STANDARD_BAR)*100))

        if all_frame_3t_pieces:
            st.header("📐 2. 3-TRACK OUTER FRAME CUTTING PLAN")
            bars = cutting_stock_1d(STANDARD_BAR, all_frame_3t_pieces, BLADE_THICKNESS)
            st.subheader(f"Total 3-Track Frame Bars (5.8m): {len(bars)} Pcs")
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"🖼️ 3-TRACK FRAME BAR {idx} -> Pieces: {bar}"):
                    st.progress(int((sum(bar)/STANDARD_BAR)*100))

        if all_sash_pieces:
            st.header("⚡ 3. GLASS SASH PROFILE CUTTING PLAN")
            bars = cutting_stock_1d(STANDARD_BAR, all_sash_pieces, BLADE_THICKNESS)
            st.subheader(f"Total Sash Bars (5.8m): {len(bars)} Pcs")
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"🪟 SASH BAR {idx} -> Pieces: {bar}"):
                    st.progress(int((sum(bar)/STANDARD_BAR)*100))

        if all_mesh_pieces:
            st.header("🕸️ 4. MESH SASH (JAALI) CUTTING PLAN")
            bars = cutting_stock_1d(STANDARD_BAR, all_mesh_pieces, BLADE_THICKNESS)
            st.subheader(f"Total Mesh Sash Bars (5.8m): {len(bars)} Pcs")
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"🕸️ MESH BAR {idx} -> Pieces: {bar}"):
                    st.progress(int((sum(bar)/STANDARD_BAR)*100))
