from struct import unpack as sup
import svgwrite as svg
import json

def chunk(l, n):
	for i in xrange(0,len(l), n):
		yield l[i:i+n]

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.pair = (x,y)
	def __repr__(self):
		return "({}, {})".format(self.x, self.y)

class Poly:
	def __init__(self, r,g,b,a, verts):
		self.r = r
		self.g = g
		self.b = b
		self.a = a
		self.verts = []
		for x,y in chunk(verts, 2):
			self.verts.append(Point(x,y))
		self.dict = {'r':self.r,'g':self.g,'b':self.b,'a':self.a,'verts':[i.pair for i in self.verts]}
		
	def json(self):
		fn = raw_input('File Name?')
		with open('{}.json'.format(fn.lower()),'w') as f:
			f.write(json.dumps(self.dict))

	def draw2svg(self, canvas, scale):
		pnts = [tuple((vert.x*scale, vert.y*scale)) for vert in self.verts]
		print pnts, (self.r*255,self.g*255,self.b*255), self.a
		canvas.add(svg.shapes.Polygon(points=pnts, fill=svg.rgb(self.r*255,self.g*255,self.b*255), opacity=self.a))
			
	def __repr__(self):
		return "Color:\n\tRed: {}\n\tGreen: {}\n\tBlue: {}\n\tAlpha: {}\nVerticies:\n\t{}".format(self.r,self.g,self.b,self.a,'\n\t'.join(str(i) for i in self.verts))
		
class DNA:
	def json(self, fn):
		with open('{}.json'.format(fn.lower()),'w') as f:
			f.write(json.dumps(dict(zip(xrange(0,len(self.polys),1),[i.dict for i in self.polys]))))
	
	def svg(self, saveLoc, hieght, width, scale):
		canvas = svg.Drawing(saveLoc, size=(str(int(width)*int(scale)),str(int(hieght)*int(scale))))
		for poly in self.polys:
			poly.draw2svg(canvas, int(scale))
		canvas.save()
		
class MonaDNA(DNA):
	def __init__(self, rawDNA):
		self.polys = []
		self.verts_per_poly, self.polys_total = tuple(struct.unpack('i',i)[0] for i in (rawDNA[0:4], rawDNA[4:8]))
		for i in [[sup('d',i)[0] for i in chunk(k,8)][0:4+int(self.verts_per_poly)*2] for k in chunk(rawDNA[8:],288)]:
			self.polys.append(Poly(i[0],i[1],i[2],i[3],i[4:]))
		
class WebDNA(DNA):
	def __init__(self, rawDNA):
		self.polys = []
		rawDNA = [float(i) for i in rawDNA.split(' ')]
		self.verts_per_poly, self.polys_total = [int(i) for i in rawDNA[0:2]]
		self.polys = [Poly(i[0],i[1],i[2],i[3],i[4:]) for i in chunk(rawDNA[2:],int(4+ 2*self.verts_per_poly))]
