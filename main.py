import os
from convert.pdf_to_cbz import PDFtoCBZConverter

def ask_for_directory(prompt):
    """
    Pide al usuario que ingrese una ruta y la normaliza.
    """
    while True:
        path = input(prompt)
        path = os.path.normpath(path)  # Normaliza la ruta (usa \ o / según el sistema)
        if os.path.exists(path):
            return path
        print(f"La ruta '{path}' no existe. Inténtalo de nuevo.")

if __name__ == "__main__":
    # Preguntar al usuario por la ruta del directorio
    folder_path = ask_for_directory("Ingresa la ruta del directorio con los PDFs: ")
    
    # Preguntar al usuario por la calidad de compresión
    quality = int(input("Ingresa la calidad de compresión (1-100, recomendado 85): "))
    
    # Preguntar al usuario por el formato de salida
    format = input("Ingresa el formato de salida (jpg o png): ").lower()
    while format not in ["jpg", "png"]:
        print("Formato no válido. Usa 'jpg' o 'png'.")
        format = input("Ingresa el formato de salida (jpg o png): ").lower()
    
    # Convertir todos los PDFs en la carpeta
    PDFtoCBZConverter.convert_folder_to_cbz(folder_path, quality=quality, format=format)