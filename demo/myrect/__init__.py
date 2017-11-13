class Rect(object):
	def __init__(self,_w=0,_h=0):
		self.w=_w
		self.h=_h
	    
	def area(self):
		return self.w*self.h
	def perim(self):
		return 2*(self.w+self.h)
	def __str__(self):
		return "w: {}, h: {}, area: {}, perim:{}".format(
			self.w, self.h, self.area(), self.perim()
		)

class Square(Rect):
	def __init__(self,_e=0):
		self.w=_e
		self.h=_e
	def inner_cir_area(self):
		return 3.14159*self.w*self.w*0.5