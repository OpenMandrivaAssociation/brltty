%define major		0.5
%define libname		%mklibname brlapi %{major}
%define develname	%mklibname brlapi -d

%ifarch %{arm} %{mips}
%bcond_with	java
%else
%bcond_without	java
%endif

Summary:	Braille display driver for Linux/Unix
Name:		brltty
Version:	4.4
Release:	2
License:	GPLv2+
Group:		System/Servers
URL:		http://mielke.cc/brltty/
Source0:	http://mielke.cc/brltty/releases/%{name}-%{version}.tar.gz
Patch0:		brltty-cppflags.patch
Patch1:		brltty-4.4-add-missing-include-path.patch
BuildRequires:	bison
BuildRequires:	gpm-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	python-devel
BuildRequires:	bluez-devel
BuildRequires:  python-pyrex
BuildRequires:  ocaml
BuildRequires:  festival-devel
BuildRequires:  libbraille-devel
BuildRequires:  speech_tools-devel
BuildRequires:	subversion
%if %{with java}
BuildRequires:	java-rpmbuild
%endif
BuildConflicts: findlib

%description
BRLTTY is a background process (daemon) which provides
access to the Linux/Unix console (when in text mode)
for a blind person using a refreshable braille display.
It drives the braille display,
and provides complete screen review functionality.
Some speech capability has also been incorporated.

%package -n	%{libname}
Summary:	API for brltty
Group:		System/Libraries
License:	LGPL+
Obsoletes:	%{mklibname brlapi 0.5.1 0} <= %{version}-%{release}
Obsoletes:	%{mklibname brlapi 0.4.1 0} <= %{version}-%{release}

%description -n	%{libname}
This package provides the run-time support for the Application
Programming Interface to BRLTTY.

Install this package if you have an application which directly accesses
a refreshable braille display.

%package -n	%{develname}
Group:		Development/C
License:	LGPL+
Summary:	Headers, static archive, and documentation for BrlAPI
Provides:	brlapi-devel = %{EVRD}
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

%if %{with java}
%package -n	brlapi-java
Group:		Development/Java
Summary:	Java bindings for BrlAPI
Requires:	java-devel-openjdk
Obsoletes:	%{mklibname brlapi 0.5}-java <= %{version}-%{release}

%description -n	brlapi-java
This package provides the Java bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Java application
which directly accesses a refreshable braille display.
%endif

%package -n	brlapi-python
Summary:	Python bindings for BrlAPI
Group:		Development/Python
Obsoletes:	%{mklibname brlapi 0.5.1 0}-python <= %{version}-%{release}
Obsoletes:	%{mklibname brlapi 0.5}-python <= %{version}-%{release}

%description -n	brlapi-python
This package provides the Python bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Python application
which directly accesses a refreshable braille display.

%package -n	ocaml-brlapi
Summary:	Ocaml bindings for BrlAPI
Group:		Development/Other
%rename		brlapi-ocaml

%description -n	ocaml-brlapi
This package provides the Ocaml bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Ocaml application
which directly accesses a refreshable braille display.

%package -n	ocaml-brlapi-devel
Summary:	Development files for ocaml-brlapi
Group:		Development/Other
Requires:	ocaml-brlapi = %{EVRD}
Requires:	brlapi-devel = %{EVRD}

%description -n	ocaml-brlapi-devel
The ocaml-brlapi-devel package contains libraries and signature files for
developing applications that use ocaml-brlapi.

%prep
%setup -q
%patch0 -p1 -b .cppflags~
%patch1 -p1 -b .includes~
autoconf

%build
# Patch6 changes aclocal.m4:
for i in -I/usr/lib/jvm/java/include{,/linux}; do
      java_inc="$java_inc $i"
done
%configure2_5x	CPPFLAGS="$java_inc" \
		--bindir=/bin \
		--libdir=/%{_lib} \
		--with-install-root="%{buildroot}" \
		--disable-relocatable-install \
		--disable-tcl-bindings \
		--disable-stripping
%make

%install
# just to avoid an installation error
make install
install -m644 Documents/%{name}.conf -D %{buildroot}%{_sysconfdir}/%{name}.conf
install -m644 Documents/%{name}.1 -D %{buildroot}%{_mandir}/man1/%{name}.1

install -d %{buildroot}%{_bindir}
for f in brltty-config brltty-ctb /brltty-install xbrlapi; do
	mv "%{buildroot}/bin/$f" "%{buildroot}%{_bindir}/$f"
done

# Missing ocaml library
cp Bindings/OCaml/*.cmx '%{buildroot}%{_libdir}/ocaml/brlapi/'

directory="doc"
mkdir -p "${directory}"
for file in `find . \( -path "./${directory}" -o -path ./Documents \) -prune -o \( -name 'README*' -o -name '*.patch' -o -name '*.txt' -o -name '*
.html' -o -name '*.sgml' -o \( -path "./Bootdisks/*" -type f -perm +ugo=x \) \) -print`
do
   mkdir -p "${directory}/${file%/*}"
   cp -rp "${file}" "${directory}/${file}"
done

%files -n %{name}
%doc README Documents/ChangeLog Documents/TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755,root,root) /bin/*
%{_bindir}/*
%{_sysconfdir}/%{name}
/%{_lib}/%{name}
%{_mandir}/man1/*

%files -n %{libname}
/%{_lib}/*.so.%{major}*

%files -n %{develname}
%doc Documents/BrlAPIref
/%{_lib}/*.so
/%{_lib}/*.a
%{_includedir}/brlapi.h
%{_includedir}/brlapi_*.h
%{_includedir}/brltty
%{_mandir}/man3/*

%if %{with java}
%files -n brlapi-java
%{_prefix}/lib/java/libbrlapi_java.so
%{_datadir}/java/brlapi.jar
%endif

%files -n brlapi-python
%{py_platsitedir}/brlapi.*
%{py_platsitedir}/Brlapi-*

%files -n ocaml-brlapi
%dir %{_libdir}/ocaml/brlapi
%{_libdir}/ocaml/brlapi/META
%{_libdir}/ocaml/brlapi/*.cma
%{_libdir}/ocaml/brlapi/*.cmi
%{_libdir}/ocaml/stublibs/*.so*

%files -n ocaml-brlapi-devel
%{_libdir}/ocaml/brlapi/*.a
%{_libdir}/ocaml/brlapi/*.cmxa
%{_libdir}/ocaml/brlapi/*.cmx
%{_libdir}/ocaml/brlapi/*.mli
