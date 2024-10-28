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
from pathlib import Path
import tempfile
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
from utils.video_processor import VideoProcessor
from utils.audio_processor import AudioTranscriber

class VideoToPDFConverter:
    def __init__(self):
        self.transcriber = AudioTranscriber()
        self.transcriber.load_model()

    def convert_video_to_pdf(self, uploaded_file) -> bytes:
        """Convert video to audio, transcribe, and generate a PDF."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_video_path = Path(temp_dir) / "input_video.mp4"
            temp_audio_path = Path(temp_dir) / "temp_audio.wav"

            # Save uploaded video locally
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.read())

            # Convert video to audio
            if VideoProcessor.convert_video_to_audio(str(temp_video_path), str(temp_audio_path)):
                # Transcribe audio to text
                result = self.transcriber.transcribe_audio(str(temp_audio_path))
                transcription = result.get('text', '') if isinstance(result, dict) else str(result)

                # Generate and return PDF content as bytes
                pdf_content = self.generate_pdf(transcription)
                return pdf_content
            else:
                raise Exception("Failed to convert video to audio.")

    def generate_pdf(self, text: str) -> bytes:
        """Generate a PDF from the transcription text."""
        buffer = BytesIO()
        pdf_writer = PdfWriter()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 50  # Start writing from the top of the page

        # Split text into lines and write to PDF
        for line in text.splitlines():
            if y < 50:  # Start a new page if space runs out
                c.showPage()
                y = height - 50
            c.drawString(50, y, line)
            y -= 15

        c.save()
        buffer.seek(0)  # Reset buffer position

        # Final PDF construction
        pdf_reader = PdfReader(buffer)
        output_buffer = BytesIO()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        pdf_writer.write(output_buffer)
        output_buffer.seek(0)

        return output_buffer.getvalue()
