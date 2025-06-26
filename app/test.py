import requests
import re
import json
from urllib.parse import unquote


def obtener_url_directa_vimeo(video_id):
    """
    Extrae la URL directa del video de Vimeo usando diferentes métodos
    """
    print(f"Extrayendo URL directa para video ID: {video_id}")

    # Método 1: API no oficial de Vimeo
    urls_directas = []

    try:
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://vimeo.com/',
            'Origin': 'https://vimeo.com'
        }

        # URL del player embebido
        player_url = f"https://player.vimeo.com/video/{video_id}"
        print(f"Accediendo al player: {player_url}")

        response = requests.get(player_url, headers=headers)
        response.raise_for_status()

        # Buscar configuración JSON en el HTML
        config_patterns = [
            r'window\.playerConfig\s*=\s*({.*?});',
            r'"config":\s*({.*?"video".*?})',
            r'var\s+config\s*=\s*({.*?});',
            r'playerConfig\s*=\s*({.*?});'
        ]

        config_data = None
        for pattern in config_patterns:
            matches = re.findall(pattern, response.text, re.DOTALL)
            for match in matches:
                try:
                    # Limpiar el JSON
                    json_str = match.strip()
                    if json_str.endswith(','):
                        json_str = json_str[:-1]

                    config_data = json.loads(json_str)
                    print("✓ Configuración JSON encontrada")
                    break
                except json.JSONDecodeError:
                    continue
            if config_data:
                break

        if config_data:
            urls_directas = extraer_urls_de_config(config_data)

        # Método 2: Buscar directamente en el HTML
        if not urls_directas:
            print("Método 1 falló, intentando extracción directa...")
            urls_directas = extraer_urls_html(response.text)

        # Método 3: API endpoint alternativo
        if not urls_directas:
            print("Método 2 falló, probando API alternativa...")
            urls_directas = extraer_con_api_alternativa(video_id, headers)

        return urls_directas

    except Exception as e:
        print(f"Error en extracción: {e}")
        return []


def extraer_urls_de_config(config_data):
    """
    Extrae URLs de video desde la configuración JSON
    """
    urls = []

    try:
        # Estructura típica de Vimeo
        if 'video' in config_data and 'files' in config_data['video']:
            files = config_data['video']['files']

            for file_info in files:
                if 'link_secure' in file_info:
                    url_info = {
                        'url': file_info['link_secure'],
                        'quality': f"{file_info.get('width', '?')}x{file_info.get('height', '?')}",
                        'size_mb': round(file_info.get('size', 0) / (1024 * 1024), 1) if file_info.get('size') else 0,
                        'type': file_info.get('type', 'video/mp4')
                    }
                    urls.append(url_info)
                    print(f"✓ URL encontrada: {url_info['quality']} ({url_info['size_mb']} MB)")

        # Buscar en otras estructuras posibles
        elif 'request' in config_data and 'files' in config_data['request']:
            files = config_data['request']['files']
            for quality, file_data in files.items():
                if isinstance(file_data, dict) and 'url' in file_data:
                    url_info = {
                        'url': file_data['url'],
                        'quality': quality,
                        'size_mb': 0,
                        'type': 'video/mp4'
                    }
                    urls.append(url_info)
                    print(f"✓ URL encontrada: {quality}")

    except Exception as e:
        print(f"Error extrayendo de config: {e}")

    return urls


def extraer_urls_html(html_content):
    """
    Busca URLs de video directamente en el HTML
    """
    urls = []

    # Patrones para URLs de video
    patterns = [
        r'"link_secure":"([^"]*)"',
        r'"url":"(https://[^"]*\.mp4[^"]*)"',
        r"'url':'(https://[^']*\.mp4[^']*)'",
        r'https://[^"\s]*vod-progressive[^"\s]*\.mp4[^"\s]*',
        r'https://[^"\s]*skyfire[^"\s]*\.mp4[^"\s]*'
    ]

    for pattern in patterns:
        matches = re.findall(pattern, html_content)
        for match in matches:
            # Limpiar URL (puede estar escapada)
            clean_url = match.replace('\\/', '/').replace('\\u0026', '&')
            if clean_url.startswith('http') and '.mp4' in clean_url:
                url_info = {
                    'url': clean_url,
                    'quality': 'unknown',
                    'size_mb': 0,
                    'type': 'video/mp4'
                }
                urls.append(url_info)
                print(f"✓ URL directa encontrada en HTML")

    return urls


