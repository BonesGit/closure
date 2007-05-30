desktopdir   = $(datadir)/applications
desktop_DATA = closure.desktop
@INTLTOOL_DESKTOP_RULE@


$(desktop_DATA).in: $(desktop_DATA).in.in
	sed -e "s|\@PKGDATADIR\@|$(pkgdatadir)|g" $< > $@

icon_DATA = 							\
			closure.svg					\
			button-background.svg		\
			system-lock-screen.svg		\
			system-log-out.svg			\
			computer-reboot.svg			\
			computer.svg				\
			preferences-desktop-screensaver.svg \
			emblem-unreadable.svg		\
			emblem-unreadable-focus.svg	\
			closure-24.png				\
			closure-48.png

icondir = $(pkgdatadir)

EXTRA_DIST = $(icon_DATA) $(desktop_DATA).in.in

CLEANFILES = $(desktop_DATA) $(desktop_DATA).in

