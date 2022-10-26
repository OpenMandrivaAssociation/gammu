%define major 8
%define libname	%mklibname %{name}
%define devname %mklibname %{name} -d

%bcond_without	test

Summary:	Mobile phones tools for Unix (Linux) and Win32
Name:		gammu
Version:	1.42.0
Release:	4
License:	GPLv2+
Group:		Communications
#Source0	http://dl.cihar.com/gammu/releases/%{name}-%{version}.tar.xz
Source0:	https://github.com/gammu/%{name}/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Source1:	69-gammu-acl.rules
URL:		http://www.gammu.org/
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(dbi)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libusb-1.0)
%{?with_test:
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(mariadb)
BuildRequires:	pkgconfig(odbc)
}
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-units

%description
Gammu can do such things with cellular phones as making data calls,
updating the address book, changing calendar and ToDo entries, sending and
receiving SMS messages, loading and getting ring tones and pictures (different
types of logos), synchronizing time, enabling NetMonitor, managing WAP
settings and bookmarks and much more. Functions depend on the phone model.

%files -f %{name}.lang
%doc ChangeLog COPYING INSTALL README.rst
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}rc
%{_sysconfdir}/udev/rules.d/*.rules
%{_sysconfdir}/bash_completion.d/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}-detect
%{_bindir}/%{name}-smsd
%{_bindir}/%{name}-smsd-inject
%{_bindir}/%{name}-smsd-monitor
%{_bindir}/jadmaker
%{_mandir}/man1/%{name}-detect.*
%{_mandir}/man1/%{name}-smsd-inject.*
%{_mandir}/man1/%{name}-smsd-monitor.1.*
%{_mandir}/man1/%{name}-smsd.*
%{_mandir}/man1/%{name}.*
%{_mandir}/man1/jadmaker.*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_docdir}/%{name}/examples
%{_docdir}/%{name}/manual
%{_datadir}/%{name}
%{_systemd_util_dir}/system/%{name}-smsd.service

#---------------------------------------------------------------------------

%package -n %libname
Summary:	Mobile phones tools for Unix (Linux) and Win32 (libraries)
Group:		System/Libraries
Requires:	%{name} = %{version}

%description -n %libname
Gammu can do such things with cellular phones as making data calls,
updating the address book, changing calendar and ToDo entries, sending and
receiving SMS messages, loading and getting ring tones and pictures (different
types of logos), synchronizing time, enabling NetMonitor, managing WAP
settings and bookmarks and much more. Functions depend on the phone model.

%files -n %libname
%{_libdir}/*.so.%{major}*

#---------------------------------------------------------------------------

%package -n %devname
Summary:	Headers and pkgconfig file for Gammu development
Group:		Development/Other
Requires:	%libname = %{version}
Provides:	libgammu-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %devname
This package contains the headers and pkgconfig file that programmers
will need to develop applications which will use libGammu.

%files -n %devname
%{_bindir}/gammu-config
%{_libdir}/*.so
%{_includedir}/gammu
%{_mandir}/man1/gammu-config.*
%{_libdir}/pkgconfig/*.pc

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
export LDFLAGS+=-lcurl
%cmake \
	-DINSTALL_LIB_DIR=%{_lib} \
	-DONLINE_TESTING:BOOL=OFF \
	-DPSQL_TESTING:BOOL=%{?with_test:ON}%{?without_test:OFF} \
	-DMYSQL_TESTING:BOOL=%{?with_test:ON}%{?without_test:OFF} \
	-DODBC_TESTING:BOOL=%{?with_test:ON}%{?without_test:OFF} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# config
install -dm 0755 %{buildroot}%{_sysconfdir}
sed -e 's|^port =.*$|port = /dev/ttyS0|' \
	-e 's|^connection =.*$|connection = dlr3|' \
	-e 's/$//' \
	< docs/config/gammurc > %{buildroot}%{_sysconfdir}/gammurc

# udev rule
install -dm 0755 %{buildroot}%{_sysconfdir}/udev/rules.d/
install -pm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/69-gammu-acl.rules

# locales
%find_lang %{name} lib%{name} %{name}.lang

