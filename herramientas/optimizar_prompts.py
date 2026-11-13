"""Banco para probar variantes de los prompts de las dos IA del consenso, sin sobreajustar.

    python -X utf8 herramientas/optimizar_prompts.py base guia            # afinar: solo con la guía
    python -X utf8 herramientas/optimizar_prompts.py sin_persona guia --lectores ia
    python -X utf8 herramientas/optimizar_prompts.py base validacion      # al final: exámenes reales + raros
    python -X utf8 herramientas/optimizar_prompts.py --comparar base sin_persona guia

Método (para no sesgar la IA a estos casos):
- Se AFINA solo con la guía (cada ejercicio excluido de sus propios ejemplos).
- Se VALIDA al final, sin mirar los errores, con los exámenes reales (no están en la guía) y los enunciados raros
  (ejercicios de la guía reescritos: se excluye también el ejercicio de origen).
- Solo cambios genéricos (formato, longitud, orden, cantidad de ejemplos), nunca frases de un ejercicio.
- La base se corre dos veces para medir el ruido; un cambio se adopta si mejora más que el ruido.

Resultados 11/11 (fracción por ejercicio; ruido base vs base2: ±1 guía, ±0,3 validación):
- sin_persona: guía ia +1,5 / ia_tema ±0; validación ia +1,0 → ADOPTADO (ya es la base).
- sin_claves_tema: guía ia +1,7 pero validación ia −4,1 (−5 completos) → descartado: sobreajusta a la guía.
- ej1 / ej3: peor o mixto → se quedan 2 ejemplos. reglas_al_final: neutro.
- pt_sin_lectura: neutro en guía y validación; se deja (es la única guía de tail/criterio en ia_tema).

Cada lectura se mide como en la app (`consenso._leer`): la IA arma el JSON, las reglas completan lo que sale de las
tablas y el solver resuelve. Resultados por ítem en herramientas/tmp/prompts/<variante>__<lector>__<banco>.json.
"""

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))

import evaluar_guia as eg  # noqa: E402
from evaluar_examenes import cumple  # noqa: E402
from asistente import interpretar as itp, por_tema as pt  # noqa: E402
from asistente.interpretar import completar_con_reglas, lista_incisos, pedir_ia  # noqa: E402
from asistente.por_tema import pedir_ia_tema  # noqa: E402
from interprete.resolver import resolver  # noqa: E402

SALIDA = RAIZ / "herramientas" / "tmp" / "prompts"

# ---------------------------------------------------------------------------- variantes
# Cada variante cambia atributos de los módulos (se restauran al terminar). Solo cambios GENÉRICOS.
ORIG = {"itp.SISTEMA": itp.SISTEMA, "pt.COMUNES": pt.COMUNES, "pt.UNA_DOS_POB": pt.UNA_DOS_POB,
        "itp.N": itp.N_EJEMPLOS, "pt.N": pt.N_EJEMPLOS}


def _sin_persona_itp(s: str) -> str:
    viejo = ("Sos un asistente que INTERPRETA enunciados de Estadística Aplicada (UADE, cátedra Dopazo - García) y "
             "los traduce a un JSON que después resuelve un programa. Vos NO calculás nada: solo leés el enunciado y "
             "anotás qué tema es, qué datos da y qué pide cada inciso.")
    return s.replace(viejo, "Traducí el enunciado de Estadística a un JSON (tema, datos, qué pide cada inciso). No "
                            "calcules nada: un programa resuelve después.")


def _sin_persona_pt(s: str) -> str:
    viejo = ("Sos un asistente que INTERPRETA un enunciado de Estadística Aplicada (UADE, cátedra Dopazo – García) y lo "
             "traduce a un JSON que resuelve un programa. NO calculás nada: anotás el tema, los datos que da el "
             "enunciado y qué pide cada inciso.")
    return s.replace(viejo, "Traducí el enunciado de Estadística a un JSON (tema, datos, qué pide cada inciso). No "
                            "calcules nada: un programa resuelve después.")


def _sin_claves_tema(s: str) -> str:
    i = s.find("\nCLAVES PERMITIDAS SEGÚN EL TEMA")
    assert i > 0
    return s[:i]


def _reglas_al_final(s: str) -> str:
    i, j = s.find("Reglas:"), s.find("TEMAS (campo")
    assert 0 < i < j
    return s[:i] + s[j:] + "\n\n" + s[i:j].strip()


VARIANTES = {
    "base": {},
    "base2": {},                                   # repetición: mide el ruido
    "sin_persona": {"itp.SISTEMA": lambda: _sin_persona_itp(ORIG["itp.SISTEMA"]),
                    "pt.COMUNES": lambda: _sin_persona_pt(ORIG["pt.COMUNES"])},
    "ej1": {"itp.N": lambda: 1, "pt.N": lambda: 1},
    "ej3": {"itp.N": lambda: 3, "pt.N": lambda: 3},
    "sin_claves_tema": {"itp.SISTEMA": lambda: _sin_claves_tema(ORIG["itp.SISTEMA"])},
    "reglas_al_final": {"itp.SISTEMA": lambda: _reglas_al_final(ORIG["itp.SISTEMA"])},
    "pt_sin_lectura": {"pt.UNA_DOS_POB": lambda: ""},
    # combinaciones de lo que no empeoró por separado
    "compacto": {"itp.SISTEMA": lambda: _sin_claves_tema(_sin_persona_itp(ORIG["itp.SISTEMA"])),
                 "pt.COMUNES": lambda: _sin_persona_pt(ORIG["pt.COMUNES"])},
    "compacto_min": {"itp.SISTEMA": lambda: _sin_claves_tema(_sin_persona_itp(ORIG["itp.SISTEMA"])),
                     "pt.COMUNES": lambda: _sin_persona_pt(ORIG["pt.COMUNES"]), "pt.UNA_DOS_POB": lambda: ""},
}


