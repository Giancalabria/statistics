"""Consultas a la IA en segundo plano: siguen aunque cambies de página, y al volver ves lo que lleva o el resultado.

Streamlit corta el script de la página cuando te vas a otra, y con él la respuesta que se estaba generando. Por eso
cada consulta larga corre en un hilo propio que no toca Streamlit: va dejando en un objeto `Tarea` (guardado en la
sesión) en qué etapa está y el texto que genera; la página lo muestra mientras avanza y toma el resultado al final.

    t = Tarea("Chat", "pages/8_Asistente_IA.py")
    lanzar(t, funcion, arg1, arg2)       # funcion(t, arg1, arg2) corre en otro hilo; lo que devuelve -> t.resultado
"""

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, Optional


@dataclass
class Tarea:
    titulo: str                     # para el aviso de la barra lateral («Redacción», «Chat»...)
    pagina: str                     # archivo de la página que la lanzó (para volver a ella)
    etapa: str = ""                 # qué está haciendo ahora («Resolviendo con la app…»)
    texto: str = ""                 # lo que lleva generado (se muestra a medida que llega)
    extra: Dict[str, Any] = field(default_factory=dict)   # resultados parciales para mostrar mientras sigue
    resultado: Any = None
    error: Optional[BaseException] = None
    terminada: bool = False
    inicio: float = field(default_factory=time.time)

    def escribir(self, trozos: Iterable[str]) -> str:
        """Consume un stream de texto dejándolo en `texto` a medida que llega; devuelve el texto completo."""
        self.texto = ""
        for trozo in trozos:
            self.texto += trozo
        return self.texto

    def segundos(self) -> float:
        return time.time() - self.inicio


def lanzar(tarea: Tarea, funcion: Callable[..., Any], *args, **kwargs) -> Tarea:
    """Corre `funcion(tarea, *args, **kwargs)` en un hilo aparte. La función no debe usar Streamlit."""
    def correr():
        try:
            tarea.resultado = funcion(tarea, *args, **kwargs)
        except Exception as e:          # se muestra en la página al recoger la tarea
            tarea.error = e
        finally:
            tarea.terminada = True

    threading.Thread(target=correr, name=f"ia-{tarea.titulo}", daemon=True).start()
    return tarea
