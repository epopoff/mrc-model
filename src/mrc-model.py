import salabim as sim
#import salabim_mrc as sim_mrc
import numpy as np
import matplotlib.pyplot as plt

from misc_tools import time_format
from nhpp import get_arrivals

SIM_TIME = 5  			# дней

DEVICES = 8 			# количество аппаратов
#DOCTORS = 10  			# количество врачей

# распределения
D_INTERPRETATION = sim.Uniform(15, 40)

# интенсивность исследований в час (на 24 часа)
#m_mrt = [0, 0, 0, 0, 0, 0.5, 0.5, 1, 1, 1.5, 1, 1, 1, 1, 1.5, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0, 0]

#m_mrt = [
#	0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0
#]

knots = {
	0: 0, 5: 0, 6: 0.02, 7: 0.2, 8: 0.68, 9: 1, 10: 1.1, 11: 0.93, 12: 0.92, 13: 0.84, 14: 0.82, 15: 1.07, 16: 1.18, 17: 1.09, 18: 1.05, 19: 0.61, 20: 0.25, 21: 0.08, 22: 0.01, 24: 0
	}


# количество врачей в час (на 24 часа)
m_doc = [
	0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0
]


# генератор исследований
class Generator(sim.Component):
	def __init__(self, knots, mdoc, *args, **kwargs):
		#self.mstud = mstud * SIM_TIME
		self.knots = knots
		self.mdoc = mdoc * SIM_TIME

		sim.Component.__init__(self, *args, **kwargs)
	'''
	# функция генерирует массив временных меток когда были выполнены исследования
	def study_iat(self):
		t = [0.0]
		n = 0
		time = 0
		while time <= int(env.days(SIM_TIME)):
			if self.mstud[int(time) // 60] != 0:
				lmbd = self.mstud[int(time) // 60] / 60
				r = np.random.uniform(0, 1)
				teta = (-1 / lmbd) * np.log(r)
				if time + teta < int(env.days(SIM_TIME)):
					time += teta
					t.append(time)
				else:
					break
			else:
				time += 60
				pass
			n += 1
		return t
	'''

	def process(self):
		times = get_arrivals(knots)
		
		l = len(times)

		for i in range(1, SIM_TIME):
			for j in range(l):
				times.append(times[j] + 24 * i)

		prev = 0
		for time in times:
			doctors.set_capacity(int(self.mdoc[int(env.hours(time) // 60)]))  	# устанавливаем кол_во врачей
			print('Doctors capacity ', doctors.capacity())
			Study()  								# создаем исследование
			yield self.hold(env.hours(time) - prev)
			prev = env.hours(time)


# обычные исследования
class Study(sim.Component):
	def process(self):
		self.enter(worklist)
		t = env.now()
		print(time_format(env.now()), self.name(), 'выполнено')
		if len(cito_worklist) == 0:
			yield self.request(doctors, fail_delay=env.hours(24))
			yield self.hold(D_INTERPRETATION)
			if self.failed():  												# проверка нарушения SLA
				env.studies_failed += 1
				print(time_format(env.now()), self.name(), 'FAILED')
				#env.print_trace("", "", "FAILED")
			self.leave(worklist)
			t = env.now() - t
			print(
				time_format(env.now()), self.name(), 'описано.', 'Время в очереди: ', time_format(t))
		else:
			pass
			#yield self.hold(5)
			#self.release()


'''
# экстренные исследования
class Study_CITO(sim.Component):
	def process(self):
		self.enter(cito_worklist)
		print('CITO исследование: ', self.name(), 'поставлено в очередь в ', time(env.now()))
		yield self.request(doctors, fail_delay=120)
		yield self.hold(D_INTERPRETATION)
		print('CITO исследование: ', self.name(), 'описано в ', time(env.now()))
		if self.failed():
			env.cito_studies_failed += 1
			env.print_trace("", "", " cito failed")
		self.leave(cito_worklist)
		self.release()
'''


# определяем окружение
env = sim.Environment(time_unit='minutes', trace=False)

# счетчики нарушения SLA
env.cito_studies_failed = 0
env.studies_failed = 0

# очереди
worklist = sim.Queue("worklist")
cito_worklist = sim.Queue("cito_worklist")

# врачи
doctors = sim.Resource(name='doctor.', capacity=0)

# запуск генератора исследований
for i in range(DEVICES):
	gen = Generator(knots, m_doc)
	gen.process()

# начинаем симуляцию
env.run(till=env.days(SIM_TIME))

# статистика
#worklist.print_statistics()
#cito_worklist.print_statistics()
#doctors.print_statistics()

# нарушения SLA
print('Нарушения SLA обычные', env.studies_failed)
print('Нарушения SLA CITO', env.cito_studies_failed)

# графики
plt.plot(
	*worklist.length.tx(), *cito_worklist.length.tx(), drawstyle='steps')
plt.show()
'''
x = []

y = 0
for _ in range(24):
	x.append(y)
	y += 1
plt.plot(x, m_doc, drawstyle='steps')
plt.plot(x, m_rg, drawstyle='steps')
plt.show()
'''

