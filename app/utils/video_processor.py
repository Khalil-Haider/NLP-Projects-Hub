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
from moviepy.editor import VideoFileClip

class VideoProcessor:
    def __init__(self):
        self.temp_dir = None
        self.transcription = None

    @staticmethod
    def convert_video_to_audio(input_file, output_file):
        try:
            # Load the video file
            video = VideoFileClip(input_file)
            
            # Extract the audio
            audio = video.audio
            
            # Write the audio file
            audio.write_audiofile(
                output_file,
                fps=16000,      # Sample rate
                nbytes=2,       # 16-bit audio
                codec='pcm_s16le'  # Same codec as before
            )
            
            # Close the clips to free up system resources
            audio.close()
            video.close()
            
            return True
            
        except Exception as e:
            raise Exception(f"Error during conversion: {str(e)}")