from pathlib import Path

def removeFile(file_path):
    try:
        file_path = Path(file_path)
        file_path.unlink()
        print(f"'{file_path}' nomli fayl muvaffaqiyatli o'chirildi.")
    except FileNotFoundError:
        print(f"Xatolik: '{file_path}' nomli fayl topilmadi.")