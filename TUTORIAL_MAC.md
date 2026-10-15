# Tutorial: IA local en la Mac

Pasos 1 y 2 una sola vez, con internet. Después funciona sin conexión.

## 1. Instalar Ollama

Descargar e instalar la app desde <https://ollama.com/download> (o `brew install ollama`).
Al abrirla queda corriendo en segundo plano (ícono de la llama en la barra de menú).

## 2. Descargar el modelo

```bash
ollama pull qwen3:8b
```

Opcional, más preciso pero más lento: `ollama pull qwen3:14b`.

## 3. Usar la app

Todo junto, con un solo comando (desde la carpeta del proyecto):

```bash
./levantar.sh
```

Si la IA no está andando, la levanta; si falta el modelo, lo descarga; lo deja cargado en memoria y abre la app en
el navegador. Mientras corre, la Mac no se suspende. `Ctrl+C` para cerrar. Sin IA: `./levantar.sh --sin-ia`.

A mano (lo mismo, paso por paso):

```bash
git pull
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

- **Interpretar un enunciado**: *🤖 Interpretar con IA* y, después de calcular, *💬 Explicar con IA*.
- **Asistente IA**: chat libre (dudas, material propio, *🧮 Resolver mi mensaje con la app*).
- El modelo y el modo "Razonar" se eligen en la barra lateral.

## Comandos útiles de Ollama

| Comando | Para qué |
|---|---|
| `ollama list` | Ver los modelos descargados |
| `ollama run qwen3:8b` | Chatear en la terminal (sirve para probar que anda; `/bye` para salir) |
| `ollama ps` | Ver qué modelo está cargado en memoria |
| `ollama serve` | Levantar Ollama a mano si la app no está abierta |
| `ollama rm qwen3:14b` | Borrar un modelo |

## Antes del examen

1. Medir el modelo contra la guía: `python herramientas/evaluar_guia.py --ia --limite 30`
2. Apagar el Wi-Fi y probar que todo anda.
3. Hacer una pregunta en *Asistente IA* unos minutos antes para que el modelo quede cargado.

Más detalles en `ASISTENTE_IA.md`.
