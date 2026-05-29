import streamlit as st

# Custom CSS for Premium "The Dark Mentor" Theme
st.set_page_config(page_title="The Dark Mentor - UPVC Track Pro", page_icon="🥷", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3, h4 { color: #00ffcc !important; }
    .stButton>button { background-color: #00ffcc; color: #000000; font-weight: bold; border-radius: 8px; width: 100%; height: 50px; font-size: 18px; }
    .stButton>button:hover { background-color: #00ccaa; color: #000000; }
    div[data-testid="stExpander"] { background-color: #1f2937; border: 1px solid #374151; border-radius: 8px; }
    select { background-color: #1f2937; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🥷 The Dark Mentor | Intelligent Multi-Track Optimizer")
st.write("2 Track, 2.5 Track aur 3 Track ka exact material bill aur cutting layout ek sath.")

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

# --- BULK INPUT SECTION ---
st.subheader("📝 Site Multi-Track Entries")

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
        total_frame_3t_m = 0  # 2.5T aur 3T me 3-track outer lagta hai
        total_sash_m = 0
        total_mesh_sash_m = 0
        
        total_rollers = 0
        total_mesh_rollers = 0
        total_locks = 0
        total_gasket = 0
        total_wool_pile = 0
        
        all_frame_2t_pieces = []
        all_frame_3t_pieces = []
        all_sash_pieces = []
        all_mesh_pieces = []
        
        for win in window_list:
            t = win["track"]
            w = win["width"]
            h = win["height"]
            qty = win["qty"]
            
            # 1. DEDUCTIONS & LOGIC BASED ON TRACK TYPE
            if t == "2 Track":
                # 2 Track standard formulas
                sash_w = (w / 2) + 25
                sash_h = h - 50
                num_sash = 2
                
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_2t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_2t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                
                total_rollers += 4 * qty
                total_locks += 2 * qty
                
            elif t == "2.5 Track":
                # 3 Track Outer Frame but 2 Glass Sash + 1 Mesh Sash
                sash_w = (w / 2) + 25  # standard overlap
                sash_h = h - 50
                
                # Glass area for 2 sashes
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * 2 * qty
                # Mesh area for 1 net sash
                total_mesh_area += (sash_w / 304.8) * (sash_h / 304.8) * 1 * qty
                
                total_frame_3t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                
                # 2 Glass sash + 1 Mesh sash = total 3 sash pieces
                all_sash_pieces.extend([int(sash_w)] * (4 * qty)) # 2 glass sash width
                all_sash_pieces.extend([int(sash_h)] * (4 * qty)) # 2 glass sash height
                all_mesh_pieces.extend([int(sash_w)] * (2 * qty)) # 1 mesh width
                all_mesh_pieces.extend([int(sash_h)] * (2 * qty)) # 1 mesh height
                
                total_rollers += 4 * qty
                total_mesh_rollers += 2 * qty
                total_locks += 3 * qty
                
            elif t == "3 Track":
                # 3 Track Outer Frame with 3 Sliding Glass Sashes
                sash_w = (w / 3) + 30  # Overlap changes for 3-track sliding
                sash_h = h - 50
                num_sash = 3
                
                total_glass_area += (sash_w / 304.8) * (sash_h / 304.8) * num_sash * qty
                total_frame_3t_m += (((w * 2) + (h * 2)) * qty) / 1000
                all_frame_3t_pieces.extend([int(w), int(w), int(h), int(h)] * qty)
                
                total_rollers += 6 * qty
                total_locks += 3 * qty

            # Common Profile & Consumables collection
            if t != "2.5 Track":
                all_sash_pieces.extend([int(sash_w)] * (2 * num_sash * qty))
                all_sash_pieces.extend([int(sash_h)] * (2 * num_sash * qty))
            
            current_sash_total_mm = ((sash_w * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2)) + (sash_h * 2 * (3 if t=="3 Track" or t=="2.5 Track" else 2))) * qty
            total_sash_m += current_sash_total_mm / 1000
            total_gasket += (current_sash_total_mm * 2) / 1000
            total_wool_pile += ((sash_h * 4) + (sash_w * 2)) * qty / 1000

        # ------------------ PRINT MATERIAL BILL ------------------
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

        # ------------------ OPTIMIZATION LAYOUTS ------------------
        # 1. 2-Track Frame Optimization
        if all_frame_2t_pieces:
            st.header("📐 1. 2-TRACK OUTER FRAME CUTTING PLAN")
            bars = cutting_stock_1d(STANDARD_BAR, all_frame_2t_pieces, BLADE_THICKNESS)
            st.subheader(f"Total 2-Track Frame Bars (5.8m): {len(bars)} Pcs")
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"🖼️ 2-TRACK FRAME BAR {idx} -> Pieces: {bar}"):
                    st.progress(int((sum(bar)/STANDARD_BAR)*100))

        # 2. 3-Track Frame Optimization
        if all_frame_3t_pieces:
            st.header("📐 2. 3-TRACK OUTER FRAME CUTTING PLAN")
            bars = cutting_stock_1d(STANDARD_BAR, all_frame_3t_pieces, BLADE_THICKNESS)
            st.subheader(f"Total 3-Track Frame Bars (5.8m): {len(bars)} Pcs")
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"🖼️ 3-TRACK FRAME BAR {idx} -> Pieces: {bar}"):
                    st.progress(int((sum(bar)/STANDARD_BAR)*100))

        # 3. Glass Sash Optimization
        if all_sash_pieces:
            st.header("⚡ 3. GLASS SASH PROFILE CUTTING PLAN")
            bars = cutting_stock_1d(STANDARD_BAR, all_sash_pieces, BLADE_THICKNESS)
            st.subheader(f"Total Sash Bars (5.8m): {len(bars)} Pcs")
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"🪟 SASH BAR {idx} -> Pieces: {bar}"):
                    st.progress(int((sum(bar)/STANDARD_BAR)*100))

        # 4. Mesh Sash Optimization
        if all_mesh_pieces:
            st.header("🕸️ 4. MESH SASH (JAALI) CUTTING PLAN")
            bars = cutting_stock_1d(STANDARD_BAR, all_mesh_pieces, BLADE_THICKNESS)
            st.subheader(f"Total Mesh Sash Bars (5.8m): {len(bars)} Pcs")
            for idx, bar in enumerate(bars, 1):
                with st.expander(f"🕸️ MESH BAR {idx} -> Pieces: {bar}"):
                    st.progress(int((sum(bar)/STANDARD_BAR)*100))
