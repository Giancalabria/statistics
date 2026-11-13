"""¿La redacción final se parece a lo que escribió el profesor en el pizarrón? (ejercicios resueltos en clase)

    python -X utf8 herramientas/comparar_redaccion_clase.py                 # temas del 2° parcial (III a VII)
    python -X utf8 herramientas/comparar_redaccion_clase.py --solo IV-1 V-12
    python -X utf8 herramientas/comparar_redaccion_clase.py --hilos 3       # en paralelo (Ollama con NUM_PARALLEL ≥ 3)

Necesita Ollama. Mide la REDACCIÓN, no la interpretación: el planteo sale de las reglas (como si el alumno ya lo
hubiera controlado), el solver hace las cuentas y la IA redacta A CIEGAS: el ejemplo de ESTILO_CATEDRA.md de ese
mismo ejercicio no se le manda (`excluir`). Mismo flujo que la app: redacción, checklist y una vuelta de corrección
que se queda solo si baja la cantidad de fallas.

Por ejercicio se compara contra el planteo del profesor (datos/clase_resueltos.json, sacado de las grabaciones):
- números: qué valores calculados del pizarrón aparecen en la redacción (no cuenta los datos del enunciado);
- pasos: si el profesor escribió H0/H1, un fractil con su argumento, CR, RD, la expresión formal P(…), la decisión
  y el criterio, ¿la redacción también?
- el checklist de la cátedra (incluye «Números sin su cuenta»).

Informe completo, con el profesor y la redacción lado a lado: herramientas/tmp/comparar_redaccion_clase.md
"""

import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))

from asistente.explicar import enunciado_texto  # noqa: E402
from asistente.redactar import controlar, corregir, problemas, redactar  # noqa: E402
from evaluar_clase import cargar, entrada  # noqa: E402
from interprete.analizador import analizar  # noqa: E402
from interprete.origen import conocidos  # noqa: E402
from interprete.resolver import resolver  # noqa: E402
from interprete.texto import buscar_numeros  # noqa: E402

TEMAS_PARCIAL = ("III", "IV", "V", "VI", "VII")

# pasos que se buscan: (nombre, patrón en el texto del profesor, patrón en la redacción)
PASOS = [
    ("H0 / H1", r"H0|H₀", r"H0|H₀"),
    ("fractil con argumento", r"\b(?:F|t|z|Z|χ²|G_b|G|F_b)\s*\(\s*0?,?\d", r"\b(?:F|t|z|Z|χ²|G_b|G|F_b)\s*\(\s*0?,?\d"),
    ("CR", r"\bCR\b|[<>≤≥]\s*\w*c\b|rc\s*=", r"\bCR\b|condici[oó]n de rechazo"),
    ("RD", r"\bRD\b", r"\bRD\b|regla de decisi[oó]n"),
    ("expresión formal P(…)", r"P\([^)]*≤[^)]*≤", r"P\s*\([^)]*≤[^)]*≤"),
    ("decisión", r"se rechaza|no se rechaza", r"se rechaza|no se rechaza"),
    ("criterio", r"pesimista|optimista", r"pesimista|optimista"),
]


def _decimales(crudo: str) -> int:
    c = crudo.replace("%", "").strip()
    return len(c.rsplit(",", 1)[1]) if "," in c else 0


def numeros_del_profesor(texto: str, enunciado: str):
    """Valores calculados del pizarrón: sin enteros chicos ni datos del enunciado."""
    base = conocidos(enunciado)
    salida = []
    for n in buscar_numeros(texto):
        v = n.valor / 100 if n.pct else n.valor
        if float(n.valor).is_integer() and abs(n.valor) <= 20:
            continue
        if any(abs(v - k) < 1e-9 for k in base):
            continue
        salida.append((v, n.crudo.strip()))
    return list(dict(((round(v, 6), c), None) for v, c in salida))


def aparece(v: float, crudo: str, texto: str) -> bool:
    """El valor está en la redacción, con la misma cifra o redondeado distinto en la última (0,2036 ~ 0,2035)."""
    tol = 1.01 * 10 ** -max(_decimales(crudo), 0) if _decimales(crudo) else 0.5
    for n in buscar_numeros(texto):
        w = n.valor / 100 if n.pct else n.valor
        if abs(abs(w) - abs(v)) <= max(tol, 10 ** -_decimales(n.crudo)) + 1e-9:
            return True
    return False


def secciones(texto: str):
    partes = re.split(r"(?m)^#{2,4}\s*(?:inciso\s+)?(única|[a-h](?:\.[a-h])?)\)", texto, flags=re.IGNORECASE)
    out = {}
    for k in range(1, len(partes) - 1, 2):
        out[partes[k].lower()] = out.get(partes[k].lower(), "") + partes[k + 1]
    return out


