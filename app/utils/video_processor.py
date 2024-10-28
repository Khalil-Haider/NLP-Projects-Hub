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
import ffmpeg
import os
from pathlib import Path

class VideoProcessor:
    def __init__(self):
        self.temp_dir = None
        self.transcription = None



    @staticmethod
    def convert_video_to_audio(input_file, output_file):
        try:
            # Using ffmpeg-python to create the stream
            stream = ffmpeg.input(input_file)
            
            # Configure the audio settings
            stream = ffmpeg.output(
                stream,
                output_file,
                acodec='pcm_s16le',  # Audio codec
                ac=1,                 # Number of audio channels (mono)
                ar=16000,            # Audio sample rate
                loglevel='error'     # Reduce logging output
            )
            
            # Overwrite output file if it exists
            stream = ffmpeg.overwrite_output(stream)
            
            # Run the ffmpeg command
            ffmpeg.run(stream, quiet=True)
            return True
            
        except Exception as e:
            raise Exception(f"Error during conversion: {str(e)}")
