from rich.progress import (
    Progress, 
    BarColumn, 
    TextColumn, 
)
from rich.console import Console

from cbz_convert.enums import ProgressStage
from cbz_convert.utils.callback_type import ProgressUpdate

class SimpleRichProgress:
    """Versión simplificada para casos donde no necesitas tanto control."""
    def __init__(self):
        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[icon]} {task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=Console(),
            transient=False
        )
        self.task_id = None
        
    def __enter__(self):
        self.progress.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()
    
    def handle_update(self, update: ProgressUpdate):
        """Maneja actualizaciones de progreso de forma sencilla."""
        
        if update.stage == ProgressStage.START:
            self.task_id = self.progress.add_task(
                description="Iniciando...",
                icon="🚀",
                total=update.total
            )
            
        elif update.stage == ProgressStage.LOADING:
            if self.task_id:
                self.progress.update(
                    self.task_id,
                    description=f"Cargando página {update.current}",
                    icon="📖",
                    completed=update.current
                )
                
        elif update.stage == ProgressStage.SAVING:
            if self.task_id:
                self.progress.update(
                    self.task_id,
                    description=f"Guardando página {update.current}",
                    icon="💾",
                    completed=update.current
                )
                
        elif update.stage == ProgressStage.COMPLETE:
            if self.task_id:
                self.progress.update(
                    self.task_id,
                    description="¡Completado!",
                    icon="✅",
                    completed=update.total
                )