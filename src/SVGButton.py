#!/usr/bin/env python
#
#  Copyright (C) 2007 Anthony Arobone <aarobone@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.
#
#  Author: Anthony Arobone <aarobone@gmail.com>
#
#  Notes: Closure SVGButton widget
#

import gobject
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gdk
import cairo
import rsvg
import os
import math
import pango
import pangocairo

#
# Class to handle doing SVG Image Buttons
#
class SVGButton(gtk.EventBox):
	"SVGButton Widget"

	width = 48
	height = 48
	text_width = 0
	text_height = 0
	text_offset = 2
	
	def __init__( self, scale=1, text=None, bin=None ):
		gtk.EventBox.__init__(self)


		# instance variables
		self.text_layout = None
		self.bin = None
		if bin:
			self.bin = bin.split( " " )
			
		self.set_size( 48, 48 )
		self.scale = scale
		self.scale_background = self.scale + 1 # normal scale
		if text != None and len(text) > 0:
			self.scale_background = self.scale + 1.5 # make background big enough to fit text
			self.text_layout = self.create_pango_layout( text )
			self.text_layout.set_font_description( pango.FontDescription( "Sans 16" ) )
			self.text_width, self.text_height = self.text_layout.get_pixel_size()
			self.set_size( self.text_width, self.text_height )

		self.inside = False
		self.svg_background = None
		self.svg_foreground = None
		self.svg_focus = None
		self.pressed = False


		# tell widget we want to draw it ourself
		self.set_app_paintable( True )
		self.set_visible_window( False )

		# turn on these events
		self.add_events( gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | \
						gtk.gdk.ENTER_NOTIFY_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | \
						gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK | \
						gtk.gdk.FOCUS_CHANGE_MASK )

		# enable focus 
		self.set_flags( gtk.CAN_FOCUS )
		
		# register callbacks for events
		self.connect( "screen-changed", self.screen_changed )
		self.connect( "configure-event", self.do_configure )
		self.connect( "expose-event", self.do_expose )
		self.connect( "button-press-event", self.press )
		self.connect( "button-release-event", self.release )
		self.connect( "enter-notify-event", self.do_enter )
		self.connect( "leave-notify-event", self.do_leave )
		


	def screen_changed( self, widget, old_screen=None ):
#		print "SVGButton screen changed"
		screen = widget.get_screen()
		colormap = screen.get_rgba_colormap()
		widget.set_colormap( colormap )

		if self.text_layout:
			self.text_layout.context_changed()

		return False


	#
	# Callback to manage widget changes, like resize
	#
	def do_configure( self, widget, event ):
		print "SVGButton configure"
		pass


	#
	# Callback to draw this widget
	#
	def do_expose( self, widget, event ):
		#print "SVGButton expose"

		rect = self.get_allocation()
		x = rect.x
		y = rect.y
		w = rect.width
		h = rect.height
#		print w, "x", h
		(w, h) = self.get_size()

		# get cairo context
		cr = self.window.cairo_create()
		
		# Debugging lines
#		cr.set_source_rgba( 1, 0, 0, 1 )
#		sw = self.get_screen().get_width()
#		sh = self.get_screen().get_height()
#		cr.move_to( sw/2, 0 )
#		cr.line_to( sw/2, sh/2 )
#		cr.line_to( sw, sh/2 )
#		cr.line_to( 0, sh/2 )
#		cr.stroke()
		
		# set clip region
#		print "expose area = ", event.area.x, ",", event.area.y, ",", event.area.width, ",", event.area.height
		cr.rectangle( event.area.x, event.area.y, event.area.width, event.area.height )
		cr.clip()
	
		# draw widget over the source
		cr.set_operator( cairo.OPERATOR_OVER )
		
		# calculate the base translation for this widget within it's parent drawing area
		if rect.height > rect.width:
			# if the physical height is bigger then the width (not square)
			# then offset all the drawing in the middle vertically
			diff = rect.width - rect.height
			diff = diff / 2
			cr.translate( x, y+diff )
		else:
			cr.translate( x, y )
		base_mat = cr.get_matrix()

