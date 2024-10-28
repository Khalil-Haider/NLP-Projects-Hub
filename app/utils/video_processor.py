# Directory structure:
# app/
# ├── Home.py
# ├── utils/
# │   ├── __init__.py
# │   ├── audio_pdf_genrator.py
# │   └── audio_processor.py
# │   └── text_processor.py
# │   ├── video_processor.py
# │   ├── video_to_pdf.py
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

# utils/video_processor.py
import os
from pathlib import Path
import ffmpeg_python

class VideoProcessor:
    def __init__(self):
        self.temp_dir = None
        self.transcription = None

    @staticmethod
    def check_ffmpeg_installation():
        try:
            ffmpeg_python.FFmpeg().version()
            return True
        except:
            return False

    @staticmethod
    def convert_video_to_audio(input_file, output_file):
        try:
            command = [
                '-y',  # Overwrite output file if it exists
                '-i', input_file,
                '-ac', '1',
                '-ar', '16000',
                '-c:a', 'pcm_s16le',
                output_file
            ]
            
            # Use FFmpeg wrapper
            ff = ffmpeg_python.FFmpeg()
            ff.run(command)
            return True
            
        except Exception as e:
            raise Exception(f"Error during conversion: {str(e)}")
