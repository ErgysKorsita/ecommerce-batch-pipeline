from pathlib import Path
import shutil

source = [
    Path.home() / "Downloads" / "ecommerce_Brazil_dataset" , 
]

destination = [
    Path('data') / 'bronze' / 'ecommerce_Brazil_dataset',
]

for src, dest in zip(source, destination, strict=True):
    shutil.copytree(src, dest, dirs_exist_ok=True)

print('Raw data uploaded!')