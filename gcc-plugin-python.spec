%define name gcc-plugin-python
%define gccdir %(gcc -print-file-name=plugin)

Name:		%{name}
Epoch:		1
Version:	0.12
Release:	2
License:	GPLv3
Summary:	GCC Python Plugin
Group:		Development/C
URL:		https://fedorahosted.org/gcc-python-plugin/
Source0:	gcc-python-plugin-0.12.tar.gz
Patch0:	0001-Using-Python-plugin-from-GCC-plugin-directory.patch
#Patch1:	0002-Add-c-common-include-directory.patch

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
BuildRequires:	python-devel

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
%{_bindir}/gcc-with-python
%{_bindir}/gcc-with-cpychecker
%{_mandir}/man1/gcc-python-plugin.1*
#%{python_sitelib}/gccutils.py
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
%doc %{_docdir}/%{name}-doc/*

%package -n gcc-python-plugin-c-api
Summary: Shared library to make it easier to write GCC plugins
Group:   Development/C
Requires: gcc

%description -n gcc-python-plugin-c-api
Shared library to make it easier to write GCC plugins

%files -n gcc-python-plugin-c-api
%{gcc_plugins_dir}/libgcc-c-api.so

%prep
%setup -q -n gcc-python-plugin-0.12

%autopatch -p1

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

#%{__install} -m644 gccutils.py %{buildroot}%{python_sitelib}/
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
