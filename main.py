from flask import Flask, render_template, request, send_file, after_this_request
from app.service.downloader import Downloader
from app.service.downloader_vimeo import VimeoD
from app.service.urldetector import  detect_url
from app.service.socialnetworkdetector import detectar_red_social
import glob
import os
import jsonify
import time
import threading


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def borrar_luego(path, delay=10):
    def borra():
        time.sleep(delay)
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error borrando archivo {path}: {e}")
    threading.Thread(target=borra).start()


@app.route("/descargar", methods=["POST"])
def descargar():
    url = request.form.get("url")
    mensaje = ""
    try:
        domain = detect_url(url)
        sites = ['vimeo', 'espn','tokyvideo', 'crunchyroll']
        if any(site in domain for site in sites):
            return jsonify({"error": "Notenemos soporte actualmente para este dominio"}), 500
        social = detectar_red_social(url)
        downloader = Downloader(url, social)
        downloader.download()
        mensaje = "✅ Video descargado correctamente."
        # Buscar el archivo más reciente en la carpeta PATH
        list_files = glob.glob(os.path.join(downloader.output_path, "*"))
        if not list_files:
            return jsonify({"error": "No se encontró el archivo descargado"}), 500

        latest_file = max(list_files, key=os.path.getctime)

        # Enviar el archivo como descarga directa
        respuesta = send_file(
            latest_file,
            as_attachment=True,
            download_name=os.path.basename(latest_file)
        )
        borrar_luego(latest_file, delay=10)
        return respuesta
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)