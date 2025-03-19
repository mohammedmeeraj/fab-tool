import sys
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)

class MplCanvasReports(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes1 = self.fig.add_subplot(221)
        self.axes2 = self.fig.add_subplot(222)
        self.axes3 = self.fig.add_subplot(223)
        self.axes4 = self.fig.add_subplot(224)
        super().__init__(self.fig)
        self.setParent(parent)
