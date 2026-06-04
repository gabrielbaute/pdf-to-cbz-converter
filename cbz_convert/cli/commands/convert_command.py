# cbz_convert/cli/commands/convert.py
"""
Comando para convertir un PDF a CBZ utilizando la clase ConverterService.

Este comando se encarga de manejar la lógica de conversión, incluyendo la gestión de errores y la actualización del progreso durante el proceso de conversión.
"""
from pathlib import Path
from rich.console import Console

from cbz_convert.enums import Format
from cbz_convert.cli.utils import RichProgressHandler
from cbz_convert.utils.callback_type import ProgressUpdate
from cbz_convert.services.converter_service import ConverterService

def convert(
        input_path: Path, 
        output_path: Path, 
        console: Console, 
        quality: int = 85,
        format: Format = Format.JPEG
    ) -> None:
    """
    Comando para convertir un PDF a CBZ.

    Args:
        input_path (Path): Ruta del archivo PDF de entrada.
        output_path (Path): Ruta del archivo CBZ de salida.
        console (Console): Instancia de Rich Console para mostrar mensajes y progreso.
        quality (int): Calidad de las imágenes en el CBZ (85 por defecto).
        format (Format): Formato de imagen para el archivo CBZ (JPEG por defecto).

    Returns:
        None
    """
    # Validar que el archivo de entrada existe
    if not input_path.exists():
        console.print(f"[red]❌ Error: El archivo {input_path} no existe[/red]")
        return

    # Asegurar que el directorio de salida existe
    output_path.mkdir(parents=True, exist_ok=True)

    convert_service = ConverterService(
        input_path=input_path, 
        output_path=output_path
    )

    with RichProgressHandler() as progress_handler:
        success = convert_service.convert_pdf_to_cbz(
            format=format,
            quality=quality,
            progress_callback=progress_handler.handle_update
        )
        
        if not success:
            console.print("[red]❌ La conversión falló. Revisa los mensajes de error arriba.[/red]")