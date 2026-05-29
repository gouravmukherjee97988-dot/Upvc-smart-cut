import streamlit as st
import re

st.set_page_config(page_title="UPVC Smart Cut & BOM", page_icon="✂️", layout="centered")

st.title("✂️ UPVC Smart Cut & Material Bill (BOM)")
st.write("Jamshedpur Workshop Special - Super Fast & No Error Version")

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

# --- MATERIAL ESTIMATION LOGIC (2-Track Window Standard) ---
def calculate_material_bill(width, height, qty):
    # Total Window Area in SqFt (For Glass)
    area_sqft = (width / 304.8) * (height / 304.8) * qty
    
    # 1. Profiles Length (mm me)
    outer_frame_total = ((width * 2) + (height * 2)) * qty
    sash_width = (width / 2) + 25  # Standard overlap 25mm assuming 2-track
    sash_height = height - 50       # Deduction assuming standard frame
    sash_total = ((sash_width * 4) + (sash_height * 4)) * qty
    
    # 2. Hardware Count
    rollers = 4 * qty         # 2 per sash, total 2 sash = 4
    touch_locks = 2 * qty     # 1 per sash
    interlocks = 2 * qty      # 2 vertical interlocks
    
    # 3. Gasket & Wool Pile (Metres me)
    glass_gasket_m = (sash_total * 2) / 1000  # Inner + Outer sash beading gasket
    wool_pile_m = ((sash_height * 4) + (sash_width * 2)) * qty / 1000
    
    return {
        "glass_area": area_sqft,
        "frame_mm": outer_frame_total,
        "sash_mm": sash_total,
        "sash_w_piece": sash_width,
        "sash_h_piece": sash_height,
        "rollers": rollers,
        "locks": touch_locks,
        "interlocks": interlocks,
        "gasket": glass_gasket_m,
        "wool_pile": wool_pile_m
    }

# --- APP INTERFACE ---
st.subheader("📋 Step 1: Window Ka Size Aur Quantity Dalein")
col1, col2, col3 = st.columns(3)
with col1:
    w_input = st.number_input("Width (mm)", value=1200)
with col2:
    h_input = st.number_input("Height (mm)", value=1500)
with col3:
    q_input = st.number_input("Quantity (Sets)", value=2, min_value=1)

if st.button("Generate Bill & Cutting Plan", type="primary"):
    # 1. Calculate Material Bill
    bom = calculate_material_bill(w_input, h_input, q_input)
    
    st.header("📦 Pura Material Bill (BOM)")
    
    # Tables for clean look
    st.subheader("1. Profile & Glass Requirement")
    st.write(f"🔹 **Total Glass Area Needed:** `{bom['glass_area']:.2f} Sq.Ft.`")
    st.write(f"🔹 **Total Outer Frame Profile:** `{bom['frame_mm']/1000:.2f} Meters`")
    st.write(f"🔹 **Total Sash Profile:** `{bom['sash_mm']/1000:.2f} Meters`")
    
    st.subheader("2. Hardware Items")
    st.write(f"🛞 **Rollers:** `{bom['rollers']} Pcs`")
    st.write(f"🔒 **Touch Locks:** `{bom['locks']} Pcs`")
    st.write(f"🥢 **Interlocks:** `{bom['interlocks']} Pcs`")
    
    st.subheader("3. Gasket & Wool Pile")
    st.write(f"⬛ **Rubber Gasket:** `{bom['gasket']:.1f} Meters`")
    st.write(f"💨 **Wool Pile:** `{bom['wool_pile']:.1f} Meters`")
    
    # 2. Run Cutting Optimization for Sash
    st.header("📊 Step 2: Sash Cutting Optimization Plan")
    
    # Hum saare sash pieces ko list me convert kar rahe hain cutting ke liye
    sash_w_pieces = [int(bom['sash_w_piece'])] * (4 * q_input)
    sash_h_pieces = [int(bom['sash_h_piece'])] * (4 * q_input)
    all_sash_pieces = sash_w_pieces + sash_h_pieces
    
    result_bars = cutting_stock_1d(STANDARD_BAR, all_sash_pieces, BLADE_THICKNESS)
    
    st.metric(label="Total 5.8m Sash Bars Needed", value=f"{len(result_bars)} Pieces")
    
    for idx, bar in enumerate(result_bars, 1):
        used_space = sum(bar) + ((len(bar)-1) * BLADE_THICKNESS)
        wastage = STANDARD_BAR - used_space
        wastage_pct = (wastage / STANDARD_BAR) * 100
        
        with st.expander(f"📦 SASH BAR NO. {idx} Cutting Details"):
            st.write(f"**Kaatne wale pieces (mm):** {bar}")
            st.write(f"**Wastage (Tukda):** {wastage} mm ({wastage_pct:.1f}%)")
            st.progress(int((used_space / STANDARD_BAR) * 100))
