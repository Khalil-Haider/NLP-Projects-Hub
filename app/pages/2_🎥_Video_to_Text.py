# pages/2_🎥_Video_to_Text.py
import streamlit as st
import tempfile
from pathlib import Path
import os
from utils.video_processor import VideoProcessor
from utils.audio_processor import AudioTranscriber
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to the Video to Text conversion page"""
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            background-color: var(--background-color);
            color: var(--text-color);
            padding: 1rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: rgba(251, 251, 251, 0.05);
            border-right: 1px solid rgba(251, 251, 251, 0.1);
            padding: 2rem 1rem;
        }
        
        /* Sidebar headers */
        .css-1d391kg h3 {
            color: rgb(28, 131, 225);
            font-size: 1.2rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(251, 251, 251, 0.1);
        }
        
        /* Sidebar lists */
        .css-1d391kg ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .css-1d391kg li {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }
        
        .css-1d391kg li:before {
            content: "•";
            color: rgb(28, 131, 225);
            position: absolute;
            left: 0;
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
        
        /* File info box */
        .stInfo {
            background-color: rgba(28, 131, 225, 0.1);
            border: 1px solid rgba(28, 131, 225, 0.2);
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(251, 251, 251, 0.05);
            padding: 0.5rem;
            border-radius: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border: 1px solid rgba(251, 251, 251, 0.1);
            border-radius: 6px;
            padding: 0.5rem 1rem;
            color: var(--text-color);
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: rgb(28, 131, 225);
            border-color: rgb(28, 131, 225);
            color: white;
        }
        
        /* Progress bar styling */
        .stProgress > div > div {
            background-color: rgb(28, 131, 225);
            height: 8px;
            border-radius: 4px;
        }
        
        /* Status text */
        .status-text {
            color: rgb(28, 131, 225);
            font-weight: 500;
            margin: 1rem 0;
        }
        
        /* Download buttons */
        .stDownloadButton > button {
            background-color: rgba(28, 131, 225, 0.1);
            color: rgb(28, 131, 225);
            border: 1px solid rgba(28, 131, 225, 0.2);
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            transition: all 0.2s ease;
            width: 100%;
            font-weight: 500;
        }
        
        .stDownloadButton > button:hover {
            background-color: rgba(28, 131, 225, 0.2);
            border-color: rgba(28, 131, 225, 0.3);
            transform: translateY(-1px);
        }
        
        /* Settings area */
        .settings-box {
            background-color: rgba(251, 251, 251, 0.05);
            border: 1px solid rgba(251, 251, 251, 0.1);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Select box styling */
        .stSelectbox > div {
            background-color: rgba(251, 251, 251, 0.05);
            border: 1px solid rgba(251, 251, 251, 0.1);
            border-radius: 6px;
        }
        
        .stSelectbox > div:hover {
            border-color: rgb(28, 131, 225);
        }
        
        /* Checkbox styling */
        .stCheckbox > div {
            background-color: rgba(251, 251, 251, 0.05);
            border-radius: 6px;
            padding: 0.5rem;
        }
        
        /* Start transcription button */
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
        
        /* Tips expander */
        .streamlit-expanderHeader {
            background-color: rgba(251, 251, 251, 0.05);
            border-radius: 8px;
            border: 1px solid rgba(251, 251, 251, 0.1);
            padding: 0.75rem;
        }
        
        .streamlit-expanderContent {
            background-color: rgba(251, 251, 251, 0.03);
            border-radius: 0 0 8px 8px;
            padding: 1rem;
        }
        
        /* Transcription result area */
        .transcription-box {
            background-color: rgba(251, 251, 251, 0.03);
            border: 1px solid rgba(251, 251, 251, 0.1);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            font-family: 'Roboto Mono', monospace;
            white-space: pre-wrap;
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
        </style>
    """, unsafe_allow_html=True)


