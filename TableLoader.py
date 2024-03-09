from typing import List, Any, TYPE_CHECKING
from PyQt5.QtWidgets import QLabel
from Table import Table

if TYPE_CHECKING:
    from UI import mywindow


class TableLoader:
    def __init__(self, main_window, n: int = 0, m: int = 0, label: QLabel = None,
                 data: List[List[Any]] = None, **kwargs):
        self.data = data
        if data is None:
            self.data = []
        self.n = n
        self.m = m
        self.main_window: 'mywindow' = main_window
        self.kwargs = kwargs
        self.label = label

    def open_table(self):
        self.main_window.variables.update()
        tale_window = Table(self.main_window, self.n, self.m, self.data, **self.kwargs)
        tale_window.show()
        tale_window.exec_()
        self.data = tale_window.data

        if self.label:
            if self.main_window:
                self.label.setStyleSheet("background-color: lightgreen")
            else:
                self.label.setStyleSheet("background-color: red")

    def valid(self, m, n):
        if len(self.data) == self.m:
            if len(self.data[0]) == self.n or len(self.data) == 0 == self.n:
                if self.n == n and self.m == m:
                    return True
                else:
                    self.n = n
                    self.m = m
        if self.label:
            self.label.setStyleSheet("background-color: red")
        return False
