from rich.progress import (
    Progress, 
    BarColumn, 
    TextColumn, 
    TimeRemainingColumn,
)
from rich.console import Console
from rich.panel import Panel

from cbz_convert.enums import ProgressStage
from cbz_convert.utils.callback_type import ProgressUpdate

class RichProgressHandler:
    """
    Manejador de progreso que usa Rich para visualización. Este manejador se encarga de mostrar el progreso de la conversión de PDF a CBZ utilizando barras de progreso y paneles informativos.
    """
    def __init__(self):
        self.console = Console()
        self.progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=self.console,
            transient=False,  # Mantener la barra después de completar
        )
        self.current_task = None
        self.current_stage = ""
        
    def __enter__(self):
        self.progress.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()
    
    def handle_update(self, update: ProgressUpdate):
        """
        Maneja una actualización de progreso.

        Args:
            update (ProgressUpdate): La actualización de progreso a manejar.
        """
        if update.stage == ProgressStage.START:
            # Crear nueva tarea
            if self.current_task:
                self.progress.remove_task(self.current_task)
            
            self.current_task = self.progress.add_task(
                description=f"[cyan]📄 {update.message}",
                total=update.total
            )
            self.current_stage = ProgressStage.LOADING
            
        elif update.stage == ProgressStage.LOADING:
            if self.current_task:
                # Actualizar descripción para mostrar página actual
                self.progress.update(
                    self.current_task,
                    description=f"[cyan]📖 Cargando página {update.current}/{update.total}",
                    completed=update.current
                )
                
        elif update.stage == ProgressStage.SAVING:
            # Si cambiamos de fase, reiniciamos la tarea
            if self.current_stage != ProgressStage.SAVING:
                if self.current_task:
                    self.progress.remove_task(self.current_task)
                self.current_task = self.progress.add_task(
                    description=f"[green]💾 {update.message}",
                    total=update.total
                )
                self.current_stage = ProgressStage.SAVING
            else:
                # Actualizar progreso de guardado
                self.progress.update(
                    self.current_task,
                    description=f"[green]💾 Guardando página {update.current}/{update.total}",
                    completed=update.current
                )
                
        elif update.stage == ProgressStage.COMPLETE:
            # Completar la tarea actual
            if self.current_task:
                self.progress.update(
                    self.current_task,
                    description=f"[bold green]{update.message}",
                    completed=update.total
                )
            # Mostrar panel con información final
            self.console.print()
            self.console.print(Panel(
                f"[bold green]✓ Conversión exitosa[/bold green]\n"
                f"📁 Archivo generado: {update.message.split(':')[1].strip() if ':' in update.message else 'desconocido'}",
                title="✨ Completado",
                border_style="green"
            ))
            
        elif update.stage == ProgressStage.ERROR:
            # Manejar error
            if self.current_task:
                self.progress.remove_task(self.current_task)
            self.console.print()
            self.console.print(Panel(
                f"[bold red]Error durante la conversión[/bold red]\n{update.message}",
                title="❌ Error",
                border_style="red"
            ))

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