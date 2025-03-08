# PDF to CBZ Converter

Este es un script en Python que convierte archivos PDF a archivos CBZ (un formato común para cómics y mangas). El script extrae las páginas del PDF como imágenes, las comprime en un archivo CBZ y elimina los archivos temporales.

## Características

- Convierte PDFs a CBZs de manera rápida y eficiente.
- Soporta formatos de imagen JPG y PNG.
- Permite ajustar la calidad de compresión de las imágenes.
- Conversión por lotes: procesa todos los PDFs en una carpeta y sus subcarpetas.
- Interfaz de consola interactiva.

## Requisitos

- Python 3.7 o superior.
- Bibliotecas: `PyMuPDF` (`fitz`), `Pillow`, `tqdm`.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/gabrielbaute/pdf-to-cbz-converter
   cd pdf-to-cbz-converter
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Coloca tus archivos PDF en una carpeta.
2. Ejecuta el script:
   ```bash
   python main.py
   ```
3. Sigue las instrucciones en la consola para seleccionar la carpeta, la calidad de compresión y el formato de salida.

## Ejemplo

```bash
$ python main.py
Ingresa la ruta del directorio con los PDFs: C:/Users/gabri/Videos/cbz
Ingresa la calidad de compresión (1-100, recomendado 85): 85
Ingresa el formato de salida (jpg o png): jpg
```

## Contribuir

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Haz commit de tus cambios (`git commit -m 'Añade nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.