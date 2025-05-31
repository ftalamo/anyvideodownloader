from urllib.parse import urlparse


def detect_url(url):
    try:
        resultado = urlparse(url)
        netloc = resultado.netloc
        if not netloc:
            return None
        nombre_dominio = netloc.split('.')
        nombre_dominio = '.'.join(nombre_dominio[:-1])
        if 'www.' in nombre_dominio:
            nombre_dominio = nombre_dominio.split('.')
            nombre_dominio = '.'.join(nombre_dominio[1:])
        return nombre_dominio
    except Exception as e:
        print(f"Error al procesar la URL: {e}")
        return None
