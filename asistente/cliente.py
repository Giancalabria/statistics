"""Cliente mínimo de la API local de Ollama (solo biblioteca estándar, sin dependencias nuevas).

    from asistente import cliente
    cliente.disponible()                       # ¿está corriendo Ollama?
    cliente.chat([{"role": "user", "content": "hola"}])
    for trozo in cliente.chat(mensajes, stream=True): ...
"""

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, Iterator, List, Optional, Union

HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
if not HOST.startswith("http"):
    HOST = "http://" + HOST
MODELO = os.environ.get("ASISTENTE_MODELO", "qwen3:8b")

# Contexto suficiente para el enunciado + ejemplos de la guía + apuntes (Ollama trae 2048-4096 por defecto).
NUM_CTX = int(os.environ.get("ASISTENTE_NUM_CTX", "12288"))
TIMEOUT = 600


class ErrorIA(RuntimeError):
    pass


def _pedir(ruta: str, cuerpo: Optional[Dict] = None, timeout: float = TIMEOUT):
    datos = json.dumps(cuerpo).encode("utf-8") if cuerpo is not None else None
    req = urllib.request.Request(HOST + ruta, data=datos, headers={"Content-Type": "application/json"},
                                 method="POST" if datos else "GET")
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", "replace")
        try:
            detalle = json.loads(detalle).get("error", detalle)
        except ValueError:
            pass
        raise ErrorIA(f"Ollama respondió {e.code}: {detalle}") from e
    except (urllib.error.URLError, OSError) as e:
        raise ErrorIA(f"No se pudo conectar con Ollama en {HOST} ({e}). ¿Está abierto? (`ollama serve`)") from e


def disponible(timeout: float = 2) -> bool:
    try:
        with _pedir("/api/tags", timeout=timeout):
            return True
    except ErrorIA:
        return False


def modelos(timeout: float = 5) -> List[str]:
    """Modelos descargados (`ollama list`)."""
    with _pedir("/api/tags", timeout=timeout) as r:
        return [m["name"] for m in json.load(r).get("models", [])]


def modelo_instalado(nombre: str, instalados: List[str]) -> bool:
    """'qwen3:8b' está en ['qwen3:8b'], y 'qwen3' equivale a 'qwen3:latest'."""
    nombre = nombre if ":" in nombre else nombre + ":latest"
    return nombre in instalados


def chat(mensajes: List[Dict[str, str]], modelo: Optional[str] = None, formato: Union[None, str, Dict] = None,
         stream: bool = False, temperatura: float = 0.2, pensar: Optional[bool] = False,
         num_ctx: Optional[int] = None) -> Union[str, Iterator[str]]:
    """Manda la conversación al modelo.

    - `formato`: un JSON Schema (o "json") para forzar la salida estructurada.
    - `pensar`: modo razonamiento de los modelos que lo tienen (Qwen3, DeepSeek-R1...): más preciso pero
      bastante más lento. None = lo que traiga el modelo por defecto.
    - `stream`: devuelve un iterador de trozos de texto (para mostrarlo mientras se genera).
    """
    cuerpo: Dict[str, Any] = {
        "model": modelo or MODELO,
        "messages": mensajes,
        "stream": stream,
        "keep_alive": "30m",
        "options": {"temperature": temperatura, "num_ctx": num_ctx or NUM_CTX},
    }
    if formato is not None:
        cuerpo["format"] = formato
    if pensar is not None:
        cuerpo["think"] = pensar
    try:
        r = _pedir("/api/chat", cuerpo)
    except ErrorIA as e:
        if "think" in cuerpo and "think" in str(e).lower():
            cuerpo.pop("think")          # el modelo no tiene modo razonamiento: se pide sin la opción
            r = _pedir("/api/chat", cuerpo)
        else:
            raise
    if stream:
        return _trozos(r)
    with r:
        return json.load(r).get("message", {}).get("content", "")


def _trozos(r) -> Iterator[str]:
    with r:
        for linea in r:
            if not linea.strip():
                continue
            evento = json.loads(linea)
            if evento.get("error"):
                raise ErrorIA(evento["error"])
            texto = evento.get("message", {}).get("content", "")
            if texto:
                yield texto
            if evento.get("done"):
                break
