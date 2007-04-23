
install-exec-local:
	sed -e "s|\@PKGLIBDIR\@|$(pkgpythondir)|g" closure.in > closure
	sed -e "s|\@PKGLIBDIR\@|$(pkgpythondir)|g" closure-preferences.in > closure-preferences
	$(INSTALL) -m 755 closure $(DESTDIR)$(bindir)/closure
	$(INSTALL) -m 755 closure-preferences $(DESTDIR)$(bindir)/closure-preferences

clean:
	rm -f closure closure-preferences
