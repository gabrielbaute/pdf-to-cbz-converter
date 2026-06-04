from enum import StrEnum

class ProgressStage(StrEnum):
    """
    Etapas del proceso de conversión.

    Attributes:
        START (str): Etapa de inicio de la conversión.
        LOADING (str): Etapa de carga del PDF.
        SAVING (str): Etapa de guardado de las imágenes en el CBZ.
        COMPLETE (str): Etapa de finalización exitosa.
        ERROR (str): Etapa de error durante la conversión.
        NONE (str): Etapa sin estado específico.
    """
    START = "start"
    LOADING = "loading"
    SAVING = "saving"
    COMPLETE = "complete"
    ERROR = "error"
    NONE = "none"
    
    @staticmethod
    def map_stage(stage: str) -> 'ProgressStage':
        """
        Convierte el nombre en string de una etapa a su representación enum.

        Args:
            stage (str): Nombre en string de la etapa.

        Returns:
            ProgressStage: Representación enum de la etapa.
        """
        stages = {
            "start": ProgressStage.START,
            "loading": ProgressStage.LOADING,
            "saving": ProgressStage.SAVING,
            "complete": ProgressStage.COMPLETE,
            "error": ProgressStage.ERROR,
            "none": ProgressStage.NONE
        }
        return stages.get(stage.lower(), ProgressStage.NONE)