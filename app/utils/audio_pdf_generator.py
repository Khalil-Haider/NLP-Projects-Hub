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

# utils/audio_pdf_generator.py
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader

class AudioToPDFConverter:
    """Utility class for generating PDFs from text."""

    @staticmethod
    def generate_pdf(text: str) -> bytes:
        """Generate a PDF from the given text."""
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Split text into lines and write to PDF
        y = height - 50
        words = text.split()
        current_line = []

        for word in words:
            current_line.append(word)
            if c.stringWidth(' '.join(current_line), 'Helvetica', 12) > width - 100:
                current_line.pop()
                line_text = ' '.join(current_line)
                if y < 50:
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, line_text)
                y -= 15
                current_line = [word]

        if current_line:
            line_text = ' '.join(current_line)
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(50, y, line_text)

        c.save()
        buffer.seek(0)

        output_buffer = BytesIO()
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(buffer)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        pdf_writer.write(output_buffer)
        output_buffer.seek(0)
        return output_buffer.getvalue()
