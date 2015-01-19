%define major 7
%define libname %mklibname %{name} %major
%define libnamedev %mklibname %{name} -d

Summary:		Mobile phones tools for Unix (Linux) and Win32
Name:			gammu
Version:		1.34.0
Release:		1
License:		GPLv2+
Group:			Communications
Source:			http://dl.cihar.com/gammu/releases/%{name}-%{version}.tar.xz
Source1:		69-gammu-acl.rules
URL:			http://www.gammu.org/
BuildRequires:		pkgconfig(bluez)
BuildRequires:		cmake
BuildRequires:		doxygen
BuildRequires:		gettext-devel
BuildRequires:		curl-devel
BuildRequires:		mysql-devel
BuildRequires:		postgresql-devel
BuildRequires:		python-devel
BuildRequires:		dbi-devel
BuildRequires:		usb1.0-devel
BuildRequires:		systemd-units
BuildRequires:		pkgconfig(systemd)

%description
Gammu can do such things with cellular phones as making data calls,
updating the address book, changing calendar and ToDo entries, sending and
receiving SMS messages, loading and getting ring tones and pictures (different
types of logos), synchronizing time, enabling NetMonitor, managing WAP
settings and bookmarks and much more. Functions depend on the phone model.

%package -n %libname
Summary: Mobile phones tools for Unix (Linux) and Win32 (libraries)
Group: System/Libraries
Requires: %{name} = %{version}

%description -n %libname
Gammu can do such things with cellular phones as making data calls,
updating the address book, changing calendar and ToDo entries, sending and
receiving SMS messages, loading and getting ring tones and pictures (different
types of logos), synchronizing time, enabling NetMonitor, managing WAP
settings and bookmarks and much more. Functions depend on the phone model.

%package -n %libnamedev
Summary:		Headers and pkgconfig file for Gammu development
Group:			Development/Other
Requires:		%libname = %{version}
Provides:		libgammu-devel = %{version}-%{release}
Provides:		%{name}-devel = %{version}-%{release}
Obsoletes:		%mklibname -d gammu 0.0
Obsoletes:		%mklibname -d gammu 1.0

%description -n %libnamedev
This package contains the headers and pkgconfig file that programmers
will need to develop applications which will use libGammu.

%package -n python-%{name}
Summary:		Python module to communicate with mobile phones
Group:			Communications
Requires:		%{name} = %{version}
BuildRequires:  python-devel

%description -n python-%{name}
This provides gammu module, that can work with any phone Gammu
supports - many Nokias, Siemens, Alcatel, ...

%prep
%setup -q

%build
%cmake -DINSTALL_LIB_DIR=%{_lib}
%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_sysconfdir}
%__sed -e 's|^port =.*$|port = /dev/ttyS0|' \
         -e 's|^connection =.*$|connection = dlr3|' \
         -e 's/$//' \
         < docs/config/gammurc > %{buildroot}%{_sysconfdir}/gammurc

mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/69-gammu-acl.rules

%find_lang %{name} lib%{name} %{name}.lang

%files -f %{name}.lang
%doc ChangeLog COPYING INSTALL
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/gammurc
%{_sysconfdir}/udev/rules.d/*.rules
%{_sysconfdir}/bash_completion.d/gammu
%{_bindir}/gammu
%{_bindir}/gammu-detect
%{_bindir}/gammu-smsd
%{_bindir}/gammu-smsd-inject
%{_bindir}/gammu-smsd-monitor
%{_bindir}/jadmaker
%{_mandir}/man1/gammu-detect.*
%{_mandir}/man1/gammu-smsd-inject.*
%{_mandir}/man1/gammu-smsd-monitor.1.*
%{_mandir}/man1/gammu-smsd.*
%{_mandir}/man1/gammu.*
%{_mandir}/man1/jadmaker.*
%{_mandir}/man5/*
%{_mandir}/man7/*
#%doc %{_datadir}/doc/%{name}
%{_datadir}/%{name}
/lib/systemd/system/gammu-smsd.service

%files -n %libname
%{_libdir}/*.so.%{major}*

%files -n %libnamedev
%{_bindir}/gammu-config
%{_libdir}/*.so
%{_includedir}/gammu
%{_mandir}/man1/gammu-config.*
%{_libdir}/pkgconfig/*.pc

%files -n python-%{name}
%doc python/examples
%{py_platsitedir}/gammu

