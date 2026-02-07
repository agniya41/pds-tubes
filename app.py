import sys
sys.dont_write_bytecode = True
import streamlit as st
from menu import dashboard,barchart,gis_polygon



st.set_page_config(layout="wide", page_title="LakaLantas Indonesia")

# ================= CSS =================
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<style>

body{background:#f4f6fb;}

[data-testid="stSidebar"]{
background:#0b3c5d;
min-width:240px;
max-width:240px;
box-shadow:4px 0 12px rgba(0,0,0,.2);
}

.sidebar-title{
color:white;
font-size:20px;
font-weight:700;
padding:20px;
border-bottom:1px solid #1f2937;
}

.menu-btn{
display:flex;
align-items:center;
gap:12px;
padding:12px 18px;
margin:6px 12px;
border-radius:10px;
font-size:14px;
cursor:pointer;
color:#cbd5f5;
transition:.2s;
}

.menu-btn i{
width:20px;
text-align:center;
}

.menu-btn:hover{
background:#145a8d;
color:white;
transform:translateX(4px);
}


.active{
background:#1976d2;
color:white;
box-shadow:0 6px 18px rgba(25,118,210,.35);
}

.topbar{
background:white;
padding:14px 22px;
border-radius:14px;
margin-bottom:25px;
display:flex;
justify-content:space-between;
align-items:center;
box-shadow:0 4px 15px rgba(0,0,0,.06);
}

.profile{
background:#2563eb;
color:white;
padding:6px 16px;
border-radius:20px;
font-size:13px;
}

.card{
background:white;
padding:20px;
border-radius:18px;
box-shadow:0 6px 20px rgba(0,0,0,.06);
}
.sidebar-title img{
border-radius:6px;
}


</style>
""", unsafe_allow_html=True)

# ================= STATE =================
if "page" not in st.session_state:
    st.session_state.page="dashboard"

# ================= SIDEBAR =================
st.sidebar.markdown(""" <div class="sidebar-title"> 🚓</i> Lakalantas Indonesia </div> """, unsafe_allow_html=True)

def nav(label, icon, key):
    active="active" if st.session_state.page==key else ""
    if st.sidebar.button(label, use_container_width=True):
        st.session_state.page=key

nav("🏠 Dashboard","fa-home","dashboard")
nav("📊 Analytics","fa-chart","analytics")
nav("🗺️ Gigs","fa-briefcase","gigs")

# ================= ROUTER =================
if st.session_state.page=="dashboard":
    dashboard.app()

elif st.session_state.page=="analytics":
    barchart.app()

else:
    gis_polygon.app()

