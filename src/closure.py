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
#  Notes: Closure app
#


import gobject
import pygtk
pygtk.require('2.0')
import gtk
import cairo
import rsvg
import gconf
import os
import SVGButton
import common
import closure_preferences


class Closure:
	"Closure"
	
	width = 640
	height = 480
	# fullscreen mode
	#	NOTE: fullscreen mode causes slowness with mouse presses, not sure why.
	do_fullscreen = False
	background_style = None
	background_solid = None
	background_linear_1 = None
	background_linear_2 = None
	background_linear_3 = None
	background_svg = None
	background_svg_scale = 1
	button_background = None
	lock_svg = None
	logout_svg = None
	reboot_svg = None
	shutdown_svg = None
	cancel_svg = None
	cancel_focus_svg = None


	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title( "Closure" )
		try:
			self.window.set_icon_from_file( os.path.join( common.DATA_DIR, "closure.svg") )
		except:
			print "Icon closure.svg not found."

		self.width = self.window.get_screen().get_width()
		self.height = self.window.get_screen().get_height()
		self.window.set_position( gtk.WIN_POS_CENTER )
		self.window.set_default_size( self.width, self.height ) 
		self.window.set_geometry_hints( None, self.width, self.height )

		self.client = gconf.client_get_default()
		self.client.add_dir( common.GENERAL_PATH, gconf.CLIENT_PRELOAD_NONE )
		self.client.add_dir( common.BACKGROUND_PATH, gconf.CLIENT_PRELOAD_NONE )
		self.client.add_dir( common.BUTTONS_PATH, gconf.CLIENT_PRELOAD_NONE )
		self.client.add_dir( common.COMMANDS_PATH, gconf.CLIENT_PRELOAD_NONE )

	
		# set fullscreen mode
		self.do_fullscreen = self.client.get_bool( common.GENERAL_FULLSCREEN )
		if self.do_fullscreen:
			self.window.fullscreen()

		# register callbacks
		self.window.connect( "expose-event", self.expose )
		self.window.connect( "screen-changed", self.screen_changed )
		self.window.connect( "key-press-event", self.keypressed)
		self.window.connect( "destroy", self.destroy)
		
	
		# set alpha
		self.window.set_app_paintable( True )
		self.screen_changed( self.window )
		
		self.window.set_resizable( False )
		self.window.set_keep_above( True )
		#self.window.set_urgency_hint( True )
		self.window.set_decorated( False )
		self.window.set_gravity( gtk.gdk.GRAVITY_CENTER )
	
		# load background properties
		self.background_style = common.loadString( self.client, common.BACKGROUND_STYLE, "linear" )
		self.background_solid = common.loadColor( self.client, common.BACKGROUND_SOLID, "000000AA" )
		self.background_linear_1 = common.loadColor( self.client, common.BACKGROUND_LINEAR_STEP_1, "000000E6" )
		self.background_linear_2 = common.loadColor( self.client, common.BACKGROUND_LINEAR_STEP_2, "000000BF" )
		self.background_linear_3 = common.loadColor( self.client, common.BACKGROUND_LINEAR_STEP_3, "00000080" )

		# load SVG images
		self.loadSVGImages()
	

		# Read button properties
		button_scale = common.loadFloat( self.client, common.BUTTONS_SCALE, 1 )
		show_lock = common.loadBool(  self.client, common.BUTTONS_LOCK_ENABLED, True )
		lock_label = common.loadString(  self.client, common.BUTTONS_LOCK_LABEL, "Lock" )
		lock_cmd = common.loadString(  self.client, common.COMMANDS_LOCK, None )
		
		show_logout = common.loadBool(  self.client, common.BUTTONS_LOGOUT_ENABLED, False )
		logout_label = common.loadString(  self.client, common.BUTTONS_LOGOUT_LABEL, "Logout" )
		logout_cmd = common.loadString(  self.client, common.COMMANDS_LOGOUT, None )

		show_reboot = common.loadBool(  self.client, common.BUTTONS_REBOOT_ENABLED, True )
		reboot_label = common.loadString(  self.client, common.BUTTONS_REBOOT_LABEL, "Reboot" )
		reboot_cmd = common.loadString(  self.client, common.COMMANDS_REBOOT, None )

		show_shutdown = common.loadBool(  self.client, common.BUTTONS_SHUTDOWN_ENABLED, True )
		shutdown_label = common.loadString(  self.client, common.BUTTONS_SHUTDOWN_LABEL, "Shutdown" )
		shutdown_cmd = common.loadString(  self.client, common.COMMANDS_SHUTDOWN, None )

		show_cancel = common.loadBool(  self.client, common.BUTTONS_CANCEL_ENABLED, True )
		cancel_label = common.loadString(  self.client, common.BUTTONS_CANCEL_LABEL, None )
	
		# create SVG Buttons
		if show_lock:
			if self.lock_svg:
				self.button_svg_lock = SVGButton.SVGButton( button_scale, lock_label, lock_cmd )
				self.button_svg_lock.set_foreground_svg( self.lock_svg )
				self.button_svg_lock.set_background_svg( self.button_background )
				self.button_svg_lock.set_flags( gtk.CAN_DEFAULT )
			else:
				print "Disabled Lock button"

		if show_logout:
			if self.logout_svg:
				self.button_svg_logout = SVGButton.SVGButton( button_scale, logout_label, logout_cmd )
				self.button_svg_logout.set_foreground_svg( self.logout_svg )
				self.button_svg_logout.set_background_svg( self.button_background )
			else:
				print "Disabled Logout button"


		if show_reboot:
			if self.reboot_svg:
				self.button_svg_reboot = SVGButton.SVGButton( button_scale, reboot_label, reboot_cmd )
				self.button_svg_reboot.set_foreground_svg( self.reboot_svg )
				self.button_svg_reboot.set_background_svg( self.button_background )
			else:
				print "Disabled Reboot button"


		if show_shutdown:
			if self.shutdown_svg:
				self.button_svg_halt = SVGButton.SVGButton( button_scale, shutdown_label, shutdown_cmd )
				self.button_svg_halt.set_foreground_svg( self.shutdown_svg )
				self.button_svg_halt.set_background_svg( self.button_background )
			else:
				print "Disabled Shutdown button"


		if show_cancel:
			if self.cancel_svg:
				self.button_cancel = SVGButton.SVGButton( 1, cancel_label, " " )
				self.button_cancel.set_foreground_svg( self.cancel_svg )
				self.button_cancel.set_focus_svg( self.cancel_focus_svg )
			else:
				print "Disabled Cancel button"



		# add buttons to HBox
		self.box = gtk.HButtonBox()
		self.box.set_layout( gtk.BUTTONBOX_SPREAD )
		self.box.set_spacing( 0 )
		expand = False
		fill = False
		if show_lock and self.button_svg_lock:
			self.box.pack_start(self.button_svg_lock, expand, fill, 0)
		if show_logout and self.button_svg_logout:
			self.box.pack_start(self.button_svg_logout, expand, fill, 0)
		if show_reboot and self.button_svg_reboot:
			self.box.pack_start(self.button_svg_reboot, expand, fill, 0)
		if show_shutdown and self.button_svg_halt:
			self.box.pack_start(self.button_svg_halt, expand, fill, 0)


		# add HBox to alignment and to main window
		self.align = gtk.Alignment( 0.5, 0.5, 0.3, 0 )
		self.align.add( self.box )
		
		con = gtk.Table( 2 )
		con.attach( self.align, 1, 2, 1, 2, gtk.EXPAND | gtk.FILL, gtk.EXPAND )
		if show_cancel and self.button_cancel:
			con.attach( self.button_cancel, 1, 2, 2, 3, gtk.SHRINK, gtk.SHRINK )
		self.window.add( con )

	
		self.window.show_all()



	#
	# Loads all SVGs closure might need
	#
	def loadSVGImages(self):
		svg = self.client.get_string( common.BACKGROUND_SVG_IMAGE )
		if svg:
			try:
				self.background_svg = rsvg.Handle( svg )
				
				# for now we'll uniformly scale the bg image to fit the screen
				# TODO: make this a closure-preferences setting, uniform and non-uniform
				dw = abs(self.width - self.background_svg.props.width)
				dh = abs(self.height - self.background_svg.props.height)
				if dw > dh:
					# the width is smaller then the height
					self.background_svg_scale = self.width / float(self.background_svg.props.width)
				else:
					# the height is smaller then the width
					self.background_svg_scale = self.height / float(self.background_svg.props.height)
			except:
				print "SVG file not found:", svg

		svg = self.client.get_string( common.BUTTONS_BG_SVG )
		if svg:
			try:
				self.button_background = rsvg.Handle( svg )
			except:
				print "SVG file not found:", svg
		
		svg = self.client.get_string( common.BUTTONS_LOCK_SVG )
		if svg:
			try:
				self.lock_svg = rsvg.Handle( svg )
			except:
				print "SVG file not found:", svg

		svg = self.client.get_string( common.BUTTONS_LOGOUT_SVG )
		if svg:
			try:
				self.logout_svg = rsvg.Handle( svg )
			except:
				print "SVG file not found:", svg

		svg = self.client.get_string( common.BUTTONS_REBOOT_SVG )
		if svg:
			try:
				self.reboot_svg = rsvg.Handle( svg )
			except:
				print "SVG file not found:", svg

		svg = self.client.get_string( common.BUTTONS_SHUTDOWN_SVG )
		if svg:
			try:
				self.shutdown_svg = rsvg.Handle( svg )
			except:
				print "SVG file not found:", svg
		
		svg = self.client.get_string( common.BUTTONS_CANCEL_SVG )
		if svg:
			try:
				self.cancel_svg = rsvg.Handle( svg )
			except:
				print "SVG file not found:", svg
			svg = svg.replace(".svg", "-focus.svg")
			try:
				self.cancel_focus_svg = rsvg.Handle( svg )
			except:
				print "SVG file not found:", svg
	

	def expose( self, widget, event):
		cr = widget.window.cairo_create()

		# set clip region
		#print "expose area = ", event.area.x, ",", event.area.y, ",", event.area.width, ",", event.area.height
		cr.rectangle( event.area.x, event.area.y, event.area.width, event.area.height )
		cr.clip()

		(w, h) = widget.window.get_size()
		cr.set_operator( cairo.OPERATOR_SOURCE )

		# radial gradient attempt, not so hot
