from argparse import ArgumentParser

def create_parser() -> ArgumentParser:
    """
    Crea un parser de argumentos para la conversión de PDF a CBZ.
    
    Returns:
        argparse.ArgumentParser: El parser de argumentos configurado.
    """
    parser = ArgumentParser(
        prog="CBZConvert",
        description="Convierte archivos PDF a CBZ.",
        epilog="Ejemplo de uso: cbz_convert convert input.pdf -o output_folder -q 85 -f jpg",
        add_help=True,
        allow_abbrev=True,
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Comando a ejecutar. Usa 'convert' para convertir un PDF a CBZ."
    )

    # -------------------------------------------
    # Subcommand: version
    # -------------------------------------------
    subparsers.add_parser("version", help="Shows CLI version")

    # -------------------------------------------
    # Subcommand: convert
    # -------------------------------------------
    convert_parser = subparsers.add_parser("convert", help="Convert a pdf file")
    convert_parser.add_argument("input_file", type=str, help="Path to the input PDF file.")
    convert_parser.add_argument("-o", "--output_folder", type=str, default=".", help="Path to the output folder where the CBZ file will be saved. Default is the current directory.")
    convert_parser.add_argument("-q", "--quality", type=int, default=85, help="Quality of the images in the CBZ file (1-100). Default is 85.")
    convert_parser.add_argument("-f", "--format", type=str, choices=["jpeg", "png", "webp", "tiff"], default="jpg", help="Image format for the CBZ file. Choices are 'jpg' or 'png'. Default is 'jpg'.")

    return parser