#! /usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

#plot image
def im(data,num_sd=0):
	myim = plt.imshow(np.transpose(data),interpolation='nearest',origin='lower')
	plt.axis('off')
	return myim


#Given size of image and/or center of rectangle, return corners to plot rectangle
def drawrec(size,pos=np.zeros(2,int)):

	reclength = np.int(np.round(size/1.8))
	recheight = np.int(np.round(reclength*(1/2)))

	if not np.array_equal(pos,np.zeros(2)):
		pos[0] = np.round(pos[0] - reclength/2)
		pos[1] = np.round(pos[1] - recheight/2)
		
		#checking size of rectangle and keep it within image
		if pos[0]+reclength > size:
			pos[0] = size-reclength
		elif pos[0] < 0:
			pos[0] = 0
		
		if pos[1]+recheight > size:
			pos[1] = size-recheight
		elif pos[1] < 0:
			pos[1] = 0		
				
	rec = np.array([[0, 0, reclength, reclength, 0 ],[0, recheight, recheight, 0, 0]])
	rec[0,:] = pos[0]+rec[0,:]
	rec[1,:] = pos[1]+rec[1,:]
	
	return rec.copy()


#plot the lower full image with a rectangle and the and upper cropped image of the area enclosed by the rectangle
def plotimandzoom(myim,myzoomim,ax,myplot,cbox,topo):

	#plots full image
	myim.set_data(topo.transpose())
	#plot cropped image
	myzoomim.set_data(topo[cbox[0,0]:cbox[0,2],cbox[1,0]:cbox[1,2]].transpose())
	#remove dots on full image
	ax.lines.remove(myplot)
	#plot new dots
	myplot, = ax.plot(cbox[0,:],cbox[1,:],'k')

	plt.draw()
	
	return myplot
	
#Plot points on upper cropped image
#points => all dots on entire image
#cbox => coordinates for cropped rectangle
#ax => plot handle for plotting or deleting data
#myplot => plot handle for plotting or deleting data
#numtext => plot text handle for numbers correspoinding dots
def plotclickedpointtop(points,cbox,ax,myplot,numtext):
	if myplot != 0:
		try:	
			ax.lines.remove(myplot)
		except Exception as e: 
			print(e)
			
	mylogic_lowleft = (points >= cbox[:,0])
	mylogic_upperright = (points <= cbox[:,2])

	zoompoints = []
	pointlabel = []
	
	
	for i in range(0,len(points)):
		if np.all(mylogic_lowleft[i,:]) and np.all(mylogic_upperright[i,:]):
			x_zoompoint = np.round(points[i,0] - cbox[0,0])
			y_zoompoint = np.round(points[i,1] - cbox[1,0])
			zoompoints.append([x_zoompoint,y_zoompoint])
			pointlabel.append(i)
	
	zoompoints = np.array(zoompoints)

	if not np.array_equal(zoompoints,[]):
		myplot, = ax.plot(zoompoints[:,0],zoompoints[:,1],'r.',markersize=10)
		numtext = numlabel(zoompoints,ax,pointlabel,numtext)

	else:
		if str(type(numtext[0])) == "<class 'matplotlib.text.Text'>":
			for i in range(0,len(numtext)):
				numtext[i].remove()
		numtext = [0]

	plt.draw()

	return (myplot,numtext)
	
def plotclickedpointbottom(points,ax,myplot,numtext):
	if myplot != 0:
		try:		
			ax.lines.remove(myplot)
		except Exception as e: 
			print(e)
	
	if not np.array_equal(points,[]):
		myplot, = ax.plot(points[:,0],points[:,1],'r.',markersize=10)
		pointlabel = np.arange(0,len(points))
		numtext = numlabel(points,ax,pointlabel,numtext)

	plt.draw()
	return (myplot,numtext)

def numlabel(points,ax,pointlabel,numtext):

	if str(type(numtext[0])) == "<class 'matplotlib.text.Text'>":
		for i in range(0,len(numtext)):
				numtext[i].remove()
	numtext = []

	
	for i in range(0,len(points)):
		mylabel = pointlabel[i]+1
		
		if not np.array_equal(points,[]):
			numtext.append(ax.text(points[i,0],points[i,1],'%d' % mylabel,color='orange'))

	return numtext

