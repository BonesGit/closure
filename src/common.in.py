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
#  Notes: Closure commons
#         Taken from avant-window-navigator's preferences
#

try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
except:
	sys.exit(1)


DATA_DIR = "@PKGDATADIR@"


# GCONF KEYS

GENERAL_PATH			= "/apps/closure/general"
GENERAL_FULLSCREEN		= "/apps/closure/general/fullscreen"		# bool
GENERAL_COMPACT			= "/apps/closure/general/compact"			# bool
GENERAL_WINDOWTYPE		= "/apps/closure/general/window_type"		# string

BACKGROUND_PATH			= "/apps/closure/background"
BACKGROUND_STYLE		= "/apps/closure/background/style" #bool
BACKGROUND_SOLID		= "/apps/closure/background/solid" #string
BACKGROUND_LINEAR_STEP_1	= "/apps/closure/background/linear_step_1" #string
BACKGROUND_LINEAR_STEP_2	= "/apps/closure/background/linear_step_2" #string
BACKGROUND_LINEAR_STEP_3	= "/apps/closure/background/linear_step_3" #string
BACKGROUND_SVG_IMAGE		= "/apps/closure/background/svg" 		#string

BUTTONS_PATH		= "/apps/closure/buttons"
BUTTONS_BG_SVG		= "/apps/closure/buttons/bg_svg"				#string
BUTTONS_CANCEL_ENABLED	= "/apps/closure/buttons/cancel_enabled"	#bool
BUTTONS_CANCEL_LABEL	= "/apps/closure/buttons/cancel_label"		#string
BUTTONS_CANCEL_SVG		= "/apps/closure/buttons/cancel_svg" 		#color
BUTTONS_LOCK_ENABLED	= "/apps/closure/buttons/lock_enabled"		#bool
BUTTONS_LOCK_LABEL		= "/apps/closure/buttons/lock_label"		#string
BUTTONS_LOCK_SVG		= "/apps/closure/buttons/lock_svg" 			#color
BUTTONS_LOGOUT_ENABLED	= "/apps/closure/buttons/logout_enabled"	#bool
BUTTONS_LOGOUT_LABEL	= "/apps/closure/buttons/logout_label"		#string
BUTTONS_LOGOUT_SVG		= "/apps/closure/buttons/logout_svg" 		#color
BUTTONS_REBOOT_ENABLED	= "/apps/closure/buttons/reboot_enabled"	#bool
BUTTONS_REBOOT_LABEL	= "/apps/closure/buttons/reboot_label"		#string
BUTTONS_REBOOT_SVG		= "/apps/closure/buttons/reboot_svg" 		#color
BUTTONS_SHUTDOWN_ENABLED	= "/apps/closure/buttons/shutdown_enabled"	#bool
BUTTONS_SHUTDOWN_LABEL		= "/apps/closure/buttons/shutdown_label"	#string
BUTTONS_SHUTDOWN_SVG		= "/apps/closure/buttons/shutdown_svg" 		#color
BUTTONS_SCALE				= "/apps/closure/buttons/scale"				#float

COMMANDS_PATH		= "/apps/closure/commands"
COMMANDS_LOCK		= "/apps/closure/commands/lock"		#string
COMMANDS_LOGOUT		= "/apps/closure/commands/logout"	#string
COMMANDS_REBOOT		= "/apps/closure/commands/reboot"	#string
COMMANDS_SHUTDOWN	= "/apps/closure/commands/shutdown"	#string


COLOR_BIT_MAX = 65535




#
# Load a boolean from gconf
#
def loadBool(client, key, default):
	v = client.get_bool( key )
	if v == None:
		return default
	else:
		return v

#
# Load a float from gconf
#
def loadFloat(client, key, default):
	v = client.get_float( key )
	if v == None:
		return default
	else:
		return v


#
# Load a string from gconf
#
def loadString(client, key, default):
	v = client.get_string( key )
	if v == None:
		return default
	else:
		return v
	
#
# Load a string from gconf
#
# Returns: A 4-tuple containing floats for RGBA color.
#
def loadColor(client, key, default):
	v = client.get_string( key )
	if v == None:
		v = default
	(color, alpha) = make_color( v )
	r = color.red / float(COLOR_BIT_MAX)
	g = color.green / float(COLOR_BIT_MAX)
	b = color.blue / float(COLOR_BIT_MAX)
	a = alpha / float(COLOR_BIT_MAX)

	return (r, g, b, a)




def dec2hex(n):
	"""return the hexadecimal string representation of integer n"""
	n = int(n)
	if n == 0:
		return "00"
	return "%0.2X" % n
 
 
def hex2dec(s):
	"""return the integer value of a hexadecimal string s"""
	return int(s, 16)


def make_color(hexi):
	"""returns a gtk.gdk.Color from a hex string RRGGBBAA"""
	color = gtk.gdk.color_parse('#' + hexi[:6])
	alpha = hex2dec(hexi[6:])
	alpha = (float(alpha)/255)* COLOR_BIT_MAX
	return color, int(alpha)


def make_color_string(color, alpha):
	"""makes readable string from gdk.color & alpha (0-65535) """
	string = ""
	
	string = string + dec2hex(int( (float(color.red) / COLOR_BIT_MAX)*255))
	string = string + dec2hex(int( (float(color.green) / COLOR_BIT_MAX)*255))
	string = string + dec2hex(int( (float(color.blue) / COLOR_BIT_MAX)*255))
	string = string + dec2hex(int( (float(alpha) / COLOR_BIT_MAX)*255))
	
	#hack
	return string	
