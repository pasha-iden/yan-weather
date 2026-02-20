import json
from pathlib import Path
from typing import Dict

# Словарь в памяти
_users: Dict[str, int] = {}


def load_users(is_dev: bool) -> Dict[str, int]:
    global _users

    if is_dev: storage_file = Path("users.json")
    else: storage_file = Path("/app/data/users.json")

    if not storage_file.exists():
        _users = {}
        return _users

    try:
        with open(storage_file, 'r', encoding='utf-8') as f:
            _users = json.load(f)
        return _users
    except Exception:
        _users = {}
        return _users


def save_users(is_dev: bool) -> None:
    if is_dev: storage_file = Path("users.json")
    else: storage_file = Path("/app/data/users.json")

    storage_file.parent.mkdir(parents=True, exist_ok=True)

    with open(storage_file, 'w', encoding='utf-8') as f:
        json.dump(_users, f, ensure_ascii=False, indent=2)


def add_user(user_id: int, message_id: int) -> None:
    _users[str(user_id)] = message_id


def delete_user(user_id: int) -> None:
    _users.pop(str(user_id), None)


def get_all_users() -> Dict[str, int]:
    return _users.copy()  # копия чтобы не меняли оригинал