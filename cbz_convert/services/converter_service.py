import shutil
import fitz
import logging
from PIL import Image
from pathlib import Path
from zipfile import ZipFile
from fitz import Document, Page
from typing import List, Optional, Union, Callable

from cbz_convert.enums import Format, ProgressStage
from cbz_convert.utils.callback_type import ProgressUpdate

# Callback type for progress updates
ProgressCallback = Callable[[ProgressUpdate], None]

class ConverterService:
    """
    Servicio para convertir archivos PDF a CBZ.
    """
    def __init__(
            self, 
            input_path: Union[str, Path], 
            output_path: Union[str, Path], 
            temp_folder: Path = "temp"
        ):
        """
        Inicializa el servicio de conversión de PDF a CBZ.

        Args:
            input_path (Union[str, Path]): Ruta al archivo PDF de entrada.
            output_path (Union[str, Path]): Ruta al archivo CBZ de salida.
            temp_folder (Path): Carpeta temporal para guardar las imágenes.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.temp_folder = Path(temp_folder)
        
        # Aseguramos que los directorios se creen:
        self.temp_folder.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def _load_document(self) -> Document:
        """
        Carga el documento PDF.

        Returns:
            Document: El documento PDF cargado.
        """
        if not self.input_path.exists():
            raise FileNotFoundError(f"El archivo PDF no existe: {self.input_path}")
        return fitz.open(self.input_path)

    def _load_page(self, document: Document, page_number: int) -> Page:
        """
        Carga una página específica del documento PDF.

        Args:
            document (Document): El documento PDF.
            page_number (int): El número de página a cargar.

        Returns:
            Page: La página cargada.
        """
        self.logger.debug(f"Cargando página {page_number}...")
        return document.load_page(page_number)
    
    def _collect_images(
            self, 
            document: Document, 
            progress_callback: Optional[ProgressCallback] = None
        ) -> List[Image.Image]:
        """
        Colecta las imágenes de un documento PDF.

        Args:
            document (Document): El documento PDF.
            progress_callback (Optional[ProgressCallback]): Callback para actualizar el progreso. Función que recibe (página_actual, total_páginas).

        Returns:
            List[Image.Image]: Lista de imágenes.
        """
        images = []
        pages = len(document)
        self.logger.info(f"Número de páginas a analizar: {pages}")

        for page_number in range(pages):
            page = self._load_page(document, page_number)
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(image)

            if progress_callback:
                progress_callback(
                    ProgressUpdate(
                        current=page_number + 1, 
                        total=pages, 
                        stage=ProgressStage.LOADING, 
                        page_number=page_number + 1, 
                        message=f"Cargando página {page_number + 1}/{pages}"
                    )
                )

        self.logger.info(f"Imágenes recopiladas: {len(images)}")
        return images
    
    def convert_pdf_to_cbz(
            self, 
            format: Format = Format.JPEG, 
            quality: Optional[int] = 85,
            progress_callback: Optional[ProgressCallback] = None
        ) -> bool:
        """
        Convierte un archivo de PDF a CBZ.
        Args:
            format (Format): El formato de salida de las imágenes.
            quality (Optional[int]): Calidad de compresión para imágenes JPG (1-100).
            progress_callback (Optional[ProgressCallback]): Callback para actualizar el progreso. Función que recibe (página_actual, total_páginas).

        Returns:
            bool: True si la conversión fue exitosa, False en caso contrario.
        """
        if quality > 100 or quality < 1:
            raise ValueError("Valor no permitido. La calidad debe estar entre 1 y 100.")
        
        cbz_output = self.output_path / f"{self.input_path.stem}.cbz"
        
        try:
            document = self._load_document()
            total_pages = len(document)
            
            # Notificar inicio
            if progress_callback:
                progress_callback(ProgressUpdate(
                    current=0,
                    total=total_pages,
                    stage=ProgressStage.START,
                    message=f"Iniciando conversión de {total_pages} páginas..."
                ))
            
            # Fase 1: Cargar imágenes del PDF
            images = self._collect_images(document, progress_callback)
            
            # Notificar cambio de fase
            if progress_callback:
                progress_callback(ProgressUpdate(
                    current=0,
                    total=len(images),
                    stage=ProgressStage.SAVING,
                    message=f"Guardando {len(images)} imágenes en CBZ..."
                ))
            
            # Fase 2: Guardar imágenes en CBZ
            with ZipFile(cbz_output, 'w') as cbz_file:
                for i, image in enumerate(images):
                    image_path = self.temp_folder / f"page_{i + 1}.{format.value}"
                    image.save(image_path, format=format.value, quality=quality)
                    cbz_file.write(image_path, arcname=f"page_{i + 1}.{format.value}")

                    if progress_callback:
                        progress_callback(ProgressUpdate(
                            current=i + 1,
                            total=len(images),
                            stage=ProgressStage.SAVING,
                            page_number=i + 1,
                            message=f"Guardando página {i + 1}/{len(images)}"
                        ))
            
            # Notificar completado
            if progress_callback:
                progress_callback(ProgressUpdate(
                    current=total_pages,
                    total=total_pages,
                    stage=ProgressStage.COMPLETE,
                    message=f"✅ Conversión completada: {cbz_output.name}"
                ))
            
            shutil.rmtree(self.temp_folder)
            return True
        except Exception as e:
            self.logger.error(f"Error durante la conversión: {e}")
            if progress_callback:
                progress_callback(ProgressUpdate(
                    current=0,
                    total=0,
                    stage=ProgressStage.ERROR,
                    message=f"❌ Error: {str(e)}"
                ))
            return False
        finally:
            if self.temp_folder.exists():
                shutil.rmtree(self.temp_folder)