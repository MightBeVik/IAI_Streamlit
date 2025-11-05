import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Set page configuration
st.set_page_config(
    page_title="🖥️ THYROID-OS v2.1 | Medical Computer System",
    page_icon="�️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced retro computer styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=VT323&display=swap');
    
    .stApp {
        background: linear-gradient(45deg, #000000 0%, #0a0a0a 25%, #1a1a2e 50%, #16213e 75%, #0f3460 100%);
        font-family: 'VT323', monospace;
        background-attachment: fixed;
    }
    
    /* Scanlines effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 255, 65, 0.03) 0px,
            rgba(0, 255, 65, 0.03) 1px,
            transparent 1px,
            transparent 2px
        );
        pointer-events: none;
        z-index: 1000;
    }
    
    .main-header {
        font-size: 3rem;
        color: #00ff41;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41;
        font-family: 'VT323', monospace;
        font-weight: bold;
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        padding: 2rem;
        border: 3px solid #00ff41;
        border-radius: 15px;
        box-shadow: 
            0 0 30px rgba(0, 255, 65, 0.4),
            inset 0 0 20px rgba(0, 255, 65, 0.1);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(0, 255, 65, 0.3); }
        to { box-shadow: 0 0 40px rgba(0, 255, 65, 0.6); }
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    .blinking-cursor::after {
        content: '█';
        animation: blink 1s infinite;
        color: #00ff41;
    }
    
    .section-header {
        font-size: 2.2rem;
        color: #ff6b35;
        margin-top: 2rem;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px #ff6b35, 0 0 15px #ff6b35;
        font-family: 'VT323', monospace;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    .retro-terminal {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 100%);
        color: #00ff41;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #00ff41;
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
        box-shadow: 
            0 0 25px rgba(0, 255, 65, 0.3),
            inset 0 0 15px rgba(0, 255, 65, 0.05);
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .retro-terminal::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff41, transparent);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .diagnostic-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border: 2px solid #ff6b35;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 
            0 0 20px rgba(255, 107, 53, 0.3),
            inset 0 0 10px rgba(255, 107, 53, 0.05);
        font-family: 'VT323', monospace;
        font-size: 1.1rem;
        position: relative;
    }
    
    .diagnostic-box::after {
        content: '';
        position: absolute;
        top: 5px;
        right: 5px;
        width: 8px;
        height: 8px;
        background: #ff6b35;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .computer-screen {
        background: radial-gradient(ellipse at center, #001100 0%, #000000 100%);
        border: 4px solid #333;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 0 50px rgba(0, 255, 65, 0.2),
            inset 0 0 30px rgba(0, 0, 0, 0.8);
        position: relative;
    }
    
    .ascii-art {
        font-family: 'Courier Prime', monospace;
        color: #00ff41;
        font-size: 0.7rem;
        line-height: 1;
        text-shadow: 0 0 5px #00ff41;
        white-space: pre;
        text-align: center;
        margin: 1rem 0;
    }
    
    .status-led {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1.5s infinite;
    }
    
    .led-green { background: #00ff41; box-shadow: 0 0 10px #00ff41; }
    .led-orange { background: #ff6b35; box-shadow: 0 0 10px #ff6b35; }
    .led-red { background: #ff4444; box-shadow: 0 0 10px #ff4444; }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #000 0%, #1a1a2e 50%, #000 100%);
        border-right: 2px solid #00ff41;
    }
    
    .stSelectbox > div > div {
        background-color: #000;
        color: #00ff41;
        border: 2px solid #00ff41;
        font-family: 'VT323', monospace;
        font-size: 1.1rem;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff6b35 0%, #f7931e 50%, #ff6b35 100%);
        color: #000;
        border: 2px solid #ff6b35;
        border-radius: 10px;
        font-family: 'VT323', monospace;
        font-weight: bold;
        font-size: 1.2rem;
        box-shadow: 0 0 15px rgba(255, 107, 53, 0.4);
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(255, 107, 53, 0.6);
        transform: translateY(-2px);
    }
    
    .system-boot {
        background: #000;
        color: #00ff41;
        padding: 1rem;
        border: 1px solid #00ff41;
        border-radius: 5px;
        font-family: 'Courier Prime', monospace;
        font-size: 0.9rem;
        margin: 1rem 0;
    }
    
    .progress-bar-retro {
        background: #333;
        height: 25px;
        border-radius: 12px;
        border: 2px solid #00ff41;
        overflow: hidden;
        position: relative;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff41, #00aa2e, #00ff41);
        border-radius: 10px;
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shine 2s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .matrix-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        opacity: 0.05;
    }
    
    .dataframe {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid #00ff41 !important;
        border-radius: 5px !important;
    }
    
    .dataframe th {
        background: #1a1a2e !important;
        color: #ff6b35 !important;
        border: 1px solid #ff6b35 !important;
    }
    
    .dataframe td {
        background: rgba(0, 0, 0, 0.6) !important;
        color: #00ff41 !important;
        border: 1px solid #333 !important;
    }
</style>
""", unsafe_allow_html=True)

def generate_thyroid_data():
    """Generate sample thyroid patient data for demonstrations"""
    np.random.seed(42)
    n_samples = 500
    
    # Generate realistic thyroid data
    data = {
        'PatientID': [f'THY-{i:04d}' for i in range(1, n_samples + 1)],
        'Age': np.random.normal(45, 15, n_samples).astype(int).clip(18, 80),
        'TSH': np.random.lognormal(0.5, 0.8, n_samples).clip(0.1, 50),
        'T3': np.random.normal(1.8, 0.4, n_samples).clip(0.5, 4.0),
        'T4': np.random.normal(9.5, 2.0, n_samples).clip(4.0, 18.0),
        'T4U': np.random.normal(1.0, 0.15, n_samples).clip(0.6, 1.5),
        'FTI': np.random.normal(9.5, 2.2, n_samples).clip(4.0, 18.0),
        'Gender': np.random.choice(['Male', 'Female'], n_samples, p=[0.3, 0.7]),
        'Goitre': np.random.choice(['Yes', 'No'], n_samples, p=[0.2, 0.8]),
        'Tumor': np.random.choice(['Yes', 'No'], n_samples, p=[0.1, 0.9]),
        'Hypopituitary': np.random.choice(['Yes', 'No'], n_samples, p=[0.05, 0.95]),
        'Psych': np.random.choice(['Yes', 'No'], n_samples, p=[0.15, 0.85]),
    }
    
    # Generate diagnosis based on TSH levels (simplified)
    diagnosis = []
    for tsh in data['TSH']:
        if tsh < 0.4:
            diagnosis.append('Hyperthyroid')
        elif tsh > 4.0:
            diagnosis.append('Hypothyroid')
        else:
            diagnosis.append('Normal')
    
    data['Diagnosis'] = diagnosis
    data['Risk_Level'] = np.random.choice(['Low', 'Medium', 'High'], n_samples, p=[0.6, 0.3, 0.1])
    
    return pd.DataFrame(data)

def main():
    # Main title with retro computer styling
    st.markdown('''
    <div class="main-header">
        �️ THYROID-OS v2.1<br>
        <small style="font-size: 0.6em; color: #ff6b35;">Medical Diagnostic Computer System</small><br>
        <small style="font-size: 0.4em; color: #888;">© 1985 MedTech Industries</small>
    </div>
    ''', unsafe_allow_html=True)
    
    # Terminal-style welcome message
    st.markdown('''
    <div class="retro-terminal">
        > SYSTEM BOOTED SUCCESSFULLY<br>
        > LOADING THYROID DIAGNOSTIC MODULE...<br>
        > STATUS: ONLINE<br>
        > USER ACCESS LEVEL: PHYSICIAN<br>
        > TYPE 'HELP' FOR COMMAND LIST
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar navigation with retro styling
    st.sidebar.markdown('''
    <div style="color: #00ff41; font-family: 'Courier Prime', monospace; font-weight: bold; text-align: center; padding: 1rem; background: #000; border: 1px solid #00ff41; border-radius: 5px;">
        🖥️ NAVIGATION MENU
    </div>
    ''', unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "Select Module:",
        ["🏠 Main Terminal", "📊 Patient Database", "🧪 Lab Results", "📈 Diagnostic Charts", "📁 Data Import", "📝 Patient Entry"]
    )
    
    if page == "🏠 Main Terminal":
        show_home()
    elif page == "📊 Patient Database":
        show_data_analysis()
    elif page == "🧪 Lab Results":
        show_widgets()
    elif page == "📈 Diagnostic Charts":
        show_charts()
    elif page == "📁 Data Import":
        show_file_upload()
    elif page == "📝 Patient Entry":
        show_form_demo()

def show_home():
    # ASCII Art Header for home
    st.markdown('''
    <div class="ascii-art">
████████╗██╗  ██╗██╗   ██╗██████╗  ██████╗ ██╗██████╗       ██████╗ ███████╗
╚══██╔══╝██║  ██║╚██╗ ██╔╝██╔══██╗██╔═══██╗██║██╔══██╗     ██╔═══██╗██╔════╝
   ██║   ███████║ ╚████╔╝ ██████╔╝██║   ██║██║██║  ██║     ██║   ██║███████╗
   ██║   ██╔══██║  ╚██╔╝  ██╔══██╗██║   ██║██║██║  ██║     ██║   ██║╚════██║
   ██║   ██║  ██║   ██║   ██║  ██║╚██████╔╝██║██████╔╝     ╚██████╔╝███████║
   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝       ╚═════╝ ╚══════╝
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🖥️ THYROID DIAGNOSTIC SYSTEM - MAIN TERMINAL</h2>', unsafe_allow_html=True)
    
    # Enhanced terminal boot sequence
    st.markdown('''
    <div class="retro-terminal">
        <div style="color: #ff6b35; font-size: 1.2rem;">THYROID-OS BOOT SEQUENCE v2.1.4</div>
        <div style="color: #00ff41;">════════════════════════════════════════════════</div>
        <span class="status-led led-green"></span>SYSTEM INITIALIZATION: COMPLETE<br>
        <span class="status-led led-green"></span>MEMORY TEST: 640KB OK, EXTENDED MEMORY: 15MB OK<br>
        <span class="status-led led-green"></span>THYROID DATABASE: MOUNTED [/dev/thyroid0]<br>
        <span class="status-led led-green"></span>HORMONE ANALYZER: CALIBRATED AND READY<br>
        <span class="status-led led-orange"></span>LAB INTERFACE: ESTABLISHING CONNECTION... OK<br>
        <span class="status-led led-green"></span>DIAGNOSTIC AI: NEURAL NETWORK LOADED<br>
        <span class="status-led led-green"></span>SECURITY: PHYSICIAN ACCESS VERIFIED<br>
        <span class="status-led led-green"></span>BACKUP SYSTEMS: ONLINE<br>
        <div style="color: #ff6b35;">════════════════════════════════════════════════</div>
        <div style="color: #00ff41; font-size: 1.1rem;">SYSTEM STATUS: OPERATIONAL</div>
        <div style="color: #888; font-size: 0.9rem; margin-top: 5px;">Last boot: NOV-05-1985 08:45:23 | Uptime: 127:45:23</div>
        <div class="blinking-cursor" style="margin-top: 10px;">AWAITING PHYSICIAN COMMANDS</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Enhanced diagnostic metrics with computer terminal styling
    st.markdown('''
    <div class="computer-screen">
        <div style="color: #ff6b35; font-family: 'VT323', monospace; font-size: 1.4rem; text-align: center; margin-bottom: 1rem;">
            📊 REAL-TIME DIAGNOSTIC METRICS 📊
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold; text-align: center; font-size: 1.1rem;">PATIENT DATABASE</div>
            <div style="color: #ff6b35; font-size: 2.5rem; text-align: center; font-family: 'VT323', monospace;">1,247</div>
            <div style="color: #888; text-align: center;">TOTAL RECORDS</div>
            <div style="color: #00ff41; text-align: center; font-size: 0.9rem;">↗ +23 THIS MONTH</div>
            <div class="progress-bar-retro" style="margin-top: 10px;">
                <div class="progress-fill" style="width: 89%;"></div>
            </div>
            <div style="color: #888; text-align: center; font-size: 0.8rem; margin-top: 5px;">DATABASE: 89% CAPACITY</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold; text-align: center; font-size: 1.1rem;">DIAGNOSTIC ACCURACY</div>
            <div style="color: #ff6b35; font-size: 2.5rem; text-align: center; font-family: 'VT323', monospace;">94.8%</div>
            <div style="color: #888; text-align: center;">AI MODEL PERFORMANCE</div>
            <div style="color: #00ff41; text-align: center; font-size: 0.9rem;">↗ +1.2% IMPROVED</div>
            <div class="progress-bar-retro" style="margin-top: 10px;">
                <div class="progress-fill" style="width: 95%;"></div>
            </div>
            <div style="color: #888; text-align: center; font-size: 0.8rem; margin-top: 5px;">CONFIDENCE: OPTIMAL</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold; text-align: center; font-size: 1.1rem;">PENDING ANALYSIS</div>
            <div style="color: #ff6b35; font-size: 2.5rem; text-align: center; font-family: 'VT323', monospace;">42</div>
            <div style="color: #888; text-align: center;">LAB RESULTS QUEUE</div>
            <div style="color: #ff6b35; text-align: center; font-size: 0.9rem;">⚠ PRIORITY ATTENTION</div>
            <div class="progress-bar-retro" style="margin-top: 10px;">
                <div class="progress-fill" style="width: 68%; background: linear-gradient(90deg, #ff6b35, #f7931e);"></div>
            </div>
            <div style="color: #888; text-align: center; font-size: 0.8rem; margin-top: 5px;">PROCESSING: 68%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced system information with more retro computer styling
    st.markdown('''
    <div class="retro-terminal">
        <div style="text-align: center; margin-bottom: 15px;">
            <div style="color: #ff6b35; font-size: 1.4rem; font-family: 'VT323', monospace;">🔬 THYROID DIAGNOSTIC CAPABILITIES 🔬</div>
        </div>
        <div style="color: #00ff41;">
        ╔════════════════════════════════════════════════════════════════╗<br>
        ║  MODULE NAME           │  STATUS    │  VERSION  │  ACCURACY    ║<br>
        ╠════════════════════════════════════════════════════════════════╣<br>
        ║  HYPERTHYROID.EXE      │  <span style="color: #00ff41;">ONLINE</span>    │  v3.2.1   │  96.2%       ║<br>
        ║  HYPOTHYROID.EXE       │  <span style="color: #00ff41;">ONLINE</span>    │  v3.1.8   │  94.7%       ║<br>
        ║  RISK_ASSESS.EXE       │  <span style="color: #00ff41;">ONLINE</span>    │  v2.9.4   │  92.1%       ║<br>
        ║  HORMONE_TRACK.EXE     │  <span style="color: #00ff41;">ONLINE</span>    │  v4.0.2   │  98.9%       ║<br>
        ║  DATA_EXPORT.EXE       │  <span style="color: #00ff41;">ONLINE</span>    │  v1.5.7   │  99.8%       ║<br>
        ║  NEURAL_NET.AI         │  <span style="color: #ff6b35;">LEARNING</span> │  v5.2.1   │  94.8%       ║<br>
        ╚════════════════════════════════════════════════════════════════╝
        </div>
        <br>
        <div style="color: #888; font-size: 0.9rem; text-align: center;">
            All modules initialized successfully | Memory usage: 547KB/640KB
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Advanced system status with ASCII graphics
    st.markdown('''
    <div class="computer-screen">
        <div style="color: #ff6b35; font-family: 'VT323', monospace; font-size: 1.3rem; text-align: center; margin-bottom: 1rem;">
            ⚡ ADVANCED SYSTEM MONITORING ⚡
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # System status indicators
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold;">LAB CONNECTIVITY</div>
            <div class="progress-bar" style="background: #333; height: 20px; border-radius: 10px; margin: 10px 0;">
                <div style="background: linear-gradient(90deg, #00ff41, #00aa2e); width: 98%; height: 100%; border-radius: 10px;"></div>
            </div>
            <div style="color: #00ff41;">98% - EXCELLENT</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold;">MODEL ACCURACY</div>
            <div class="progress-bar" style="background: #333; height: 20px; border-radius: 10px; margin: 10px 0;">
                <div style="background: linear-gradient(90deg, #ff6b35, #f7931e); width: 94%; height: 100%; border-radius: 10px;"></div>
            </div>
            <div style="color: #ff6b35;">94% - OPTIMAL</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold;">DATABASE STATUS</div>
            <div class="progress-bar" style="background: #333; height: 20px; border-radius: 10px; margin: 10px 0;">
                <div style="background: linear-gradient(90deg, #00ff41, #00aa2e); width: 100%; height: 100%; border-radius: 10px;"></div>
            </div>
            <div style="color: #00ff41;">100% - ONLINE</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold;">SYSTEM UPTIME</div>
            <div class="progress-bar" style="background: #333; height: 20px; border-radius: 10px; margin: 10px 0;">
                <div style="background: linear-gradient(90deg, #00ff41, #00aa2e); width: 99%; height: 100%; border-radius: 10px;"></div>
            </div>
            <div style="color: #00ff41;">99.7% - STABLE</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Recent alerts with enhanced styling and ASCII art
    st.markdown('''
    <div class="retro-terminal">
        <div style="text-align: center; margin-bottom: 15px;">
            <div style="color: #ff6b35; font-size: 1.3rem; font-family: 'VT323', monospace;">⚠ RECENT SYSTEM ALERTS ⚠</div>
        </div>
        <div style="color: #00ff41; font-family: 'Courier Prime', monospace;">
        ┌─────────────────────────────────────────────────────────────────┐<br>
        │ TIME     │ PRIORITY │ MESSAGE                                   │<br>
        ├─────────────────────────────────────────────────────────────────┤<br>
        │ 11:45:23 │ <span style="color: #ff4444;">HIGH</span>     │ TSH LEVEL CRITICAL - Patient THY-0847      │<br>
        │ 11:42:15 │ <span style="color: #00ff41;">INFO</span>     │ Lab batch #2847 uploaded - 15 patients     │<br>
        │ 11:38:09 │ <span style="color: #ff6b35;">MEDIUM</span>   │ AI model retrained - Accuracy: 94.8%       │<br>
        │ 11:35:44 │ <span style="color: #00ff41;">INFO</span>     │ Backup completed - 1.2GB archived          │<br>
        │ 11:30:12 │ <span style="color: #00ff41;">INFO</span>     │ System scan complete - No anomalies        │<br>
        │ 11:28:07 │ <span style="color: #ff6b35;">MEDIUM</span>   │ Database optimization running...            │<br>
        │ 11:25:33 │ <span style="color: #ff4444;">HIGH</span>     │ Abnormal T4 detected - Patient THY-0923    │<br>
        └─────────────────────────────────────────────────────────────────┘
        </div>
        <div style="color: #888; font-size: 0.9rem; text-align: center; margin-top: 10px;">
            Alert buffer: 47/100 | Auto-refresh: ENABLED | Sound alerts: OFF
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # ASCII art footer with system info
    st.markdown('''
    <div class="ascii-art" style="margin-top: 20px; font-size: 0.7rem; color: #00ff41;">
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                              THYROID-OS v2.1.4                              ║
    ║                          Medical Diagnostic System                           ║
    ║                                                                              ║
    ║  CPU: Intel 8086 @ 4.77MHz    │  RAM: 640KB + 15MB Extended                ║
    ║  GPU: CGA Graphics Adapter     │  Storage: 40MB Hard Drive                  ║
    ║  Network: Lab Interface v3.2   │  AI Core: Neural Net v5.2.1               ║
    ║                                                                              ║
    ║  Licensed to: Regional Medical Center    │  License: PERPETUAL              ║
    ║  Serial: THY-2185-MED-DIAG-4077         │  Support: 24/7 AVAILABLE         ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    </div>
    ''', unsafe_allow_html=True)

def show_data_analysis():
    st.markdown('<h2 class="section-header">📊 PATIENT DATABASE - THYROID ANALYSIS</h2>', unsafe_allow_html=True)
    
    # Generate thyroid data
    df = generate_thyroid_data()
    
    st.markdown('''
    <div class="retro-terminal">
        > ACCESSING PATIENT DATABASE...<br>
        > LOADING THYROID RECORDS...<br>
        > DATABASE CONNECTION: ESTABLISHED<br>
        > RECORDS LOADED: 500 PATIENTS
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar filters with retro styling
    st.sidebar.markdown('''
    <div style="color: #ff6b35; font-family: 'Courier Prime', monospace; font-weight: bold; text-align: center; padding: 0.5rem; background: #000; border: 1px solid #ff6b35; border-radius: 5px; margin-bottom: 1rem;">
        🔬 DIAGNOSTIC FILTERS
    </div>
    ''', unsafe_allow_html=True)
    
    # Age range filter
    age_range = st.sidebar.slider(
        "Age Range",
        min_value=int(df['Age'].min()),
        max_value=int(df['Age'].max()),
        value=(int(df['Age'].min()), int(df['Age'].max()))
    )
    
    # Gender filter
    genders = st.sidebar.multiselect(
        "Gender",
        options=df['Gender'].unique(),
        default=df['Gender'].unique()
    )
    
    # Diagnosis filter
    diagnoses = st.sidebar.multiselect(
        "Diagnosis",
        options=df['Diagnosis'].unique(),
        default=df['Diagnosis'].unique()
    )
    
    # Risk level filter
    risk_levels = st.sidebar.multiselect(
        "Risk Level",
        options=df['Risk_Level'].unique(),
        default=df['Risk_Level'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['Age'] >= age_range[0]) & 
        (df['Age'] <= age_range[1]) &
        (df['Gender'].isin(genders)) &
        (df['Diagnosis'].isin(diagnoses)) &
        (df['Risk_Level'].isin(risk_levels))
    ]
    
    # Display metrics in retro style
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold; text-align: center;">TOTAL PATIENTS</div>
            <div style="color: #ff6b35; font-size: 1.5rem; text-align: center;">{len(filtered_df)}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        avg_tsh = filtered_df['TSH'].mean()
        st.markdown(f'''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold; text-align: center;">AVG TSH</div>
            <div style="color: #ff6b35; font-size: 1.5rem; text-align: center;">{avg_tsh:.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        abnormal_count = len(filtered_df[filtered_df['Diagnosis'] != 'Normal'])
        st.markdown(f'''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold; text-align: center;">ABNORMAL CASES</div>
            <div style="color: #ff6b35; font-size: 1.5rem; text-align: center;">{abnormal_count}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        high_risk = len(filtered_df[filtered_df['Risk_Level'] == 'High'])
        st.markdown(f'''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold; text-align: center;">HIGH RISK</div>
            <div style="color: #ff6b35; font-size: 1.5rem; text-align: center;">{high_risk}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Data table with styling
    st.markdown('<h3 style="color: #00ff41; font-family: \'Courier Prime\', monospace;">📋 FILTERED PATIENT RECORDS</h3>', unsafe_allow_html=True)
    
    # Configure the dataframe display
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )
    
    # Download button with retro styling
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="💾 DOWNLOAD PATIENT DATA",
        data=csv,
        file_name=f"thyroid_patients_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def show_widgets():
    st.markdown('<h2 class="section-header">🧪 LAB RESULTS - MANUAL ENTRY SYSTEM</h2>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="retro-terminal">
        > INITIALIZING LAB RESULT ENTRY MODULE...<br>
        > HORMONE LEVEL ANALYZERS ONLINE<br>
        > AWAITING PHYSICIAN INPUT...
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">📝 PATIENT INFORMATION</h3>', unsafe_allow_html=True)
        
        # Patient info inputs
        patient_id = st.text_input("Patient ID", "THY-0001", help="Format: THY-XXXX")
        patient_age = st.number_input("Patient Age", min_value=1, max_value=120, value=45)
        patient_gender = st.selectbox("Gender", ["Female", "Male"])
        
        st.markdown('<h3 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">🔬 HORMONE LEVELS</h3>', unsafe_allow_html=True)
        
        # Hormone level inputs
        tsh_level = st.slider("TSH Level (mIU/L)", 0.1, 20.0, 2.5, 0.1)
        t3_level = st.slider("T3 Level (ng/dL)", 0.5, 4.0, 1.8, 0.1)
        t4_level = st.slider("T4 Level (μg/dL)", 4.0, 18.0, 9.5, 0.1)
        t4u_level = st.slider("T4U Uptake", 0.6, 1.5, 1.0, 0.01)
        fti_level = st.slider("FTI", 4.0, 18.0, 9.5, 0.1)
        
        st.markdown('<h3 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">⚕️ CLINICAL HISTORY</h3>', unsafe_allow_html=True)
        
        # Clinical history
        goitre = st.radio("Goitre Present?", ["No", "Yes"])
        tumor = st.radio("Tumor History?", ["No", "Yes"])
        hypopituitary = st.radio("Hypopituitary?", ["No", "Yes"])
        psych = st.radio("Psychological Symptoms?", ["No", "Yes"])
        
    with col2:
        st.markdown('<h3 style="color: #00ff41; font-family: \'Courier Prime\', monospace;">🖥️ DIAGNOSTIC ANALYSIS</h3>', unsafe_allow_html=True)
        
        # Real-time diagnosis based on TSH levels
        if tsh_level < 0.4:
            diagnosis = "HYPERTHYROID"
            color = "#ff4444"
            status = "⚠ ABNORMAL"
        elif tsh_level > 4.0:
            diagnosis = "HYPOTHYROID"
            color = "#ff6b35"
            status = "⚠ ABNORMAL"
        else:
            diagnosis = "NORMAL RANGE"
            color = "#00ff41"
            status = "✓ NORMAL"
        
        st.markdown(f'''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold; text-align: center;">PRELIMINARY DIAGNOSIS</div>
            <div style="color: {color}; font-size: 1.5rem; text-align: center; font-weight: bold;">{diagnosis}</div>
            <div style="color: {color}; text-align: center;">{status}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Risk assessment
        risk_factors = 0
        if tsh_level < 0.4 or tsh_level > 4.0:
            risk_factors += 2
        if goitre == "Yes":
            risk_factors += 1
        if tumor == "Yes":
            risk_factors += 2
        if patient_age > 60:
            risk_factors += 1
        if psych == "Yes":
            risk_factors += 1
        
        if risk_factors >= 4:
            risk_level = "HIGH"
            risk_color = "#ff4444"
        elif risk_factors >= 2:
            risk_level = "MEDIUM"
            risk_color = "#ff6b35"
        else:
            risk_level = "LOW"
            risk_color = "#00ff41"
        
        st.markdown(f'''
        <div class="diagnostic-box">
            <div style="color: #00ff41; font-weight: bold; text-align: center;">RISK ASSESSMENT</div>
            <div style="color: {risk_color}; font-size: 1.5rem; text-align: center; font-weight: bold;">{risk_level} RISK</div>
            <div style="color: {risk_color}; text-align: center;">Risk Factors: {risk_factors}/7</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Detailed results
        st.markdown('<h4 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">📊 LAB VALUES SUMMARY</h4>', unsafe_allow_html=True)
        
        results_data = {
            'Test': ['TSH', 'T3', 'T4', 'T4U', 'FTI'],
            'Value': [f"{tsh_level:.2f}", f"{t3_level:.2f}", f"{t4_level:.2f}", f"{t4u_level:.2f}", f"{fti_level:.2f}"],
            'Unit': ['mIU/L', 'ng/dL', 'μg/dL', 'ratio', 'index'],
            'Reference': ['0.4-4.0', '0.8-2.8', '4.5-12.0', '0.8-1.2', '4.5-12.0']
        }
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        # Recommendations
        st.markdown('''
        <div class="retro-terminal">
            <h4 style="color: #ff6b35;">💡 SYSTEM RECOMMENDATIONS:</h4>
            <br>
        ''', unsafe_allow_html=True)
        
        if diagnosis == "HYPERTHYROID":
            st.markdown('• Recommend endocrinology referral<br>• Consider anti-thyroid medication<br>• Monitor cardiovascular function<br>', unsafe_allow_html=True)
        elif diagnosis == "HYPOTHYROID":
            st.markdown('• Consider thyroid hormone replacement<br>• Recheck levels in 6-8 weeks<br>• Monitor for hypothyroid symptoms<br>', unsafe_allow_html=True)
        else:
            st.markdown('• Continue routine monitoring<br>• Annual thyroid screening<br>• Maintain healthy lifestyle<br>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_charts():
    st.markdown('<h2 class="section-header">📈 DIAGNOSTIC CHARTS - THYROID DATA VISUALIZATION</h2>', unsafe_allow_html=True)
    
    df = generate_thyroid_data()
    
    st.markdown('''
    <div class="retro-terminal">
        > LOADING VISUALIZATION MODULE...<br>
        > PLOTTING THYROID HORMONE DISTRIBUTIONS...<br>
        > GENERATING DIAGNOSTIC CORRELATIONS...<br>
        > GRAPHICS SUBSYSTEM: READY
    </div>
    ''', unsafe_allow_html=True)
    
    # Chart type selector with retro styling
    chart_type = st.selectbox(
        "📊 Select Visualization Type:",
        ["TSH Distribution", "Hormone Correlation", "Diagnosis by Age", "Gender Analysis", "Risk Factor Matrix", "3D Hormone Plot"]
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown('<h4 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">⚙️ CHART OPTIONS</h4>', unsafe_allow_html=True)
        
        if chart_type in ["TSH Distribution"]:
            bins = st.slider("Histogram Bins", 10, 50, 25)
            show_normal_range = st.checkbox("Show Normal Range", True)
        elif chart_type == "Diagnosis by Age":
            age_groups = st.checkbox("Group by Age Ranges", True)
        elif chart_type == "Hormone Correlation":
            correlation_method = st.selectbox("Correlation Method", ["pearson", "spearman"])
    
    with col1:
        if chart_type == "TSH Distribution":
            fig = go.Figure()
            
            # Create histogram
            fig.add_trace(go.Histogram(
                x=df['TSH'],
                nbinsx=bins,
                name='TSH Distribution',
                marker_color='rgba(0, 255, 65, 0.7)',
                marker_line=dict(color='#00ff41', width=2)
            ))
            
            # Add normal range indicators
            if show_normal_range:
                fig.add_vline(x=0.4, line_dash="dash", line_color="#ff6b35", 
                             annotation_text="Normal Min (0.4)")
                fig.add_vline(x=4.0, line_dash="dash", line_color="#ff6b35", 
                             annotation_text="Normal Max (4.0)")
            
            fig.update_layout(
                title="TSH Level Distribution in Patient Population",
                xaxis_title="TSH Level (mIU/L)",
                yaxis_title="Number of Patients",
                plot_bgcolor='black',
                paper_bgcolor='black',
                font_color='#00ff41',
                title_font_color='#ff6b35'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Hormone Correlation":
            # Create correlation matrix
            corr_data = df[['TSH', 'T3', 'T4', 'T4U', 'FTI', 'Age']].corr(method=correlation_method)
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_data.values,
                x=corr_data.columns,
                y=corr_data.columns,
                colorscale='RdYlGn',
                text=corr_data.values.round(2),
                texttemplate="%{text}",
                textfont={"size":12},
                colorbar=dict(title="Correlation")
            ))
            
            fig.update_layout(
                title="Thyroid Hormone Correlation Matrix",
                plot_bgcolor='black',
                paper_bgcolor='black',
                font_color='#00ff41',
                title_font_color='#ff6b35'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Diagnosis by Age":
            if age_groups:
                # Create age groups
                df_copy = df.copy()
                df_copy['Age_Group'] = pd.cut(df_copy['Age'], 
                                            bins=[0, 30, 45, 60, 100], 
                                            labels=['18-30', '31-45', '46-60', '60+'])
                
                fig = px.histogram(df_copy, x='Age_Group', color='Diagnosis',
                                 title="Thyroid Diagnosis Distribution by Age Group",
                                 color_discrete_map={
                                     'Normal': '#00ff41',
                                     'Hyperthyroid': '#ff6b35',
                                     'Hypothyroid': '#ff4444'
                                 })
            else:
                fig = px.scatter(df, x='Age', y='TSH', color='Diagnosis',
                               title="TSH Levels vs Age by Diagnosis",
                               color_discrete_map={
                                   'Normal': '#00ff41',
                                   'Hyperthyroid': '#ff6b35',
                                   'Hypothyroid': '#ff4444'
                               })
            
            fig.update_layout(
                plot_bgcolor='black',
                paper_bgcolor='black',
                font_color='#00ff41',
                title_font_color='#ff6b35'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Gender Analysis":
            # Gender distribution by diagnosis
            gender_diag = df.groupby(['Gender', 'Diagnosis']).size().reset_index(name='Count')
            
            fig = px.bar(gender_diag, x='Gender', y='Count', color='Diagnosis',
                        title="Thyroid Conditions by Gender",
                        color_discrete_map={
                            'Normal': '#00ff41',
                            'Hyperthyroid': '#ff6b35',
                            'Hypothyroid': '#ff4444'
                        })
            
            fig.update_layout(
                plot_bgcolor='black',
                paper_bgcolor='black',
                font_color='#00ff41',
                title_font_color='#ff6b35'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Risk Factor Matrix":
            # Risk factors analysis
            risk_data = df.groupby(['Risk_Level', 'Diagnosis']).size().reset_index(name='Count')
            
            fig = px.sunburst(risk_data, path=['Risk_Level', 'Diagnosis'], values='Count',
                            title="Risk Level and Diagnosis Distribution",
                            color_discrete_map={
                                'Low': '#00ff41',
                                'Medium': '#ff6b35',
                                'High': '#ff4444'
                            })
            
            fig.update_layout(
                plot_bgcolor='black',
                paper_bgcolor='black',
                font_color='#00ff41',
                title_font_color='#ff6b35'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "3D Hormone Plot":
            # 3D scatter plot of hormone levels
            fig = go.Figure(data=[go.Scatter3d(
                x=df['TSH'],
                y=df['T3'],
                z=df['T4'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df['Age'],
                    colorscale='Viridis',
                    opacity=0.8,
                    colorbar=dict(title="Age")
                ),
                text=df['Diagnosis'],
                hovertemplate='<b>TSH:</b> %{x:.2f}<br><b>T3:</b> %{y:.2f}<br><b>T4:</b> %{z:.2f}<br><b>Diagnosis:</b> %{text}<extra></extra>'
            )])
            
            fig.update_layout(
                title="3D Hormone Level Visualization",
                scene=dict(
                    xaxis_title='TSH (mIU/L)',
                    yaxis_title='T3 (ng/dL)',
                    zaxis_title='T4 (μg/dL)',
                    bgcolor='black'
                ),
                plot_bgcolor='black',
                paper_bgcolor='black',
                font_color='#00ff41',
                title_font_color='#ff6b35'
            )
            
            st.plotly_chart(fig, use_container_width=True)

def show_file_upload():
    st.markdown('<h2 class="section-header">📁 DATA IMPORT - THYROID LAB RESULTS</h2>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="retro-terminal">
        > THYROID DATA IMPORT SYSTEM v2.1<br>
        > SUPPORTED FORMATS: CSV, TSV<br>
        > MAXIMUM FILE SIZE: 100MB<br>
        > AWAITING FILE UPLOAD...
    </div>
    ''', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "🔬 Upload Thyroid Lab Results (CSV format)",
        type="csv",
        help="Upload a CSV file containing thyroid hormone test results"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.markdown('''
            <div class="diagnostic-box">
                <div style="color: #00ff41; font-weight: bold; text-align: center;">✓ FILE UPLOAD SUCCESSFUL</div>
                <div style="color: #ff6b35; text-align: center;">Processing thyroid data...</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Show basic info in retro style
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'''
                <div class="diagnostic-box">
                    <div style="color: #00ff41; font-weight: bold;">📊 DATASET INFORMATION</div>
                    <div style="color: #ff6b35;">Patients: {df.shape[0]}</div>
                    <div style="color: #ff6b35;">Data Fields: {df.shape[1]}</div>
                    <div style="color: #ff6b35;">Memory: {df.memory_usage(deep=True).sum() / 1024:.2f} KB</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<h4 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">🔍 COLUMN ANALYSIS</h4>', unsafe_allow_html=True)
                column_types = df.dtypes.to_frame('Data Type').reset_index()
                column_types.columns = ['Column', 'Type']
                st.dataframe(column_types, use_container_width=True, hide_index=True)
            
            # Data preview with retro styling
            st.markdown('<h3 style="color: #00ff41; font-family: \'Courier Prime\', monospace;">📋 DATA PREVIEW</h3>', unsafe_allow_html=True)
            st.dataframe(df.head(10), use_container_width=True)
            
            # Thyroid-specific analysis if appropriate columns exist
            thyroid_columns = ['TSH', 'T3', 'T4', 'T4U', 'FTI']
            found_columns = [col for col in thyroid_columns if col in df.columns]
            
            if found_columns:
                st.markdown('''
                <div class="retro-terminal">
                    <h3 style="color: #ff6b35;">🔬 THYROID HORMONE ANALYSIS DETECTED</h3>
                    <br>Found hormone data columns: ''' + ', '.join(found_columns) + '''<br>
                </div>
                ''', unsafe_allow_html=True)
                
                # Statistical summary for hormone data
                if st.checkbox("📊 Show Hormone Statistics", value=True):
                    st.markdown('<h4 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">📈 HORMONE LEVEL STATISTICS</h4>', unsafe_allow_html=True)
                    hormone_stats = df[found_columns].describe()
                    st.dataframe(hormone_stats, use_container_width=True)
                    
                    # Check for abnormal values
                    abnormal_count = 0
                    if 'TSH' in df.columns:
                        abnormal_tsh = len(df[(df['TSH'] < 0.4) | (df['TSH'] > 4.0)])
                        abnormal_count += abnormal_tsh
                        
                    if abnormal_count > 0:
                        st.markdown(f'''
                        <div class="diagnostic-box">
                            <div style="color: #ff6b35; font-weight: bold; text-align: center;">⚠ ABNORMAL VALUES DETECTED</div>
                            <div style="color: #ff4444; text-align: center;">{abnormal_count} patients with abnormal TSH levels</div>
                        </div>
                        ''', unsafe_allow_html=True)
            
            # Missing values analysis
            if st.checkbox("🔍 Check Missing Values"):
                st.markdown('<h4 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">❓ MISSING DATA ANALYSIS</h4>', unsafe_allow_html=True)
                missing_data = df.isnull().sum()
                if missing_data.sum() > 0:
                    missing_df = missing_data[missing_data > 0].to_frame('Missing Count').reset_index()
                    missing_df.columns = ['Column', 'Missing Count']
                    missing_df['Percentage'] = (missing_df['Missing Count'] / len(df) * 100).round(2)
                    st.dataframe(missing_df, use_container_width=True, hide_index=True)
                else:
                    st.markdown('''
                    <div class="diagnostic-box">
                        <div style="color: #00ff41; font-weight: bold; text-align: center;">✓ DATA INTEGRITY CHECK PASSED</div>
                        <div style="color: #00ff41; text-align: center;">No missing values detected</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
        except Exception as e:
            st.markdown(f'''
            <div class="diagnostic-box">
                <div style="color: #ff4444; font-weight: bold; text-align: center;">❌ FILE PROCESSING ERROR</div>
                <div style="color: #ff4444; text-align: center;">Error: {str(e)}</div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="diagnostic-box">
            <div style="color: #ff6b35; font-weight: bold; text-align: center;">📁 NO FILE SELECTED</div>
            <div style="color: #888; text-align: center;">Please upload a CSV file containing thyroid lab results</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Sample data download
        st.markdown('<h3 style="color: #00ff41; font-family: \'Courier Prime\', monospace;">💾 SAMPLE DATASET AVAILABLE</h3>', unsafe_allow_html=True)
        st.markdown("Don't have thyroid data? Download our sample dataset for testing:")
        
        sample_df = generate_thyroid_data()
        csv = sample_df.to_csv(index=False)
        st.download_button(
            label="💾 DOWNLOAD SAMPLE THYROID DATA",
            data=csv,
            file_name="sample_thyroid_data.csv",
            mime="text/csv"
        )

def show_form_demo():
    st.markdown('<h2 class="section-header">📝 PATIENT ENTRY - THYROID SCREENING FORM</h2>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="retro-terminal">
        > PATIENT REGISTRATION SYSTEM v2.1<br>
        > THYROID SCREENING MODULE LOADED<br>
        > MEDICAL RECORD DATABASE: CONNECTED<br>
        > READY FOR PATIENT INPUT...
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form("thyroid_patient_form"):
        st.markdown('<h3 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">👤 PATIENT INFORMATION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name*", placeholder="Enter patient's first name")
            patient_id = st.text_input("Patient ID*", placeholder="THY-XXXX")
            birth_date = st.date_input("Date of Birth*", value=date(1980, 1, 1))
            phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
            
        with col2:
            last_name = st.text_input("Last Name*", placeholder="Enter patient's last name")
            gender = st.selectbox("Gender*", ["Female", "Male", "Other", "Prefer not to say"])
            emergency_contact = st.text_input("Emergency Contact", placeholder="Name and phone")
            insurance_id = st.text_input("Insurance ID", placeholder="Insurance number")
        
        st.markdown('<h3 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">🔬 THYROID SCREENING QUESTIONNAIRE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Physical Symptoms:**")
            fatigue = st.radio("Experiencing unusual fatigue?", ["No", "Mild", "Moderate", "Severe"])
            weight_changes = st.radio("Recent weight changes?", ["No", "Weight gain", "Weight loss"])
            heart_rate = st.radio("Heart rate irregularities?", ["No", "Slow heart rate", "Fast heart rate"])
            temperature = st.radio("Temperature sensitivity?", ["No", "Cold sensitivity", "Heat sensitivity"])
            
        with col2:
            st.markdown("**Medical History:**")
            family_history = st.checkbox("Family history of thyroid disease")
            previous_thyroid = st.checkbox("Previous thyroid problems")
            medications = st.checkbox("Currently taking thyroid medications")
            autoimmune = st.checkbox("History of autoimmune disorders")
        
        st.markdown('<h3 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">📊 CURRENT LAB RESULTS (if available)</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tsh_available = st.checkbox("TSH result available")
            if tsh_available:
                tsh_value = st.number_input("TSH (mIU/L)", min_value=0.0, max_value=50.0, value=2.5, step=0.1)
            else:
                tsh_value = None
                
        with col2:
            t3_available = st.checkbox("T3 result available")
            if t3_available:
                t3_value = st.number_input("T3 (ng/dL)", min_value=0.0, max_value=10.0, value=1.8, step=0.1)
            else:
                t3_value = None
                
        with col3:
            t4_available = st.checkbox("T4 result available")
            if t4_available:
                t4_value = st.number_input("T4 (μg/dL)", min_value=0.0, max_value=20.0, value=9.5, step=0.1)
            else:
                t4_value = None
        
        # Risk assessment
        st.markdown('<h3 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">⚠️ RISK FACTORS</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            smoking = st.checkbox("Current or former smoker")
            pregnancy = st.checkbox("Currently pregnant or recently gave birth")
            
        with col2:
            radiation = st.checkbox("History of radiation exposure")
            iodine_deficiency = st.checkbox("Lives in iodine-deficient area")
        
        # Additional notes
        additional_notes = st.text_area("Additional Notes/Symptoms", 
                                       placeholder="Any other symptoms or concerns...", 
                                       max_chars=1000)
        
        # Consent and submission
        st.markdown('<h3 style="color: #ff6b35; font-family: \'Courier Prime\', monospace;">📋 CONSENT & SUBMISSION</h3>', unsafe_allow_html=True)
        
        consent_treatment = st.checkbox("I consent to thyroid screening and treatment*")
        consent_data = st.checkbox("I consent to data storage for medical records*")
        consent_contact = st.checkbox("I consent to follow-up contact if needed*")
        newsletter = st.checkbox("Send me thyroid health information")
        
        # Submit button
        submitted = st.form_submit_button("🏥 SUBMIT PATIENT RECORD", type="primary")
        
        if submitted:
            # Validation
            errors = []
            if not first_name:
                errors.append("First name is required")
            if not last_name:
                errors.append("Last name is required")
            if not patient_id:
                errors.append("Patient ID is required")
            elif not patient_id.startswith("THY-"):
                errors.append("Patient ID must start with 'THY-'")
            if not consent_treatment:
                errors.append("Treatment consent is required")
            if not consent_data:
                errors.append("Data storage consent is required")
            if not consent_contact:
                errors.append("Contact consent is required")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Calculate risk score
                risk_score = 0
                if family_history: risk_score += 2
                if previous_thyroid: risk_score += 3
                if autoimmune: risk_score += 2
                if smoking: risk_score += 1
                if radiation: risk_score += 2
                if pregnancy: risk_score += 1
                if fatigue in ["Moderate", "Severe"]: risk_score += 1
                if weight_changes != "No": risk_score += 1
                if heart_rate != "No": risk_score += 1
                if temperature != "No": risk_score += 1
                
                # Lab-based assessment
                lab_abnormal = False
                if tsh_available and tsh_value:
                    if tsh_value < 0.4 or tsh_value > 4.0:
                        lab_abnormal = True
                        risk_score += 3
                
                # Success message with risk assessment
                st.success("✅ Patient record submitted successfully!")
                st.balloons()
                
                # Display submitted information
                st.markdown('''
                <div class="retro-terminal">
                    <h3 style="color: #00ff41;">📋 PATIENT RECORD SUMMARY:</h3>
                    <br>
                ''', unsafe_allow_html=True)
                
                st.write(f"**Patient:** {first_name} {last_name} (ID: {patient_id})")
                st.write(f"**Age:** {datetime.now().year - birth_date.year} years")
                st.write(f"**Gender:** {gender}")
                
                # Risk assessment display
                if risk_score >= 8:
                    risk_level = "HIGH"
                    risk_color = "#ff4444"
                elif risk_score >= 4:
                    risk_level = "MEDIUM"
                    risk_color = "#ff6b35"
                else:
                    risk_level = "LOW"
                    risk_color = "#00ff41"
                
                st.markdown(f'''
                <div class="diagnostic-box">
                    <div style="color: #00ff41; font-weight: bold; text-align: center;">RISK ASSESSMENT</div>
                    <div style="color: {risk_color}; font-size: 1.5rem; text-align: center; font-weight: bold;">{risk_level} RISK</div>
                    <div style="color: {risk_color}; text-align: center;">Risk Score: {risk_score}/15</div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Lab results if available
                if any([tsh_available, t3_available, t4_available]):
                    st.markdown("**Lab Results:**")
                    if tsh_available:
                        status = "⚠ ABNORMAL" if lab_abnormal else "✓ NORMAL"
                        st.write(f"TSH: {tsh_value} mIU/L - {status}")
                    if t3_available:
                        st.write(f"T3: {t3_value} ng/dL")
                    if t4_available:
                        st.write(f"T4: {t4_value} μg/dL")
                
                # Recommendations
                st.markdown("**System Recommendations:**")
                if risk_score >= 8 or lab_abnormal:
                    st.write("🔴 Urgent endocrinology referral recommended")
                    st.write("🔴 Schedule comprehensive thyroid panel")
                elif risk_score >= 4:
                    st.write("🟡 Schedule thyroid function tests")
                    st.write("🟡 Follow-up in 3-6 months")
                else:
                    st.write("🟢 Routine annual screening")
                    st.write("🟢 Maintain healthy lifestyle")
                
                st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
