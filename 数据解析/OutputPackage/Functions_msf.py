# -*- coding UTF-8 -*-
def Start_PG():
    print(r"\********程序运行开始********/")


def End_PG():
    print(r"\********程序运行结束********/")


def Print_Tip(x):
    print(r"\****" + str(x) + "****/")


def Newline():
    print("")


def Space():
    print("    ", end="")


# 输出一个tab
def Tab():
    print("\t", end="")


def Print(x, y=0, name=None):
    if name is None:
        if y == 0:
            if isinstance(x, int):
                print(f"Int:\t\t{x:3d}")
            if isinstance(x, float):
                print(f"Float:\t\t{x:.2f}")
            if isinstance(x, complex):
                print(f"Complex:\t\t{x.real:.2f}{x.imag:+.2f}")
            if isinstance(x, list):
                print("List:\t", x)
            if isinstance(x, tuple):
                print("Tuple:\t", x)
            if isinstance(x, set):
                print("Set:\t", x)
            if isinstance(x, dict):
                print("Dict:\t", x)
            if isinstance(x, str):
                print(f"Str:\t\t{x}")
        else:
            if isinstance(x, int):
                print(f"\tInt:\t\t{x:3d}")
            if isinstance(x, float):
                print(f"\tFloat:\t\t{x:.2f}")
            if isinstance(x, complex):
                print(f"\tComplex:\t\t{x.real:.2f}{x.imag:+.2f}")
            if isinstance(x, list):
                print("\tList:\t", x)
            if isinstance(x, tuple):
                print("\tTuple:\t", x)
            if isinstance(x, set):
                print("\tSet:\t", x)
            if isinstance(x, dict):
                print("\tDict:\t", x)
            if isinstance(x, str):
                print(f"\tStr:\t\t{x}")
    else:
        if y == 0:
            print(f"{name}:\t{x}")
        else:
            print(f"\t{name}:\t{x}")
