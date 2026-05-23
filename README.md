# Pérdida de Carga en Tuberías

Calculadora web de pérdidas de carga en tuberías circulares a presión.  
Soporta tres métodos: **Darcy‑Weisbach**, **Hazen‑Williams** y **Manning**.  
Incluye pérdidas por fricción tramo a tramo y pérdidas localizadas de entrada y salida.

## 🌐 Acceso

Abre la aplicación directamente desde el navegador, sin instalación:  
👉 [https://atkbane.github.io/perdida_de_carga_tuberias](https://atkbane.github.io/perdida_de_carga_tuberias)

> Funciona completamente en el navegador. No envía datos a ningún servidor.

## 🧮 Métodos implementados

| Método          | Fórmula                                            | Coeficiente    |
|-----------------|----------------------------------------------------|----------------|
| Darcy‑Weisbach  | `hf = f · (8/(π²·g)) · Q² · L / D⁵`               | Rugosidad `k` (mm) |
| Hazen‑Williams  | `hf = 10.67 · L · Q^1.852 / (C^1.852 · D^4.87)`   | Coeficiente `C` |
| Manning         | `hf = 10.29 · n² · L · Q² / D^5.333`              | Rugosidad `n`  |

- **Pérdidas localizadas**: `h_local = K · V²/(2g)`
- **Potencia perdida**: `P = γ · Q · h_total` (γ = 9.81 kN/m³, resultado en kW o MW)

El factor de fricción de Darcy‑Weisbach se calcula con la aproximación explícita de **Swamee‑Jain**, asumiendo agua a 20 °C (ν = 1.004×10⁻⁶ m²/s).

## ✨ Características

- **Segmentación dinámica** – añade o elimina tramos de tubería sin límite práctico.
- **Pérdidas localizadas** – coeficiente K de entrada (aplicado al primer segmento) y de salida (aplicado al último).
- **Resultados por tramo** – velocidad media, pérdida por fricción, y totales de pérdida y potencia.
- **Validación de entrada** – resalta campos inválidos con mensajes descriptivos.
- **Responsive** – funciona en móviles y escritorio (columnas se apilan en pantallas pequeñas).

## 🧪 Cómo usar

1. Ingresa el título del proyecto y el caudal Q (m³/s).
2. Selecciona el método de cálculo.
3. Ajusta los coeficientes K de entrada y salida.
4. Añade los segmentos de tubería (longitud L, diámetro D y coeficiente según el método).
5. Presiona **Calcular**.
6. Los resultados aparecen en el panel derecho sin recargar la página.

## 🛠️ Tecnologías

- [Pyodide v0.26.4](https://pyodide.org/) — Python en el navegador vía WebAssembly
- HTML5, CSS3, JavaScript vanilla
- Python 3.12 (solo biblioteca estándar: `math`, `dataclasses`, `typing`)

## 📁 Estructura del proyecto

```
perdida_de_carga_tuberias/
├── calculos.py      # Lógica hidráulica (fricción, pérdidas, modelos)
├── web_main.py      # Puente Python/Pyodide para la web
├── index.html       # Interfaz web
├── .gitignore
├── LICENSE
└── README.md
```

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Creado por [atkbane](https://github.com/atkbane) – ingeniero civil y entusiasta de la programación.
