import salabim as sim
import numpy as np
import matplotlib.pyplot as plt

SIM_TIME = 5  # дней

DEVICES = 8  # количество аппаратов
#DOCTORS = 10  # количество врачей

# распределения
D_INTERPRETATION = sim.Uniform(3, 15)
#D_STUDY_IAT = sim.Normal(10, 2)

# интенсивность исследований в час (на 24 часа)
m_rg = [2, 2, 2, 2, 3, 3, 4, 4, 5, 6, 6, 6, 4, 4, 5, 5, 5, 4, 4, 3, 3, 3, 3, 2]

# количество врачей в час (на 24 часа)
m_doc = [1, 1, 1, 1, 1, 1, 1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1]

# функция преобразование формата времени
def time(t):
	return '{0:02.0f}:{1:02.0f}'.format(*divmod(t, 60))


# генератор исследований
class Generator(sim.Component):
	def __init__(self, data, mdoc, *args, **kwargs):
		self.data = data * SIM_TIME
		self.mdoc = mdoc * SIM_TIME

		sim.Component.__init__(self, *args, **kwargs)

	def study_iat(self):
		t = [0.0]
		n = 0
		while t[n] <= int(env.days(SIM_TIME)):
			lmbd = self.data[int(t[n]) // 60] / 60
			r = np.random.uniform(0, 1)
			teta = (-1 / lmbd) * np.log(r)
			if t[n] + teta < int(env.days(SIM_TIME)):
				time = t[n] + teta
				t.append(time)
			else:
				break
			n += 1
		return t

	def process(self):
		times = self.study_iat()
		prev = 0
		for time in times:
			doctors.set_capacity(int(self.mdoc[int(time//60)]))
			Study()
			yield self.hold(time - prev)
			prev = time


# обычные исследования
class Study(sim.Component):
	def process(self):
		self.enter(worklist)
		print('Исследование: ', self.name(), 'поставлено в очередь в ', time(env.now()))
		if len(cito_worklist) == 0:
			yield self.request(doctors, fail_delay=1440)
			yield self.hold(D_INTERPRETATION)
			if self.failed():
				env.studies_failed += 1
				env.print_trace("", "", "failed")
			self.leave(worklist)
			print('Исследование: ', self.name(), 'описано в ', time(env.now()))
		else:
			yield self.hold(5)
			self.release()


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
#env.time_to_str_format('{0:02.0f}')

# счетчики нарушения SLA
env.cito_studies_failed = 0
env.studies_failed = 0

# очереди
worklist = sim.Queue("worklist")
cito_worklist = sim.Queue("cito_worklist")

# врачи
doctors = sim.Resource("doctors", capacity=0)


# запуск генератора исследований
for i in range(DEVICES):
	gen = Generator(m_rg, m_doc)
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
	*worklist.length.tx(), *cito_worklist.length.tx(), drawstyle='steps-plot')
plt.show()

