# Transcripción verificada de la Guía de Problemas 2026

Cada `tema_<X>.json` es la transcripción revisada contra el PDF (imagen de cada página) de los
ejercicios de ese tema. `herramientas/armar_guia.py` los une en `datos/guia_ejercicios.json`.

Formato: lista de ejercicios, cada uno:

```json
{
  "id": "VII-1", "tema": "VII", "numero": 1,
  "pagina": 51,                       // número impreso "51 de 62"
  "planteo": "texto del enunciado antes de los incisos; las tablas van aplanadas fila por fila",
  "tablas": [{"titulo": "", "columnas": ["Área (10^6 ha)", "PBI"], "filas": [[3.0402, 8.014]]}],
  "incisos": [{"letra": "a", "texto": "...",
               "respuesta": "texto de la Resp de ese inciso",
               "valores": [8.488544]}],   // números clave de la respuesta (ver abajo)
  "respuesta": "texto completo de la Resp tal cual",
  "respuesta_fuente": "resp" | "solucion" | "ninguna",
  "resuelto": true,                   // la guía trae una Solución desarrollada
  "conclusiones": ["oraciones de conclusión de la Solución, si hay"],
  "observaciones": "dudas: texto ilegible, respuesta que parece inconsistente, etc."
}
```

- Números en JSON con punto decimal (la guía usa coma decimal y punto de miles: 5.401.000 → 5401000).
- Si el ejercicio no tiene incisos, un único inciso con `"letra": "única"` y el texto de la consigna.
- `valores`: solo los resultados numéricos (límites de IC, n, Δn, β, valores críticos, estadísticos,
  coeficientes de la recta, r...). No poner los datos del enunciado. Los porcentajes como en la guía.
- Si no hay `Resp:` pero la Solución trae resultados, armar la respuesta desde la Solución y poner
  `respuesta_fuente: "solucion"`.
- NO corregir la guía: si una respuesta parece mal, se transcribe igual y se anota en `observaciones`.
