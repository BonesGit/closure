# About #
![http://closure.googlecode.com/svn/trunk/data/closure-48.png](http://closure.googlecode.com/svn/trunk/data/closure-48.png) What is Closure and why do I need it?
Closure was created because I don't use a desktop manager like KDE or GNOME and I had no way to gracefully shutdown or reboot my computer in a pretty graphically way.  I built Closure to fill in the gaps of my X environment. You may not have a direct need for Closure.

Closure was built with eye candy in mind.  It currently will only run on top of a composite X window manager like Beryl or Compiz. Currently I use the Avant Window Navigator as my only desktop panel, so Closure will integrate nicely with it.  Get [AWN](http://code.google.com/p/avant-window-navigator/).

## Features ##
These four features execute command line programs. Sudo might be required for some.
  * Lock computer
  * Logout User
  * Reboot computer
  * Shutdown computer

Other features:
  * Preferences for configuration
  * SVG image drawing support

See the project's [TODO](http://closure.googlecode.com/svn/trunk/TODO) file for a list of features still to come.

## Screenshot ##

![![](http://closure.googlecode.com/svn/trunk/screenshots/closure-tn.jpg)](http://closure.googlecode.com/svn/trunk/screenshots/closure.png)

# Download #
Download the latest stable build from the 'Downloads' tab or go to the 'Source' tab to get the latest unstable version directly from SVN.

# Dependencies #
Closure is currently written in Python and is dependent on Python 2.4.  Time willing, this project might be converted to C/C++ but as of now there is no need for it.

Closure also depends on a number of other libraries such as; glib, gtk, cairo, librsvg, gnome-desktop, and libglade (and the python bindings for these libraries, see the project [README](http://closure.googlecode.com/svn/trunk/README) for more info).

# Get Involved #
## Bugs & Features ##
File bugs & feature enhancements using the 'Issues' tab above.