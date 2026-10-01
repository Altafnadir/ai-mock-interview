import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

class StorageService:
    def __init__(self, base_dir: str = settings.STORAGE_DIR):
        self.base_dir = Path(base_dir)
        self.subdirs = {
            "resumes": self.base_dir / "resumes",
            "recordings": self.base_dir / "recordings",
            "reports": self.base_dir / "reports",
            "posters": self.base_dir / "posters",
            "avatars": self.base_dir / "avatars",
        }
        for path in self.subdirs.values():
            path.mkdir(parents=True, exist_ok=True)

    def save_upload_file(self, file: UploadFile, folder: str, allowed_extensions: list = None) -> tuple[str, str]:
        """
        Saves an uploaded file safely with a unique filename.
        Returns: (relative_or_absolute_file_path, original_filename)
        """
        if folder not in self.subdirs:
            raise ValueError(f"Unknown storage folder: {folder}")

        original_name = file.filename or "unknown"
        ext = Path(original_name).suffix.lower()

        if allowed_extensions and ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file extension {ext}. Allowed: {allowed_extensions}"
            )

        unique_filename = f"{uuid.uuid4()}{ext}"
        destination = self.subdirs[folder] / unique_filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return standardized relative path
        stored_path = f"{settings.STORAGE_DIR}/{folder}/{unique_filename}".replace("\\", "/")
        return stored_path, original_name

    def get_absolute_path(self, stored_path: str) -> Path:
        """Resolves stored path to an absolute Path object."""
        return Path(stored_path).resolve()

    def delete_file(self, stored_path: str) -> bool:
        """Removes a file from storage if it exists."""
        try:
            path = self.get_absolute_path(stored_path)
            if path.exists() and path.is_file():
                path.unlink()
                return True
        except Exception:
            pass
        return False

storage_service = StorageService()
