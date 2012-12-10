%define name gcc-plugin-python
%define gccdir %(gcc -print-file-name=plugin)

Name:		%{name}
Epoch:		1
Version:	0.6.53gfbfa7fa
Release:	3
License:	GPLv3
Summary:	GCC Python Plugin
Group:		Development/C
URL:		https://fedorahosted.org/gcc-python-plugin/
Source0:	%{name}-0.6.53gfbfa7fa.tar.bz2
Patch0:	0001-Using-Python-plugin-from-GCC-plugin-directory.patch
Patch1:	0002-Add-c-common-include-directory.patch

Requires:	gcc
Requires:	graphviz
Requires:	xdg-utils
Suggests:	%{name}-doc
BuildRequires:	gcc-plugin-devel
BuildRequires:  gmp-devel
BuildRequires:  ppl-devel
BuildRequires:  ppl_c-devel
BuildRequires:  mpfr-devel
BuildRequires:  libmpc-devel
BuildRequires:	python-sphinx
BuildRequires:	python-six
%py_requires -d

%description
This is a plugin for GCC, which links against libpython, and
(I hope) allows you to invoke arbitrary Python scripts from
inside the compiler. The aim is to allow you to write GCC
plugins in Python.

The plugin is Free Software, licensed under the GPLv3 (or
later).

It's still at the "experimental proof-of-concept stage";
expect crashes and tracebacks (I'm new to insides of GCC,
and I may have misunderstood things).

It's already possible to use this to add additional compiler
errors/warnings, e.g. domain-specific checks, or static
analysis. One of my goals for this is to "teach" GCC about
the common mistakes people make when writing extensions for
CPython, but it could be used e.g. to teach GCC about GTK's
reference-counting semantics, or about locking in the Linux
kernel, or about signal-safety in APIs. 

