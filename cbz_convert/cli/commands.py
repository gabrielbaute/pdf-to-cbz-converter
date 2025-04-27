from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from cbz_convert.core.converter import PDFtoCBZConverter

console = Console()

def convert_single_file(pdf_path, output_folder, quality, format):
    """Convierte un único archivo PDF a CBZ."""
    console.print(f"[bold blue]Procesando archivo:[/bold blue] {pdf_path}")
    
    try:
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            "[green]{task.percentage:>3.0f}%",
            console=console
        ) as progress:
            task = progress.add_task("Convirtiendo PDF...", total=1)
            
            converter = PDFtoCBZConverter(pdf_path, output_folder, quality)
            converter.convert_to_cbz(format)
            
            progress.update(task, advance=1)
        
        console.print("[bold green]¡Conversión completada con éxito![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error durante la conversión:[/bold red] {e}")

def convert_batch(folder_path, output_folder, quality, format):
    """Convierte todos los archivos PDF en un directorio a CBZ."""
    console.print(f"[bold blue]Procesando directorio:[/bold blue] {folder_path}")
    
    try:
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            "[green]{task.percentage:>3.0f}%",
            console=console
        ) as progress:
            # Recopilar archivos PDF
            converter_task = progress.add_task("Buscando PDFs...", total=None)
            PDFtoCBZConverter.convert_folder_to_cbz(
                folder_path=folder_path,
                output_folder=output_folder,
                quality=quality,
                format=format
            )
            progress.update(converter_task, completed=True)
        
        console.print("[bold green]¡Conversión en lote completada con éxito![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error durante la conversión en lote:[/bold red] {e}")