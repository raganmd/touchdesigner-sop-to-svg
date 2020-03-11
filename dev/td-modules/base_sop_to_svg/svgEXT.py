'''SVG Write in TouchDesigner Class
Authors | matthew ragan, updated by Mickey van Olst
matthewragan.com
mickeyvanolst.com
'''

import svgwrite
import numpy as np
import math
import webbrowser
import re

class Soptosvg:
	'''
	This class is inteded to handle writing SVGs from SOPs in TouchDesigner.
	
	This is a largely experimental approach so there are bound to be things
	that are wrong or don't work. 

	---------------
	
	'''

	def __init__( self ):
		''' This is the init method for the Soptosvg process
		'''
		self.Polylinesop 			= parent.svg.par.Polylinesop
		self.Polygonsop				= parent.svg.par.Polygonsop

		# mickey addded
		self.UseGeo					= parent.svg.par.Usegeo
		self.Geocomp				= parent.svg.par.Geocomp

		self.Svgtype 				= parent.svg.par.Svgtype
		self.Filepath 				= "{dir}/{file}.svg"
		self.UseCamera 				= parent.svg.par.Usecamera
		self.Camera 				= parent.svg.par.Camera
		self.Aspect 				= (parent.svg.par.Aspect1, parent.svg.par.Aspect2)

		self.Axidocumentation 		= "http://wiki.evilmadscientist.com/AxiDraw"
		self.Axipdf 				= "http://cdn.evilmadscientist.com/wiki/axidraw/software/AxiDraw_V33.pdf"
		self.Svgwritedocumentation 	= "http://svgwrite.readthedocs.io/en/latest/svgwrite.html"

		print( "Sop to SVG Initialized" )
		return


	def WorldToCam(self, oldP):
		'''Method to convert worldspace coords to cameraspace coords.

		Args
		-------------
		oldP (tdu.Position) : the tdu.Position to convert to camera space.

		Returns
		-------------
		newP (tuple) : tuple of x,y coordinates after camera projection. 

		'''
		camera 		= op(self.Camera.eval())
		view 		= camera.transform()
		view.invert()
		pers 		= camera.projection( self.Aspect[0].eval(), self.Aspect[1].eval() )
		viewP 		= view * oldP
		adjusted 	= pers * viewP 
		newX 		= adjusted.x/adjusted.z
		newY 		= adjusted.y/adjusted.z
		newP 		= (newX, newY)

		return newP

	def Canvas_size(self):
		''' This is a helper method to return the dimensions of the canvas.

		Having an output size for the SVG isn't necessary, but for working with the axi-draw
		it's often helpful to have your file set-up and ready to plot from if possible.
		This method grabs the par of the svgWrite tox and returns those dimensions to other methods.
						
		Notes
		---------------

		Args
		---------------
		none

		Returns
		---------------
		canvassize (tupple) : a tupple of width and height dimensions measured in millimeters
		'''
		canvassize 					= None

		if parent.svg.par.Canvassize == 'letter':
			canvassize 				= ('279.4mm','279.4mm')
		elif parent.svg.par.Canvassize == 'A4':
			canvassize 				= ('210mm','297mm')

		return canvassize

	def SavePolyline(self, path, pline):
		''' This is a sample method.

		This sample method is intended to help illustrate what method docstrings should look like.
						
		Notes
		---------------
		'self' does not need to be included in the Args section.

		Args
		---------------
		name (str): A string name, with spaces as underscores
		age (int): Age as full year measurements
		height (float): Height in meters to 2 significant digits, ex: 1.45

		Examples
		---------------

		Returns
		---------------
		formatted_profile (str) : A formatted string populated with the with the supplied information
		'''
		Canvassize 		= self.Canvas_size()

		prims 			= pline.prims
		dwg 			= svgwrite.Drawing(path, profile='tiny', size=Canvassize)

		# ok in order to make this work we first see if instancing is turned on with the parent geo otherwise we don't need to iterate
		myGeo = op(self.Geocomp)
		if myGeo.par.instancing == True:
			# ok so instancing, we'll need to grab a few things here to make sure we can do what is needed
			numInstances = 0
			if myGeo.par.instancecountmode == 0: # manual
				numInstances = myGeo.par.numinstances
			else:
				if myGeo.par.instanceop:
					numInstances = op(myGeo.par.instanceop).numSamples
				elif myGeo.par.instancetop:
					numInstances = op(myGeo.par.instancetop).numSamples
				elif myGeo.par.instancerop:
					numInstances = op(myGeo.par.instancerop).numSamples
				elif myGeo.par.instancesop:
					numInstances = op(myGeo.par.instancesop).numSamples
				elif myGeo.par.instancepop:
					numInstances = op(myGeo.par.instancepop).numSamples
				else:
					print("no instance OPs found!")
			
			for i in range(numInstances):
				itop = op(myGeo.par.instancetop)
				if itop:
					try:
						tx = itop[str(myGeo.par.instancetx)][i] # needs to be string otherwise it just gives us a value we don't want
					except:
						tx = 0
					try:
						ty = itop[str(myGeo.par.instancety)][i]
					except:
						ty = 0
					try:
						tz = itop[str(myGeo.par.instancetz)][i]
					except:
						tz = 0
				
				irop = op(myGeo.par.instancerop)
				if irop:
					try:
						rx = irop[str(myGeo.par.instancerx)][i]
					except:
						rx = 0
					try:
						ry = irop[str(myGeo.par.instancery)][i]
					except:
						ry = 0
					try:
						rz = irop[str(myGeo.par.instancerz)][i]
					except:
						rz = 0

				isop = op(myGeo.par.instancesop)
				if isop:
					try:
						sx = isop[myGeo.par.instancesx][i]
					except:
						sx = 1
					try:
						sy = isop[myGeo.par.instancesy][i]
					except:
						sy = 1
					try:
						sz = isop[myGeo.par.instancesz][i]
					except:
						sz = 1

				for item in prims:
					newPoints = []

					if self.UseCamera:
						#newPoints 	= [self.WorldToCam(vert.point.P) for vert in item ]
						for vert in item:
							p = vert.point.P
							
							qrx = tdu.Quaternion(rx, tdu.Vector(1, 0, 0))
							qry = tdu.Quaternion(ry, tdu.Vector(0, 1, 0))
							qrz = tdu.Quaternion(rz, tdu.Vector(0, 0, 1))
							
							p = qrx.rotate(p)
							p = qry.rotate(p)
							p = qrz.rotate(p)
							
							p.scale(sx,sy,sz)

							# move each instance to its position
							p = tdu.Position(p)
							p.translate(tx,ty,tz)

							p = self.WorldToCam(p)
							p = (p[0], -p[1]) # somehow our Y axis is inverted
							if(math.isnan(p[0]) == False):
								newPoints.append(p)
					else:
						#newPoints 	= [(vert.point.x,vert.point.y) for vert in item ]
						for vert in item:
							p = self.rotate_origin_only( (vert.point.x * sx, vert.point.y * sy), -math.radians(rx) )
							p = (p[0] + tx, (p[1] + ty)*-1)

							if(math.isnan(p[0]) == False):
								newPoints.append(p)

					
					newPoly		= dwg.polyline(points=newPoints, stroke='black', stroke_width=1, fill='none')
					dwg.add(newPoly)
		
		else:

			for item in prims:
				
				if self.UseCamera:
					newPoints 	= [self.WorldToCam(vert.point.P) for vert in item ]
				else:
					newPoints 	= [(vert.point.x,vert.point.y) for vert in item ]
				
				newPoly		= dwg.polyline(points=newPoints, stroke='black', stroke_width=1, fill='none')
				dwg.add(newPoly)

		dwg.save()

		return

	def SavePolygon(self, path, pgon):
		''' This is a sample method.

		This sample method is intended to help illustrate what method docstrings should look like.
						
		Notes
		---------------
		'self' does not need to be included in the Args section.

		Args
		---------------
		name (str): A string name, with spaces as underscores
		age (int): Age as full year measurements
		height (float): Height in meters to 2 significant digits, ex: 1.45

		Examples
		---------------

		Returns
		---------------
		formatted_profile (str) : A formatted string populated with the with the supplied information
		'''
		Canvassize 		= self.Canvas_size()
	
		prims 			= pgon.prims
		dwg 			= svgwrite.Drawing(path, profile='tiny', size=Canvassize)

		# ok in order to make this work we first see if instancing is turned on with the parent geo otherwise we don't need to iterate
		myGeo = op(self.Geocomp)
		if myGeo.par.instancing == True:
			# ok so instancing, we'll need to grab a few things here to make sure we can do what is needed
			numInstances = 0
			if myGeo.par.instancecountmode == 0: # manual
				numInstances = myGeo.par.numinstances
			else:
				if myGeo.par.instanceop:
					numInstances = op(myGeo.par.instanceop).numSamples
				elif myGeo.par.instancetop:
					numInstances = op(myGeo.par.instancetop).numSamples
				elif myGeo.par.instancerop:
					numInstances = op(myGeo.par.instancerop).numSamples
				elif myGeo.par.instancesop:
					numInstances = op(myGeo.par.instancesop).numSamples
				elif myGeo.par.instancepop:
					numInstances = op(myGeo.par.instancepop).numSamples
				else:
					print("no instance OPs found!")
			
			for i in range(numInstances):
				itop = op(myGeo.par.instancetop)
				if itop:
					try:
						tx = itop[str(myGeo.par.instancetx)][i] # needs to be string otherwise it just gives us a value we don't want
					except:
						tx = 0
					try:
						ty = itop[str(myGeo.par.instancety)][i]
					except:
						ty = 0
					try:
						tz = itop[str(myGeo.par.instancetz)][i]
					except:
						tz = 0
				
				irop = op(myGeo.par.instancerop)
				if irop:
					try:
						rx = irop[str(myGeo.par.instancerx)][i]
					except:
						rx = 0
					try:
						ry = irop[str(myGeo.par.instancery)][i]
					except:
						ry = 0
					try:
						rz = irop[str(myGeo.par.instancerz)][i]
					except:
						rz = 0

				isop = op(myGeo.par.instancesop)
				if isop:
					try:
						sx = isop[myGeo.par.instancesx][i]
					except:
						sx = 1
					try:
						sy = isop[myGeo.par.instancesy][i]
					except:
						sy = 1
					try:
						sz = isop[myGeo.par.instancesz][i]
					except:
						sz = 1

				
				for item in prims:
					newPoints = []
					if self.UseCamera:
						#newPoints 	= [self.WorldToCam(vert.point.P) for vert in item ]
						for vert in item:
							p = vert.point.P
							
							qrx = tdu.Quaternion(rx, tdu.Vector(1, 0, 0))
							qry = tdu.Quaternion(ry, tdu.Vector(0, 1, 0))
							qrz = tdu.Quaternion(rz, tdu.Vector(0, 0, 1))
							
							p = qrx.rotate(p)
							p = qry.rotate(p)
							p = qrz.rotate(p)
							
							p.scale(sx,sy,sz)

							# move each instance to its position
							p = tdu.Position(p)
							p.translate(tx,ty,tz)

							p = self.WorldToCam(p)
							p = (p[0], -p[1]) # somehow our Y axis is inverted
							if(math.isnan(p[0]) == False):
								newPoints.append(p)
					else:
						for vert in item:
							#newPoints 	= [(vert.point.x,vert.point.y) for vert in item ]
							#p = (vert.point.x + tx, vert.point.y + ty)
							p = self.rotate_origin_only( (vert.point.x * sx, vert.point.y * sy), -math.radians(rx) )
							p = (p[0] + tx, (p[1] + ty)*-1)


							if(math.isnan(p[0]) == False):
								newPoints.append(p)

					newPoly		= dwg.polygon(points=newPoints, stroke='black', stroke_width=1, fill='none')
					dwg.add(newPoly)

		else:

			for item in prims:
				
				if self.UseCamera:
					newPoints 	= [self.WorldToCam(vert.point.P) for vert in item ]
				else:
					newPoints 	= [(vert.point.x,vert.point.y) for vert in item ]

				newPoly		= dwg.polygon(points=newPoints, stroke='black', stroke_width=1, fill='none')
				dwg.add(newPoly)

		dwg.save()

	def SavePolygonAndPolygon(self, path, pline, pgon):
		''' This is a sample method.

		This sample method is intended to help illustrate what method docstrings should look like.
						
		Notes
		---------------
		'self' does not need to be included in the Args section.

		Args
		---------------
		name (str): A string name, with spaces as underscores
		age (int): Age as full year measurements
		height (float): Height in meters to 2 significant digits, ex: 1.45

		Examples
		---------------

		Returns
		---------------
		formatted_profile (str) : A formatted string populated with the with the supplied information
		'''

		Canvassize 		= self.Canvas_size()
	
		dwg 			= svgwrite.Drawing(path, profile='tiny', size=Canvassize)
		

		# ok in order to make this work we first see if instancing is turned on with the parent geo otherwise we don't need to iterate
		myGeo = op(self.Geocomp)
		if myGeo.par.instancing == True:
			# ok so instancing, we'll need to grab a few things here to make sure we can do what is needed
			numInstances = 0
			if myGeo.par.instancecountmode == 0: # manual
				numInstances = myGeo.par.numinstances
			else:
				if myGeo.par.instanceop:
					numInstances = op(myGeo.par.instanceop).numSamples
				elif myGeo.par.instancetop:
					numInstances = op(myGeo.par.instancetop).numSamples
				elif myGeo.par.instancerop:
					numInstances = op(myGeo.par.instancerop).numSamples
				elif myGeo.par.instancesop:
					numInstances = op(myGeo.par.instancesop).numSamples
				elif myGeo.par.instancepop:
					numInstances = op(myGeo.par.instancepop).numSamples
				else:
					print("no instance OPs found!")
			
			for i in range(numInstances):
				itop = op(myGeo.par.instancetop)
				if itop:
					try:
						tx = itop[str(myGeo.par.instancetx)][i] # needs to be string otherwise it just gives us a value we don't want
					except:
						tx = 0
					try:
						ty = itop[str(myGeo.par.instancety)][i]
					except:
						ty = 0
					try:
						tz = itop[str(myGeo.par.instancetz)][i]
					except:
						tz = 0
				
				irop = op(myGeo.par.instancerop)
				if irop:
					try:
						rx = irop[str(myGeo.par.instancerx)][i]
					except:
						rx = 0
					try:
						ry = irop[str(myGeo.par.instancery)][i]
					except:
						ry = 0
					try:
						rz = irop[str(myGeo.par.instancerz)][i]
					except:
						rz = 0

				isop = op(myGeo.par.instancesop)
				if isop:
					try:
						sx = isop[myGeo.par.instancesx][i]
					except:
						sx = 1
					try:
						sy = isop[myGeo.par.instancesy][i]
					except:
						sy = 1
					try:
						sz = isop[myGeo.par.instancesz][i]
					except:
						sz = 1

				pgonPrims 		= pgon.prims
				plinePrims 		= pline.prims

				for item in pgonPrims:
					newPoints = []
					if self.UseCamera:
						#newPoints 	= [self.WorldToCam(vert.point.P) for vert in item ]
						for vert in item:
							p = vert.point.P
							
							qrx = tdu.Quaternion(rx, tdu.Vector(1, 0, 0))
							qry = tdu.Quaternion(ry, tdu.Vector(0, 1, 0))
							qrz = tdu.Quaternion(rz, tdu.Vector(0, 0, 1))
							
							p = qrx.rotate(p)
							p = qry.rotate(p)
							p = qrz.rotate(p)
							
							p.scale(sx,sy,sz)

							# move each instance to its position
							p = tdu.Position(p)
							p.translate(tx,ty,tz)

							p = self.WorldToCam(p)
							p = (p[0], -p[1]) # somehow our Y axis is inverted
							if(math.isnan(p[0]) == False):
								newPoints.append(p)
					else:
						#newPoints 	= [(vert.point.x,vert.point.y) for vert in item ]
						for vert in item:
							#p = (vert.point.x + tx, vert.point.y + ty)
							p = self.rotate_origin_only( (vert.point.x * sx, vert.point.y * sy), -math.radians(rx) )
							p = (p[0] + tx, (p[1] + ty)*-1)

							if(math.isnan(p[0]) == False):
								newPoints.append(p)
					if newPoints:
						newPoly		= dwg.polygon(points=newPoints, stroke='black', stroke_width=1, fill='none')
					if newPoly:
						dwg.add(newPoly)
				
				for item in plinePrims:
					newPoints = []
					if self.UseCamera:
						#newPoints 	= [self.WorldToCam(vert.point.P) for vert in item ]
						for vert in item:
							p = vert.point.P
							
							qrx = tdu.Quaternion(rx, tdu.Vector(1, 0, 0))
							qry = tdu.Quaternion(ry, tdu.Vector(0, 1, 0))
							qrz = tdu.Quaternion(rz, tdu.Vector(0, 0, 1))
							
							p = qrx.rotate(p)
							p = qry.rotate(p)
							p = qrz.rotate(p)
							
							p.scale(sx,sy,sz)

							# move each instance to its position
							p = tdu.Position(p)
							p.translate(tx,ty,tz)

							p = self.WorldToCam(p)
							p = (p[0], -p[1]) # somehow our Y axis is inverted
							if(math.isnan(p[0]) == False):
								newPoints.append(p)
					else:
						#newPoints 	= [(vert.point.x,vert.point.y) for vert in item ]
						for vert in item:
							p = self.rotate_origin_only( (vert.point.x * sx, vert.point.y * sy), -math.radians(rx) )
							p = (p[0] + tx, (p[1] + ty)*-1)

							if(math.isnan(p[0]) == False):
								newPoints.append(p)
					if newPoints:
						newPoly		= dwg.polyline(points=newPoints, stroke='black', stroke_width=1, fill='none')
					if newPoly:
						dwg.add(newPoly)


		else:
			# we just grab whatever the geo has as an input
			pgonPrims 		= pgon.prims
			plinePrims 		= pline.prims
			
			for item in pgonPrims:
				newPoints = []
				if self.UseCamera:
					#newPoints 	= [self.WorldToCam(vert.point.P) for vert in item ]
					for vert in item:
						p = self.WorldToCam(vert.point.P)
						if(math.isnan(p[0]) == False):
							newPoints.append(p)
				else:
					#newPoints 	= [(vert.point.x,vert.point.y) for vert in item ]
					for vert in item:
						p = (vert.point.x, vert.point.y)
						if(math.isnan(p[0]) == False):
							newPoints.append(p)
				if newPoints:
					newPoly		= dwg.polygon(points=newPoints, stroke='black', stroke_width=1, fill='none')
				if newPoly:
					dwg.add(newPoly)
			
			for item in plinePrims:
				newPoints = []
				if self.UseCamera:
					#newPoints 	= [self.WorldToCam(vert.point.P) for vert in item ]
					for vert in item:
						p = self.WorldToCam(vert.point.P)
						if(math.isnan(p[0]) == False):
							newPoints.append(p)
				else:
					#newPoints 	= [(vert.point.x,vert.point.y) for vert in item ]
					for vert in item:
						p = (vert.point.x,vert.point.y)
						if(math.isnan(p[0]) == False):
							newPoints.append(p)
				if newPoints:
					newPoly		= dwg.polyline(points=newPoints, stroke='black', stroke_width=1, fill='none')
				if newPoly:
					dwg.add(newPoly)

		if dwg:
			dwg.save()

		return

	def rotate_origin_only(self, xy, radians):
		"""Only rotate a point around the origin (0, 0)."""
		x, y = xy
		xx = x * math.cos(radians) + y * math.sin(radians)
		yy = -x * math.sin(radians) + y * math.cos(radians)
		return xx, yy

	def Par_check(self, svg_type):
		''' Par_check() is an error handling method.

		Par_check aims to ensrue that all parameters are correctly set up so we can advance to the
		steps of creating our SVGs. This means checking to ensure that all needed fields are
		completed in the TOX. If we pass all of the par check tests then we can move on to 
		writing our SVG file to disk.
						
		Notes
		---------------
		'self' does not need to be included in the Args section.

		Args
		---------------
		svg_type (str): the string name for the inteded type of output - polygon, polyline, both

		Returns
		---------------
		ready (bool) : the results of a set of logical checks to that ensures all requisite 
						pars have been supplied for a sucessful write to disk for the file.
		'''		

		ready 				= False

		title 				= "We're off the RAILS!"
		message 			= '''Hey there, things don't look totally right.
Check on these parameters to make sure everything is in order:\n{}'''
		buttons 			= ['okay']
		checklist 			= []

		# error handling for geometry permutations
		# handling polyline saving
		if self.Svgtype 	== 'pline':
			if self.Polylinesop != None and op(self.Polylinesop).isSOP:
				pass
			else:
				checklist.append( 'Missing Polygon SOP' )

		# handling polygon saving
		elif self.Svgtype 	== 'pgon':
			if self.Polygonsop != None and op(self.Polygonsop).isSOP:
				pass
			else:
				checklist.append( 'Missing Polyline SOP' )

		# handling combined objects - polyline and polygon saving
		elif self.Svgtype 	== 'both':
			polyline 		= self.Polylinesop != None and op(self.Polylinesop).isSOP
			polygon 		= self.Polygonsop != None and op(self.Polygonsop).isSOP

			# both sops are present
			if polyline and polygon:
				pass
			# missing polyline sop
			elif polygon and not polyline:
				checklist.append( 'Missing Polyline SOP' )
			# missing polygon sop
			elif polyline and not polygon:
				checklist.append( 'Missing Polygon SOP' )
			# missing both polyline and polygon sops
			elif not polyline and not polygon:
				checklist.append( 'Missing Polygon SOP')
				checklist.append( 'Missing Polyline SOP')

		# handling to check for a directory path
		if parent.svg.par.Dir == None or parent.svg.par.Dir.val == '':
			checklist.append( 'Missing Directory Path' )
		
		else:
			pass

		# handling to check for a file path
		if parent.svg.par.Filename == None or parent.svg.par.Filename.val == '':
			checklist.append( 'Missing File name' )

		# Check for camera
		if parent.svg.par.Usecamera:
			if parent.svg.par.Camera == None or op(parent.svg.par.Camera).type != "cam":
				checklist.append( 'Missing Camera' )

		else:
			pass

		# mickey added handling to use Geocomp instancing
		if parent.svg.par.Usegeo:
			if parent.svg.par.Geocomp == None or op(parent.svg.par.Geocomp).type != "geo":
				checklist.append('Missing Geo COMP')
		else:
			pass

		# we're in the clear, everything is ready to go
		if len(checklist) 			== 0:
			ready 					= True
		# correctly format message for ui.messageBox and warn user about missing elements
		else:
			ready 					= False	
			messageChecklist 		= '\n'
			for item in checklist:
				messageChecklist 	+= '     * {}\n'.format(item)
			
			message 				= message.format(messageChecklist)
			ui.messageBox(title, message, buttons=buttons)
		return ready

	def Save(self):
		''' This is the Save method, used to start the process of writing the svg to disk.

		Based on settings in the tox's parameters the Save() method will utilize other
		helper methods to correctly save out the file. Pragmatically, this means first
		ensuring that all pars are correctly set up (error prevention), then the 
		appropriate calling of other methods to ensure that geometry is correclty 
		written to file.
						
		Notes
		---------------
		none

		Args
		---------------
		none

		Returns
		---------------
		none
		'''
		
		# get the svg type
		svgtype 				= self.Svgtype

		# start with Par_check to see if we're ready to proced.
		readyToContinue 		= self.Par_check( svgtype )

		if readyToContinue:
			filepath 			= self.Filepath.format( dir=parent.svg.par.Dir, 
														file=parent.svg.par.Filename)
			
			if svgtype == 'pline':
				if parent.svg.par.Usegeo:
					plinpath = str(self.Geocomp) + '/' + op(self.Polylinesop).name
					self.SavePolyline(	path=filepath, 
										pline=op(plinpath))
				else:
					self.SavePolyline(	path=filepath, 
										pline=op(self.Polylinesop))

			elif svgtype == 'pgon':
				if parent.svg.par.Usegeo:
					pgonpath = str(self.Geocomp) + '/'  + op(self.Polygonsop).name
					self.SavePolygon(	path=filepath,
										pgon=op(pgonpath))
				else:
					self.SavePolygon(	path=filepath,
										pgon=op(self.Polygonsop))

			elif svgtype == 'both':
				if parent.svg.par.Usegeo:
					plinpath = str(self.Geocomp) + '/' + op(self.Polylinesop).name
					pgonpath = str(self.Geocomp) + '/'  + op(self.Polygonsop).name
					self.SavePolygonAndPolygon( path=filepath,
												pline=op(plinpath), 
												pgon=op(pgonpath))
				else:
					self.SavePolygonAndPolygon( path=filepath,
												pline=op(self.Polylinesop), 
												pgon=op(self.Polygonsop))
			else:
				print("Woah... something is very wrong")
				pass

			print(filepath)
			print(self.Polylinesop)
			print(self.Svgtype)
		
		else:
			pass

		return
