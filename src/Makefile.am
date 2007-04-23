
glade_DATA = pref.glade
gladedir = $(pkgdatadir)

schemadir = @GCONF_SCHEMA_FILE_DIR@
schema_DATA_IN = closure.schemas.in
schema_DATA = closure.schemas

@INTLTOOL_SCHEMAS_RULE@

$(schema_DATA): $(schema_DATA_IN)
	sed -e "s|\@PREFIX\@|$(prefix)|g" $< > $@

install-data-local:
#	sed -e "s|\@PREFIX\@|$(prefix)|g" $(schema_DATA_IN) > $(schema_DATA)
	GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) $(GCONFTOOL) --makefile-install-rule $(srcdir)/$(schema_DATA)


pkgpyexecdirdir = $(pkgpythondir)
pkgpyexecdirPYTHON_INSTALL = $(INSTALL_PROGRAM)

pkgpython_PYTHON=SVGButton.py common.py
pkgpyexecdir_PYTHON=closure.py closure_preferences.py

install-exec-local:
	sed -e "s|\@PKGDATADIR\@|$(pkgdatadir)|g" common.in.py > common.py
	sed -e "s|\@PREFIX\@|$(prefix)|g" closure.pc.in > closure.pc
	$(INSTALL_DATA) closure.pc $(libdir)/pkgconfig/closure.pc


EXTRA_DIST = $(glade_DATA) common.in.py $(schema_DATA) $(schema_DATA_IN)

clean:
	rm -f *.pyo *.pyc common.py closure.pc $(schema_DATA)
