from typing import NamedTuple, Optional

from cbz_convert.enums import ProgressStage

class ProgressUpdate(NamedTuple):
    """
    Formato de actualización de progreso.

    Attributes:
        current (int): Página actual.
        total (int): Total de páginas.
        stage (ProgressStage): Etapa: "loading" o "saving".
        page_number (Optional[int]): Número de página específica (1-indexed).
        message (Optional[str]): Mensaje adicional para mostrar.
    """
    current: int
    total: int
    stage: ProgressStage
    page_number: Optional[int] = None 
    message: Optional[str] = None