#		print "button = ", w, "x", h, " scaled by ", self.scale

		# render background
		if self.inside and self.svg_background:
			cr.scale( self.scale_background, self.scale_background )
			self.svg_background.render_cairo( cr )
			cr.set_matrix( base_mat )
	
		# render foreground
		if self.svg_foreground:
			iw = self.svg_foreground.props.width * self.scale
			ih = self.svg_foreground.props.height * self.scale
			# center foreground
			cr.translate( (w-iw)/2, (h-ih)/2 )
			if self.text_layout:
				cr.translate( 0, self.text_height/-2 )
			cr.scale( self.scale, self.scale )
			self.svg_foreground.render_cairo( cr )
			cr.set_matrix( base_mat )

		# render focus layer
		if self.inside and self.svg_focus:
			iw = self.svg_focus.props.width * self.scale
			ih = self.svg_focus.props.height * self.scale
			# center focus
			cr.translate( (w-iw)/2, (h-ih)/2 )
			if self.text_layout:
				cr.translate( 0, self.text_height/-2 )
			cr.scale( self.scale, self.scale )
			self.svg_focus.render_cairo( cr )
			cr.set_matrix( base_mat )

		# render text
		if self.text_layout:
			# calc where the text should go
			fw, fh = self.text_layout.get_pixel_size()
			if self.svg_foreground:
				ih = self.svg_foreground.props.height * self.scale
				cr.translate( (w-fw)/2, (h-ih)/2 + ih)
			else:
				cr.translate( (w-fw)/2, h/2 )
			cr.translate( 0, self.text_height / -2 + self.text_offset )
			text_mat = cr.get_matrix()
			
			if True or self.inside:
				# black shadow
				cr.translate( 1, 2 ) # bottom right
				cr.set_source_rgba( 0.1, 0.1, 0.1, 1.0 )
				cr.update_layout( self.text_layout )
				cr.show_layout( self.text_layout )
				cr.set_source_rgba( 0.6, 0.6, 0.6, 1.0 )
				cr.translate( -2, -1 ) # bottom left
				cr.show_layout( self.text_layout )
				cr.translate( 0, -1 ) # left
				cr.show_layout( self.text_layout )
				cr.translate( 2, 0 ) # right
				cr.show_layout( self.text_layout )
				cr.translate( -1, -1 ) # top
				cr.show_layout( self.text_layout )

			# white 
			cr.set_matrix( text_mat )
			cr.set_source_rgba( 1.0, 1.0, 1.0, 1.0 )
			cr.update_layout( self.text_layout )
			cr.show_layout( self.text_layout )

		# don't let anyone else draw this widget after this method ends
		return True


	def do_enter( self, widget, event ):
#		print "SVGButton enter", event.mode
		if event.mode == gtk.gdk.CROSSING_NORMAL:
			self.inside = True
			rect = self.get_allocation()
			self.window.invalidate_rect( rect, False )
			self.window.process_updates( False )
		return True
		
		
	def do_leave( self, widget, event ):
#		print "SVGButton leave", event.mode
		if event.mode == gtk.gdk.CROSSING_NORMAL:
			self.inside = False
			rect = self.get_allocation()
			self.window.invalidate_rect( rect, False )
			self.window.process_updates( False )
		return True
		
	
	def press(self, widget, event ):
#		print "SVGButton press "
		if event.button == 1:
			self.pressed = True

#			rect = self.get_allocation()
#			self.window.invalidate_rect( rect, False )
#			self.window.process_updates( False )
		return True


	def release(self, widget, event ):
		retval = True
		if event.button == 1:
			if self.inside:
				# do button action here
#				print "SVGButton release"
				
				if self.bin:
					# if the binary is empty string, just exit the program
					if self.bin[0] == "":
						gtk.main_quit()
						return retval
					
					# replace current process [Clean up needed? Got me]
					print self.bin, len(self.bin)
					if len(self.bin) > 1:
						os.execvp( self.bin[0], self.bin )
					else:
						os.execlp( self.bin[0], self.bin[0] )
					
					# stop closure, and start process
#					gtk.main_quit()
#					print os.spawnlp(os.P_NOWAIT, self.bin, " " )
				
					retval = False

		self.pressed = False

#		rect = self.get_allocation()
#		self.window.invalidate_rect( rect, False )
#		self.window.process_updates( False )
		return retval


	def set_background_svg( self, svg ):
		self.svg_background = svg
		
		# on set background, resize the widget
		self.set_size( svg.props.width * self.scale_background, svg.props.height * self.scale_background)


	def set_foreground_svg( self, svg ):
		self.svg_foreground = svg

		# on set foreground, resize the widget
		# don't forget to add on the height of the text
		self.set_size( svg.props.width * self.scale, svg.props.height * self.scale + self.text_height )
			
	
	def set_focus_svg( self, svg ):
		self.svg_focus = svg

		# on set focus, resize the widget
		# don't forget to add on the height of the text
		self.set_size( svg.props.width * self.scale, svg.props.height * self.scale + self.text_height )
		

	#
	# Sets the size of this button
	# Only grows, never shrinks
	#
	def set_size( self, w, h ):
		# account for floats
		self.width = max( self.width, int(math.ceil( w )) )
		self.height = max( self.height, int( math.ceil( h )) )
		self.set_size_request( self.width, self.height )

	#
	# Gets the size of this button
	#
	def get_size( self ):
		return ( self.width, self.height )
