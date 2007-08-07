%define name	gammu
%define version	1.12.93
%define release	%mkrel 1

%define major 2
%define libname %mklibname %{name} %major
%define libnamedev %mklibname %{name} -d

Summary:		Mobile phones tools for Unix (Linux) and Win32
Name:			%{name}
Version:		%{version}
Release:		%{release}
License:		GPL
Group:			Communications
Source:			http://www.mwiacek.com/zips/gsm/gammu/stable/1_0x/%{name}-%{version}.tar.bz2
URL:			http://www.gammu.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-root
BuildRequires:		libbluez-devel cmake doxygen

%description
Gammu can do such things with cellular phones as making data calls,
updating the address book, changing calendar and ToDo entries, sending and
receiving SMS messages, loading and getting ring tones and pictures (different
types of logos), synchronizing time, enabling NetMonitor, managing WAP
settings and bookmarks and much more. Functions depend on the phone model.

%package -n %libname
Summary: Mobile phones tools for Unix (Linux) and Win32 (libraries)
Group: System/Libraries

%description -n %libname
Gammu can do such things with cellular phones as making data calls,
updating the address book, changing calendar and ToDo entries, sending and
receiving SMS messages, loading and getting ring tones and pictures (different
types of logos), synchronizing time, enabling NetMonitor, managing WAP
settings and bookmarks and much more. Functions depend on the phone model.

%package -n %libnamedev
Summary:		Headers and pkgconfig file for Gammu development
Group:			Development/Other
Requires:		%libname = %version
Provides:		libgammu-devel
Obsoletes:		%libname-devel

%description -n %libnamedev
This package contains the headers and pkgconfig file that programmers
will need to develop applications which will use libGammu.

%prep
%setup -q

%build
%cmake -DENABLE_SHARED=ON
make

%install
rm -rf %{buildroot}
cd build
%makeinstall_std
cd -
%__mkdir_p %{buildroot}%{_sysconfdir}
%__sed -e 's|^port =.*$|port = /dev/ttyS0|' \
         -e 's|^connection =.*$|connection = dlr3|' \
         -e 's/$//' \
         < docs/examples/config/gammurc > %{buildroot}%{_sysconfdir}/gammurc

%find_lang %name

%files -f %name.lang
%defattr(-,root,root)
%doc ChangeLog COPYING INSTALL README VERSION docs/examples
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/gammurc
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%doc docs/develop/*
%attr(0755,root,root) %{_libdir}/*.so
%{_includedir}/gammu
%{_libdir}/pkgconfig/gammu.pc

%clean
rm -rf %{buildroot}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig
