from pathlib import Path

folders = ['data', 'src', 'sql', 'test']
layers = ['bronze', 'silver', 'gold']
files = ['README.md', 'requirements.txt', '.gitignore', 'main.py']

for folder in folders:
    Path(folder).mkdir(exist_ok=True)

for layer in layers:
    Path('data', layer).mkdir(parents=True, exist_ok=True)

for file in files:
    Path(file).touch(exist_ok=True)

print("Project structure created successfully!")