%files
%defattr(-,root,root,-)
%{_bindir}/gcc-with-python
%{_bindir}/gcc-with-cpychecker
%{_mandir}/man1/gcc-python-plugin.1*
%{python_sitelib}/gccutils.py
%{python_sitelib}/cpybuilder.py
%{python_sitelib}/cpychecker.py
%{python_sitelib}/libcpychecker/*.py
%{gccdir}/python.so

%package doc
Summary:	GCC Python Plugin HTML Documentation
BuildArch:	noarch

%description doc
This package provides HTML documentation for the GCC Python
Plugin, a GCC plugin aimed at tying together Python and GCC
to be able to use Python script from inside the compiler.

%files doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}-doc/*

%prep
%setup -q -n %{name}-0.6.53gfbfa7fa

%apply_patches

%build
%make plugin

pushd docs
	%make man
	%make html
popd

%install
%{__install} -m755 -d %{buildroot}%{_bindir}
%{__install} -m755 -d %{buildroot}%{_mandir}/man1/
%{__install} -m755 -d %{buildroot}%{_docdir}/%{name}-doc/
%{__install} -m755 -d %{buildroot}%{_docdir}/%{name}-doc/_images/
%{__install} -m755 -d %{buildroot}%{_docdir}/%{name}-doc/_sources/
%{__install} -m755 -d %{buildroot}%{_docdir}/%{name}-doc/_static/
%{__install} -m755 -d %{buildroot}%{gccdir}
%{__install} -m755 -d %{buildroot}%{python_sitelib}
%{__install} -m755 -d %{buildroot}%{python_sitelib}/libcpychecker/

%{__install} -m755 python.so %{buildroot}%{gccdir}/
%{__install} -m755 gcc-with-python %{buildroot}%{_bindir}/
%{__install} -m755 gcc-with-cpychecker %{buildroot}%{_bindir}/

%{__install} -m644 gccutils.py %{buildroot}%{python_sitelib}/
%{__install} -m644 cpychecker.py %{buildroot}%{python_sitelib}/
%{__install} -m644 cpybuilder.py %{buildroot}%{python_sitelib}/
pushd libcpychecker
	%{__install} -m644 *.py %{buildroot}%{python_sitelib}/libcpychecker/
popd
pushd docs
	%{__install} -m644 _build/man/gcc-python-plugin.1* %{buildroot}%{_mandir}/man1/
	%{__install} -m644 _build/html/*.html %{buildroot}%{_docdir}/%{name}-doc/
	%{__install} -m644 _build/html/*.js %{buildroot}%{_docdir}/%{name}-doc/
	%{__install} -m644 _build/html/*.inv %{buildroot}%{_docdir}/%{name}-doc/
	%{__install} -m644 _build/html/_images/* %{buildroot}%{_docdir}/%{name}-doc/_images/
	%{__install} -m644 _build/html/_sources/* %{buildroot}%{_docdir}/%{name}-doc/_sources/
	%{__install} -m644 _build/html/_static/* %{buildroot}%{_docdir}/%{name}-doc/_static/
popd

%clean
rm -fr %{buildroot}


%changelog
* Fri Oct 21 2011 Alexandre Lissy <alissy@mandriva.com> 1:0.6.53gfbfa7fa-3
+ Revision: 705588
- Updating for latest GCC build

* Sun Oct 16 2011 Alexandre Lissy <alissy@mandriva.com> 1:0.6.53gfbfa7fa-2
+ Revision: 704861
- Updating gcc python plugin to latest git snapshot (post v0.6)

* Thu Aug 25 2011 Alexandre Lissy <alissy@mandriva.com> 1:0.6.53gfbfa7fa-1
+ Revision: 697093
- Fixing build
- Updating to latest git snapshot

* Wed Aug 17 2011 Alexandre Lissy <alissy@mandriva.com> 1:0.6-2
+ Revision: 695031
- Add missing installation of /usr/bin/gcc-with-cpychecker
- Adding install of gcc-with-cpychecker

* Wed Aug 17 2011 Alexandre Lissy <alissy@mandriva.com> 1:0.6-1
+ Revision: 694858
- Update to latest post 0.6 snapshot

* Fri Aug 12 2011 Alexandre Lissy <alissy@mandriva.com> 1:0.5-1
+ Revision: 694207
- Adding BuildRequires against python-six in specfile
- Adding BuildRequires against python-six
- Updating source and patches thanks to gitrpm helper
- Updating for latest gitrpm helper
- Update for latest rpm-common changes
- GCC Python Plugin v0.5
- Push Epoch to 1
  Change versioning: removing gcc version
- Remove commit id from package version
- Adding gitrpm stuff

* Wed Jul 06 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.20110706giteeb6135-1
+ Revision: 688944
- Fixing git funny things
- Re-enabling Git funny stuff, just to see if it passes the buildsystem this time.

* Fri Jul 01 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.20110701git8fc9ca7-1
+ Revision: 688467
- Revert git fun, as the buildsystem seems not to like it :(
- Remove GCC version autodetection
- Updating sources to latest git
  Experimenting with rpm and git

* Wed Jun 29 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.20110628git7b437b2-8
+ Revision: 688232
- Fix doc paths, and release bump

* Wed Jun 29 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.20110628git7b437b2-7
+ Revision: 688209
- Remove unneeded dependency against gcc-plugin-devel
  Release bump
- Modifying gcc-with-python patch: removing hard-coded path, let's use the shorter way.

* Wed Jun 29 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.20110628git7b437b2-6
+ Revision: 688206
- Adding HTML documentation as a separate, noarch package.
- Fix man page directory

* Tue Jun 28 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.20110628git7b437b2-5
+ Revision: 687795
- Fix Python BuildRequires
- Fix patch level
- Change patch format
- Fix patch backups names
- Adding patch for replacement of 'eog' with 'xdg-open' (and the Requires corresponding)
- Fix python related BuildRequires
  Adding cpybuilder, cpychecker and libcpychecker
- Changing BuildRequires for python-devel to use the macro
- Remove use less post/preun
- Adding gccutils.py

* Tue Jun 28 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.20110628git7b437b2-4
+ Revision: 687701
- Release bump
- Adding a patch for correct reference to the GCC plugins' directory

* Tue Jun 28 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.20110628git7b437b2-3
+ Revision: 687678
- Fix version
- Updating sources to latest git
  Correct fix for Werror=format-security errors reported previously during compilation (patch sent upstream)

* Tue Jun 28 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.git431bc10-2
+ Revision: 687648
- gcc-plugin-devel release bump
- gcc-plugin-devel release bump

* Mon Jun 27 2011 Alexandre Lissy <alissy@mandriva.com> 4.6.1+0.0.git431bc10-1
+ Revision: 687571
- Adding missing BuildRequires from GCC
- Add missing BuildRequires against Python
- Missing patch
- Added manpages
- Fix paths and remove gcc melt oldies
- Adding build section
  Adding install section
- Initial non functionnal import of GCC Python Plugin
- Created package structure for gcc-plugin-python.

