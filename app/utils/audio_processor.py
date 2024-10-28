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
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

class AudioTranscriber:
    def __init__(self):
        self.model = None
        self.processor = None
        self.pipe = None

    def load_model(self):
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model_id = "openai/whisper-large-v3"
        
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, 
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=False,
            use_safetensors=True
            #device_map="auto"
        )
        
        self.processor = AutoProcessor.from_pretrained(model_id)
        
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=torch_dtype,
            model_kwargs={"use_cache": True}
        )

    def transcribe_audio(self, audio_path):
        generate_kwargs = {
            "max_new_tokens": 445,
            "num_beams": 1,
            "temperature": 0.2,
            "logprob_threshold": -1.0,
            "no_speech_threshold": 0.6,
            "return_timestamps": True
        }
        
        result = self.pipe(audio_path, generate_kwargs=generate_kwargs)
        print(result)  # Add this line to inspect the output
        return result["text"]
        