def comparar(ej, guia, modelo=None):
    planteo, incisos, tablas = entrada(guia[ej["guia"]])
    an = analizar(planteo, incisos, tablas=tablas)
    res = resolver(an)
    t0 = time.time()
    trozos, fuentes = redactar(an, res, modelo=modelo, excluir=[ej["guia"]])
    texto = "".join(trozos)
    fallas = problemas(controlar(texto, an, fuentes, res))
    corregida = False
    if fallas:
        texto2 = "".join(corregir(an, res, texto, fallas, modelo=modelo, excluir=[ej["guia"]]))
        fallas2 = problemas(controlar(texto2, an, fuentes, res))
        if len(fallas2) < len(fallas):
            texto, fallas, corregida = texto2, fallas2, True
    seg = time.time() - t0
    enun = enunciado_texto(an)
    secs = secciones(texto)
    filas = []
    for k, prof in enumerate(ej["profesor"]):
        inc = an.incisos[k] if k < len(an.incisos) else None
        letra = inc.letra.lower() if inc else "?"
        sec = secs.get(letra) or (texto if len(ej["profesor"]) == 1 else "")
        nums = numeros_del_profesor(prof, enun)
        hallados = [c for v, c in nums if aparece(v, c, sec)]
        faltan = [c for v, c in nums if not aparece(v, c, sec)]
        pasos = [(nombre, bool(re.search(p_ia, sec, re.IGNORECASE)))
                 for nombre, p_prof, p_ia in PASOS if re.search(p_prof, prof)]
        filas.append(dict(letra=letra, profesor=prof, hallados=hallados, faltan=faltan, pasos=pasos))
    return dict(id=ej["guia"], clase=ej["clase"], texto=texto, fallas=fallas, corregida=corregida, seg=seg,
                filas=filas)


def main():
    args = sys.argv[1:]
    solo = args[args.index("--solo") + 1:] if "--solo" in args else []
    solo = [s for s in solo if not s.startswith("--")]
    hilos = int(args[args.index("--hilos") + 1]) if "--hilos" in args else 1
    banco, guia = cargar()
    elegidos = [e for e in banco if (e["guia"] in solo if solo else e["guia"].split("-")[0] in TEMAS_PARCIAL)]
    with ThreadPoolExecutor(max_workers=hilos) as pool:
        resultados = list(pool.map(lambda e: comparar(e, guia), elegidos))

    tot_n = tot_h = tot_p = tot_pok = 0
    resumen, detalle = [], []
    for r in resultados:
        n = sum(len(f["hallados"]) + len(f["faltan"]) for f in r["filas"])
        h = sum(len(f["hallados"]) for f in r["filas"])
        p = sum(len(f["pasos"]) for f in r["filas"])
        pok = sum(ok for f in r["filas"] for _, ok in f["pasos"])
        tot_n, tot_h, tot_p, tot_pok = tot_n + n, tot_h + h, tot_p + p, tot_pok + pok
        sin_cuenta = next((f for f in r["fallas"] if f.startswith("Números sin su cuenta")), "")
        resumen.append(f"| {r['id']} | {h}/{n} | {pok}/{p} | {len(r['fallas'])} | "
                       f"{'sí' if sin_cuenta else 'no'} | {'sí' if r['corregida'] else 'no'} | {r['seg']:.0f} s |")
        detalle.append(f"\n## {r['id']} (clase del {r['clase']})\n")
        for f in r["filas"]:
            detalle.append(f"### {f['letra']})\n\n**Profesor:** {f['profesor']}\n")
            detalle.append(f"- Números del pizarrón en la redacción: {len(f['hallados'])}/"
                           f"{len(f['hallados']) + len(f['faltan'])}" +
                           (f" — faltan: {', '.join(f['faltan'])}" if f["faltan"] else ""))
            detalle.append("- Pasos: " + (", ".join(f"{n} {'✔' if ok else '✘'}" for n, ok in f["pasos"]) or "—") + "\n")
        detalle.append("**Checklist:** " + ("; ".join(r["fallas"]) if r["fallas"] else "todo ✔") + "\n")
        detalle.append("<details><summary>Redacción de la IA</summary>\n\n" + r["texto"] + "\n\n</details>\n")

    cab = ["# Redacción de la IA vs. el pizarrón del profesor", "",
           f"Números del pizarrón encontrados: **{tot_h}/{tot_n}** · pasos del profesor presentes: **{tot_pok}/{tot_p}**",
           "", "| Ejercicio | Números | Pasos | Fallas del checklist | Números sin cuenta | Corregida | Tiempo |",
           "|---|---|---|---|---|---|---|"]
    informe = "\n".join(cab + resumen) + "\n" + "\n".join(detalle)
    salida = RAIZ / "herramientas" / "tmp" / "comparar_redaccion_clase.md"
    salida.parent.mkdir(exist_ok=True)
    salida.write_text(informe, encoding="utf-8")
    print("\n".join(cab + resumen))
    print(f"\nInforme: {salida}")


if __name__ == "__main__":
    main()
