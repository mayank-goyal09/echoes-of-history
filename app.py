import streamlit as st
import json
import os
import time
from engine import HistoricalEngine

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="🏛️ The Historical Persona Museum",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
#  PERSONA ICONS — Mapping persona IDs to emoji "passport photos"
# ============================================================
PERSONA_ICONS = {
    "Abraham_Lincoln": "🎩",
    "Mahatma_Gandhi": "🕊️",
    "Grandfather": "👴",
    "Marie_Curie": "⚗️",
    "Nikola_Tesla": "⚡",
    "Donald_Trump": "🦅",
    "default": "📜"
}

# ============================================================
#  CSS — THE VINTAGE PARCHMENT THEME
# ============================================================
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&family=Special+Elite&family=Playfair+Display:wght@400;700;900&display=swap');

    /* === MAIN BACKDROP === */
    .stApp {
        background: linear-gradient(145deg, #f4ecd8 0%, #e8dcc8 50%, #ddd0b8 100%) !important;
    }

    /* === SIDEBAR — THE CONTROL ROOM === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c1810 0%, #3d2416 50%, #2c1810 100%) !important;
        border-right: 3px solid #8b6914 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #f4ecd8 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stTextInput label {
        font-family: 'Playfair Display', serif !important;
        font-size: 14px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        color: #c9a84c !important;
    }
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: #4a2e1a !important;
        border: 1px solid #8b6914 !important;
        border-radius: 4px !important;
    }
    section[data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #8b6914, #c9a84c) !important;
        color: #2c1810 !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 4px !important;
        transition: all 0.3s ease !important;
    }
    section[data-testid="stSidebar"] button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 4px 15px rgba(139, 105, 20, 0.4) !important;
    }

    /* === HEADER STYLES === */
    .museum-header {
        text-align: center;
        padding: 30px 20px 20px;
        border-bottom: 2px solid #8b6914;
        margin-bottom: 30px;
        background: linear-gradient(180deg, rgba(44,24,16,0.08) 0%, transparent 100%);
    }
    .museum-header h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.6em !important;
        color: #2c1810 !important;
        margin: 0 !important;
        letter-spacing: 3px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .museum-header .subtitle {
        font-family: 'Crimson Text', serif;
        font-size: 1.1em;
        color: #6b4423;
        font-style: italic;
        margin-top: 8px;
    }

    /* === PERSONA VITALS CARD === */
    .vitals-card {
        background: linear-gradient(135deg, #4a2e1a, #3d2416);
        border: 1px solid #8b6914;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: inset 0 1px 0 rgba(201,168,76,0.2);
    }
    .vitals-card .icon {
        font-size: 3em;
        text-align: center;
        margin-bottom: 10px;
    }
    .vitals-card .persona-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.3em;
        color: #c9a84c !important;
        text-align: center;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .vitals-label {
        font-family: 'Crimson Text', serif;
        font-size: 0.8em;
        color: #a08050 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 2px;
    }
    .vitals-value {
        font-family: 'Crimson Text', serif;
        font-size: 1em;
        color: #f4ecd8 !important;
        margin-bottom: 10px;
        padding-left: 8px;
        border-left: 2px solid #8b6914;
    }

    /* === CHAT BUBBLES === */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
    }

    /* Persona (AI) Message */
    .persona-msg {
        background: linear-gradient(135deg, #fff9ed, #f5ecda);
        border: 1px solid #c9a84c;
        border-left: 4px solid #8b6914;
        border-radius: 2px 12px 12px 2px;
        padding: 20px 24px;
        margin: 16px 0;
        font-family: 'Crimson Text', serif;
        font-size: 1.05em;
        line-height: 1.7;
        color: #2c1810;
        box-shadow: 3px 3px 10px rgba(44,24,16,0.12), inset 0 1px 0 rgba(255,255,255,0.6);
        position: relative;
        animation: fadeInUp 0.6s ease;
    }
    .persona-msg::before {
        content: '🪶';
        position: absolute;
        top: -10px;
        left: 12px;
        font-size: 1.2em;
    }
    .persona-msg .speaker {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        color: #8b6914;
        font-size: 0.85em;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    /* Student (User) Message */
    .student-msg {
        background: linear-gradient(135deg, #3d2416, #2c1810);
        border: 1px solid #6b4423;
        border-radius: 12px 2px 2px 12px;
        border-right: 4px solid #8b6914;
        padding: 16px 20px;
        margin: 16px 0;
        font-family: 'Special Elite', cursive;
        font-size: 1em;
        line-height: 1.6;
        color: #f4ecd8;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.15);
        text-align: right;
        animation: fadeInUp 0.3s ease;
    }
    .student-msg .speaker {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        color: #c9a84c;
        font-size: 0.75em;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    /* === CONTEXT INDICATOR === */
    .archive-indicator {
        text-align: center;
        padding: 10px;
        font-family: 'Crimson Text', serif;
        font-style: italic;
        color: #8b6914;
        font-size: 0.9em;
        animation: pulse 1.5s ease-in-out infinite;
    }

    /* === WELCOME CARD === */
    .welcome-card {
        background: linear-gradient(135deg, #fff9ed, #f5ecda);
        border: 2px solid #c9a84c;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        max-width: 600px;
        margin: 60px auto;
        box-shadow: 0 8px 30px rgba(44,24,16,0.12);
    }
    .welcome-card h2 {
        font-family: 'Playfair Display', serif !important;
        color: #2c1810 !important;
        font-size: 1.8em !important;
        margin-bottom: 15px !important;
    }
    .welcome-card p {
        font-family: 'Crimson Text', serif;
        color: #6b4423;
        font-size: 1.1em;
        line-height: 1.6;
    }

    /* === STATUS BADGES === */
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-family: 'Crimson Text', serif;
        font-size: 0.75em;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .badge-active {
        background: rgba(139, 105, 20, 0.2);
        border: 1px solid #8b6914;
        color: #c9a84c !important;
    }

    /* === KNOWLEDGE LIMIT ALERT === */
    .knowledge-alert {
        background: linear-gradient(135deg, #4a2e1a, #3d2416);
        border: 1px solid #8b6914;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 10px 0;
        font-family: 'Crimson Text', serif;
        font-size: 0.9em;
        color: #c9a84c;
        text-align: center;
    }
    .knowledge-alert .icon { font-size: 1.3em; }

    /* === ANIMATIONS === */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50%      { opacity: 1; }
    }

    /* === HIDE STREAMLIT DEFAULTS & KEEP SIDEBAR TOGGLE === */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background-color: transparent !important;
        box-shadow: none !important;
        display: flex !important;
        z-index: 99999 !important;
    }
    [data-testid="stAppDeployButton"], 
    [data-testid="stToolbar"], 
    [data-testid="stDecoration"] {
        display: none !important;
    }
    /* Force visibility and styling of the sidebar toggle button */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: block !important;
        background-color: #fff9ed !important;
        border: 2px solid #8b6914 !important;
        border-radius: 6px !important;
        margin: 10px !important;
        box-shadow: 2px 2px 8px rgba(44,24,16,0.2) !important;
        z-index: 100000 !important;
        opacity: 1 !important;
    }
    [data-testid="collapsedControl"] button {
        color: #2c1810 !important;
        background-color: transparent !important;
        border: none !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #2c1810 !important;
        color: #2c1810 !important;
        stroke: #2c1810 !important;
    }



    /* === CHAT INPUT STYLING === */
    .stChatInput, [data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
    }
    .stChatInput > div, [data-testid="stChatInput"] > div {
        background-color: transparent !important;
        border: none !important;
    }
    .stChatInput textarea, [data-testid="stChatInput"] textarea {
        background-color: #fff9ed !important;
        color: #2c1810 !important;
        border: 2px solid #8b6914 !important;
        border-radius: 8px !important;
        font-family: 'Crimson Text', serif !important;
    }
    .stChatInput textarea::placeholder, [data-testid="stChatInput"] textarea::placeholder {
        color: #8b6914 !important;
        opacity: 0.75 !important;
    }

    /* === DIVIDER === */
    .ornamental-divider {
        text-align: center;
        color: #8b6914;
        font-size: 1.2em;
        margin: 10px 0;
        letter-spacing: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
#  HELPER FUNCTIONS
# ============================================================
def load_config():
    config_path = "persona_config.json"
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump({}, f)
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(config):
    with open('persona_config.json', 'w') as f:
        json.dump(config, f, indent=4)

def get_icon(persona_id):
    return PERSONA_ICONS.get(persona_id, PERSONA_ICONS["default"])

def render_persona_message(name, content):
    st.markdown(f"""
    <div class="persona-msg">
        <div class="speaker">{name}</div>
        {content}
    </div>
    """, unsafe_allow_html=True)

def render_student_message(content):
    st.markdown(f"""
    <div class="student-msg">
        <div class="speaker">📝 You</div>
        {content}
    </div>
    """, unsafe_allow_html=True)


# ============================================================
#  MAIN APP
# ============================================================
def main():
    inject_css()

    # --- SESSION STATE INITIALIZATION ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "engine" not in st.session_state:
        st.session_state.engine = None
    if "current_persona_id" not in st.session_state:
        st.session_state.current_persona_id = None
    if "config" not in st.session_state:
        st.session_state.config = load_config()

    config = st.session_state.config

    # =====================================================
    #  SIDEBAR — THE CONTROL ROOM
    # =====================================================
    with st.sidebar:
        st.markdown('<div class="ornamental-divider">— ✦ —</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; margin-bottom: 20px;">
            <span style="font-size: 2.5em;">🏛️</span><br>
            <span style="font-family: 'Playfair Display', serif; font-size: 1.4em; font-weight: 700;
                         color: #c9a84c !important; letter-spacing: 2px;">
                THE MUSEUM
            </span><br>
            <span style="font-family: 'Crimson Text', serif; font-size: 0.85em; font-style: italic;
                         color: #a08050 !important;">
                Soul Registry & Control Room
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="ornamental-divider">— ✦ —</div>', unsafe_allow_html=True)

        # --- ZONE 1: PERSONA PICKER ---
        persona_ids = list(config.keys())
        persona_display = {pid: f"{get_icon(pid)} {config[pid]['name']}" for pid in persona_ids}

        if persona_ids:
            selected_display = st.selectbox(
                "Select a Historical Persona",
                options=persona_ids,
                format_func=lambda x: persona_display.get(x, x),
                key="persona_selector"
            )

            # Handle persona switch
            if selected_display != st.session_state.current_persona_id:
                st.session_state.current_persona_id = selected_display
                st.session_state.messages = []
                st.session_state.engine = None  # Will lazy-load below

            persona = config[selected_display]
            icon = get_icon(selected_display)

            # --- METADATA DISPLAY: THE VITALS ---
            vocab_str = ", ".join(persona.get("vocabulary", [])) if isinstance(persona.get("vocabulary"), list) else str(persona.get("vocabulary", ""))
            st.markdown(f"""
            <div class="vitals-card">
                <div class="icon">{icon}</div>
                <div class="persona-name">{persona['name']}</div>
                <div class="vitals-label">Era / Setting</div>
                <div class="vitals-value">{persona.get('era', 'Unknown')}</div>
                <div class="vitals-label">Tone</div>
                <div class="vitals-value">{persona.get('tone_description', 'Unknown')}</div>
                <div class="vitals-label">Knowledge Cutoff</div>
                <div class="vitals-value">⏳ Year {persona.get('cutoff_year', '?')}</div>
                <div class="vitals-label">Vocabulary</div>
                <div class="vitals-value">{vocab_str}</div>
                <div style="text-align:center; margin-top:8px;">
                    <span class="status-badge badge-active">● Persona Active</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- CLEAR CHAT ---
            if st.button("🗑️ Clear Chat & Reset Memory", use_container_width=True):
                st.session_state.messages = []
                if st.session_state.engine:
                    st.session_state.engine.memory.history = []
                st.rerun()
        else:
            st.info("No personas registered yet. Use the Discovery panel below to add one!")

        st.markdown('<div class="ornamental-divider">— ✦ —</div>', unsafe_allow_html=True)

        # --- ZONE 2: THE LAB — NEW DISCOVERY ---
        with st.expander("🔬 New Discovery — Add Persona"):
            st.markdown("""
            <span style="font-family: 'Crimson Text', serif; font-size: 0.9em; color: #a08050 !important;">
                Place a folder with <code>.txt</code> files inside <code>source_data/</code>, 
                then enter the folder name below.
            </span>
            """, unsafe_allow_html=True)

            new_folder = st.text_input("Folder Name", placeholder="e.g., Nikola_Tesla")

            if st.button("⚡ Analyze & Register", use_container_width=True):
                if new_folder:
                    data_path = f"./source_data/{new_folder}"
                    if os.path.exists(data_path):
                        if new_folder not in config:
                            with st.spinner(f"📜 Consulting the archives of {new_folder}..."):
                                try:
                                    temp_engine = HistoricalEngine()
                                    sample = temp_engine.ingest_new_persona(new_folder)
                                    profile = temp_engine.auto_profile(sample)
                                    config[new_folder] = profile
                                    save_config(config)
                                    st.session_state.config = config
                                    st.success(f"✅ {profile.get('name', new_folder)} has entered the Museum!")
                                    time.sleep(1)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"⚠️ The archives are unclear: {e}")
                        else:
                            st.warning("This persona already exists in the Registry.")
                    else:
                        st.markdown("""
                        <div class="knowledge-alert">
                            <span class="icon">📂</span><br>
                            I'm afraid I cannot find those records in the archives, Citizen.
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Please enter a folder name.")

    # =====================================================
    #  MAIN STAGE — THE EXHIBIT
    # =====================================================
    # Museum Header
    st.markdown("""
    <div class="museum-header">
        <h1>🏛️ The Historical Persona Museum</h1>
        <div class="subtitle">Step into the past. Converse with the echoes of history.</div>
    </div>
    """, unsafe_allow_html=True)

    if not persona_ids or not st.session_state.current_persona_id:
        # --- WELCOME STATE ---
        st.markdown("""
        <div class="welcome-card">
            <h2>Welcome, Citizen</h2>
            <p>
                The Museum awaits your curiosity.<br><br>
                Select a historical persona from the <strong>Control Room</strong> on the left,
                or discover a new one by adding source documents to the archives.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # --- LAZY LOAD ENGINE ---
    selected_id = st.session_state.current_persona_id
    persona = config[selected_id]

    if st.session_state.engine is None:
        with st.spinner(f"🔮 Summoning {persona['name']} from the archives..."):
            st.session_state.engine = HistoricalEngine(persona_id=selected_id)

    engine = st.session_state.engine

    # --- RENDER CHAT HISTORY ---
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if not st.session_state.messages:
        # First message greeting
        st.markdown(f"""
        <div class="persona-msg" style="text-align: center; border-left: 4px solid #c9a84c;">
            <div class="speaker">{persona['name']}</div>
            <em>I am here, Citizen. What knowledge do you seek from my era?</em>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_student_message(msg["content"])
        else:
            render_persona_message(persona["name"], msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)

    # --- CHAT INPUT ---
    if prompt := st.chat_input(f"Ask {persona['name']} a question..."):
        # Store user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        render_student_message(prompt)

        # Show archive consultation indicator
        st.markdown("""
        <div class="archive-indicator">
            📚 Consulting the Archives...
        </div>
        """, unsafe_allow_html=True)

        # Get AI response
        with st.spinner(""):
            response = engine.ask(prompt, persona)

        # Store AI message
        st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()


if __name__ == "__main__":
    main()
