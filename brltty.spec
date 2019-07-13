%global _disable_ld_no_undefined 1

%define major	0.7
%define libname	%mklibname brlapi %{major}
%define devname	%mklibname brlapi -d

%ifarch %{arm} %{mips}
%bcond_with	java
%else
%bcond_without	java
%endif

Summary:	Braille display driver for Linux/Unix
Name:		brltty
Version:	6.0
Release:	1
License:	GPLv2+
Group:		System/Servers
Url:		http://mielke.cc/brltty/
Source0:	http://mielke.cc/brltty/archive/brltty-%{version}.tar.xz
Patch0:		brltty-cppflags.patch
Patch1:		brltty-4.4-add-missing-include-path.patch
Patch2:		brltty-6.0-no--L_usr_lib.patch

BuildRequires:	bison
BuildRequires:	ocaml
BuildRequires:	python-cython
BuildRequires:	subversion
BuildRequires:	festival-devel
BuildRequires:	gpm-devel
BuildRequires:	libbraille-devel
BuildRequires:	speech_tools-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xtst)
%if %{with java}
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel
%endif
BuildConflicts:	findlib

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
License:	LGPLv2+

%description -n	%{libname}
This package provides the run-time support for the Application
Programming Interface to BRLTTY.

Install this package if you have an application which directly accesses
a refreshable braille display.

%package -n	%{devname}
Summary:	Headers, static archive, and documentation for BrlAPI
Group:		Development/C
License:	LGPLv2+
Provides:	brlapi-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package provides the header files, static archive, shared object
linker reference, and reference documentation for BrlAPI (the
Application Programming Interface to BRLTTY).  It enables the
implementation of applications which take direct advantage of a
refreshable braille display in order to present information in ways
which are more appropriate for blind users and/or to provide user
interfaces which are more specifically atuned to their needs.

%if %{with java}
%package -n	java-brlapi
Summary:	Java bindings for BrlAPI
Group:		Development/Java
Requires:	java-devel-openjdk
%rename		brlapi-java

%description -n	java-brlapi
This package provides the Java bindings for BrlAPI,
which is the Application Programming Interface to BRLTTY.

Install this package if you have a Java application
which directly accesses a refreshable braille display.
%endif

%package -n	python-brlapi
Summary:	Python bindings for BrlAPI
Group:		Development/Python
Obsoletes:	python3-brlapi

%description -n	python-brlapi
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
Requires:	ocaml-brlapi = %{version}-%{release}
Requires:	brlapi-devel = %{version}-%{release}

%description -n	ocaml-brlapi-devel
The ocaml-brlapi-devel package contains libraries and signature files for
developing applications that use ocaml-brlapi.

%prep
%setup -q
%apply_patches
autoconf

%build
# Patch6 changes aclocal.m4:
for i in -I/usr/lib/jvm/java/include{,/linux}; do
      java_inc="$java_inc $i"
done
%configure \
	CPPFLAGS="$java_inc" \
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
rm -f %{buildroot}/%{_lib}/*.a %{buildroot}%{_libdir}/ocaml/brlapi/*.a

install -m644 Documents/%{name}.conf -D %{buildroot}%{_sysconfdir}/%{name}.conf
install -m644 Documents/%{name}.1 -D %{buildroot}%{_mandir}/man1/%{name}.1

install -d %{buildroot}%{_bindir}
for f in brltty-config brltty-ctb xbrlapi; do
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

# handle locales
%find_lang %{name}

%files -n %{name} -f %{name}.lang
%doc README Documents/ChangeLog Documents/TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
/bin/*
%{_bindir}/*
%{_sysconfdir}/X11/Xsession.d/60xbrlapi
%exclude %{_bindir}/brltty-config
%{_sysconfdir}/%{name}
%{_datadir}/gdm/greeter/autostart/xbrlapi.desktop
/%{_lib}/%{name}
%{_mandir}/man1/*
%{_datadir}/polkit-1/actions/org.a11y.brlapi.policy

%files -n %{libname}
/%{_lib}/libbrlapi.so.%{major}*

%files -n %{devname}
%{_bindir}/brltty-config
%doc Documents/BrlAPIref/html
/%{_lib}/*.so
%{_includedir}/brlapi.h
%{_includedir}/brlapi_*.h
%{_includedir}/brltty
%{_mandir}/man3/*

%if %{with java}
%files -n java-brlapi
%{_datadir}/java/brlapi.jar
%endif

%files -n python-brlapi
%{py3_platsitedir}/brlapi.*
%{py3_platsitedir}/Brlapi-*

%files -n ocaml-brlapi
%dir %{_libdir}/ocaml/brlapi
%{_libdir}/ocaml/brlapi/META
%{_libdir}/ocaml/brlapi/*.cma
%{_libdir}/ocaml/brlapi/*.cmi
%{_libdir}/ocaml/brlapi/dllbrlapi_stubs.so

%files -n ocaml-brlapi-devel
%{_libdir}/ocaml/brlapi/*.cmxa
%{_libdir}/ocaml/brlapi/*.cmx
%{_libdir}/ocaml/brlapi/*.mli
