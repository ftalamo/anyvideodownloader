📦 Any Video Downloader
Any Video Downloader is a sleek, minimalist, and futuristic web application built with Python + Flask that allows users to download videos from social media and video platforms using yt-dlp — right from their browser.

🚀 Features

🧠 Modular, extensible, and decoupled Flask backend

📥 Download any video via a single URL input

🎯 Responsive, elegant UI built with TailwindCSS (via CDN)

⚡ Direct browser downloads — no file management required

🐳 Docker-ready for fast and clean deployment

🛠️ Tech Stack
Python 3.11

Flask

yt-dlp

TailwindCSS (CDN)

Docker

📂 Project Structure
bash
Copiar
Editar
.
├── app/
│   ├── service/
│   │   └── downloader.py   # yt-dlp download logic
│   └── templates/
│       └── index.html      # Web interface
├── main.py                 # Flask entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image config
└── docker-compose.yml      # Optional orchestration

▶️ Getting Started
bash
Copiar
Editar
# Build the Docker image
docker build -t any-video-downloader .

# Run the app
docker run -p 5000:5000 any-video-downloader
Then open your browser at: http://localhost:5000