def aplicar(nombre: str):
    for clave, val in ORIG.items():                 # primero restaurar
        _poner(clave, val)
    for clave, f in VARIANTES[nombre].items():
        _poner(clave, f())


def _poner(clave, val):
    mod, attr = clave.split(".")
    m = {"itp": itp, "pt": pt}[mod]
    setattr(m, {"N": "N_EJEMPLOS"}.get(attr, attr), val)


# ---------------------------------------------------------------------------- lectura (como consenso._leer)

def leer(lector, planteo, incisos, tablas, excluir):
    an, _ = (pedir_ia if lector == "ia" else pedir_ia_tema)(planteo, incisos, tablas, None, excluir=excluir)
    pl, lista = lista_incisos(planteo, incisos)
    completar_con_reglas(an, pl, lista, an.tablas or None)
    return an


# ---------------------------------------------------------------------------- bancos

def items(banco):
    if banco == "guia":
        return [("guia", e) for e in eg.GUIA]
    if banco == "validacion":
        ex = json.loads((RAIZ / "datos" / "examenes_reales.json").read_text(encoding="utf-8"))
        ra = json.loads(eg.RAROS.read_text(encoding="utf-8"))
        return [("examen", e) for e in ex] + [("raro", r) for r in ra]
    raise SystemExit(f"banco desconocido: {banco}")


def puntuar(lector, tipo, e):
    """-> (id, aciertos, total)"""
    try:
        if tipo == "guia":
            planteo, incisos = eg.entradas(e)
            an = leer(lector, planteo, incisos, e.get("tablas") or None, [e["id"]])
            _, tot, ok, _, dtot, dok = eg.evaluar(e, obtener=lambda *a: an)
            return e["id"], ok + dok, tot + dtot
        if tipo == "examen":
            incisos = [tuple(i) for i in e["incisos"]] if e["incisos"] else None
            an = leer(lector, e["planteo"], incisos, e["tablas"], [])
            res = resolver(an)
            esp = [x for x in e["esperado"]]
            ok = sum(1 for r, x in zip(res, esp) if x is not None and cumple(r, x))
            return e["id"], ok, sum(x is not None for x in esp)
        # raro: excluir también el ejercicio de la guía del que sale
        ej = eg.como_guia(e)
        incisos = [(i["letra"], i["texto"]) for i in e["incisos"]] or None
        an = leer(lector, e["enunciado"], incisos, ej["tablas"] or None, [e["id"], e.get("ejercicio_origen", "")])
        res = resolver(an)
        ok = tot = 0
        for inc, r, guia, nums in eg.emparejar(ej, an, res):
            esperado = guia.get("valores", []) or []
            tot += len(esperado)
            ok += sum(1 for v in esperado if eg.coincide(v, nums))
            if guia.get("decision"):
                tot += 1
                ok += eg.decision_de(r) == guia["decision"]
        return e["id"], ok, tot
    except Exception as ex:   # noqa: BLE001 — una lectura rota cuenta como 0
        tot = (sum(len(i.get("valores") or []) + bool(i.get("decision")) for i in e["incisos"])
               if tipo == "guia" else 0)
        return e["id"], 0, tot or 1


def correr(variante, banco, lectores, hilos):
    aplicar(variante)
    SALIDA.mkdir(parents=True, exist_ok=True)
    trabajos = [(l, t, e) for l in lectores for t, e in items(banco)]
    t0 = time.time()
    with ThreadPoolExecutor(hilos) as pool:
        res = list(pool.map(lambda x: (x[0],) + puntuar(*x), trabajos))
    aplicar("base")
    for l in lectores:
        filas = {i: (ok, tot) for lec, i, ok, tot in res if lec == l}
        (SALIDA / f"{variante}__{l}__{banco}.json").write_text(json.dumps(filas), encoding="utf-8")
        ok, tot = sum(v[0] for v in filas.values()), sum(v[1] for v in filas.values())
        print(f"{variante:14} {l:8} {banco:11} {ok}/{tot} ({100 * ok / max(1, tot):.1f}%)")
    print(f"   {time.time() - t0:.0f} s")


def comparar(a, b, banco):
    for l in ("ia", "ia_tema"):
        fa, fb = SALIDA / f"{a}__{l}__{banco}.json", SALIDA / f"{b}__{l}__{banco}.json"
        if not (fa.exists() and fb.exists()):
            continue
        A, B = json.loads(fa.read_text()), json.loads(fb.read_text())
        mejor = [k for k in A if B.get(k, [0])[0] > A[k][0]]
        peor = [k for k in A if B.get(k, [0])[0] < A[k][0]]
        print(f"{l}: {a} {sum(v[0] for v in A.values())} → {b} {sum(v[0] for v in B.values())}  "
              f"(mejoran {len(mejor)} ejercicios, empeoran {len(peor)})")


def main():
    args = sys.argv[1:]
    if args[0] == "--comparar":
        return comparar(*args[1:4])
    lectores = args[args.index("--lectores") + 1].split(",") if "--lectores" in args else ["ia", "ia_tema"]
    hilos = int(args[args.index("--hilos") + 1]) if "--hilos" in args else 4
    correr(args[0], args[1], lectores, hilos)


if __name__ == "__main__":
    main()
