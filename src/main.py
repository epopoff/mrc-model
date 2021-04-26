import matplotlib.pyplot as plt
from nhpp import get_arrivals

knots = {0: 0, 5: 0, 6: 0.02, 7: 0.2, 8: 0.68, 9: 1, 10: 1.1, 11: 0.93, 12: 0.92, 13: 0.84, 14: 0.82, 15: 1.07, 16: 1.18, 17: 1.09, 18: 1.05, 19: 0.61, 20: 0.25, 21: 0.08, 22: 0.01, 24: 0}

ST = 3

arrs = get_arrivals(knots)
print('Sum: ', len(arrs))
#for arr in arrs:
#	print(round(arr, 2))

l = len(arrs)

for i in range(1,ST):
  for j in range(l):
    arrs.append(arrs[j] + 24 * i)

sdph_y = [0] * 24 * ST
sdph_x = []
for i in range(0, 24 * ST):
	sdph_x.append(i)
for arr in arrs:
	sdph_y[int(arr)] += 1

plt.plot(sdph_x, sdph_y, drawstyle='steps')
#plt.plot(sdph_x, m_mrt, drawstyle='steps')
plt.show()