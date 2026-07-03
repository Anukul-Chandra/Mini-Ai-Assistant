from io import BytesIO

from fastapi import UploadFile
from pypdf import PdfReader, PdfReadError


ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


def validate_file(file: UploadFile) -> bool:
    if not file.filename:
        raise ValueError("No filename provided")

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    ext = f".{ext}"

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"File extension '{ext}' is not allowed. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    return True


def read_document(file: UploadFile) -> str:
    if not file.filename:
        raise ValueError("No filename provided")

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    ext = f".{ext}"

    try:
        if ext == ".pdf":
            pdf_reader = PdfReader(BytesIO(file.file.read()))
            text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
        else:
            text = file.file.read().decode("utf-8")
    except PdfReadError:
        raise ValueError("Invalid or corrupted PDF file")
    except UnicodeDecodeError:
        raise ValueError("File is not valid UTF-8 text")
    except Exception:
        raise ValueError("Failed to read the document")

    if not text.strip():
        raise ValueError("No readable text found in the document")

    return text
