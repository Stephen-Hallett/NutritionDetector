import shutil
from pathlib import Path

qr_path = Path("data/qrcode")
bar_path = Path("data/barcode")

for file in bar_path.glob("*/labels/*.txt"):
    with open(file, "r+") as f:
        items = f.read().split("\n")
        f.seek(0)
        if len(items):
            new_items = ["1" + item[1:] for item in items]
            f.write("\n".join(new_items))
            f.truncate()

for folder in ("train", "test", "valid"):
    for subfolder in ("images", "labels"):
        Path(f"./data/combined/{folder}/{subfolder}").mkdir(parents=True, exist_ok=True)

for dir in ("barcode", "qrcode"):
    for file in Path(f"data/{dir}").glob("*/*/*"):
        path_list = str(file).split("/")
        path_list.pop(1)
        path_list.insert(1, "combined")
        newfile = "/".join(path_list)
        shutil.copy(file, newfile)
