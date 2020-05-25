import numpy as np
from PIL import Image
im = Image.open("flower.jpg")  #Image location
fil= (-0.25,-0.5,-0.25,-0.5,4,-0.5,-0.25,-0.5,-0.25)   #Sharpening filter
fil=np.reshape(fil,(3,3))   

#Sharpening the Value component of the HSV data
def sharpen(height, width, v):

	for i in range(1,height-1):
		for j in range(1,width-1):
			ker=[[v[i-1][j-1],v[i-1][j],v[i-1][j+1]],[v[i][j-1],v[i][j],v[i][j+1]],[v[i+1][j-1],v[i+1][j],v[i+1][j+1]]]
			v[i][j]=np.sum(np.multiply(ker,fil))

	return v

#Boosting the Saturation
def saturation(s,a):
    #s= s+a/100*(1-s)
    s=s*(1+a/100)
    if s>1: s=1
    return s

#Converting HSV data of the Image to its equivalent RGB data
def hsv_rgb(hsv):

	rgb= list()
	for i in hsv:
		h = i[0]
		s = i[1]
		v = i[2]
		c = v * s
		x = c* (1- abs(((h / 60) %2)-1))
		m = v - c

		if h>=0 and h<60:
				r = c
				g = x
				b = 0

		elif h>=60 and h<120:
				r = x
				g = c
				b = 0

		elif h>=120 and h<180:
				r = 0
				g = c
				b = x

		elif h>=180 and h<240:
				r = 0
				g = x
				b = c

		elif h>=240 and h<300:
				r = x
				g = 0
				b = c

		elif h>=300 and h<360:
				r = c
				g = 0
				b = x

		R = (r+m)*255
		G = (g+m)*255
		B = (b+m)*255

		rgb.append((int(R),int(G),int(B)))
	return rgb
def startProcess():
	rgbim = Image.new('RGB', im.size)
	width,height = im.size
	hsv=[]
	v=[]
	pix_val=list(im.getdata())
	a=float(input("Enter the Saturation value to change the Saturation of Image:"))

#Converting RGB data to its equivalent HSV data
	for i in pix_val:
		r= i[0]/255
		g= i[1]/255
		b= i[2]/255
			
		Cmax = max(r,g,b)
		Cmin = min(r,g,b)
		delta = Cmax - Cmin

		#Hue Calculation:
		if delta == 0:
			h = 0
		elif Cmax == r:
			h = 60*(((g-b)/delta) % 6)
		elif Cmax == g:
			h = 60*(((b-r)/delta) + 2)
		elif Cmax == b:
			h = 60*(((r-g)/delta) + 4)

		# Saturation calculation:
		if Cmax == 0:
			sat = 0
		else:
			sat = delta/Cmax

		#Value calculation:
		val = Cmax

		v.append(val)
		
		sat=Saturation(sat,0.3)

		hsv.append([h , sat, val])	
	# Reshaping the value matrix
	v = np.reshape(v, (height,width))
	v = sharpen(height, width, v)
	
	k=0
	for i in range(0, height):
		for j in range(0, width):
			hsv[k][2] = v[i][j]
			k+=1
	
	rgb=hsv_rgb(hsv)

	#Reconstructing the image
	rgbim.putdata(rgb)
	rgbim.show()

startProcess()


	
