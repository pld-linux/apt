Name:		apt
Version:	0.3.19cnc21
Release:	1
Summary:	Debian's Advanced Packaging Tool with RPM support
Summary(pl):	Zawansowane Narzêdzie do Zarz±dzania Pakietami
Summary(pt_BR):Frontend avançado para pacotes rpm e deb
Summary(es):	Advanced Packaging Tool frontend for rpm and dpkg
Group:		Applications/Archiving
Group(de):	Applikationen/Archivierung
Group(es):	Administración
Group(pl):	Aplikacje/Archiwizacja
License:	GPL
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	sources.list
Source3:	vendors.list
URL:		ftp://ftp.conectiva.com/pub/conectiva/EXPERIMENTAL/apt/
BuildRequires:	rpm-devel >= 3.0.5
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
BuildRequires:	db3-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A port of Debian's apt tools for RPM based distributions. It provides
the apt-get utility that provides a simpler, safer way to install and
upgrade packages. APT features complete installation ordering,
multiple source capability and several other unique features.

%description -l pl
Port Debianowego narzêdzia apt dla dystrybucji bazuj±cych na zarz±dcy
pakietów RPM. apt dostarcza narzêdzie apt-get, który umo¿liwia prost±
bezpieczn± instalacjê i aktualizacjê pakietów. Mo¿liwo¶ci APT to wybór
kolejno¶ci instalacji, mo¿liwo¶æ ustawienia kilku ¼róde³ pakietów itp.

%description -l pt_BR
Um porte das ferramentas apt do Debian para distribuições baseadas no
RPM. Sob desenvolvimento, use por sua própria conta e risco.

%package -n libapt-pkg-devel
Summary:	Development files for APT's libapt-pkg
Summary(pl):	Pliki developerskie dla APT libapt-pkg
Summary(pt_BR):Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT
Summary(es):	Development files for APT's libapt-pkg
Group:		Development
Group(de):	Entwicklung
Group(pl):	Programowanie
Group(pt_BR):Desenvolvimento
Group:		
Group():	
Group(de):	Applikationen/Archivierung
Group(es):	Desarrollo
Group(pl):	Aplikacje/Archiwizacja
Requires:	%{name}-%{version}

%description -n libapt-pkg-devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%description -l pl -n libapt-pkg-devel
Pakiet zawiera pliki nag³ówkowe potrzebne do rozwoju aplikacji
korzystaj±cych z biblioteki libapt-pkg.

%description -l pt_BR -n libapt-pkg-devel
Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT

%description -l es -n libapt-pkg-devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%package -n libapt-pkg-static
Summary:	Static libapt-pkg library
Summary(pl):	Statyczna biblioteka libapt-pkg
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki

%description -n libapt-pkg-static
Static libapt-pkg library

%description -l pl -n libapt-pkg-static
Statyczna biblioteka libapt-pkg.

%prep
%setup -q
tar xzf docs.tar.gz

%build
%configure \
	--enable-nls \
	--with-gpm \
	--with-cpus=1
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_localstatedir}/cache/%{name}/archives/partial
install -d $RPM_BUILD_ROOT%{_localstatedir}/state/%{name}/lists/partial

install -d $RPM_BUILD_ROOT%{_libdir}/
cp -a	bin/libapt-pkg.so.*	$RPM_BUILD_ROOT%{_libdir}/
cp -a	bin/libapt-pkg.so	$RPM_BUILD_ROOT%{_libdir}/

install -D bin/apt-get		$RPM_BUILD_ROOT%{_bindir}/apt-get
install -D bin/apt-cache	$RPM_BUILD_ROOT%{_bindir}/apt-cache
install -D bin/apt-config	$RPM_BUILD_ROOT%{_bindir}/apt-config
install -D bin/apt-cdrom	$RPM_BUILD_ROOT%{_bindir}/apt-cdrom
install -D bin/genpkglist	$RPM_BUILD_ROOT%{_bindir}/genpkglist
install -D bin/gensrclist	$RPM_BUILD_ROOT%{_bindir}/gensrclist
install -D tools/genbasedir	$RPM_BUILD_ROOT%{_bindir}/genbasedir

