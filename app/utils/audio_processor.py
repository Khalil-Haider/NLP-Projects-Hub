# Directory structure:
# app/
# ├── Home.py
# ├── utils/
# │   ├── __init__.py
# │   ├── audio_pdf_genrator.py
# │   └── audio_processor.py
# │   └── text_processor.py
# │   └── rag_processor.py
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
# utils/audio_processor.py

import os
import json
import wave
from pathlib import Path
from vosk import Model, KaldiRecognizer, SetLogLevel
import soundfile as sf
import numpy as np
import tempfile



# utils/audio_processor.py
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline



class AudioTranscriber:
    def __init__(self):
        # Suppress Vosk logs
        SetLogLevel(-1)
        self.temp_dir = None
        self.transcription = None
        
        # Load English model - using models directory in project structure
        self.model = self._load_model()
    
    def _load_model(self):
        """Load Vosk English model"""
        try:
            # Look for model in the project's models directory
            base_dir = Path(__file__).parent.parent
            model_path = os.path.join(base_dir, "models", "vosk-model-en-us-0.22-lgraph")
            
            if not os.path.exists(model_path):
                raise Exception(f"Model not found: {model_path}")
            return Model(model_path)
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")

    def _convert_to_wav(self, input_path, output_path):
        """Convert audio to WAV format with required parameters"""
        try:
            audio, sample_rate = sf.read(input_path)
            
            # Convert to mono if stereo
            if len(audio.shape) > 1:
                audio = audio.mean(axis=1)
            
            # Save as WAV with required parameters for Vosk
            sf.write(output_path, audio, 16000, subtype='PCM_16')
            
        except Exception as e:
            raise Exception(f"Error converting audio: {str(e)}")

    def transcribe_audio(self, audio_path):
        """Transcribe audio file to text"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                self.temp_dir = temp_dir
                temp_wav = os.path.join(temp_dir, "temp.wav")
                self._convert_to_wav(audio_path, temp_wav)
                
                rec = KaldiRecognizer(self.model, 16000)
                
                with wave.open(temp_wav, "rb") as wf:
                    while True:
                        data = wf.readframes(4000)
                        if len(data) == 0:
                            break
                        rec.AcceptWaveform(data)
                    
                    result = json.loads(rec.FinalResult())
                    self.transcription = result.get("text", "")
                    return self.transcription
                    
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")

    def get_transcription(self):
        """Return the last transcription"""
        return self.transcription if self.transcription else ""

    def cleanup(self):
        """Cleanup temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                for file in os.listdir(self.temp_dir):
                    os.remove(os.path.join(self.temp_dir, file))
                os.rmdir(self.temp_dir)
            except Exception:
                pass