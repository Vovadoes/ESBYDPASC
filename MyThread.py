from PyQt5.QtCore import QThread


class MyThread(QThread):
    def __init__(self, fun=lambda: None):
        self.fun = fun
        super(MyThread, self).__init__()

    def start(self, priority: 'QThread.Priority' = None) -> None:
        self.fun()
        super().start()
        self.exec_()
        self.quit()
