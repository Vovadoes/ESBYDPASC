from typing import Callable
from typing import List, Any

from PyQt5 import QtWidgets

from files.MainWindow import Ui_MainWindow
from files.ResultWindow import Ui_Form
from files.TableWindow import Ui_Form as Ui_Form_Table

from main import Calculation
from functions import change_size, get_sub, get_super
from MyThread import MyThread
from TableLoader import TableLoader
# from ChartPLTWindow import ChartPLTWindow

from settings import DEDUG

import sys


# from functions import get_super, get_sub


class Variables:
    def __init__(self, main_window):
        self.main_window: mywindow = main_window
        self.n = None
        self.k = None
        self.load()

    def load(self):
        self.n = mywindow.is_float(self.main_window.ui.doubleSpinBox_8)
        self.k = mywindow.is_int(self.main_window.ui.doubleSpinBox_9)

    def update(self):
        self.load()
        self.main_window.table_loader1.m = self.k
        # self.main_window.table_loader2.n = self.n


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()

        self.calculation = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if DEDUG:
            self.ui.doubleSpinBox_8.setValue(100)  # n
            self.ui.doubleSpinBox_9.setValue(7)  # k

        change_size(self)

        self.lst_Thread = []

        self.variables = Variables(self)

        loader1_n = 3
        loader1_m = self.variables.k
        loader1_label = self.ui.label_13
        loader1_data = [
            [23, 25, 3],
            [25, 27, 10],
            [27, 29, 6],
            [29, 31, 16],
            [31, 33, 15],
            [33, 35, 30],
            [35, 37, 20]
        ]
        loader1_block = False
        loader1_heading_x = lambda iterator: \
            ["Начало промежутка", "Конец промежутка", "Площадь, га"][iterator]
        loader1_types_matrix = [[int, int, float] for _ in range(loader1_m)]

        # loader2_n = self.variables.n
        # loader2_m = 1
        # loader2_label = self.ui.label_4
        # loader2_data = [[1, 1.6]]
        # loader2_block = False
        # loader2_heading_x = lambda iterator: f"E{get_sub(str(iterator + 1))}"

        self.table_loader1 = TableLoader(
            self, loader1_n, loader1_m, loader1_label,
            block=loader1_block,
            heading_x=loader1_heading_x,
            types_matrix=loader1_types_matrix
        )
        # self.table_loader2 = TableLoader(
        #     self, loader2_n, loader2_m, loader2_label,
        #     block=loader2_block,
        #     heading_x=loader2_heading_x
        # )

        if DEDUG:
            pass
            self.table_loader1.data = loader1_data
            # self.table_loader2.data = loader2_data

        self.ui.pushButton_8.clicked.connect(self.table_loader1.open_table)
        # self.ui.pushButton_3.clicked.connect(self.table_loader2.open_table)

        # add_def_pushButton = lambda : self.calculation.simple_bid()
        # add_def_pushButton_2 = lambda : self.calculation.difficult_bet()
        # self.ui.pushButton.clicked.connect(lambda : self.calculate(add_def_pushButton))
        # self.ui.pushButton_2.clicked.connect(lambda : self.calculate(add_def_pushButton_2))

        add_def_pushButton = lambda: None
        self.ui.pushButton.clicked.connect(lambda: self.calculate(add_def_pushButton))

    def calculate(self, fun, *args, **kwargs):
        self.variables.update()
        condition = self.table_loader1.valid(self.variables.k, 3)
        # condition = True
        if condition:
            self.calculation = Calculation(
                n=self.variables.n,
                k=self.variables.k,
                lst=self.table_loader1.data
            )
            fun(*args, **kwargs)
            window = Finish(
                self
            )
            window.show()

            # def main():
            #     window.exec_()
            #
            # t = MyThread(main)
            # t.start()
            windowThread = MyThread(lambda: window.exec_())
            windowThread.start()
            self.lst_Thread.append(windowThread)

    def exec_(self) -> int:
        a = super().exec_()
        for i in self.lst_Thread:
            i.wait()
        return a

    @staticmethod
    def is_float(value: QtWidgets.QDoubleSpinBox) -> float:
        try:
            a = float(value.value())
            value.setStyleSheet("QDoubleSpinBox {}")
            return a
        except ValueError:
            value.setStyleSheet("QDoubleSpinBox { background-color: red; }")
            raise ValueError()

    @staticmethod
    def is_int(value: QtWidgets.QDoubleSpinBox) -> int:
        try:
            a = int(round(float(value.value())))
            value.setStyleSheet("QDoubleSpinBox {}")
            return a
        except ValueError:
            value.setStyleSheet("QDoubleSpinBox { background-color: red; }")
            raise ValueError()


