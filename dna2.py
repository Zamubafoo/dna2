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
	def __init__(self, rawDNA, numPoints):
		self.polys = []
		processedDNA = [[sup('d',i)[0] for i in chunk(k,8)][0:4+int(numPoints)*2] for k in chunk(rawDNA,288)]
		for i in processedDNA:
			self.polys.append(Poly(i[0],i[1],i[2],i[3],i[4:]))
	
	def json(self):
		fn = raw_input('File Name? ')
		with open('{}.json'.format(fn.lower()),'w') as f:
			f.write(json.dumps(dict(zip(xrange(0,len(self.polys),1),[i.dict for i in self.polys]))))
	
	def svg(self, saveLoc, hieght, width, scale):
		canvas = svg.Drawing(saveLoc, size=(str(int(width)*int(scale)),str(int(hieght)*int(scale))))
		for poly in self.polys:
			poly.draw2svg(canvas, int(scale))
		canvas.save()

if __name__ == "__main__":
	from sys import argv
	print argv
	with open(argv[1]) as f:
		rawDNA=f.read()
	dnaStruct = DNA(rawDNA, argv[2])
	dnaStruct.json()
	dnaStruct.svg(argv[6],argv[3],argv[4],argv[5])
	
	#dna2svg <filepath to .dna> <points per poly> <height> <width> <scale> <svg save path>
