import re
from pathlib import Path

from werkzeug.utils import secure_filename

ALLOWED_CV_EXTENSIONS = {".pdf", ".txt", ".doc", ".docx"}
MAX_CV_SIZE = 5 * 1024 * 1024


class CVService:
    @staticmethod
    def allowed_file(filename: str) -> bool:
        return Path(filename or "").suffix.lower() in ALLOWED_CV_EXTENSIONS

    @staticmethod
    def save_upload(upload_folder: Path, user_id: int, file_storage) -> tuple[str | None, str | None]:
        if not file_storage or not file_storage.filename:
            return None, "Please select a CV file."
        if not CVService.allowed_file(file_storage.filename):
            return None, "Allowed formats: PDF, TXT, DOC, DOCX."
        file_storage.seek(0, 2)
        size = file_storage.tell()
        file_storage.seek(0)
        if size > MAX_CV_SIZE:
            return None, "File is too large (max 5 MB)."

        upload_folder.mkdir(parents=True, exist_ok=True)
        ext = Path(file_storage.filename).suffix.lower()
        safe = secure_filename(file_storage.filename)
        stored_name = f"user_{user_id}{ext}"
        path = upload_folder / stored_name
        file_storage.save(path)
        return stored_name, None

    @staticmethod
    def extract_text(file_path: Path) -> str:
        ext = file_path.suffix.lower()
        if ext == ".txt":
            return file_path.read_text(encoding="utf-8", errors="ignore")
        if ext == ".pdf":
            try:
                from pypdf import PdfReader

                reader = PdfReader(str(file_path))
                parts = []
                for page in reader.pages[:15]:
                    parts.append(page.extract_text() or "")
                return "\n".join(parts)
            except Exception:
                return ""
        if ext in (".doc", ".docx"):
            return CVService._read_docx(file_path)
        return ""

    @staticmethod
    def _read_docx(file_path: Path) -> str:
        try:
            import zipfile

            with zipfile.ZipFile(file_path) as zf:
                xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
            return re.sub(r"<[^>]+>", " ", xml)
        except Exception:
            return ""