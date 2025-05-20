import os
from app.config.ydl_config import PATH

def search_directory():
    if not os.path.exists(PATH):
        os.makedirs(PATH)
        print(f"✅ Directorio creado: {PATH}")
    else:
        print(f"📁 El directorio ya existe: {PATH}")

