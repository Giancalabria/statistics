# Tutorial: transcribir los audios de las clases (PC con Windows y placa AMD)

Para qué sirve: con las clases transcriptas se pueden sacar los ejercicios que el profesor resuelve en clase, con
sus frases textuales y el minuto, y usarlos como ejemplos reales en `ESTILO_CATEDRA.md` (lo que lee la IA para
redactar como pide la cátedra).

Se usa **whisper.cpp** con **Vulkan**, que aprovecha la placa AMD (las versiones de Whisper de OpenAI y
`faster-whisper` solo usan la GPU con placas NVIDIA; con una AMD correrían en el procesador, varias veces más
lento). Todo es local y gratis: los audios no se suben a ningún lado.

Pasos 1 a 3 una sola vez. Después, el paso 4 transcribe todos los audios de una carpeta.

> **Sin probar en esa PC.** La guía se armó sin acceso a la computadora con Windows. Lo que más probablemente no
> coincida está en [Si algo no coincide](#si-algo-no-coincide), al final.

## 1. Instalar lo necesario

1. **Driver de la placa** al día: AMD Software: Adrenalin Edition, desde <https://www.amd.com/es/support>.
2. **Vulkan SDK**: <https://vulkan.lunarg.com/sdk/home> → Windows → instalar con las opciones por defecto.
3. **Visual Studio Build Tools 2022**: <https://visualstudio.microsoft.com/es/downloads/> (abajo, en
   *Herramientas para Visual Studio*). En el instalador, marcar **Desarrollo para el escritorio con C++**.
4. **Git, CMake y FFmpeg**, en una terminal (PowerShell):

   ```powershell
   winget install Git.Git Kitware.CMake Gyan.FFmpeg
   ```

Cerrar y volver a abrir la terminal para que encuentre los programas recién instalados. Comprobar:

```powershell
git --version; cmake --version; ffmpeg -version
```

> Si en <https://github.com/ggml-org/whisper.cpp/releases> hay un `.zip` para Windows con **vulkan** en el
> nombre, se puede bajar ese y saltear la compilación del paso 2 (el ejecutable es `whisper-cli.exe`). Igual hace
> falta FFmpeg.

## 2. Compilar whisper.cpp con Vulkan

```powershell
cd $HOME
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp
cmake -B build -DGGML_VULKAN=1
cmake --build build -j --config Release
```

Tarda unos minutos. El programa queda en `build\bin\Release\whisper-cli.exe`.

## 3. Bajar el modelo y probar con 10 minutos de audio

```powershell
cd $HOME\whisper.cpp
.\models\download-ggml-model.cmd large-v3-turbo
```

