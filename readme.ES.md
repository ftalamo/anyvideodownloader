📦 Any Video Downloader
Any Video Downloader es una aplicación web minimalista y futurista, desarrollada con Python + Flask, que te permite descargar videos desde redes sociales y plataformas de video usando yt-dlp, directamente desde tu navegador.

🚀 Características

🧠 Backend en Flask con lógica desacoplada y extensible

📥 Descarga automática de videos desde una URL

🎯 Interfaz web responsive y elegante con TailwindCSS vía CDN

⚡ Descarga directa al navegador sin pasos intermedios

🐳 Docker-ready para despliegue rápido y limpio

🛠️ Tecnologías usadas
Python 3.11

Flask

yt-dlp

TailwindCSS (CDN)

Docker

📂 Estructura del proyecto
bash
Copiar
Editar
.
├── app/
│   ├── service/
│   │   └── downloader.py  # Lógica de descarga con yt-dlp
│   └── templates/
│       └── index.html     # Interfaz web
├── main.py                # Entry point de Flask
├── requirements.txt       # Dependencias
├── Dockerfile             # Imagen Docker personalizada
└── docker-compose.yml     # Orquestación opcional

▶️ Cómo usar
bash
Copiar
Editar
# Construir la imagen
docker build -t any-video-downloader .

# Correr la app
docker run -p 5000:5000 any-video-downloader
Luego abre tu navegador en: http://localhost:5000