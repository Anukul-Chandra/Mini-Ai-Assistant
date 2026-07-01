from fastapi import UploadFile


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
