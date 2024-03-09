import matplotlib.pyplot as plt
from pandas import DataFrame

# CONST
pi = 3.14159265
Yc = 17.3 * (10 ** -6)

class ChartLinePltData:
    def __init__(self, n, df: DataFrame, xlabel: str = '', ylabel: str = ''):
        self.n = n
        self.columns = df.columns
        self.index = df.index
        self.df = df
        self.xlabel = xlabel
        self.ylabel = ylabel


class ChartQuadRegressPltData:
    def __init__(self, n, df: DataFrame, linestyle='dashed', linewidth=2):
        self.n = n
        self.columns = df.columns
        self.index = df.index
        self.df = df
        self.linestyle = linestyle
        self.linewidth = linewidth
        pass


class ChartLinePLT:
    def __init__(self, data: ChartLinePltData, alpha=0.75):
        plt.figure(data.n)
        plt.plot(data.df, marker='o', label=[f"E={i}" for i in data.columns], alpha=alpha)
        plt.grid(linestyle='--')
        plt.ylabel(data.xlabel)
        plt.xlabel(data.ylabel)
        plt.xlim([0, max(data.index) * 1.2])
        plt.ylim([0, max(data.df.max()) * 1.2])
