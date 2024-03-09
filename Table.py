from typing import Callable
from typing import List, Any

from PyQt5 import QtWidgets, QtGui
from files.TableWindow import Ui_Form as Ui_Form_Table
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UI import mywindow


class Table(QtWidgets.QDialog):
    def __init__(self, base: 'mywindow', n: int, m: int, data: List[List[Any]] = None,
                 block: bool = False,
                 heading_x: Callable[[int], str] = lambda iterator: str(iterator),
                 heading_y: Callable[[int], str] = lambda iterator: str(iterator),
                 filter_table=lambda dct:
                 round(dct['value'], 5)
                 if dct['value'] is int or dct['value'] is float else
                 dct['value'],
                 types_matrix=None
                 ):
        super(Table, self).__init__()
        self.ui = Ui_Form_Table()
        self.ui.setupUi(self)
        self.setWindowTitle('Таблица')
        self.base = base
        self.block = block
        self.heading_x = heading_x
        self.heading_y = heading_y
        if types_matrix is None:
            types_matrix = [[float for _ in range(n)] for _ in range(m)]
        self.types_matrix = types_matrix
        if data is None:
            data = []
        self.data = data
        self.n = n
        self.m = m
        self.filter = filter_table

        VerticalHeaderLabels = [self.heading_y(i) for i in range(max(len(self.data), self.m))]
        HorizontalHeaderLabels = [
            self.heading_x(i) for i in
            range(max(len(self.data[0]) if len(self.data) > 0 else self.n, self.n))
        ]
        for j in range(min(len(self.data[0]) if len(self.data) > 0 else self.n, self.n)):
            self.ui.tableWidget.insertColumn(j)

        for i in range(min(len(self.data), self.m)):
            self.ui.tableWidget.insertRow(i)
            for j in range(min(len(self.data[0]) if len(self.data) > 0 else self.n, self.n)):
                self.ui.tableWidget.setItem(
                    i,
                    j,
                    QtWidgets.QTableWidgetItem(
                        str(self.filter({'i': i, 'j': j, 'value': self.data[i][j]}))
                    )
                )

        for j in range(len(self.data[0]) if len(self.data) > 0 else 0, self.n):
            self.ui.tableWidget.insertColumn(j)
        for i in range(len(self.data), self.m):
            self.ui.tableWidget.insertRow(i)

        for i in range(0, self.m):
            start = len(self.data[0]) if len(self.data) > 0 else 0
            if len(self.data) <= i < self.m:
                start = 0
            for j in range(start, self.n):
                self.ui.tableWidget.setItem(
                    i,
                    j,
                    QtWidgets.QTableWidgetItem("0.0")
                )
        self.ui.tableWidget.setHorizontalHeaderLabels(HorizontalHeaderLabels)
        self.ui.tableWidget.setVerticalHeaderLabels(VerticalHeaderLabels)

        self.ui.tableWidget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.ui.tableWidget.resizeColumnsToContents()

        if self.block:
            self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.ui.pushButton.clicked.connect(self.download_table)
        # self.ui.pushButton.clicked.connect(self.close_window)

    def close_window(self):
        self.close()

    def download_table(self):
        flag = False
        self.data = []
        for i in range(self.m):
            lst = []
            for j in range(self.n):
                try:
                    lst.append(
                        self.types_matrix[i][j](self.ui.tableWidget.item(i, j).text().replace(",", '.')))
                    self.ui.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 255, 255))
                except ValueError:
                    # print('error')
                    self.ui.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 0, 0))
                    flag = True
                except IndexError as s:
                    print(i, j, s)
            self.data.append(lst)
        if flag:
            self.data = []
        else:
            self.close()
        print(f"download_table data = {self.data}")