def onclick(event,reftopo,movtopo,myfig,ax,myim,myplot,refpoints,movpoints,refpointlist,movpointlist,cbox):
	
	global cid	
	
	if event.inaxes.get_geometry()[2] == 1:
		if event.button == 1:
			refnewpoint = np.array(np.round([event.xdata, event.ydata]))
			refnewpoint = np.array([np.round(cbox[0][0,0]+refnewpoint[0]), np.round(cbox[0][1,0]+refnewpoint[1])])
			refpointlist.append(refnewpoint)
		elif event.button == 3:
			if not np.array_equal(refpointlist,[]):
				refpointlist.pop(-1)
		refpoints[2], refpoints[3] = plotclickedpointbottom(np.asanyarray(refpointlist),ax[0],refpoints[2],refpoints[3])			
		refpoints[0], refpoints[1] = plotclickedpointtop(np.asarray(refpointlist),cbox[0],ax[2],refpoints[0],refpoints[1])
	elif event.inaxes.get_geometry()[2] == 2:
		if event.button == 1:
			movnewpoint = np.array(np.round([event.xdata, event.ydata]))
			movnewpoint = np.array([np.round(cbox[1][0,0]+movnewpoint[0]), np.round(cbox[1][1,0]+movnewpoint[1])])
			movpointlist.append(movnewpoint)
		elif event.button == 3:
			if not np.array_equal(movpointlist,[]):
				movpointlist.pop(-1)
		movpoints[2], movpoints[3] = plotclickedpointbottom(np.asanyarray(movpointlist),ax[1],movpoints[2],movpoints[3])
		movpoints[0], movpoints[1] = plotclickedpointtop(np.asarray(movpointlist),cbox[1],ax[3],movpoints[0],movpoints[1])
	elif event.inaxes.get_geometry()[2] == 3:
		refnewpos = np.array(np.round([event.xdata, event.ydata]))
		cbox[0] = drawrec(reftopo.shape[0],refnewpos)
		if event.button == 1:		
			myplot[0] = plotimandzoom(myim[0],myim[2],ax[0],myplot[0],cbox[0],reftopo)
			refpoints[0], refpoints[1] = plotclickedpointtop(np.asarray(refpointlist),cbox[0],ax[2],refpoints[0],refpoints[1])
		elif event.button == 3:
			myfig.canvas.mpl_disconnect(cid)
			plt.close(myfig)
	elif event.inaxes.get_geometry()[2] == 4:
		movnewpos = np.array(np.round([event.xdata, event.ydata]))
		cbox[1] = drawrec(movtopo.shape[0],movnewpos)
		if event.button == 1:
			myplot[1] = plotimandzoom(myim[1],myim[3],ax[1],myplot[1],cbox[1],movtopo)
			movpoints[0], movpoints[1] = plotclickedpointtop(np.asarray(movpointlist),cbox[1],ax[3],movpoints[0],movpoints[1])
		elif event.button == 3:
			myfig.canvas.mpl_disconnect(cid)
			plt.close(myfig)

	#print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f, axes=%s' % (event.button, event.x, event.y, event.xdata, event.ydata, event.inaxes.get_geometry()))


	
def cpselect(myreftopo,mymovtopo):

	global cid
		
	reftopo = myreftopo.T.copy()
	movtopo = mymovtopo.T.copy()

	reftopo = np.flipud(reftopo)
	movtopo = np.flipud(movtopo)
	
	reftopplot = 0
	refnumtexttop = [0]
	refbottomplot = 0
	refnumtextbottom = [0]
	refpointlist = []
	
	movtopplot = 0
	movnumtexttop = [0]
	movbottomplot = 0
	movnumtextbottom = [0]
	movpointlist = []

	refpoints = [reftopplot, refnumtexttop, refbottomplot, refnumtextbottom, refpointlist]	
	movpoints = [movtopplot, movnumtexttop, movbottomplot, movnumtextbottom, movpointlist]	
		
	
	myfig = plt.figure('cpselect')
	
	
	
	#Plot refence image in the lower left
	ax1 = myfig.add_subplot(223)
	plt.set_cmap('gray')
	myim1 = im(reftopo)
	refcbox = drawrec(reftopo.shape[0],[0,0]) #Draw rectangle in original lower left image
	myplot1, = ax1.plot(refcbox[0,:],refcbox[1,:],'k')
	ax1.autoscale_view('tight')
	
	#Plot moving image in the lower right
	ax2 = myfig.add_subplot(224)
	myim2 = im(movtopo)
	movcbox = drawrec(movtopo.shape[0],[0,0])
	myplot2, = ax2.plot(movcbox[0,:],movcbox[1,:],'k')
	ax2.autoscale_view('tight')
	
	#Plot cropped refence image in the upper left
	ax3 = myfig.add_subplot(221)
	myim3 = im(reftopo[refcbox[0,0]:refcbox[0,2],refcbox[1,0]:refcbox[1,2]])
	ax3.autoscale_view('tight')
	
	#Plot cropped moving image in the upper right
	ax4 = myfig.add_subplot(222)
	myim4 = im(movtopo[movcbox[0,0]:movcbox[0,2],movcbox[1,0]:movcbox[1,2]])
	ax4.autoscale_view('tight')
	
	plt.tight_layout(pad=.2)
		
	ax = [ax1, ax2, ax3, ax4]
	myim = [myim1, myim2, myim3, myim4]
	myplot = [myplot1, myplot2]
	cbox = [refcbox,movcbox]

	cid = myfig.canvas.mpl_connect('button_press_event', lambda event: onclick(event,reftopo,movtopo,myfig,ax,myim,myplot,refpoints,movpoints,refpointlist,movpointlist,cbox))
	
	return (refpointlist,movpointlist,reftopo.shape[0])