install -d $RPM_BUILD_ROOT%{_includedir}/apt-pkg/
install -D apt-pkg/*.h		$RPM_BUILD_ROOT%{_includedir}/apt-pkg/
install -D apt-pkg/*/*.h	$RPM_BUILD_ROOT%{_includedir}/apt-pkg/

install -d $RPM_BUILD_ROOT/%{_mandir}/man5/
install -d $RPM_BUILD_ROOT/%{_mandir}/man8/
install -D doc/apt.conf.5	$RPM_BUILD_ROOT/%{_mandir}/man5/apt.conf.5
install -D doc/sources.list.5	$RPM_BUILD_ROOT/%{_mandir}/man5/sources.list.5
install -D doc/vendors.list.5	$RPM_BUILD_ROOT/%{_mandir}/man5/vendors.list.5
install -D doc/apt-cache.8	$RPM_BUILD_ROOT/%{_mandir}/man8/apt-cache.8
install -D doc/apt-config.8	$RPM_BUILD_ROOT/%{_mandir}/man8/apt-config.8
install -D doc/apt.8		$RPM_BUILD_ROOT/%{_mandir}/man8/apt.8
install -D doc/apt-cdrom.8	$RPM_BUILD_ROOT/%{_mandir}/man8/apt-cdrom.8
install -D doc/apt-get.8	$RPM_BUILD_ROOT/%{_mandir}/man8/apt-get.8
install -D doc/apt-get.8	$RPM_BUILD_ROOT/%{_mandir}/man8/apt-get.8

install -d $RPM_BUILD_ROOT%{_libdir}/apt
install  bin/methods/* $RPM_BUILD_ROOT%{_libdir}/apt

install -D %{SOURCE1}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf
install -D %{SOURCE2}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/sources.list
install -D %{SOURCE3}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/vendors.list
install -D rpmpriorities	$RPM_BUILD_ROOT%{_sysconfdir}/apt/rpmpriorities

(cd po;make install DESTDIR=$RPM_BUILD_ROOT)

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING* README* TODO
%doc docs/examples/configure-index
%doc docs/examples/vendors.list
%doc docs/examples/sources.list
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_libdir}/libapt-pkg.so.*
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%dir %{_sysconfdir}/apt
%config(noreplace) %{_sysconfdir}/apt/apt.conf 
%config(noreplace) %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/apt/vendors.list
%config %{_sysconfdir}/apt/rpmpriorities
%dir %{_localstatedir}/cache/apt
%dir %{_localstatedir}/cache/apt/archives       
%dir %{_localstatedir}/cache/apt/archives/partial
%dir %{_localstatedir}/state/apt
%dir %{_localstatedir}/state/apt/lists
%dir %{_localstatedir}/state/apt/lists/partial
%defattr(755,root,root)
%dir %{_libdir}/apt
%config %verify(not mode) %{_libdir}/apt/*
%attr(755,root,root) %{_bindir}/apt-get
%attr(755,root,root) %{_bindir}/apt-cache
%attr(755,root,root) %{_bindir}/apt-cdrom
%attr(755,root,root) %{_bindir}/apt-config
%attr(755,root,root) %{_bindir}/genpkglist
%attr(755,root,root) %{_bindir}/gensrclist
%attr(755,root,root) %{_bindir}/genbasedir

%files -n libapt-pkg-devel
%defattr(644,root,root,755)
%{_libdir}/libapt-pkg.so
%{_includedir}/apt-pkg

%files -n libapt-pkg-static
%defattr(644,root,root,755)
%{_libdir}/libapt-pkg.a
%doc docs/*.text.gz docs/*.html