#		pat = cairo.RadialGradient( w/2, h/2, 10, w/2, h/2, w )
#		pat.add_color_stop_rgba( 0.0, 1.0, 0.0, 0.0, 0.8 )
#		pat.add_color_stop_rgba( 1.0, 1.0, 1.0, 1.0, 0.3 )
#		cr.set_source( pat )
#		cr.paint()
#
#		cr.set_operator( cairo.OPERATOR_OVER )
#		return False

		# SVG image background, better make something worthwhile
		if self.background_style == "svg":
			if self.background_svg:
				if self.background_svg_scale != 1:
					cr.scale( self.background_svg_scale, self.background_svg_scale )
				self.background_svg.render_cairo( cr )
			else:
				# if svg does not exist fall back to solid bg
				self.background_style = "solid"

		# solid black, decent
		if self.background_style == "solid":
#			cr.set_source_rgba( 0.1, 0.1, 0.1, 0.5 )
			cr.set_source_rgba( self.background_solid[0], self.background_solid[1], self.background_solid[2], self.background_solid[3] )
			cr.paint()

		# diagonal linear gradient, ok
		if self.background_style == "linear":
			pat = cairo.LinearGradient( 0.0, 0.0, w/1.5, h )
#			pat.add_color_stop_rgba( 0.1, 0.0, 0.0, 0.0, 0.9 )
#			pat.add_color_stop_rgba( 0.6, 0.0, 0.0, 0.0, 0.75 )
#			pat.add_color_stop_rgba( 1.0, 0.0, 0.0, 0.0, 0.5 )
			pat.add_color_stop_rgba( 0.1, self.background_linear_1[0], self.background_linear_1[1], self.background_linear_1[2], self.background_linear_1[3] )
			pat.add_color_stop_rgba( 0.6, self.background_linear_2[0], self.background_linear_2[1], self.background_linear_2[2], self.background_linear_2[3] )
			pat.add_color_stop_rgba( 1.0, self.background_linear_3[0], self.background_linear_3[1], self.background_linear_3[2], self.background_linear_3[3] )
			cr.set_source( pat )
			cr.paint()
		
		# radial gradient attempt, not so hot
#		pat = cairo.RadialGradient( 200, 200, 10, 200, 200, w )
#		pat.add_color_stop_rgba( 0.0, 0.0, 0.0, 0.0, 0.8 )
#		pat.add_color_stop_rgba( 1.0, 0.0, 0.0, 0.0, 0.3 )
#		cr.set_source( pat )
#		cr.paint()

		return False

	def screen_changed( self, widget, old_screen=None):
		screen = widget.get_screen()
		colormap = screen.get_rgba_colormap()
		widget.set_colormap( colormap )
		return False


	def keypressed(self, widget, event, data=None):
		if event.keyval == 96: #tilda
			self.window.destroy()
			app = closure_preferences.preferences()
			gtk.main()
		if event.keyval == 65307: #ESC
			gtk.main_quit()


	def destroy(self, widget, data=None):
		gtk.main_quit()


	def main(self):
		gtk.main()


if __name__ == "__main__":
	closure = Closure()
	closure.main()
