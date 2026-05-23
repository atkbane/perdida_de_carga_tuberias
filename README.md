# Pérdidas de Carga en Tuberías

Calculadora web de pérdidas de carga en tuberías a presión, usando las fórmulas de **Darcy-Weisbach**, **Hazen-Williams** y **Manning**.

## Demo

Accede desde cualquier navegador:  
👉 [https://tu-usuario.github.io/perdida-de-carga-tuberias/](https://tu-usuario.github.io/perdida-de-carga-tuberias/)

## Captura

Tres columnas: datos del proyecto (izquierda), segmentos de tubería (centro), resultados (derecha).  
Los segmentos se agregan/eliminan dinámicamente. Al cambiar el método, la etiqueta del coeficiente se actualiza automáticamente.

## Características

- **Métodos soportados:** Darcy-Weisbach (Swamee-Jain), Hazen-Williams, Manning
- **Segmentos dinámicos:** agregar o eliminar tramos de tubería sin límite práctico
- **Pérdidas localizadas:** coeficientes K de entrada y salida
- **Resultados:** pérdida por fricción total, pérdidas localizadas, pérdida total, potencia perdida
- **Validación de entrada:** resalta campos inválidos y muestra errores descriptivos
- **Responsive:** funciona en móviles y escritorio (columnas se apilan en pantallas pequeñas)
- **Sin servidor:** todo corre en el navegador usando Pyodide (Python compilado a WebAssembly)

## Tecnologías

- [Pyodide v0.26.4](https://pyodide.org/) — Python en el navegador
- HTML5, CSS3, JavaScript vanilla
- Python 3.12 (solo biblioteca estándar: `math`, `dataclasses`, `typing`)

## Estructura de archivos

```
perdida-de-carga-tuberias/
├── index.html       # Página web principal
├── web_main.py      # Módulo Python que orquesta la simulación
├── calculos.py      # Lógica hidráulica (fricción, pérdidas, modelos)
├── LICENSE
└── README.md
```

## Despliegue en GitHub Pages

1. Sube los 3 archivos (`index.html`, `web_main.py`, `calculos.py`) a un repositorio público en GitHub.
2. Ve a **Settings → Pages**.
3. En "Source", selecciona **Deploy from a branch**.
4. Elige `main` y la carpeta `/ (root)` (o `/docs` si prefieres).
5. Guarda. En ~1 minuto el sitio estará disponible en `https://tu-usuario.github.io/tu-repo/`.

## Uso

1. Ingresa el título del proyecto y el caudal (m³/s).
2. Selecciona el método de cálculo.
3. Ajusta los coeficientes K de entrada y salida.
4. Agrega los segmentos de tubería (longitud L, diámetro D, coeficiente de fricción).
5. Presiona **Calcular**.
6. Los resultados se muestran al instante en el panel derecho (sin recargar la página).

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.