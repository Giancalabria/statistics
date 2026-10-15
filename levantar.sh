#!/bin/zsh
# Levanta todo para usar la app: la IA local (Ollama + qwen3:8b) si hace falta, y la app en el navegador.
#
#   ./levantar.sh            (desde la carpeta del proyecto; o `zsh levantar.sh`)
#   ./levantar.sh --sin-ia   (solo la app, sin tocar Ollama)
#
# Mientras corre, la Mac no se suspende. Para cortar: Ctrl+C.

cd "$(dirname "$0")"
MODELO="${ASISTENTE_MODELO:-qwen3:8b}"
PY=".venv/bin/python"

if [[ ! -x "$PY" ]]; then
  echo "❌ No encuentro el entorno .venv. Crealo con:  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  exit 1
fi

ia_responde() { curl -s -m 2 http://localhost:11434/api/tags > /dev/null; }

if [[ "$1" != "--sin-ia" ]]; then
  if ! command -v ollama > /dev/null; then
    echo "⚠️  Ollama no está instalado: la app anda igual, pero sin IA (instalalo con: brew install ollama)."
  else
    if ia_responde; then
      echo "✅ La IA (Ollama) ya estaba funcionando."
    else
      echo "⏳ Levantando la IA (Ollama)…"
      if command -v brew > /dev/null && brew services list 2>/dev/null | grep -q '^ollama'; then
        brew services start ollama > /dev/null
      else
        nohup ollama serve > /tmp/ollama.log 2>&1 &
      fi
      for i in {1..30}; do ia_responde && break; sleep 1; done
      if ia_responde; then echo "✅ IA levantada."; else echo "⚠️  Ollama no respondió: la app anda igual, sin IA."; fi
    fi
    if ia_responde; then
      if ! ollama list | awk 'NR>1 {print $1}' | grep -qx "$MODELO"; then
        echo "⏳ Falta el modelo $MODELO: descargándolo (5 GB, una sola vez)…"
        ollama pull "$MODELO"
      fi
      echo "⏳ Cargando $MODELO en memoria para que la primera consulta no tarde…"
      curl -s -m 120 http://localhost:11434/api/generate \
        -d "{\"model\": \"$MODELO\", \"prompt\": \"\", \"keep_alive\": \"60m\"}" > /dev/null \
        && echo "✅ Modelo listo." || echo "⚠️  No pude precargar el modelo (se carga en la primera consulta)."
    fi
  fi
fi

echo "🚀 Abriendo la app en el navegador (Ctrl+C para cerrarla)…"
exec caffeinate -dims "$PY" -m streamlit run app.py
