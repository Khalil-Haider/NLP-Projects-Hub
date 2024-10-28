# Directory structure:
# app/
# ├── Home.py
# ├── utils/
# │   ├── init.py
# │   ├── audio_pdf_genrator.py
# │   └── audio_processor.py
# │   └── rag_processor.py
# │   └── text_processor.py
# │   ├── video_processor.py
# │   ├── video_topdf.py
# ├── pages/
# │   ├── 1🎥_Video_toAudio.py
# │   ├── 2🎥_Video_toText.py
# │   ├── 3🎧_Audio_toText.py
# │   ├── 4💬_Chat_withVideo.py
# │   ├── 5💬_Chat_withAudio.py
# │   └── 6💬_Chat_with_Documents.py
# └── assets/
#     └── style.css
# pages/1_🎥_Video_to_Audio.py
import streamlit as st
import tempfile
from pathlib import Path
import os
from utils.video_processor import VideoProcessor
import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to the Video to Audio conversion page"""
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            background-color: var(--background-color);
            color: var(--text-color);
            padding: 1rem;
        }
        
        /* Title and headers */
        h1, h2, h3 {
            color: rgb(255, 255, 255);
            font-weight: 600;
            margin-bottom: 1.5rem;
        }
        
        /* File uploader styling */
        .stFileUploader {
            background-color: rgba(251, 251, 251, 0.05);
            border: 2px dashed rgba(28, 131, 225, 0.3);
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            transition: all 0.2s ease;
        }
        
        .stFileUploader:hover {
            border-color: rgba(28, 131, 225, 0.5);
            background-color: rgba(251, 251, 251, 0.08);
        }
        
        /* File details expander */
        .streamlit-expanderHeader {
            background-color: rgba(251, 251, 251, 0.05);
            border-radius: 8px;
            border: 1px solid rgba(251, 251, 251, 0.1);
            padding: 0.75rem;
            margin-bottom: 1rem;
        }
        
        /* Select box styling */
        .stSelectbox {
            background-color: rgba(251, 251, 251, 0.05);
            border-radius: 6px;
            margin: 1rem 0;
        }
        
        .stSelectbox > div > div {
            background-color: rgba(251, 251, 251, 0.05);
            border: 1px solid rgba(251, 251, 251, 0.1);
        }
        
        /* Convert button styling */
        .stButton > button {
            background-color: rgb(28, 131, 225);
            color: white;
            padding: 0.75rem 2rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            transition: all 0.2s ease;
            width: 100%;
            margin: 1rem 0;
        }
        
        .stButton > button:hover {
            background-color: rgb(24, 111, 191);
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Download button styling */
        .stDownloadButton > button {
            background-color: rgb(45, 201, 55);
            color: white;
            padding: 0.75rem 2rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            transition: all 0.2s ease;
            width: 100%;
            margin: 1rem 0;
        }
        
        .stDownloadButton > button:hover {
            background-color: rgb(38, 171, 47);
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Tips section styling */
        .streamlit-expanderContent {
            background-color: rgba(251, 251, 251, 0.03);
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Success message styling */
        .stSuccess {
            background-color: rgba(45, 201, 55, 0.1);
            border: 1px solid rgba(45, 201, 55, 0.2);
            color: rgb(45, 201, 55);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Error message styling */
        .stError {
            background-color: rgba(255, 76, 76, 0.1);
            border: 1px solid rgba(255, 76, 76, 0.2);
            color: rgb(255, 76, 76);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: rgba(251, 251, 251, 0.05);
            border-right: 1px solid rgba(251, 251, 251, 0.1);
            padding: 2rem 1rem;
        }
        
        /* Footer styling */
        .footer {
            margin-top: 3rem;
            padding: 1.5rem;
            text-align: center;
            border-top: 1px solid rgba(251, 251, 251, 0.1);
        }
        
        .footer a {
            color: rgb(28, 131, 225);
            text-decoration: none;
            transition: color 0.2s ease;
        }
        
        .footer a:hover {
            color: rgb(24, 111, 191);
            text-decoration: underline;
        }
        
        /* Progress bar styling */
        .stProgress > div > div {
            background-color: rgb(28, 131, 225);
        }
        
        /* Spinner styling */
        .stSpinner > div > div {
            border-top-color: rgb(28, 131, 225) !important;
        }
        
        /* File size info styling */
        .file-info {
            background-color: rgba(251, 251, 251, 0.05);
            border-radius: 6px;
            padding: 0.5rem;
            margin: 0.5rem 0;
            font-family: monospace;
        }
        </style>
    """, unsafe_allow_html=True)



# Configure page settings

st.set_page_config(
    page_title="Video to Audio Conversion",
    page_icon="🎥",
    layout="wide"
)

def main():
     # Apply custom styling
    apply_custom_css()
    st.title("🎥 Video to Audio Conversion")
    st.markdown("Transform your videos into high-quality audio files with professional processing.")
    # Sidebar information
    st.sidebar.markdown("""
    ### 📝 Instructions
    1. Upload your video file
    2. Choose output format
    3. Click convert
    4. Download the result

    ### 🎯 Supported Formats
    - Input: MP4, AVI, MOV, MKV
    - Output: WAV, MP3
    """)

    # Main content
    uploaded_file = st.file_uploader("Upload your video file", type=['mp4', 'avi', 'mov', 'mkv'])
    
    if uploaded_file:
        # File info
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": f"{uploaded_file.size / 1024 / 1024:.2f} MB"
        }
        
        # Show file details in an expander
        with st.expander("File Details"):
            for key, value in file_details.items():
                st.write(f"{key}: {value}")

        # Output format selection
        output_format = st.selectbox(
            "Select output format",
            ["WAV", "MP3"],
            index=0
        )

        # Convert button
        if st.button("🚀 Convert to Audio"):
            with st.spinner("Converting video to audio..."):
                try:
                    # Create temporary directory
                    with tempfile.TemporaryDirectory() as temp_dir:
                        # Save uploaded video
                        temp_video_path = Path(temp_dir) / "input_video.mp4"
                        temp_audio_path = Path(temp_dir) / f"output_audio.{output_format.lower()}"
                        
                        with open(temp_video_path, "wb") as f:
                            f.write(uploaded_file.read())
                        
                        # Convert video to audio
                        if VideoProcessor.convert_video_to_audio(str(temp_video_path), str(temp_audio_path)):
                            # Read the converted audio file
                            with open(temp_audio_path, "rb") as audio_file:
                                audio_bytes = audio_file.read()
                            
                            # Show success message
                            st.success("✅ Conversion completed successfully!")
                            
                            # Download button
                            st.download_button(
                                label="⬇️ Download Audio",
                                data=audio_bytes,
                                file_name=f"{uploaded_file.name.split('.')[0]}.{output_format.lower()}",
                                mime=f"audio/{output_format.lower()}"
                            )
                        else:
                            st.error("❌ Conversion failed")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    # Tips section
    with st.expander("💡 Tips for Best Results"):
        st.markdown("""
        - Ensure your video file has clear audio
        - For best quality, use videos with minimal background noise
        - Larger files may take longer to process
        - Keep your browser tab open during conversion
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Need help? Check our <a href='#'>documentation</a> or <a href='#'>contact support</a></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()