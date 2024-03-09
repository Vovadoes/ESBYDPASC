import math

# from Charts import *


# from scipy.stats import t

# CONST
pi = 3.14159265
Yc = 17.3 * (10 ** -6)


def myround(x: float, lst: list):
    for i in lst:
        if x < i:
            return i
    return lst[-1]


class Calculation:
    def __init__(self, n: float, k: int, lst: list):
        self.lst_y = [(lst[i][0] + lst[i][1]) / 2 for i in range(k)]

        self.lst_y_n = [self.lst_y[i] * lst[i][2] for i in range(k)]

        self.x_cp_v = sum(self.lst_y_n) / n
        print(f"{self.x_cp_v=}")

        self.lst_y_x_n = [pow(self.lst_y[i] - self.x_cp_v, 2) * lst[i][2] for i in
                          range(k)]

        self.S_2_n = sum(self.lst_y_x_n) / (n - 1)

        print(f'{self.S_2_n=}')

        self.s = math.sqrt(self.S_2_n)
        print(f"{self.s=}")

        self.S_xcp = self.s / math.sqrt(n)
        print(f"{self.S_xcp=}")


if __name__ == "__main__":
    n = 100
    k = 7
    lst = [
        [23, 25, 3],
        [25, 27, 10],
        [27, 29, 6],
        [29, 31, 16],
        [31, 33, 15],
        [33, 35, 30],
        [35, 37, 20]
    ]
    calculation = Calculation(n, k, lst)

    # ChartLinePLT(calculation.chart_v_y_data)
    # plt.legend()
    # plt.show()
