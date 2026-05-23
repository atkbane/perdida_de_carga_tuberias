# Pérdida de Carga en Tuberías

Aplicación web y de escritorio para el cálculo de pérdidas de carga en tuberías circulares a presión.  
Soporta tres métodos: **Darcy‑Weisbach**, **Hazen‑Williams** y **Manning**.  
Incluye pérdidas por fricción (tramo a tramo) y pérdidas localizadas generales (entrada y salida).

![Vista previa de la web](docs/screenshot.png) *(opcional: añade una captura de pantalla)*

## ✨ Características

- **Múltiples métodos** – selecciona el más adecuado a tu material y fluido.
- **Segmentación dinámica** – añade, elimina y edita tramos de tubería.
- **Pérdidas localizadas** – coeficientes `K` de entrada y salida (generales).
- **Resultados detallados** – velocidad, pérdida por tramo, pérdida total y potencia perdida.
- **Doble interfaz**:
  - 💻 **Escritorio** – aplicación con PySide6 (Python).
  - 🌐 **Web** – versión estática con Pyodide, ejecutable en cualquier navegador sin servidor.

## 🧮 Métodos implementados

| Método            | Fórmula de pérdida continua                      | Coeficiente requerido |
|-------------------|--------------------------------------------------|------------------------|
| Darcy‑Weisbach    | `hf = f · (8/(π²·g)) · Q² · L / D⁵`             | Rugosidad `k` (mm)     |
| Hazen‑Williams    | `hf = 10.67 · L · Q^1.852 / (C^1.852 · D^4.87)` | Coeficiente `C`        |
| Manning           | `hf = 10.29 · n² · L · Q² / D^5.333`            | Rugosidad `n`          |

- **Pérdidas localizadas**: `h_local = K · V²/(2g)`
- **Potencia perdida**: `P = γ · Q · h_total`   (γ = 9.81 kN/m³)

## 🚀 Uso de la versión web (recomendada)

1. Abre la página: [https://atkbane.github.io/perdida_de_carga_tuberias](https://atkbane.github.io/perdida_de_carga_tuberias)
2. Introduce los datos del proyecto, caudal y método.
3. Añade segmentos con longitud, diámetro y coeficiente según el método.
4. Haz clic en **Calcular**.
5. Visualiza los resultados en la columna derecha (tabla, totales, potencia).

> La web funciona completamente en tu navegador. No envía datos a ningún servidor.

## 💻 Uso de la versión de escritorio

### Requisitos

- Python 3.8 o superior
- PySide6
- (opcional) Entorno virtual

### Instalación

bash
git clone https://github.com/atkbane/perdida_de_carga_tuberias.git
cd perdida_de_carga_tuberias
pip install -r requirements.txt   # si tienes un archivo con dependencias
O instala solo PySide6:

bash
pip install PySide6
Ejecutar
bash
python main.py
📁 Estructura del proyecto
text
perdida_de_carga_tuberias/
├── calculos.py            # Lógica y modelos (compartida con web)
├── interfaz_pyside.py     # UI de escritorio
├── main.py                # Punto de entrada escritorio
├── index.html             # Aplicación web
├── web_main.py            # Puente Python/Pyodide para la web
├── README.md
└── (otros archivos)
🛠️ Desarrollo y despliegue web
La versión web usa Pyodide para ejecutar Python en el navegador.
Para desplegar actualizaciones en GitHub Pages:

bash
# Desde la carpeta clonada
git add .
git commit -m "Descripción del cambio"
git push origin main
Asegúrate de que GitHub Pages esté configurado en Settings > Pages > Branch: main, carpeta: / (root).

📄 Licencia
Este proyecto se distribuye bajo la licencia MIT.
Consulta el archivo LICENSE para más detalles.

👨‍💻 Autor
Creado por atkbane – ingeniero civil y entusiasta de la programación.