class Finish(QtWidgets.QDialog):
    def __init__(self, parent: mywindow):
        super(Finish, self).__init__()
        self.ui = Ui_Form()
        self.parent = parent
        self.ui.setupUi(self)
        change_size(self)

        self.ui.doubleSpinBox_9.setValue(round(self.parent.calculation.S_2_n, 2))
        self.ui.doubleSpinBox_10.setValue(round(self.parent.calculation.s, 2))
        self.ui.doubleSpinBox_11.setValue(round(self.parent.calculation.S_xcp, 2))

        self.ui.textEdit.setText(
            f"Следовательно, оценка средней урожайности сахарной свеклы на всем массиве равна {round(self.parent.calculation.x_cp_v)} ц со средней квадратической ошибкой {round(self.parent.calculation.S_xcp, 2)} ц. Оценка среднего квадратического отклонения урожайности на всем массиве равна {round(self.parent.calculation.s, 2)} ц."
        )

        lst = []
        types_matrix = []
        summ = 0
        for i in range(self.parent.table_loader1.m):
            data = self.parent.table_loader1.data
            lst.append([
                round(data[i][0]), round(data[i][1]), round(data[i][2], 2),
                round(self.parent.calculation.lst_y[i], 2),
                round(self.parent.calculation.lst_y_n[i], 2),
                round(self.parent.calculation.lst_y_x_n[i], 2)
            ])
            types_matrix.append([int, int, float, float, float, float])
            summ += data[i][2]

        lst.append(['', '', round(summ), '', sum(self.parent.calculation.lst_y_n),
                    sum(self.parent.calculation.lst_y_x_n)])
        types_matrix.append([str, str, int, str, float, float])

        lst.append(['', '', '', '', lst[-1][4] / summ,
                    lst[-1][5] / self.parent.variables.n - 1])
        types_matrix.append([str, str, str, str, float, float])

        print(f"{lst=}")

        # filter_table_results_1 = lambda dct: round(dct['value'], 3)

        loader_results_1_n = self.parent.table_loader1.n + 3
        loader_results_1_m = self.parent.table_loader1.m + 2
        loader_results_1_data = lst
        types_matrix_results_1 = types_matrix
        loader_results_1_block = True
        loader_results_1_heading_x = lambda iterator: \
            ["Начало промежутка", "Конец промежутка", "Площадь, га", "Середина интервала",
             f"y{get_sub('i')} * n{get_sub('i')}", f"(y{get_sub('i')} - x{get_sub('v')}){get_super('2')} * n{get_sub('i')}"][iterator]
        loader_results_1_heading_y = lambda iterator: str(iterator)
        self.table_loader_results_1 = TableLoader(
            self.parent, loader_results_1_n, loader_results_1_m, data=loader_results_1_data,
            block=loader_results_1_block,
            heading_x=loader_results_1_heading_x, heading_y=loader_results_1_heading_y,
            types_matrix=types_matrix_results_1
        )

        # loader_v_y_data = self.parent.calculation.lst_v_y
        # self.table_loader_v_y = TableLoader(
        #     self.parent, loader_v_d_n, loader_v_d_m, data=loader_v_y_data,
        #     block=loader_v_d_block,
        #     heading_x=loader_v_d_heading_x, heading_y=loader_v_d_heading_y,
        #     filter_table=filter_table
        # )
        #
        # loader_v_s_data = self.parent.calculation.lst_v_s
        # self.table_loader_v_s = TableLoader(
        #     self.parent, loader_v_d_n, loader_v_d_m, data=loader_v_s_data,
        #     block=loader_v_d_block,
        #     heading_x=loader_v_d_heading_x, heading_y=loader_v_d_heading_y,
        #     filter_table=filter_table
        # )

        # self.ui.doubleSpinBox_19.setValue(round(self.parent.calculation.y))
        # self.ui.doubleSpinBox_20.setValue(round(self.parent.calculation.dy))
        # self.ui.doubleSpinBox_10.setValue(round(self.parent, 2))
        self.table_loader_results_1.kwargs['block'] = True
        # self.parent.table_loader2.kwargs['block'] = True

        self.lst_Thread = []

        self.lst_Thread.append(MyThread(lambda: self.table_loader_results_1.open_table()))
        self.ui.pushButton_2.clicked.connect(
            lambda: self.lst_Thread[0].start()
        )
        #
        # self.lst_Thread.append(MyThread(lambda: self.table_loader_v_s.open_table()))
        # self.ui.pushButton_4.clicked.connect(
        #     lambda: self.lst_Thread[1].start()
        # )
        #
        # self.lst_Thread.append(MyThread(lambda: self.table_loader_v_y.open_table()))
        # self.ui.pushButton_7.clicked.connect(
        #     lambda: self.lst_Thread[2].start()
        # )
        #
        # chart_plt_w = ChartPLTWindow(1)
        # chart_plt_w.line(self.parent.calculation.chart_v_y_data)
        # chart_plt_w.quad_regress(self.parent.calculation.chart_quad_regress_data)
        #
        # self.lst_Thread.append(MyThread(
        #     lambda: chart_plt_w.start())
        # )
        # self.ui.pushButton_8.clicked.connect(
        #     lambda: self.lst_Thread[3].start()
        # )

        self.ui.pushButton.clicked.connect(self.exit_w)
        # self.ui.pushButton_2.clicked.connect(self.view_table)

    def exit_w(self):
        self.table_loader_results_1.kwargs['block'] = False
        self.close()

    # def exec_(self) -> int:
    #     a = super().exec_()
    #     for i in self.lst_Thread:
    #         i.wait()
    #     return a

    def view_table(self):
        # self.parent.table_loader1.open_table()
        # self.parent.table_loader2.open_table()
        pass


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
