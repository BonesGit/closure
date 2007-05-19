#!/usr/bin/env python
#
#  Copyright (C) 2007 Neil Jagdish Patel <njpatel@gmail.com>
#					  Anthony Arobone <aarobone@gmail.com>
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
#  Author: Neil Jagdish Patel <njpatel@gmail.com>
#  Contributor: Anthony Arobone <aarobone@gmail.com>
#
#  Notes: Closure preferences window
#         Taken from avant-window-navigator's preferences
#

import sys, os
try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
except:
	sys.exit(1)

import gconf
import common

APP = 'closure'
DIR = '/usr/share/locale'
I18N_DOMAIN = "closure"

import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext



class preferences:
	"""This is the main preferences class"""

	def __init__(self):
		
		self.client = gconf.client_get_default()
		self.client.add_dir( common.GENERAL_PATH, gconf.CLIENT_PRELOAD_NONE )
		self.client.add_dir( common.BACKGROUND_PATH, gconf.CLIENT_PRELOAD_NONE )
		self.client.add_dir( common.BUTTONS_PATH, gconf.CLIENT_PRELOAD_NONE )
		self.client.add_dir( common.COMMANDS_PATH, gconf.CLIENT_PRELOAD_NONE )
		
		#Set the Glade file
		gtk.glade.bindtextdomain(APP, DIR)
		gtk.glade.textdomain(APP)
		self.gladefile = os.path.join( common.DATA_DIR, "pref.glade" )
		#print self.gladefile
	    	self.wTree = gtk.glade.XML(self.gladefile, domain=I18N_DOMAIN)
	    	
		
		#Get the Main Window, and connect the "destroy" event
		self.window = self.wTree.get_widget("pref-window")
		self.window.connect( "delete-event", gtk.main_quit )
		self.window.connect( "key-press-event", self.keypressed )
		
		close = self.wTree.get_widget("close-button")
		close.connect("clicked", gtk.main_quit)
		
		# General Tab
		self.setup_bool( common.GENERAL_FULLSCREEN, self.wTree.get_widget("fullscreen-checkbutton") )
		self.setup_bool( common.GENERAL_COMPACT, self.wTree.get_widget("compact-checkbutton") )
		
		
		# Background Tab
		self.setup_radio( common.BACKGROUND_STYLE, self.wTree.get_widget("solid-radiobutton"), "solid" )
		self.setup_radio( common.BACKGROUND_STYLE, self.wTree.get_widget("linear-radiobutton"), "linear" )
		self.setup_radio( common.BACKGROUND_STYLE, self.wTree.get_widget("svg-bg-radiobutton"), "svg" )
		
		self.setup_color( common.BACKGROUND_SOLID, self.wTree.get_widget("solid-colorbutton"))
		self.setup_color( common.BACKGROUND_LINEAR_STEP_1, self.wTree.get_widget("linear-first-colorbutton"))
		self.setup_color( common.BACKGROUND_LINEAR_STEP_2, self.wTree.get_widget("linear-second-colorbutton"))
		self.setup_color( common.BACKGROUND_LINEAR_STEP_3, self.wTree.get_widget("linear-third-colorbutton"))
		self.setup_chooser( common.BACKGROUND_SVG_IMAGE, self.wTree.get_widget("svg-bg-filechooserbutton"))
		
		# Buttons Tab
		self.setup_chooser( common.BUTTONS_BG_SVG, self.wTree.get_widget("button-bg-filechooserbutton"))

		self.setup_bool( common.BUTTONS_CANCEL_ENABLED, self.wTree.get_widget("cancel-checkbutton") )
		self.setup_entry( common.BUTTONS_CANCEL_LABEL, self.wTree.get_widget("cancel-entry") )
		self.setup_chooser( common.BUTTONS_CANCEL_SVG, self.wTree.get_widget("cancel-filechooserbutton"))
		
		self.setup_bool( common.BUTTONS_LOCK_ENABLED, self.wTree.get_widget("lock-checkbutton") )
		self.setup_entry( common.BUTTONS_LOCK_LABEL, self.wTree.get_widget("lock-entry") )
		self.setup_chooser( common.BUTTONS_LOCK_SVG, self.wTree.get_widget("lock-filechooserbutton"))

		self.setup_bool( common.BUTTONS_LOGOUT_ENABLED, self.wTree.get_widget("logout-checkbutton") )
		self.setup_entry( common.BUTTONS_LOGOUT_LABEL, self.wTree.get_widget("logout-entry") )
		self.setup_chooser( common.BUTTONS_LOGOUT_SVG, self.wTree.get_widget("logout-filechooserbutton"))

		self.setup_bool( common.BUTTONS_REBOOT_ENABLED, self.wTree.get_widget("reboot-checkbutton") )
		self.setup_entry( common.BUTTONS_REBOOT_LABEL, self.wTree.get_widget("reboot-entry") )
		self.setup_chooser( common.BUTTONS_REBOOT_SVG, self.wTree.get_widget("reboot-filechooserbutton"))

		self.setup_bool( common.BUTTONS_SHUTDOWN_ENABLED, self.wTree.get_widget("shutdown-checkbutton") )
		self.setup_entry( common.BUTTONS_SHUTDOWN_LABEL, self.wTree.get_widget("shutdown-entry") )
		self.setup_chooser( common.BUTTONS_SHUTDOWN_SVG, self.wTree.get_widget("shutdown-filechooserbutton"))
		
		self.setup_scale( common.BUTTONS_SCALE, self.wTree.get_widget("button-scale-hscale"))

		# Commands Tab
		self.setup_entry( common.COMMANDS_LOCK, self.wTree.get_widget("lock-cmd-entry") )
		self.setup_entry( common.COMMANDS_LOGOUT, self.wTree.get_widget("logout-cmd-entry") )
		self.setup_entry( common.COMMANDS_REBOOT, self.wTree.get_widget("reboot-cmd-entry") )
		self.setup_entry( common.COMMANDS_SHUTDOWN, self.wTree.get_widget("shutdown-cmd-entry") )
		
	

	def keypressed(self, widget, event, data=None):
		# ESC key code
		if event.keyval == 65307:
			gtk.main_quit()
	
	
	#
	# Color chooser setup
	#
	def setup_color(self, key, colorbut):
		color, alpha = common.make_color(self.client.get_string(key))
		colorbut.set_color(color)
		colorbut.set_alpha(alpha)
		colorbut.connect("color-set", self.color_changed, key)
	
	def color_changed(self, colorbut, key):
		string =  common.make_color_string(colorbut.get_color(), colorbut.get_alpha())
		self.client.set_string(key, string)


	#
	# Scale setup
	#
	def setup_scale(self, key, scale):
		val = self.client.get_float(key)
		scale.set_value(val)
		scale.connect("value-changed", self.scale_changed, key)
	
	def scale_changed(self, scale, key):
		val = scale.get_value()
		self.client.set_float(key, val)
		
	
	#
	# File chooser setup
	#
	def setup_chooser(self, key, chooser):
		"""sets up svg choosers"""
		fil = gtk.FileFilter()
		fil.set_name("SVG Files")
		fil.add_pattern("*.svg")
		fil.add_pattern("*.SVG")
		chooser.add_filter(fil)
		preview = gtk.Image()
		chooser.set_preview_widget(preview)
		if self.client.get_string(key):
			chooser.set_filename(self.client.get_string(key))
		chooser.connect("update-preview", self.update_preview, preview)
		chooser.connect("selection-changed", self.chooser_changed, key)
	
	def chooser_changed(self, chooser, key):
		f = chooser.get_filename()
		if f == None:
			return
		self.client.set_string(key, f)
	
	
	def update_preview(self, chooser, preview):
		f = chooser.get_preview_filename()
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(f, 128, 128)
			preview.set_from_pixbuf(pixbuf)
			have_preview = True
		except:
			have_preview = False
		chooser.set_preview_widget_active(have_preview)
	
	#
	# checkbox setup
	#
	def setup_bool(self, key, check):
		"""sets up checkboxes"""
		check.set_active(self.client.get_bool(key))
		check.connect("toggled", self.bool_changed, key)
		
	
	def bool_changed(self, check, key):
		self.client.set_bool(key, check.get_active())


	#
	# Radio button setup
	#
	def setup_radio(self, key, radio, value):
		"""sets up radio buttons"""
		val = self.client.get_string(key)
		if val == value:
			radio.set_active( True )
		else:
			radio.set_active( False )
		radio.connect("toggled", self.radio_changed, key, value)
	
	def radio_changed(self, radio, key, value):
		if radio.get_active():
			self.client.set_string(key, value)
		

	#
	# Textbox entry setup
	#
	def setup_entry(self, key, entry):
		"""sets up entry textboxes"""
		entry.set_text(self.client.get_string(key))
		entry.connect("changed", self.entry_changed, key)
		
	
	def entry_changed(self, entry, key):
		self.client.set_string(key, entry.get_text())




if __name__ == "__main__":
	gettext.textdomain(I18N_DOMAIN)
	gtk.glade.bindtextdomain(I18N_DOMAIN, "/usr/share/locale")
	app = preferences()
	gtk.main()