def extraer_con_api_alternativa(video_id, headers):
    """
    Intenta usar endpoints alternativos de Vimeo
    """
    urls = []

    try:
        # Endpoint de configuración
        config_url = f"https://player.vimeo.com/video/{video_id}/config"
        response = requests.get(config_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'request' in data and 'files' in data['request']:
                files = data['request']['files']
                for quality, file_info in files.items():
                    if isinstance(file_info, dict) and 'url' in file_info:
                        url_info = {
                            'url': file_info['url'],
                            'quality': quality,
                            'size_mb': 0,
                            'type': 'video/mp4'
                        }
                        urls.append(url_info)
                        print(f"✓ URL desde API alternativa: {quality}")

    except Exception as e:
        print(f"API alternativa falló: {e}")

    return urls


def validar_y_mostrar_urls(urls):
    """
    Valida las URLs encontradas y las muestra ordenadas
    """
    if not urls:
        print("❌ No se encontraron URLs directas")
        return []

    print(f"\n=== {len(urls)} URLs ENCONTRADAS ===")

    # Ordenar por calidad (aproximada)
    def calidad_a_numero(quality_str):
        if 'x' in quality_str:
            try:
                width = int(quality_str.split('x')[0])
                return width
            except:
                return 0
        elif any(q in quality_str.lower() for q in ['720', '1080', '480', '360']):
            return int(''.join(filter(str.isdigit, quality_str)))
        return 0

    urls_ordenadas = sorted(urls, key=lambda x: calidad_a_numero(x['quality']), reverse=True)

    for i, url_info in enumerate(urls_ordenadas, 1):
        print(f"\n{i}. Calidad: {url_info['quality']}")
        print(f"   Tamaño: {url_info['size_mb']} MB")
        print(f"   Tipo: {url_info['type']}")
        print(f"   URL: {url_info['url'][:80]}...")

        # Validar URL
        try:
            head_response = requests.head(url_info['url'], timeout=10)
            if head_response.status_code == 200:
                print(f"   ✅ URL válida")
            else:
                print(f"   ⚠️ URL responde con código: {head_response.status_code}")
        except:
            print(f"   ❓ No se pudo validar")

    return urls_ordenadas


def obtener_url_completa(url_info):
    """
    Retorna la URL completa lista para descargar
    """
    return url_info['url']


def main():
    """
    Función principal
    """
    video_url = "https://vimeo.com/1086974424?autoplay=1&muted=1&stream_id=ZmVhdHVyZWR8fGlkOmRlc2N8eyJyZW1vdmVfdm9kX3RpdGxlcyI6ZmFsc2V9"

    # Extraer ID del video
    video_id_match = re.search(r'vimeo\.com/(\d+)', video_url)
    if not video_id_match:
        print("❌ No se pudo extraer el ID del video")
        return

    video_id = video_id_match.group(1)
    print(f"🎬 Procesando video ID: {video_id}")
    print(f"🔗 URL original: {video_url}")

    # Extraer URLs directas
    urls_directas = obtener_url_directa_vimeo(video_id)

    # Validar y mostrar
    urls_validas = validar_y_mostrar_urls(urls_directas)

    if urls_validas:
        print(f"\n🎉 MEJOR URL DIRECTA:")
        mejor_url = urls_validas[0]
        url_final = obtener_url_completa(mejor_url)
        print(f"📺 Calidad: {mejor_url['quality']}")
        print(f"💾 Tamaño: {mejor_url['size_mb']} MB")
        print(f"🔗 URL: {url_final}")

        # Copiar al portapapeles si es posible
        try:
            import pyperclip
            pyperclip.copy(url_final)
            print("📋 URL copiada al portapapeles")
        except ImportError:
            print("💡 Instala 'pyperclip' para copiar automáticamente al portapapeles")

        return url_final
    else:
        print("❌ No se pudieron extraer URLs directas del video")
        print("💡 Posibles causas:")
        print("   - El video está privado o restringido")
        print("   - Vimeo ha cambiado su estructura")
        print("   - Se requiere autenticación")
        return None


if __name__ == "__main__":
    url_directa = main()