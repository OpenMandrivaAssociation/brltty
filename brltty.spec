%define lib_api_major 0
%define lib_api_version 0.4.1
%define lib_api_name %mklibname brlapi %{lib_api_version} %{lib_api_major}


Name:		brltty
Version:	3.7.2
Release:	%mkrel 6
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Summary:	Braille display driver for Linux/Unix
%define		_bindir	/bin
%define		_libdir	/lib

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
Provides: brlapi-devel = %{version}-%{release}
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

%prep
%setup -q
%patch0 -p1 -b .varargs
%patch1 -p1 -b .dontstrip

%build
%configure2_5x --with-install-root="$RPM_BUILD_ROOT"
%make

%install
rm -rf $RPM_BUILD_ROOT
make install-programs install-help install-tables install-drivers 
make -C Programs install-api
install -m644 Documents/%{name}.conf -D $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install -m644 Documents/%{name}.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_api_name} -p /sbin/ldconfig

%postun -n %{lib_api_name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README COPYING Documents/ChangeLog Documents/TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/%{name}
%attr(0755,root,root) %{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/*/*

%files -n %{lib_api_name}
%defattr(-,root,root)
%{_libdir}/*.so.%{lib_api_major}.*

%files -n %{lib_api_name}-devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/brltty
