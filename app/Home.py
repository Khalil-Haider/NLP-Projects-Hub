# Directory structure:
# app/
# ├── Home.py
# ├── utils/
# │   ├── __init__.py
# │   ├── video_processor.py
# │   ├── audio_processor.py
# │   └── text_processor.py
# ├── pages/
# │   ├── 1_🎥_Video_to_Audio.py
# │   ├── 2_🎥_Video_to_Text.py
# │   ├── 3_🎧_Audio_to_Text.py
# │   ├── 4_💬_Chat_with_Video.py
# │   ├── 5_💬_Chat_with_Audio.py
# │   └── 6_💬_Chat_with_Documents.py
# └── assets/
#     └── style.css

# First, let's create the utility files:



# Home.py (Main application file)
import streamlit as st
import json
from pathlib import Path

import streamlit as st
import base64



# Configure page settings
st.set_page_config(
    page_title="AI Media Processing Hub",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path("assets/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()

    # Header with dropdown menu
    st.markdown('<h1 class="main-title">🎯 AI Media Processing Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transform and interact with your media using state-of-the-art AI</p>', unsafe_allow_html=True)

    # Dropdown menu for navigation
    #menu_options = ["Home", "Video to Audio", "Video to Text", "Audio to Text", "Chat with Video", "Chat with Audio", "Chat with Documents"]
    #selected_option = st.selectbox("Select a feature:", menu_options)

    # Features section in columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎥 Media Conversion</h3>
            <ul>
                <li>Convert Video to Audio</li>
                <li>Convert Video to Text</li>
                <li>Convert Audio to Text</li>
            </ul>
            <p>Professional-grade conversion with high accuracy</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>💬 Interactive Chat</h3>
            <ul>
                <li>Chat with Video Content</li>
                <li>Chat with Audio Content</li>
                <li>Chat with Documents</li>
            </ul>
            <p>AI-powered conversations with your media</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Key Benefits</h3>
            <ul>
                <li>Fast Processing Speed</li>
                <li>High Accuracy Results</li>
                <li>Multiple Format Support</li>
                <li>Secure Processing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>🛠️ Getting Started</h3>
            <p>Select a feature from the dropdown menu to begin processing your media. Each tool is designed for specific tasks with optimal settings.</p>
        </div>
        """, unsafe_allow_html=True)

    # Statistics or metrics
    st.markdown("### 📊 Platform Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Supported Languages", "100+")
    col2.metric("File Formats", "20+")
    col3.metric("Processing Speed", "2-3x faster")
    col4.metric("Success Rate", "99.9%")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Made with ❤️ by Your Company | Professional Media Processing Services</p>
            <p>© 2024 All Rights Reserved</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()