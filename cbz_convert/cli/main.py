import sys
from pathlib import Path
from rich.console import Console

from cbz_convert.enums import Format
from cbz_convert.services import LogService
from cbz_convert.cli.parser import create_parser
from cbz_convert.cli.commands.convert_command import convert
from cbz_convert.cli.commands.version_command import show_version

def main():
    #LogService.setup_logging(level="INFO")
    parser = create_parser()
    console = Console()
    args = parser.parse_args()

    if args.command == "convert":
        input_path = Path(args.input_file)
        output_folder = Path(args.output_folder)
        quality = args.quality
        
        selected_format = Format.map_format(args.format)
        
        convert(
            input_path=input_path,
            output_path=output_folder,
            console=console,
            quality=quality,
            format=selected_format
        )
    
    elif args.command == "version":
        show_version(console)
    
    elif args.command == "help":
        parser.print_help()
        sys.exit(1)
    
    else:
        console.print(f"[red]❌ Comando desconocido: {args.command}[/red]")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[yellow]⚠️ Proceso interrumpido por el usuario[/yellow]")
        sys.exit(130)
    except Exception as e:
        console = Console()
        console.print(f"[red]❌ Error no manejado: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)