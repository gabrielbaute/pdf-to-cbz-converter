import sys
from cbz_convert.cli.parser import create_parser
from cbz_convert.cli.commands import convert_single_file, convert_batch
from cbz_convert.cli.version import __version__, show_version

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.version:
        show_version()
        sys.exit(0)
    
    if args.pdf_path.endswith(".pdf"):
        convert_single_file(
            pdf_path=args.pdf_path,
            output_folder=args.output_folder,
            quality=args.quality,
            format=args.format
        )
    else:
        convert_batch(
            folder_path=args.pdf_path,
            output_folder=args.output_folder,
            quality=args.quality,
            format=args.format
        )
