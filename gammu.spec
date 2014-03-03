%define major 7
%define libname %mklibname %{name} %major
%define libnamedev %mklibname %{name} -d

Summary:		Mobile phones tools for Unix (Linux) and Win32
Name:			gammu
Version:		1.33.0
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

%__mkdir_p %{buildroot}%{_sysconfdir}
%__sed -e 's|^port =.*$|port = /dev/ttyS0|' \
         -e 's|^connection =.*$|connection = dlr3|' \
         -e 's/$//' \
         < docs/config/gammurc > %{buildroot}%{_sysconfdir}/gammurc

mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/69-gammu-acl.rules

%find_lang %{name} lib%{name} %{name}.lang

%files -f %{name}.lang
%doc ChangeLog COPYING INSTALL README
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
%py_platsitedir/gammu

%changelog
* Tue Aug 16 2011 Alexander Barakin <abarakin@mandriva.org> 1.29.0-2mdv2012.0
+ Revision: 694692
- rebuild (see #63959)

* Wed Jan 19 2011 Funda Wang <fwang@mandriva.org> 1.29.0-1
+ Revision: 631676
- new version 1.29.0

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.28.0-6mdv2011.0
+ Revision: 627236
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1.28.0-5mdv2011.0
+ Revision: 626521
- rebuilt against mysql-5.5.8 libs

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.28.0-3mdv2011.0
+ Revision: 609658
- rebuilt against new libdbi

* Wed Nov 03 2010 Funda Wang <fwang@mandriva.org> 1.28.0-2mdv2011.0
+ Revision: 592714
- update file list

  + Michael Scherer <misc@mandriva.org>
    - rebuild for python 2.7

* Thu Jul 15 2010 Funda Wang <fwang@mandriva.org> 1.28.0-1mdv2011.0
+ Revision: 553428
- new version 1.28.0

* Thu Dec 24 2009 Frederik Himpe <fhimpe@mandriva.org> 1.27.0-1mdv2010.1
+ Revision: 481989
- update to new version 1.27.0
- Update to new version 1.26.93

* Wed Dec 16 2009 Frederic Crozat <fcrozat@mandriva.com> 1.26.92-2mdv2010.1
+ Revision: 479479
- Fix invalid udev rules (Mdv bug #56107)

* Thu Dec 03 2009 Funda Wang <fwang@mandriva.org> 1.26.92-1mdv2010.1
+ Revision: 472979
- new version 1.26.92

* Thu Nov 19 2009 Frederik Himpe <fhimpe@mandriva.org> 1.26.91-1mdv2010.1
+ Revision: 467543
- update to new version 1.26.91

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 1.26.90-1mdv2010.1
+ Revision: 462662
- Disable parallel make: it breaks build
- update to new version 1.26.90

* Tue Oct 27 2009 Frederic Crozat <fcrozat@mandriva.com> 1.26.1-2mdv2010.0
+ Revision: 459494
- Add udev ACL rules for ttyACM

* Wed Sep 09 2009 Frederik Himpe <fhimpe@mandriva.org> 1.26.1-1mdv2010.0
+ Revision: 435905
- Update to new version 1.26.1 (new major)

* Sat Jul 11 2009 Funda Wang <fwang@mandriva.org> 1.25.0-2mdv2010.0
+ Revision: 394733
- fix file list
- BR usb
- new version 1.25.0

* Mon May 04 2009 Funda Wang <fwang@mandriva.org> 1.24.0-1mdv2010.0
+ Revision: 371555
- New version 1.24.0

* Wed Mar 18 2009 Funda Wang <fwang@mandriva.org> 1.23.1-1mdv2009.1
+ Revision: 357109
- New version 1.23.1

* Mon Jan 19 2009 Funda Wang <fwang@mandriva.org> 1.22.91-1mdv2009.1
+ Revision: 331253
- New version 1.22.91
- add BRs

* Sun Jan 04 2009 Jérôme Soyer <saispo@mandriva.org> 1.22.1-1mdv2009.1
+ Revision: 324645
- update to new version 1.22.1

* Thu Dec 18 2008 Funda Wang <fwang@mandriva.org> 1.22.0-1mdv2009.1
+ Revision: 315680
- New version 1.22.0

* Sat Oct 11 2008 Funda Wang <fwang@mandriva.org> 1.21.0-1mdv2009.1
+ Revision: 292071
- New version 1.21.0

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.20.0-2mdv2009.0
+ Revision: 266832
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun May 11 2008 Funda Wang <fwang@mandriva.org> 1.20.0-1mdv2009.0
+ Revision: 205441
- update to new version 1.20.0

* Tue May 06 2008 Funda Wang <fwang@mandriva.org> 1.19.91-1mdv2009.0
+ Revision: 201768
- New version 1.19.91

* Fri Apr 25 2008 Funda Wang <fwang@mandriva.org> 1.19.90-1mdv2009.0
+ Revision: 197367
- New version 1.19.90

* Wed Apr 16 2008 Funda Wang <fwang@mandriva.org> 1.19.0-1mdv2009.0
+ Revision: 194541
- New version 1.19.0

* Thu Feb 07 2008 Funda Wang <fwang@mandriva.org> 1.18.90-1mdv2008.1
+ Revision: 163359
- New version 1.18.90

* Wed Jan 30 2008 Funda Wang <fwang@mandriva.org> 1.18.0-1mdv2008.1
+ Revision: 160290
- New version 1.18.0

* Sun Jan 27 2008 Funda Wang <fwang@mandriva.org> 1.17.92-1mdv2008.1
+ Revision: 158583
- New version 1.17.92

* Sun Jan 06 2008 Funda Wang <fwang@mandriva.org> 1.17.0-1mdv2008.1
+ Revision: 145928
- New version 1.17.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Funda Wang <fwang@mandriva.org> 1.16.0-1mdv2008.1
+ Revision: 120515
- update to new version 1.16.0

* Tue Dec 04 2007 Funda Wang <fwang@mandriva.org> 1.15.90-1mdv2008.1
+ Revision: 115295
- New version 1.15.90

* Tue Nov 20 2007 Funda Wang <fwang@mandriva.org> 1.15.0-1mdv2008.1
+ Revision: 110747
- New version 1.50.0

* Thu Nov 08 2007 Funda Wang <fwang@mandriva.org> 1.14.0-1mdv2008.1
+ Revision: 106896
- New version 1.14.0

* Sun Oct 28 2007 Funda Wang <fwang@mandriva.org> 1.13.95-1mdv2008.1
+ Revision: 102802
- New version 1.13.95

* Fri Oct 19 2007 Funda Wang <fwang@mandriva.org> 1.13.94-2mdv2008.1
+ Revision: 100168
- Obsoletes old devel package

* Wed Oct 17 2007 Funda Wang <fwang@mandriva.org> 1.13.94-1mdv2008.1
+ Revision: 99569
- New major
- Updated to svn 1628
- updated to svn release to fix build
- New version 1.13.94

* Wed Aug 22 2007 Funda Wang <fwang@mandriva.org> 1.13.0-1mdv2008.0
+ Revision: 68852
- New version 1.13.0

* Tue Aug 14 2007 Funda Wang <fwang@mandriva.org> 1.12.94-1mdv2008.0
+ Revision: 63191
- New version 1.12.94

* Tue Aug 07 2007 Funda Wang <fwang@mandriva.org> 1.12.93-2mdv2008.0
+ Revision: 59765
- renew patch from svn
- Add patch to build on 64 bit machines
- New testing version 1.12.93
- br doxygen and dot
- fix file list
- Use cmake macro
- BR cmake
- New version 1.12.0

* Tue Apr 17 2007 Erwan Velu <erwan@mandriva.org> 1.10.0-1mdv2008.0
+ Revision: 14119
- 1.10

