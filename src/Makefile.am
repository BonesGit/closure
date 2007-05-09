
glade_DATA = pref.glade
gladedir = $(pkgdatadir)

schemadir = @GCONF_SCHEMA_FILE_DIR@
schema_DATA_IN = closure.schemas.in
schema_DATA = closure.schemas

@INTLTOOL_SCHEMAS_RULE@

$(schema_DATA): $(schema_DATA_IN)
	sed -e "s|\@PREFIX\@|$(prefix)|g" $< > $@

install-data-local:
	GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) $(GCONFTOOL) --makefile-install-rule $(srcdir)/$(schema_DATA)
	killall -HUP gconfd-2


pkgpyexecdirdir = $(pkgpythondir)
pkgpyexecdirPYTHON_INSTALL = $(INSTALL_PROGRAM)

pkgpython_PYTHON=SVGButton.py common.py
pkgpyexecdir_PYTHON=closure.py closure_preferences.py

#nodistdir = .
#nobase_nodist_pkgpython_PYTHON=common.py
#nodist_pkgpython_PYTHON=common.py
#noinst_PYTHON=common.py

common.py: common.in.py
	sed -e "s|\@PKGDATADIR\@|$(pkgdatadir)|g" common.in.py > common.py

install-exec-local:
	sed -e "s|\@PKGDATADIR\@|$(pkgdatadir)|g" common.in.py > common.py
	sed -e "s|\@PREFIX\@|$(prefix)|g" closure.pc.in > closure.pc
	mkdir -p $(DESTDIR)$(libdir)/pkgconfig
	$(INSTALL_DATA) closure.pc $(DESTDIR)$(libdir)/pkgconfig/closure.pc


uninstall-local:
	GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) $(GCONFTOOL) --makefile-uninstall-rule $(srcdir)/$(schema_DATA)
	killall -HUP gconfd-2
	rm -f $(DESTDIR)$(libdir)/pkgconfig/closure.pc


EXTRA_DIST = $(glade_DATA) common.in.py closure.pc.in $(schema_DATA_IN)

clean:
	rm -f *.pyo *.pyc common.py closure.pc $(schema_DATA)
