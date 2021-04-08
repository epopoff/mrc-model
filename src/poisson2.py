import numpy as np
import matplotlib.pyplot as plt

SIM_TIME = 1440  # время симуляции в минутах
#m_rg = 2

m_rg = [
	2, 2, 2, 2, 3, 3, 4, 4, 5, 6, 6, 6, 4, 4, 5, 5, 5, 4, 4, 3, 3, 3, 3, 3
]  # интенсивность исследований в час
'''
m_rg = [
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6
]
'''

#np.random.seed(100)


# функция формирует временные интервалы на основе заданного массива интенсивностей
def inter_arrival_time(m):
	t = [0.0]
	n = 0
	while t[n] <= SIM_TIME:
		lmbd = m[int(t[n]) // 60] / 60
		#lmbd = m / 60
		r = np.random.uniform(0, 1)
		teta = (-1 / lmbd) * np.log(r)
		if t[n] + teta < SIM_TIME:
			time = t[n] + teta
			t.append(time)
		else:
			break
		n += 1
	return t


iat_rg = inter_arrival_time(m_rg)

sdph_y = [0] * 24
sdph_x = []
for i in range(0, 24):
	sdph_x.append(i)
for iat in iat_rg:
	sdph_y[int(iat // 60)] += 1

plt.plot(sdph_x, sdph_y, drawstyle='steps-plot')
plt.plot(sdph_x, m_rg, drawstyle='steps-plot')
plt.show()

print(sum(m_rg), ' - ', sum(sdph_y), ' = ', sum(m_rg)-sum(sdph_y))

'''
y = []
x = []
for i in range(10000):
	iat_rg = inter_arrival_time(m_rg)
	x.append(len(iat_rg))
	y.append(i)

#график количества получившихся исследований по экспериментам (среднее 20)
plt.plot(y, x)
plt.show()
'''

