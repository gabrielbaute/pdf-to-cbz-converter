import os
import shutil
import zipfile
import fitz
from tqdm import tqdm
from PIL import Image

class PDFtoCBZConverter:
    def __init__(self, pdf_path, output_folder="images_temp", quality=85):
        """
        Inicializa el conversor de PDF a CBZ.
        
        :param pdf_path: Ruta al archivo PDF.
        :param output_folder: Carpeta temporal para guardar las imágenes.
        :param quality: Calidad de compresión para imágenes JPG (1-100).
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")
        
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.quality = quality
        self.cbz_path = os.path.join(
            os.path.dirname(pdf_path),
            os.path.splitext(os.path.basename(pdf_path))[0] + ".cbz"
        )

    def _pdf_to_images(self, format="jpg"):
        """
        Convierte un PDF a imágenes (JPG o PNG).
        
        :param format: Formato de salida de las imágenes ("jpg" o "png").
        """
        # Abre el archivo PDF
        pdf_document = fitz.open(self.pdf_path)
        
        # Crea la carpeta de salida si no existe
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        # Itera sobre cada página del PDF
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            # Extrae la imagen sin escalar (resolución original)
            pix = page.get_pixmap()
            image_path = os.path.join(self.output_folder, f"page_{page_number + 1}.{format}")
            
            # Guarda la imagen en el formato especificado
            if format == "jpg":
                # Convierte la imagen a JPG con la calidad especificada
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.save(image_path, format="JPEG", quality=self.quality)
            elif format == "webp":
                img.save(image_path, format="WEBP", quality=self.quality)
            elif format == "tiff":
                img.save(image_path, format="TIFF")
            else:
                # Para otros formatos (como PNG), guarda sin compresión de calidad
                pix.save(image_path)

    def _images_to_cbz(self):
        """
        Comprime las imágenes en un archivo CBZ.
        """
        with zipfile.ZipFile(self.cbz_path, 'w') as cbz_file:
            for image_name in sorted(os.listdir(self.output_folder)):
                if image_name.endswith(('.jpg', '.png')):  # Acepta JPG y PNG
                    image_path = os.path.join(self.output_folder, image_name)
                    cbz_file.write(image_path, arcname=image_name)

    def _cleanup(self):
        """
        Elimina la carpeta temporal de imágenes.
        """
        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)

    def convert_to_cbz(self, format="jpg"):
        """
        Convierte un PDF a CBZ.
        
        :param format: Formato de salida de las imágenes ("jpg" o "png").
        """
        try:
            # Convierte el PDF a imágenes
            self._pdf_to_images(format)
            
            # Crea el archivo CBZ
            self._images_to_cbz()
        except Exception as e:
            tqdm.write(f"Error durante la conversión: {e}")
        
        finally:
            # Limpieza: elimina la carpeta temporal
            self._cleanup()

    @staticmethod
    def convert_folder_to_cbz(folder_path, output_folder="images_temp", quality=85, format="jpg"):
        """
        Convierte todos los PDFs en una carpeta y sus subcarpetas a CBZ.
        """
        # Recopila todos los archivos PDF
        pdf_files = []
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith(".pdf"):
                    pdf_files.append(os.path.join(root, filename))
        
        # Procesa los archivos con una barra de progreso
        for pdf_path in tqdm(pdf_files, desc="Convirtiendo PDFs", unit="archivo"):
            try:
                converter = PDFtoCBZConverter(pdf_path, output_folder, quality)
                converter.convert_to_cbz(format)
                tqdm.write(f"Procesando: {os.path.basename(pdf_path)}", end="\r")
            except Exception as e:
                tqdm.write(f"Error al procesar {os.path.basename(pdf_path)}: {e}")
        
        # Limpia la línea final
        print(" " * 100, end="\r")  # Limpia la línea
        print("Proceso completado.")