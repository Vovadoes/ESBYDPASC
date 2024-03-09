import sys

import numpy as np
from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from main import Calculation, ChartLinePltData, ChartQuadRegressPltData

from functions import get_super


class ChartPLTWindow(QtWidgets.QDialog):

    def __init__(self, n, *args, **kwargs):
        super(ChartPLTWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(f'График {n}')
        self.setFixedSize(800, 800)

        fig = Figure()
        self.axes = fig.add_subplot(111)

        sc = FigureCanvasQTAgg(fig)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(toolbar, 0, 0, 1, 1)
        layout.addWidget(sc, 1, 0, 1, 1)

        # self.axes = fig.add_subplot(111)
        # self.axes.plot(data.df, marker='o', label=[f"E={i}" for i in data.columns])
        # self.axes.grid(linestyle='--')
        #
        # self.axes.set_ylabel(data.xlabel)
        # self.axes.set_xlabel(data.ylabel)
        # self.axes.set_xlim([0, max(data.index) * 1.2])
        # self.axes.set_ylim([0, max(data.df.max()) * 1.2])
        # self.axes.legend()

        # # Create a placeholder widget to hold our toolbar and canvas.
        # widget = QtWidgets.QWidget()
        # widget.setLayout(layout)
        # # self.setCentral(widget)

    def line(self, data: ChartLinePltData):
        self.axes.plot(data.df, marker='o', label=[f"E={i}" for i in data.columns])
        self.axes.grid(linestyle='--')

        self.axes.set_ylabel(data.xlabel)
        self.axes.set_xlabel(data.ylabel)
        self.axes.set_xlim([0, max(data.index) * 1.2])
        self.axes.set_ylim([0, max(data.df.max()) * 1.2])

    def quad_regress(self, data: ChartQuadRegressPltData):
        for i in data.columns:
            model = np.poly1d(np.polyfit(data.df[i].index.tolist(), data.df[i].values.tolist(), 2))
            polyline = np.linspace(0.1, 1, 50)
            coefficients = list(model.coefficients)
            self.axes.plot(
                polyline, model(polyline), linestyle='dashed', linewidth=2,
                label=f"{round(coefficients[0], 3)}x{get_super('2')} "
                      f"{'+' if coefficients[1] > 0 else ''} {round(coefficients[1], 3)}x "
                      f"{'+' if coefficients[2] > 0 else ''} {round(coefficients[2], 3)}"
            )

    def start(self):
        self.axes.legend()
        self.show()
        self.exec_()


if __name__ == "__main__":
    d_lst_input = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    E_lst_input = [1, 1.6]
    calculation = Calculation(d_lst_input=d_lst_input, E_lst_input=E_lst_input)
    app = QtWidgets.QApplication(sys.argv)
    chartPlt = ChartPLTWindow(1)
    chartPlt.line(calculation.chart_v_y_data)
    chartPlt.quad_regress(calculation.chart_quad_regress_data)
    chartPlt.start()
    # chartPlt.exec_()
    app.exec_()