st.set_page_config(
    page_title="Video to Text Conversion",
    page_icon="🎥",
    layout="wide"
)
# pages/2_🎥_Video_to_Text.py
class VideoTextConverter:
    def __init__(self):
        self.transcriber = AudioTranscriber()
        self.transcriber.load_model()
        
    def convert_video_to_text(self, uploaded_file, language, include_timestamps):
        """Process video file and return transcription with PDF"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_video_path = Path(temp_dir) / "input_video.mp4"
            temp_audio_path = Path(temp_dir) / "temp_audio.wav"
            
            # Save uploaded video
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.read())
            
            # Convert to audio
            if VideoProcessor.convert_video_to_audio(str(temp_video_path), str(temp_audio_path)):
                # Transcribe
                result = self.transcriber.transcribe_audio(str(temp_audio_path))
                
                # Extract text from result dictionary
                transcription = result['text'] if isinstance(result, dict) else str(result)
                
                # Generate PDF
                pdf_content = self.generate_pdf(transcription)
                
                return {
                    "transcription": transcription,
                    "pdf_content": pdf_content
                }
            else:
                raise Exception("Failed to convert video to audio")
    
    def generate_pdf(self, text: str) -> bytes:
        """Generate PDF from transcription text"""
        # Create PDF using reportlab
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Split text into lines and write to PDF
        y = height - 50
        words = text.split()
        current_line = []
        
        for word in words:
            current_line.append(word)
            # Check if current line would be too long
            if c.stringWidth(' '.join(current_line), 'Helvetica', 12) > width - 100:
                # Remove last word and write line
                current_line.pop()
                line_text = ' '.join(current_line)
                if y < 50:
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, line_text)
                y -= 15
                # Start new line with the last word
                current_line = [word]
        
        # Write last line
        if current_line:
            line_text = ' '.join(current_line)
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(50, y, line_text)
        
        c.save()
        buffer.seek(0)
        
        # Create final PDF
        output_buffer = BytesIO()
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(buffer)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        pdf_writer.write(output_buffer)
        output_buffer.seek(0)
        
        return output_buffer.getvalue()

def main():

    # Apply custom styling
    apply_custom_css()

    # Rest of your existing main() function code...    
    st.title("🎥 Video to Text Conversion")
    st.markdown("Convert your video content into searchable, editable text with AI-powered transcription.")

    # Sidebar settings
    st.sidebar.markdown("""
    ### 🎯 Features
    - Multiple language support
    - Timestamps available
    - Speaker detection
    - Punctuation & formatting
    - PDF export
    
    ### 📝 Supported Formats
    - MP4, AVI, MOV, MKV
    - Max file size: 2GB
    """)

    # Main interface
    uploaded_file = st.file_uploader("Upload your video file", type=['mp4', 'avi', 'mov', 'mkv'])
    
    if uploaded_file:
        # File info display
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📁 File Information")
            st.info(f"""
            - Filename: {uploaded_file.name}
            - Size: {uploaded_file.size / 1024 / 1024:.2f} MB
            """)
        
        with col2:
            st.markdown("### ⚙️ Transcription Settings")
            language = st.selectbox("Select primary language", ["English", "Spanish", "French", "German", "Auto-detect"])
            include_timestamps = st.checkbox("Include timestamps", value=True)
        
        # Process button
        if st.button("🚀 Start Transcription"):
            try:
                with st.spinner("Processing your video..."):
                    # Create progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Initialize converter
                    converter = VideoTextConverter()
                    
                    # Step 1: Convert to audio
                    status_text.text("Converting video to audio...")
                    progress_bar.progress(25)
                    
                    # Process video
                    status_text.text("Processing video and generating transcription...")
                    progress_bar.progress(50)
                    
                    results = converter.convert_video_to_text(
                        uploaded_file,
                        language=language,
                        include_timestamps=include_timestamps
                    )
                    
                    progress_bar.progress(100)
                    status_text.text("Processing completed!")
                    
                    # Display results in tabs
                    tab1, tab2 = st.tabs(["📝 Transcription", "⬇️ Export Options"])
                    
                    with tab1:
                        st.markdown("### Transcription Result")
                        st.write(results["transcription"])  # Changed from st.markdown to st.write
                    
                    with tab2:
                        st.markdown("### Download Options")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                "📄 Download as TXT",
                                results["transcription"],
                                file_name=f"{uploaded_file.name}_transcription.txt",
                                mime="text/plain"
                            )
                        with col2:
                            st.download_button(
                                "📑 Download as PDF",
                                results["pdf_content"],
                                file_name=f"{uploaded_file.name}_transcription.pdf",
                                mime="application/pdf"
                            )
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Tips section
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        - Use videos with clear audio quality
        - Minimize background noise
        - Speak clearly and at a moderate pace
        - Position microphone properly during recording
        """)

if __name__ == "__main__":
    main()