import argparse

def create_parser():
    """Crea un parser de argumentos para la conversión de PDF a CBZ.
    Returns:
        argparse.ArgumentParser: El parser de argumentos configurado.
    """
    parser = argparse.ArgumentParser(
        prog="cbz_convert",
        description="Convierte archivos PDF a CBZ.",
        epilog="Ejemplo: cbz_convert archivo.pdf --format jpg --quality 90 --output_folder salida/")

    parser.add_argument("-v", "--version", action="store_true", help="Mostrar versión y salir")
    parser.add_argument("pdf_path", help="Ruta al archivo o carpeta de PDFs.")
    parser.add_argument("-f", "--format", default="jpg", choices=["jpg", "png"], help="Formato de salida para las imágenes.")
    parser.add_argument("-q", "--quality", type=int, default=85, help="Calidad de las imágenes (1-100).")
    parser.add_argument("--output_folder", default=None, help="Carpeta temporal para guardar las imágenes.")

    return parser