from pathlib import Path



BASE_DIR = Path("users")


def get_user_dir(user_id: int) -> Path:
    user_dir = BASE_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


def get_file_path(user_id: int, filename: str) -> Path:
    return get_user_dir(user_id) / f"{filename}.md"


