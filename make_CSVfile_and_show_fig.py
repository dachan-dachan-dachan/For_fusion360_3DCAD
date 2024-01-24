import csv
import math

import matplotlib.pyplot as plt
import pandas as pd


def func(z, z_start, z_rate, x_rate, x_b):#式．zが独立変数で，xが従属変数．
    x =  (( math.cosh( (z + z_start)/z_rate ) )/x_rate ) + x_b
    #x =  ( math.cosh( -(z/z_rate ) + z_start)/x_rate ) + x_b
    return x

def csv_save(csv_file):#x,y,zの形式で保存する．yは常に0になるようにした．
    with open(csv_file, "a", newline="") as file:
        for i in range(len(x)):
            file.write(f"{x[i]},0,{z[i]}\n")


csv_file = "A_3.csv"
point_num = 100
z_min = 0
z_max = 6
z_start = - z_max
z_rate = 2.5#ここを変えると大きく変わる．
x_min = 1
x_max = 7
x_d = 0.5


z_start = - z_max
x_rate =  ( ( math.cosh(z_max/z_rate) ) - 1 ) / ( x_max - x_min )
x_b = x_min - (1/x_rate)


tem_z = []
x = []
z = []

for i in range(point_num + 1):
    tem_z.append(( i*(z_max - z_min)/point_num ) + z_min)
    x.append(func(tem_z[i], z_start, z_rate, x_rate, x_b))
    z.append(tem_z[i])

for i in range(point_num + 1):
    k = point_num - i
    x.append( func(tem_z[k], z_start, z_rate, x_rate, x_b - x_d) )
    z.append(tem_z[k])


#csvファイルの数値の単位は[cm]，fusion360の単位は[mm]なことに注意
csv_save(csv_file)


plt.plot(x, z, marker = "")
plt.show()
