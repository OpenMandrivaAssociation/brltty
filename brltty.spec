%define lib_api_major 0
%define lib_api_version 0.5.1
%define lib_api_name %mklibname brlapi %{lib_api_version} %{lib_api_major}


Name:		brltty
Version:	3.9
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://mielke.cc/brltty/
Source0:	http://mielke.cc/brltty/releases/%{name}-%{version}.tar.bz2
Patch0:		brltty-3.7.2-varargs.patch.bz2
# (fc) 3.7.2-6mdv don't strip executable to have valid debug package (Fedora)
Patch1:		brltty-3.7.2-dontstrip.patch
BuildRequires:	bison
BuildRequires:	gpm-devel
BuildRequires:	X11-devel
Buildrequires:	python-devel ncurses-devel
Buildrequires:	bluez-devel python-pyrex
Buildrequires:  ocaml festival-devel %{mklibname braille}-devel speech_tools-devel %{mklibname alsa2}-devel
%ifarch %ix86
Buildrequires:	java-1.7.0-icedtea-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Summary:	Braille display driver for Linux/Unix
%define		_bindir	/bin
%define         _libdir /lib
%ifarch x86_64
%define		_libdir /lib64
%endif

%description
BRLTTY is a background process (daemon) which provides
access to the Linux/Unix console (when in text mode)
for a blind person using a refreshable braille display.
It drives the braille display,
and provides complete screen review functionality.
Some speech capability has also been incorporated.

%package -n %{lib_api_name}
Summary: API for brltty
Group: System/Libraries
License: LGPL

%description -n %{lib_api_name}
This package provides the run-time support for the Application
Programming Interface to BRLTTY.

Install this package if you have an application which directly accesses
a refreshable braille display.

%package -n %{lib_api_name}-devel
Group: Development/C
License: LGPL
Summary: Headers, static archive, and documentation for BrlAPI
Provides: %{lib_api_name}-devel = %{version}-%{release}
Provides: libbrlapi%{lib_api_version}-devel = %{version}-%{release}
Requires: %{lib_api_name} = %{version}

%description -n %{lib_api_name}-devel
This package provides the header files, static archive, shared object
linker reference, and reference documentation for BrlAPI (the
Application Programming Interface to BRLTTY).  It enables the
implementation of applications which take direct advantage of a
refreshable braille display in order to present information in ways
which are more appropriate for blind users and/or to provide user
interfaces which are more specifically atuned to their needs.

Install this package if you're developing or maintaining an application
which directly accesses a refreshable braille display.

%package -n %{lib_api_name}-java
Group: Development/Java
Summary: Java bindings for BrlAPI
requires: java-1.7.0-icedtea-devel
Provides: %{lib_api_name}-java = %{version}-%{release}
%description -n %{lib_api_name}-java
This package provides the Java bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Java application
which directly accesses a refreshable braille display.


%package -n %{lib_api_name}-python
Summary: Python bindings for BrlAPI
Group: Development/Python
Provides: %{lib_api_name}-python = %{version}-%{release}
%description -n %{lib_api_name}-python
This package provides the Python bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Python application
which directly accesses a refreshable braille display.

%prep
%setup -q
#%patch0 -p1 -b .varargs
#%patch1 -p1 -b .dontstrip

%build
#%configure --with-install-root="$RPM_BUILD_ROOT" --disable-java-bindings --with-speech-driver=Festival --disable-relocatable-install
%configure --with-install-root="$RPM_BUILD_ROOT" --disable-relocatable-install --disable-tcl-bindings
make

%install
rm -rf $RPM_BUILD_ROOT
make install install install-programs install-tables install-drivers install-help
install -m644 Documents/%{name}.conf -D $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install -m644 Documents/%{name}.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

directory="doc"
mkdir -p "${directory}"
for file in `find . \( -path "./${directory}" -o -path ./Documents \) -prune -o \( -name 'README*' -o -name '*.patch' -o -name '*.txt' -o -name '*
.html' -o -name '*.sgml' -o \( -path "./Bootdisks/*" -type f -perm +ugo=x \) \) -print`
do
   mkdir -p "${directory}/${file%/*}"
   cp -rp "${file}" "${directory}/${file}"
done

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_api_name} -p /sbin/ldconfig

%postun -n %{lib_api_name} -p /sbin/ldconfig

%files -n %name
%defattr(-,root,root)
%doc README COPYING Documents/ChangeLog Documents/TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755,root,root) %{_bindir}/*
%{_sysconfdir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/*

%files -n %{lib_api_name}
%defattr(-,root,root)
%{_libdir}/*.so.%{lib_api_major}.*

%files -n %{lib_api_name}-devel
%defattr(-,root,root)
%doc Documents/BrlAPIref
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/brlapi.h
%{_includedir}/brlapi_*.h
%{_includedir}/brltty
%{_mandir}/man3/*

%ifarch %ix86
%files -n %{lib_api_name}-java
%defattr(-,root,root)
/usr/%{_libdir}/java/libbrlapi_java.so
/usr/share/java/brlapi.jar
%endif

%files -n %{lib_api_name}-python
/usr/%{_libdir}/python*/site-packages/brlapi.*
/usr/%{_libdir}/python*/site-packages/Brlapi-*
