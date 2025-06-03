import io
from pathlib import Path
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

from app.models.resume import Resume


def generate_resume_pdf(resume: Resume, pdf_path: str | None = None) -> bytes:
    html_template_path = Path("app/templates/resume.html")
    env = Environment(loader=FileSystemLoader(html_template_path.parent))
    template = env.get_template(html_template_path.name)
    rendered_html = template.render(resume=resume)

    # Output to in-memory buffer
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(target=pdf_buffer)
    pdf_bytes = pdf_buffer.getvalue()

    # Optional: save to disk
    if pdf_path:
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes

def generate_coverletter_pdf(cover_letter: str, resume: Resume, pdf_path: str | None = None) -> bytes:
    html_template_path = Path("app/templates/cover_letter.html")
    env = Environment(loader=FileSystemLoader(html_template_path.parent))
    template = env.get_template(html_template_path.name)
    rendered_html = template.render(resume=resume, cover_letter=cover_letter)

    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(target=pdf_buffer)
    pdf_bytes = pdf_buffer.getvalue()

    if pdf_path:
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes