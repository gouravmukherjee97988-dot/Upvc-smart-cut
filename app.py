import streamlit as st
import re

# Custom CSS for Premium "The Dark Mentor" Theme (Black & Neon)
st.set_page_config(page_title="The Dark Mentor - UPVC Pro", page_icon="🥷", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #00ffcc !important; }
    .stButton>button { background-color: #00ffcc; color: #000000; font-weight: bold; border-radius: 8px; }
    .stButton>button:hover { background-color: #00ccaa; color: #000000; }
    div[data-testid="stExpander"] { background-color: #1f2937; border: 1px solid #374151; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🥷 The Dark Mentor | UPVC Smart Optimizer")
st.write("Frame aur Sash dono ka exact cutting plan aur billing ek sath.")

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

# --- MATERIAL ESTIMATION LOGIC ---
def calculate_material_bill(width, height, qty):
    area_sqft = (width / 304.8) * (height / 304.8) * qty
    
    # Outer Frame pieces (Har window me 2 width aur 2 height ke piece lagte hain)
    frame_w_piece = width
    frame_h_piece = height
    
    # Sash pieces deduction (Assuming standard 2-Track)
    sash_w_piece = (width / 2) + 25  
    sash_height = height - 50       
    
    rollers = 4 * qty         
    touch_locks = 2 * qty     
    interlocks = 2 * qty      
    
    outer_frame_total = ((width * 2) + (height * 2)) * qty
    sash_total = ((sash_w_piece * 4) + (sash_height * 4)) * qty
    glass_gasket_m = (sash_total * 2) / 1000  
    wool_pile_m = ((sash_height * 4) + (sash_w_piece * 2)) * qty / 1000
    
    return {
        "glass_area": area_sqft,
        "frame_total_m": outer_frame_total / 1000,
        "sash_total_m": sash_total / 1000,
        "frame_w_piece": frame_w_piece,
        "frame_h_piece": frame_h_piece,
        "sash_w_piece": sash_w_piece,
        "sash_h_piece": sash_height,
        "rollers": rollers,
        "locks": touch_locks,
        "interlocks": interlocks,
        "gasket": glass_gasket_m,
        "wool_pile": wool_pile_m
    }

# --- APP INTERFACE ---
st.subheader("📋 Step 1: Window Ka Size Input Karein")
col1, col2, col3 = st.columns(3)
with col1:
    w_input = st.number_input("Width (mm)", value=1200)
with col2:
    h_input = st.number_input("Height (mm)", value=1500)
with col3:
    q_input = st.number_input("Quantity (Sets)", value=2, min_value=1)

if st.button("🔴 GENERATE COMPLETE LAYOUT", type="primary"):
    bom = calculate_material_bill(w_input, h_input, q_input)
    
    # ------------------ BILLING SECTION ------------------
    st.header("📦 Pura Material Bill (BOM)")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.metric("Total Glass Area", f"{bom['glass_area']:.2f} Sq.Ft.")
    with col_b2:
        st.metric("Frame Profile Needed", f"{bom['frame_total_m']:.2f} Mtrs")
    with col_b3:
        st.metric("Sash Profile Needed", f"{bom['sash_total_m']:.2f} Mtrs")
        
    st.subheader("Hardware & Consumables Count:")
    st.write(f"🛞 Rollers: `{bom['rollers']} Pcs` | 🔒 Touch Locks: `{bom['locks']} Pcs` | 🥢 Interlocks: `{bom['interlocks']} Pcs`")
    st.write(f"⬛ Rubber Gasket: `{bom['gasket']:.1f} Meters` | 💨 Wool Pile: `{bom['wool_pile']:.1f} Meters`")
    
    st.write("---")
    
    # ------------------ FRAME OPTIMIZATION ------------------
    st.header("📐 1. OUTER FRAME CUTTING PLAN")
    
    # Har window ke liye 2 width aur 2 height wale pieces calculate kar rahe hain
    frame_pieces = ([int(bom['frame_w_piece'])] * (2 * q_input)) + ([int(bom['frame_h_piece'])] * (2 * q_input))
    frame_bars = cutting_stock_1d(STANDARD_BAR, frame_pieces, BLADE_THICKNESS)
    
    st.subheader(f"Required 5.8m Frame Bars: {len(frame_bars)} Pcs")
    
    for idx, bar in enumerate(frame_bars, 1):
        used = sum(bar) + ((len(bar)-1) * BLADE_THICKNESS)
        waste = STANDARD_BAR - used
        waste_pct = (waste / STANDARD_BAR) * 100
        with st.expander(f"🖼️ FRAME BAR {idx} -> Pieces: {bar}"):
            st.write(f"**Wastage:** {waste} mm ({waste_pct:.1f}%)")
            st.progress(int((used / STANDARD_BAR) * 100))

    st.write("---")

    # ------------------ SASH OPTIMIZATION ------------------
    st.header("⚡ 2. SASH CUTTING PLAN")
    
    sash_pieces = ([int(bom['sash_w_piece'])] * (4 * q_input)) + ([int(bom['sash_h_piece'])] * (4 * q_input))
    sash_bars = cutting_stock_1d(STANDARD_BAR, sash_pieces, BLADE_THICKNESS)
    
    st.subheader(f"Required 5.8m Sash Bars: {len(sash_bars)} Pcs")
    
    for idx, bar in enumerate(sash_bars, 1):
        used = sum(bar) + ((len(bar)-1) * BLADE_THICKNESS)
        waste = STANDARD_BAR - used
        waste_pct = (waste / STANDARD_BAR) * 100
        with st.expander(f"🪟 SASH BAR {idx} -> Pieces: {bar}"):
            st.write(f"**Wastage:** {waste} mm ({waste_pct:.1f}%)")
            st.progress(int((used / STANDARD_BAR) * 100))
