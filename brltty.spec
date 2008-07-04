%define	_bindir	/bin
%define	_libdir /lib
%ifarch x86_64
%define	_libdir /lib64
%endif

%define major		0.5
%define libname		%mklibname brlapi %{major}
%define develname	%mklibname brlapi -d

Name:		brltty
Version:	3.9
Release:	%mkrel 6
License:	GPL+
Group:		System/Servers
URL:		http://mielke.cc/brltty/
Source0:	http://mielke.cc/brltty/releases/%{name}-%{version}.tar.bz2
Patch0:		brltty-3.9-varargs.patch
# (fc) 3.7.2-6mdv don't strip executable to have valid debug package (Fedora)
# (aw) re-diffed and re-activated 3.9-4mdv
Patch1:		brltty-3.9-dontstrip.patch
# Works around a build error reported and partially discussed upstream:
# http://www.mail-archive.com/brltty@mielke.cc/msg01377.html
# upstream categorizes this as a workaround not a fix, but no fix seems
# yet to have been made available - AdamW 2008/07
Patch2:		brltty-3.9-buildworkaround.patch
# Fix an 'empty declarator' build error (from upstream SVN) - AdamW
# 2008/07
Patch3:		brltty-3.9-declarator.patch
# Slightly hacky fix for Java includes to make it build with openjdk,
# where jni_md.h is in a subdirectory of /include . Should not need to
# patch configure directly - just patching bindings.m4 and running
# autoreconf would be enough - but autoreconf is broken with brltty
# 3.9 - AdamW 2008/07
Patch4:		brltty-3.9-javainclude.patch
BuildRequires:	bison
BuildRequires:	gpm-devel
BuildRequires:	X11-devel
Buildrequires:	python-devel
Buildrequires:  ncurses-devel
Buildrequires:	bluez-devel
Buildrequires:  python-pyrex
Buildrequires:  ocaml
Buildrequires:  festival-devel
Buildrequires:  libbraille-devel
Buildrequires:  speech_tools-devel
Buildrequires:  libalsa-devel
Buildrequires:	java-rpmbuild
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Summary:	Braille display driver for Linux/Unix

%description
BRLTTY is a background process (daemon) which provides
access to the Linux/Unix console (when in text mode)
for a blind person using a refreshable braille display.
It drives the braille display,
and provides complete screen review functionality.
Some speech capability has also been incorporated.

%package -n %{libname}
Summary:	API for brltty
Group:		System/Libraries
License:	LGPL+
Obsoletes:	%{mklibname brlapi 0.5.1 0} <= %{version}-%{release}
Obsoletes:	%{mklibname brlapi 0.4.1 0} <= %{version}-%{release}

%description -n %{libname}
This package provides the run-time support for the Application
Programming Interface to BRLTTY.

Install this package if you have an application which directly accesses
a refreshable braille display.

%package -n %{develname}
Group:		Development/C
License:	LGPL+
Summary:	Headers, static archive, and documentation for BrlAPI
Provides:	brlapi-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{mklibname brlapi 0.5.1 0 -d} <= %{version}-%{release}
Obsoletes:	%{mklibname brlapi 0.4.1 0 -d} <= %{version}-%{release}

%description -n %{develname}
This package provides the header files, static archive, shared object
linker reference, and reference documentation for BrlAPI (the
Application Programming Interface to BRLTTY).  It enables the
implementation of applications which take direct advantage of a
refreshable braille display in order to present information in ways
which are more appropriate for blind users and/or to provide user
interfaces which are more specifically atuned to their needs.

Install this package if you're developing or maintaining an application
which directly accesses a refreshable braille display.

%package -n %{libname}-java
Group:		Development/Java
Summary:	Java bindings for BrlAPI
Requires:	java-devel-openjdk
Provides:	brlapi-java = %{version}-%{release}

%description -n %{libname}-java
This package provides the Java bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Java application
which directly accesses a refreshable braille display.

%package -n %{libname}-python
Summary:	Python bindings for BrlAPI
Group:		Development/Python
Provides:	brlapi-python = %{version}-%{release}
Obsoletes:	%{mklibname brlapi 0.5.1 0}-python <= %{version}-%{release}

%description -n %{libname}-python
This package provides the Python bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Python application
which directly accesses a refreshable braille display.

%prep
%setup -q
%patch0 -p1 -b .varargs
%patch1 -p1 -b .dontstrip
%patch2 -p1 -b .build
%patch3 -p1 -b .declarator
%patch4 -p1 -b .javainclude

%build
# must set this explicitly or else it detects it as /usr and the
# headers aren't found - AdamW 2008/07
export JAVA_HOME=%{java_home}
%configure2_5x --with-install-root="%{buildroot}" --disable-relocatable-install --disable-tcl-bindings
make

%install
rm -rf %{buildroot}
make install install-programs install-tables install-drivers install-help
install -m644 Documents/%{name}.conf -D %{buildroot}%{_sysconfdir}/%{name}.conf
install -m644 Documents/%{name}.1 -D %{buildroot}%{_mandir}/man1/%{name}.1

directory="doc"
mkdir -p "${directory}"
for file in `find . \( -path "./${directory}" -o -path ./Documents \) -prune -o \( -name 'README*' -o -name '*.patch' -o -name '*.txt' -o -name '*
.html' -o -name '*.sgml' -o \( -path "./Bootdisks/*" -type f -perm +ugo=x \) \) -print`
do
   mkdir -p "${directory}/${file%/*}"
   cp -rp "${file}" "${directory}/${file}"
done

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{name}
%defattr(-,root,root)
%doc README Documents/ChangeLog Documents/TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755,root,root) %{_bindir}/*
%{_sysconfdir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc Documents/BrlAPIref
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/brlapi.h
%{_includedir}/brlapi_*.h
%{_includedir}/brltty
%{_mandir}/man3/*

%files -n %{libname}-java
%defattr(-,root,root)
%{_prefix}/lib/java/libbrlapi_java.so
%{_datadir}/java/brlapi.jar

%files -n %{libname}-python
%defattr(-,root,root)
%{_prefix}/%{_libdir}/python*/site-packages/brlapi.*
%{_prefix}/%{_libdir}/python*/site-packages/Brlapi-*
