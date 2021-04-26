# функция преобразование формата времени
def time_format(t):
	return '{0:02.0f}:{1:02.0f}'.format(*divmod(t, 60))

# функция деления на ноль	
def zero_div(x, y):
	return x / y if y else 0