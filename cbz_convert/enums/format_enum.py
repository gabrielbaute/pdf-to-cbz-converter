from enum import StrEnum

class Format(StrEnum):
    """
    Formatos de imagen soportados.

    Attributes:
        JPEG (str): Formato JPEG.
        PNG (str): Formato PNG.
        WEBP (str): Formato WEBP.
        TIFF (str): Formato TIFF.
    """
    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"
    TIFF = "tiff"

    @staticmethod
    def map_format(format: str) -> 'Format':
        """
        Convierte el nombre en string de un formato a su representación enum.

        Args:
            format (str): Nombre en string del formato.

        Returns:
            Format: Representación enum del formato.
        """
        formats = {
            "jpeg": Format.JPEG,
            "png": Format.PNG,
            "webp": Format.WEBP,
            "tiff": Format.TIFF,
        }
        return formats.get(format.lower(), Format.JPEG)