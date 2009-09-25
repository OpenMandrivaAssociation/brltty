%define	_bindir	/bin
%define	_libdir /lib
%ifarch x86_64
%define	_libdir /lib64
%endif

%define major		0.5
%define libname		%mklibname brlapi %{major}
%define develname	%mklibname brlapi -d

%ifarch %arm %mips
%define build_java 0
%else
%define build_java 1
%endif

Name:		brltty
Version:	4.0
Release:	%mkrel 3
License:	GPL+
Group:		System/Servers
URL:		http://mielke.cc/brltty/
Source0:	http://mielke.cc/brltty/releases/%{name}-%{version}.tar.gz
Patch0:		brltty-3.9-varargs.patch
# (fc) 3.7.2-6mdv don't strip executable to have valid debug package (Fedora)
# (aw) re-diffed and re-activated 3.9-4mdv
Patch1:		brltty-3.9-dontstrip.patch
# Slightly hacky fix for Java includes to make it build with openjdk,
# where jni_md.h is in a subdirectory of /include . Should not need to
# patch configure directly - just patching bindings.m4 and running
# autoreconf would be enough - but autoreconf is broken with brltty
# 3.9 - AdamW 2008/07
Patch3:		brltty-4.0-javainclude.patch
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
%if %{build_java}
Buildrequires:	java-rpmbuild
%endif
BuildConflicts: findlib
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

%if %{build_java}
%package -n brlapi-java
Group:		Development/Java
Summary:	Java bindings for BrlAPI
Requires:	java-devel-openjdk
Obsoletes:	%{mklibname brlapi 0.5}-java <= %{version}-%{release}

%description -n brlapi-java
This package provides the Java bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Java application
which directly accesses a refreshable braille display.
%endif

%package -n brlapi-python
Summary:	Python bindings for BrlAPI
Group:		Development/Python
Obsoletes:	%{mklibname brlapi 0.5.1 0}-python <= %{version}-%{release}
Obsoletes:	%{mklibname brlapi 0.5}-python <= %{version}-%{release}

%description -n brlapi-python
This package provides the Python bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Python application
which directly accesses a refreshable braille display.

%package -n brlapi-ocaml
Summary:	Ocaml bindings for BrlAPI
Group:		Development/Other

%description -n brlapi-ocaml
This package provides the Ocaml bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Ocaml application
which directly accesses a refreshable braille display.

%prep
%setup -q
%patch0 -p1 -b .varargs
%patch1 -p1 -b .dontstrip
%patch3 -p1 -b .javainclude

%build
# must set this explicitly or else it detects it as /usr and the
# headers aren't found - AdamW 2008/07
export JAVA_HOME=%{java_home}
%configure2_5x --with-install-root="%{buildroot}" --disable-relocatable-install --disable-tcl-bindings
make

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_prefix}/%{_lib}/ocaml/stublibs
# just to avoid an installation error
touch %{buildroot}%{_prefix}/%{_lib}/ocaml/ld.conf
make install install-programs install-tables install-drivers
install -m644 Documents/%{name}.conf -D %{buildroot}%{_sysconfdir}/%{name}.conf
install -m644 Documents/%{name}.1 -D %{buildroot}%{_mandir}/man1/%{name}.1
rm -f %{buildroot}%{_prefix}/%{_lib}/ocaml/ld.conf

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

%if %{build_java}
%files -n brlapi-java
%defattr(-,root,root)
%{_prefix}/lib/java/libbrlapi_java.so
%{_datadir}/java/brlapi.jar
%endif

%files -n brlapi-python
%defattr(-,root,root)
%{py_platsitedir}/brlapi.*
%{py_platsitedir}/Brlapi-*

%files -n brlapi-ocaml
%defattr(-,root,root)
%{_prefix}/%{_lib}/ocaml/brlapi
%{_prefix}/%{_lib}/ocaml/stublibs/dllbrlapi_stubs.so*
