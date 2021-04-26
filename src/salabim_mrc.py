import salabim as sim
import numpy as np

from misc_tools import time_format

# генератор исследований
class Generator(sim.Component):
	def __init__(self, mstud, mdoc, *args, **kwargs):
		self.SIM_TIME = SIM_TIME
        self.mstud = mstud * SIM_TIME
		self.mdoc = mdoc * SIM_TIME

		sim.Component.__init__(self, *args, **kwargs)

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

	def process(self):
		times = self.study_iat()
		prev = 0
		for time in times:
			doctors.set_capacity(
				int(self.mdoc[int(time // 60)]))  	# устанавливаем кол_во врачей
			Study()  								# создаем исследование
			yield self.hold(time - prev)
			prev = time


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