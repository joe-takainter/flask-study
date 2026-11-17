import sqlite3
import time
from datetime import datetime
from pathlib import Path

SOURCE = Path("/home/centos/flask-study/people.db")
BACKUP_DIR = Path("/home/centos/flask-backups")
RETENTION_DAYS = 30



def backup_database():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.chmod(0o700)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = BACKUP_DIR / f"people-{timestamp}.db"

    if destination.exists():
        raise FileExistsError(f"同名のバックアップが存在します: {destination}")

    with sqlite3.connect(f"file:{SOURCE}?mode=ro", uri=True) as src:
        with sqlite3.connect(str(destination)) as dst:
            src.backup(dst)

    destination.chmod(0o600)

    with sqlite3.connect(f"file:{destination}?mode=ro", uri=True) as con:
        result = con.execute("PRAGMA integrity_check").fetchone()[0]

    if result != "ok":
        raise RuntimeError(f"整合性チェックに失敗しました: {result}")

    print("バックアップ成功")
    print("保存先:", destination)
    print("サイズ:", destination.stat().st_size, "bytes")
    print("整合性チェック:", result)

def cleanup_old_backups(dry_run=True):
    cutoff = time.time() - RETENTION_DAYS * 86400

    count = 0

    for file in BACKUP_DIR.glob("people-*.db"):
        if file.is_file() and not file.is_symlink():
            if file.stat().st_mtime < cutoff:
                if dry_run:
                    print("削除候補:", file.name)
                else:
                    file.unlink()
                    print("削除完了:", file.name)

                count += 1

    if dry_run:
        print("削除候補数:", count)
    else:
        print("削除件数:", count)


if __name__ == "__main__":
    backup_database()
    cleanup_old_backups(dry_run=False)
