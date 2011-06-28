%define name gcc-plugin-python
%define srcname gcc-python-plugin-%{gccpythongit}
%define gccversion 4.6.1
%define gccrelease 2
%define dategit 20110628
%define gccpythongit 7b437b2
%define gccpythonversion 0.0.%{dategit}git%{gccpythongit}
%define version %{gccversion}+%{gccpythonversion}

%define gccdir %(gcc -print-file-name=plugin)

Name:		%{name}
Version:	%{version}
Release:	5
License:	GPLv3
Summary:	GCC Python Plugin
Group:		Development/C
URL:		https://fedorahosted.org/gcc-python-plugin/
# generated by git archive --format=tar --prefix=gcc-python-plugin-$(git describe --always)/ master | bzip2 > gcc-python-plugin-$(git describe --always).tar.bz2
Source0:	%{srcname}.tar.bz2
Patch0:		0001-fix-permerror-misusage.patch
Patch1:		0001-Using-Python-plugin-from-GCC-plugin-directory.patch
Patch2:		0001-Using-Freedesktop-standard-for-image-viewing.patch
Requires:	gcc-plugin-devel = %{gccversion}-%{gccrelease}
Requires:	graphviz
Requires:	xdg-utils
BuildRequires:	gcc-plugin-devel
BuildRequires:  gmp-devel
BuildRequires:  ppl-devel
BuildRequires:  ppl_c-devel
BuildRequires:  mpfr-devel
BuildRequires:  libmpc-devel
BuildRequires:	python-sphinx
%py_requires

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
%{_mandir}/gcc-python-plugin.1*
%{python_sitelib}/gccutils.py
%{python_sitelib}/cpybuilder.py
%{python_sitelib}/cpychecker.py
%{python_sitelib}/libcpychecker/*.py
%{gccdir}/python.so

%prep
%setup -q -n %{srcname}
%patch0 -p1 -b .permerror~
%patch1 -p1 -b .pluginpath~
%patch2 -p1 -b .xdg-open~

%build
%make plugin

pushd docs
	%make man
popd

%install
%{__install} -m755 -d %{buildroot}%{_bindir}
%{__install} -m755 -d %{buildroot}%{_mandir}
%{__install} -m755 -d %{buildroot}%{gccdir}
%{__install} -m755 -d %{buildroot}%{python_sitelib}
%{__install} -m755 -d %{buildroot}%{python_sitelib}/libcpychecker/

%{__install} -m755 python.so %{buildroot}%{gccdir}/
%{__install} -m755 gcc-with-python %{buildroot}%{_bindir}/
%{__install} -m644 gccutils.py %{buildroot}%{python_sitelib}/
%{__install} -m644 cpychecker.py %{buildroot}%{python_sitelib}/
%{__install} -m644 cpybuilder.py %{buildroot}%{python_sitelib}/
pushd libcpychecker
	%{__install} -m644 *.py %{buildroot}%{python_sitelib}/libcpychecker/
popd
pushd docs
	%{__install} -m644 _build/man/gcc-python-plugin.1* %{buildroot}%{_mandir}/
popd

%clean
rm -fr %{buildroot}
