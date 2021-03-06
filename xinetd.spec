
Summary:	xinetd -- A better inetd.
Name:		xinetd
Version:	2.3.14
Release:	1
License:	BSD
Vendor:		xinetd.org (Rob Braun)
Group:		System Environment/Daemons
Packager:	Steve Grubb <linux_4ever@yahoo.com>
URL:		http://www.xinetd.org/
Source:		%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Provides:	inetd
Prereq:		/sbin/chkconfig, /sbin/service 
BuildRequires:  tcp_wrappers >= 7.6
Obsoletes:	inetd

%description
Xinetd is a powerful inetd replacement. Xinetd has access control 
mechanisms, extensive logging capabilities, the ability to make 
services available based on time, can place limits on the number 
of servers that can be started, and has a configurable defence 
mechanism to protect against port scanners, among other things.
 
%prep
%setup -q

%build
  ./configure				\
	--sbindir=%{_sbindir} 		\
	--mandir=%{_datadir}/man	\
	--with-libwrap 			\
	--with-inet6
  make
  strip xinetd/xinetd
  cp xinetd/xinetd xinetd6
  make distclean
  ./configure \
	--sbindir=$RPM_BUILD_ROOT/%{_sbindir} 		\
	--mandir=$RPM_BUILD_ROOT/%{_datadir}/man	\
	--with-libwrap 
  make
  strip xinetd/xinetd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/etc/xinetd.d

%makeinstall  
install -m 0755 xinetd6 $RPM_BUILD_ROOT/%{_sbindir}
install -m 0755 contrib/xinetd $RPM_BUILD_ROOT/etc/rc.d/init.d/xinetd
install -m 0600 contrib/xinetd.conf $RPM_BUILD_ROOT/etc/
cp contrib/xinetd.d/* $RPM_BUILD_ROOT/etc/xinetd.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then
   /sbin/chkconfig --add xinetd
fi

%preun
if [ $1 = 0 ]; then
   /sbin/service xinetd stop > /dev/null 2>&1
   /sbin/chkconfig --del xinetd
fi

%postun
if [ $1 -ge 1 ]; then
   /sbin/service xinetd condrestart > /dev/null 2>&1
fi

%files
%defattr(-, root, root)
%doc CHANGELOG COPYRIGHT README xinetd/sample.conf contrib/empty.conf 
%{_sbindir}/*
%{_datadir}/man/*/*
%attr(0750, root, root) %config(noreplace) /etc/rc.d/init.d/xinetd
%attr(0750, root, root) %config(noreplace) /etc/xinetd.conf
%attr(0750, root, root) %config(noreplace) /etc/xinetd.d/*

%changelog
* Sun Sep 07 2003 Steve Grubb <linux_4ever@yahoo.com>
- Refined installation and added services.
 
