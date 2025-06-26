from playwright.sync_api import sync_playwright
import subprocess


def extract_m3u8(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        m3u8_url = None

        def intercept_route(route, request):
            nonlocal m3u8_url
            if ".m3u8" in request.url:
                m3u8_url = request.url
                route.abort()
            else:
                route.continue_()

        page.route("**/*", intercept_route)
        page.goto(url, wait_until='networkidle')

        # Esperamos unos segundos por si tarda en cargar
        page.wait_for_timeout(5000)
        browser.close()

        return m3u8_url

def descargar_video(url_video):
    print(f"Buscando .m3u8 en: {url_video}")
    m3u8 = extract_m3u8(url_video)
    if m3u8:
        print(f"Descargando desde: {m3u8}")
        subprocess.run(["yt-dlp", m3u8])
    else:
        print("❌ No se encontró una URL .m3u8 válida.")

# Ejemplo de uso
descargar_video("https://www.tokyvideo.com/es/video/la-sopa-de-piedras-2016-pelicula-de-animacion-infantil-completa")
