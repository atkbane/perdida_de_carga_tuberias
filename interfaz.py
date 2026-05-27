"""
interfaz_pyside.py
==================
Interfaz gráfica con PySide6 para cálculo de pérdidas de carga.
Contiene la UI, los eventos y el formateo de resultados.
Layout de 3 columnas: datos | segmentos | resultados.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox,
    QTextEdit, QScrollArea, QFrame, QMessageBox,
)
from typing import List

from calculos import (
    METODOS, LABEL_COEF, Segmento, Resultado, CalculoModel,
)

# ─────────────────────────────────────────────────────────────────────────────
#  CONSTANTES DE UI
# ─────────────────────────────────────────────────────────────────────────────
PAD   = 5
PADl  = 8
WIDTH = 900
HEIGHT= 520
DEF_SEGMENTOS = 3
DEF_K_ENTRADA = "0.50"
DEF_K_SALIDA  = "1.0"


class VentanaPerdidaCarga(QWidget):
    """Ventana principal con layout de 3 columnas."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pérdidas de Carga - PySide6")
        self.resize(WIDTH, HEIGHT)

        # ── estado interno ──
        self._seg_frames: List[QGroupBox] = []
        self._seg_entries: List[dict] = []
        self.model = CalculoModel()

        # ── layout principal horizontal ──
        layout_main = QHBoxLayout(self)
        layout_main.setContentsMargins(PADl, PADl, PADl, PADl)
        layout_main.setSpacing(PADl)

        # col 0: datos (ancho fijo)
        col0 = self._build_col_datos()
        col0.setFixedWidth(280)
        layout_main.addWidget(col0)

        # col 1: segmentos (stretch 2)
        layout_main.addWidget(self._build_col_segmentos(), stretch=2)

        # col 2: resultados (stretch 4)
        layout_main.addWidget(self._build_col_resultados(), stretch=4)

    # ─────────────────────────────────────────────────────────────────────────
    #  COLUMNA IZQUIERDA — DATOS
    # ─────────────────────────────────────────────────────────────────────────

    def _build_col_datos(self) -> QFrame:
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # ---- Título del proyecto ----
        gb_proy = QGroupBox("Título del Proyecto")
        form_proy = QVBoxLayout(gb_proy)
        self.e_titulo = QLineEdit()
        self.e_titulo.setPlaceholderText("Nombre del proyecto…")
        form_proy.addWidget(self.e_titulo)
        layout.addWidget(gb_proy)

        # ---- Especificaciones ----
        gb_esp = QGroupBox("Especificaciones")
        form_esp = QFormLayout(gb_esp)
        self.e_Q = QLineEdit()
        form_esp.addRow("Caudal Q (m³/s):", self.e_Q)

        self.opt_metodo = QComboBox()
        self.opt_metodo.addItems(METODOS)
        self.opt_metodo.currentTextChanged.connect(self._on_metodo_change)
        form_esp.addRow("Método:", self.opt_metodo)
        layout.addWidget(gb_esp)

        # ---- Pérdidas Localizadas Generales ----
        gb_loc = QGroupBox("Pérdidas Localizadas Generales")
        form_loc = QFormLayout(gb_loc)
        self.e_k_entrada = QLineEdit(DEF_K_ENTRADA)
        form_loc.addRow("K entrada:", self.e_k_entrada)
        self.e_k_salida = QLineEdit(DEF_K_SALIDA)
        form_loc.addRow("K salida:", self.e_k_salida)
        layout.addWidget(gb_loc)

        # ---- Botón Calcular ----
        self.btn_calcular = QPushButton("CALCULAR")
        self.btn_calcular.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                padding: 8px;
                background-color: #2a7;
                color: white;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #1a6; }
        """)
        self.btn_calcular.clicked.connect(self._on_calcular)
        layout.addWidget(self.btn_calcular)

        # ---- Botón Limpiar ----
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.clicked.connect(self._on_limpiar)
        layout.addWidget(self.btn_limpiar)

        layout.addStretch()
        return panel

    # ─────────────────────────────────────────────────────────────────────────
    #  COLUMNA CENTRAL — SEGMENTOS
    # ─────────────────────────────────────────────────────────────────────────

    def _build_col_segmentos(self) -> QFrame:
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.Box)
        layout = QVBoxLayout(panel)
        layout.setSpacing(6)

        gb_seg = QGroupBox("Segmentos")
        layout_seg = QVBoxLayout(gb_seg)

        # Selector de número de segmentos
        h_row = QHBoxLayout()
        lbl_n = QLabel("N° Segmentos:")
        h_row.addWidget(lbl_n)
        self.opt_nseg = QComboBox()
        self.opt_nseg.addItems(["1", "2", "3", "4", "5"])
        self.opt_nseg.setCurrentText(str(DEF_SEGMENTOS))
        self.opt_nseg.currentTextChanged.connect(self._on_nseg_change)
        h_row.addWidget(self.opt_nseg)
        h_row.addStretch()
        layout_seg.addLayout(h_row)

        # Scroll area para los segmentos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._seg_scroll_content = QWidget()
        self._seg_scroll_layout = QVBoxLayout(self._seg_scroll_content)
        self._seg_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self._seg_scroll_layout.setSpacing(6)
        self._seg_scroll_layout.addStretch()
        scroll.setWidget(self._seg_scroll_content)
        layout_seg.addWidget(scroll, stretch=1)

        layout.addWidget(gb_seg)
        self._reconstruir_segmentos(DEF_SEGMENTOS)
        return panel

    def _reconstruir_segmentos(self, n: int):
        """(Re)construye los inputs de segmentos en el scroll."""
        # Limpiar existentes
        for frame in self._seg_frames:
            self._seg_scroll_layout.removeWidget(frame)
            frame.deleteLater()
        self._seg_frames.clear()
        self._seg_entries.clear()

        # Remover stretch temporal
        item = self._seg_scroll_layout.itemAt(self._seg_scroll_layout.count() - 1)
        if item is not None:
            self._seg_scroll_layout.removeItem(item)

        for i in range(n):
            gb = QGroupBox(f"Segmento {i + 1}")
            form = QFormLayout(gb)

            e_L = QLineEdit()
            form.addRow("L (m):", e_L)

            e_D = QLineEdit()
            form.addRow("D (m):", e_D)

            metodo = self.opt_metodo.currentText()
            lbl_coef = LABEL_COEF.get(metodo, "k (mm)")
            e_coef = QLineEdit()
            form.addRow(f"{lbl_coef}:", e_coef)

            self._seg_scroll_layout.addWidget(gb)
            self._seg_frames.append(gb)
            self._seg_entries.append({"L": e_L, "D": e_D, "coef": e_coef})

        self._seg_scroll_layout.addStretch()

    def _on_metodo_change(self, choice: str):
        """Actualiza etiquetas de coeficiente en los segmentos."""
        lbl = LABEL_COEF.get(choice, "k (mm)")
        for gb in self._seg_frames:
            form = gb.layout()
            if isinstance(form, QFormLayout) and form.rowCount() >= 3:
                item = form.itemAt(2, QFormLayout.ItemRole.LabelRole)
                if item is not None:
                    widget = item.widget()
                    if isinstance(widget, QLabel):
                        widget.setText(f"{lbl}:")

    def _on_nseg_change(self, choice: str):
        """Reconstruye los inputs de segmentos al cambiar el número."""
        try:
            n = int(choice)
            self._reconstruir_segmentos(n)
        except ValueError:
            pass

    # ─────────────────────────────────────────────────────────────────────────
    #  COLUMNA DERECHA — RESULTADOS
    # ─────────────────────────────────────────────────────────────────────────

    def _build_col_resultados(self) -> QFrame:
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.Box)
        layout = QVBoxLayout(panel)

        gb_res = QGroupBox("Resultados")
        layout_res = QVBoxLayout(gb_res)

        self.txt_res = QTextEdit()
        self.txt_res.setReadOnly(True)
        self.txt_res.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 11px;
            }
        """)
        layout_res.addWidget(self.txt_res, stretch=1)

        layout.addWidget(gb_res)
        return panel

    # ─────────────────────────────────────────────────────────────────────────
    #  EVENTOS (CONTROLADOR)
    # ─────────────────────────────────────────────────────────────────────────

    def _on_calcular(self):
        """Lee inputs, valida, calcula y muestra resultados."""
        try:
            titulo = self.e_titulo.text().strip() or "—"
            Q = float(self.e_Q.text())
            metodo = self.opt_metodo.currentText()
            k_entrada = float(self.e_k_entrada.text())
            k_salida = float(self.e_k_salida.text())

            segs_data = self._get_segmentos_data()
            if not segs_data:
                raise ValueError("No hay segmentos definidos.")

            segmentos: List[Segmento] = []
            for i, sd in enumerate(segs_data, 1):
                L = float(sd["L"])
                D = float(sd["D"])
                coef = float(sd["coef"])
                segmentos.append(Segmento(L=L, D=D, coef=coef))

            res: Resultado = self.model.calcular(
                titulo=titulo, Q=Q, metodo=metodo,
                segmentos=segmentos,
                k_entrada=k_entrada, k_salida=k_salida,
            )

            self.txt_res.setPlainText(self._formatear(res))

        except ValueError as ex:
            QMessageBox.critical(self, "Error de entrada", str(ex))
        except Exception as ex:
            QMessageBox.critical(self, "Error inesperado", f"{ex}")

    def _on_limpiar(self):
        """Limpia todos los campos."""
        self.e_titulo.clear()
        self.e_Q.clear()
        self.e_k_entrada.setText(DEF_K_ENTRADA)
        self.e_k_salida.setText(DEF_K_SALIDA)
        self.txt_res.clear()
        for e in self._seg_entries:
            e["L"].clear()
            e["D"].clear()
            e["coef"].clear()

    def _get_segmentos_data(self) -> List[dict]:
        """Retorna lista de dicts con 'L', 'D', 'coef' (strings)."""
        return [
            {"L": e["L"].text(), "D": e["D"].text(), "coef": e["coef"].text()}
            for e in self._seg_entries
        ]

    # ─────────────────────────────────────────────────────────────────────────
    #  FORMATEO DE RESULTADOS
    # ─────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _formatear(res: Resultado) -> str:
        """Convierte un Resultado en texto formateado."""
        sep = "─" * 44

        cab = f"{'#':>3}  {'L (m)':>7}  {'D (m)':>7}  {'V (m/s)':>8}  {'hf (m)':>8}"
        lin = "─" * 40
        filas = "\n".join(
            f"{s.idx:>3}  {s.L:>7.2f}  {s.D:>7.3f}  {s.V:>8.2f}  {s.hf:>8.4f}"
            for s in res.segmentos
        )

        pot = res.potencia_kw
        pot_str = f"{pot/1000:.2f} MW" if pot >= 1000 else f"{pot:.2f} kW"

        return (
            f"Proyecto : {res.titulo}\n"
            f"Método   : {res.metodo}\n"
            f"{sep}\n"
            f"Segmentación:\n"
            f"{cab}\n"
            f"{lin}\n"
            f"{filas}\n"
            f"{sep}\n"
            f"Perd. fricción       : {res.hf_total:>8.2f} m\n"
            f"Perd. entrada        : {res.h_entrada:>8.2f} m\n"
            f"Perd. salida         : {res.h_salida:>8.2f} m\n"
            f"{sep}\n"
            f"TOTAL PÉRDIDAS       : {res.h_total:>8.2f} m\n"
            f"Potencia perdida     : {pot_str:>8}\n"
        )