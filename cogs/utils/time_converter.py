
class TimeConverter():
	def __init__(self, number):
		self.number = number

	def toHours(self):
		return ((self.number / 60) / 60)

	def toMinutes(self):
		return ((self.number) / 60)

	def toDays(self):
		return (((self.number / 60) / 60) / 24)