(Si el script no anda, bajar `ggml-large-v3-turbo.bin` de <https://huggingface.co/ggerganov/whisper.cpp> y
guardarlo en `whisper.cpp\models\`.)

Prueba corta, para ver que use la placa y medir la velocidad:

```powershell
ffmpeg -y -i "C:\ruta\a\una_clase.mp3" -t 600 -ar 16000 -ac 1 -c:a pcm_s16le prueba.wav
.\build\bin\Release\whisper-cli.exe -m models\ggml-large-v3-turbo.bin -f prueba.wav -l es -otxt -of prueba
```

- Al arrancar tiene que mostrar algo como `ggml_vulkan: Found 1 Vulkan devices: ... AMD Radeon RX 9070 XT`. Si
  no aparece, está usando solo el procesador: revisar el driver y el Vulkan SDK, y volver a compilar.
- Mirar cuánto tardó en los 10 minutos y multiplicar por 24 para estimar una clase de 4 horas. Con la placa
  debería ser del orden de minutos, no de horas.
- Abrir `prueba.txt` y ver que se entienda. Si la calidad es floja, probar con el modelo `large-v3` (más lento,
  un poco más preciso): `.\models\download-ggml-model.cmd large-v3`.

## 4. Transcribir todas las clases

Guardar esto como `transcribir.ps1` (por ejemplo en `$HOME\Clases\`) y ajustar las dos carpetas de arriba:

```powershell
# Transcribe todos los audios de $Audios a $Salida (.srt con minutos + .txt). Si se corta, al volver a
# correrlo saltea los que ya están.
param(
    [string]$Audios  = "$HOME\Clases\audios",
    [string]$Salida  = "$HOME\Clases\transcripciones",
    [string]$Whisper = "$HOME\whisper.cpp",
    [string]$Modelo  = "large-v3-turbo"
)

$cli = Join-Path $Whisper "build\bin\Release\whisper-cli.exe"
$bin = Join-Path $Whisper "models\ggml-$Modelo.bin"
# Vocabulario de la materia: ayuda a que escriba bien los términos técnicos
$prompt = "Clase de Estadística aplicada. Hipótesis nula H0, H1, alfa, beta, chi cuadrado, grados de libertad, " +
          "frecuencias observadas y esperadas, desvío estándar, F de Snedecor, t de Student, región crítica, " +
          "condición de rechazo, regla de decisión, regresión."
$tmp = Join-Path $env:TEMP "whisper_clase.wav"
New-Item -ItemType Directory -Force $Salida | Out-Null

Get-ChildItem $Audios -File |
    Where-Object { $_.Extension -match '^\.(mp3|m4a|wav|ogg|opus|flac|aac|wma|mp4|webm)$' } |
    ForEach-Object {
        $base = Join-Path $Salida $_.BaseName
        if (Test-Path "$base.srt") { Write-Host "Ya está: $($_.Name)"; return }
        Write-Host "Convirtiendo $($_.Name)..."
        ffmpeg -hide_banner -loglevel error -y -i $_.FullName -ar 16000 -ac 1 -c:a pcm_s16le $tmp
        if ($LASTEXITCODE -ne 0) { Write-Warning "FFmpeg no pudo leer $($_.Name)"; return }
        $t0 = Get-Date
        & $cli -m $bin -f $tmp -l es -osrt -otxt -of $base --max-context 0 --prompt $prompt
        if ($LASTEXITCODE -ne 0) { Write-Warning "Whisper falló con $($_.Name)"; return }
        Write-Host ("Listo {0} en {1:N0} min" -f $_.Name, ((Get-Date) - $t0).TotalMinutes)
    }
Remove-Item $tmp -ErrorAction SilentlyContinue
```

Correrlo (el `Bypass` es porque Windows no deja correr scripts propios por defecto):

```powershell
powershell -ExecutionPolicy Bypass -File $HOME\Clases\transcribir.ps1
```

Por cada audio quedan dos archivos en `$Salida`: el `.srt` (texto con el minuto de cada frase, el que sirve para
citar y verificar) y el `.txt` (texto corrido).

**Opciones que ayudan:**

- `--max-context 0` (ya está en el script): evita que, en clases largas, Whisper se quede repitiendo la misma
  frase en bucle.
- **Detector de silencio (VAD)**: si `whisper-cli.exe --help` muestra la opción `--vad`, conviene activarla para
  que no invente frases en los recreos y silencios. Necesita un modelo aparte (en `whisper.cpp\models` hay un
  script `download-vad-model`; el modelo es Silero). Se agrega a la línea de `& $cli`:
  `--vad -vm models\ggml-silero-v5.1.2.bin` (con la ruta y el nombre del modelo que se haya bajado).

## 5. Subir las transcripciones al repositorio

1. **Nombre de cada archivo**: que diga la fecha y, si se sabe, el tema. Ej.: `2026-09-10_chi_cuadrado.srt`.
   (Si no se sabe el tema, con la fecha alcanza: se busca adentro.)
2. En la PC con Windows, con el repositorio clonado (es privado), copiar los `.srt` y `.txt` a **`datos/clases/`**
   y subirlos:

   ```powershell
   git add datos/clases
   git commit -m "Transcripciones de las clases"
   git push
   ```

   En la Mac, `git pull` y ya están. (Los audios no: pesan mucho; solo las transcripciones, que son texto.)
3. Con eso, desde Claude Code: buscar los ejercicios de la guía que el profesor resuelve en clase, extraer su paso
   a paso con las frases textuales y el minuto, y agregarlos a `ESTILO_CATEDRA.md` como ejemplos reales
   (empezando por los temas V a VIII, que hoy no tienen ninguno).

> Las transcripciones tienen errores (palabras mal entendidas, sobre todo números y símbolos). Para lo que importa
> —cómo plantea H0, cómo redacta la conclusión, qué remarca— alcanza; los **números** de un ejemplo igual se
> verifican contra la guía y el solver antes de usarlos.

## Si algo no coincide

Lo que puede ser distinto a lo que dice esta guía, y qué hacer:

| Qué | Lo que puede pasar | Qué hacer |
|---|---|---|
| Ejecutable ya compilado (nota del paso 1) | En *Releases* de whisper.cpp puede no haber un `.zip` para Windows con Vulkan (hay versiones para CPU y para NVIDIA/CUDA, que no sirven para la AMD) | Compilar como en el paso 2 |
| IDs de `winget` (paso 1) | `Git.Git`, `Kitware.CMake` o `Gyan.FFmpeg` pueden no encontrarse | Buscar el nombre con `winget search ffmpeg` (o `cmake`, `git`), o instalar desde la web de cada programa |
| Vulkan SDK (paso 1) | `cmake` dice que no encuentra Vulkan | Cerrar y abrir la terminal (el instalador agrega `VULKAN_SDK`); si sigue, reinstalar el SDK con las opciones por defecto |
| Compilación (paso 2) | `cmake` no encuentra un compilador | En el instalador de Build Tools, confirmar que esté marcado **Desarrollo para el escritorio con C++** |
| Ruta del programa (pasos 2 y 4) | `whisper-cli.exe` no está en `build\bin\Release\` (en versiones viejas se llamaba `main.exe`) | Buscarlo con `Get-ChildItem -Recurse -Filter whisper-cli.exe build` y corregir `$cli` en el script |
| Script del modelo (paso 3) | `download-ggml-model.cmd` no existe o falla | Bajar `ggml-large-v3-turbo.bin` a mano desde <https://huggingface.co/ggerganov/whisper.cpp> a `models\` |
| Uso de la placa (paso 3) | No aparece `ggml_vulkan: Found 1 Vulkan devices` | Actualizar el driver de AMD; confirmar que se compiló con `-DGGML_VULKAN=1` (borrar la carpeta `build` y volver a compilar) |
| Opciones de `whisper-cli` (paso 4) | Alguna opción no existe en la versión bajada (`--max-context`, `--prompt`, `-osrt`) | Ver los nombres con `whisper-cli.exe --help` y ajustar la línea `& $cli` |
| Detector de silencio (paso 4) | No está `--vad`, o el modelo de Silero tiene otro nombre | Es opcional: sin VAD funciona igual; si se usa, poner en `-vm` el archivo que se haya bajado a `models\` |
| Velocidad (paso 3) | Tarda horas en 10 minutos de audio | Está usando el procesador: ver la fila «Uso de la placa». Como alternativa, el modelo `medium` es bastante más rápido |

Si aparece un error que no está acá, copiar el mensaje completo y pegarlo en Claude Code.
