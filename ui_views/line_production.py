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

# class MplCanvas(FigureCanvas):
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         self.fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes1 = self.fig.add_subplot(121)
#         self.axes2 = self.fig.add_subplot(122)
#         super().__init__(self.fig)
#         self.setParent(parent)

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, subplot_spec=(1, 1), name=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.__create_subplots(subplot_spec)
        super().__init__(self.fig)
        self.setParent(parent)
        self.name = name  # Optional identifier (useful for debugging/logging)

    def __create_subplots(self, spec):
        """Creates and returns a list of axes based on the subplot layout spec."""
        rows, cols = spec
        axes = []
        for i in range(1, rows * cols + 1):
            axes.append(self.fig.add_subplot(rows, cols, i))
        return axes