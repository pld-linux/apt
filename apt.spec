Summary:	Debian's Advanced Packaging Tool with RPM support
Summary(es):	Advanced Packaging Tool frontend for rpm and dpkg
Summary(pl):	Zawansowane narz�dzie do zarz�dzania pakietami
Summary(pt_BR):	Frontend avan�ado para pacotes rpm e deb
Name:		apt
Version:	0.3.19cnc26
Release:	1
License:	GPL
Group:		Applications/Archiving
Group(de):	Applikationen/Archivierung
Group(es):	Administraci�n
Group(pl):	Aplikacje/Archiwizacja
Source0:	ftp://ftp.conectiva.com/pub/conectiva/EXPERIMENTAL/apt/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	sources.list
Source3:	vendors.list
URL:		http://bazar.conectiva.com.br/~godoy/apt-howto/
BuildRequires:	rpm-devel >= 3.0.6-2
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
BuildRequires:	db3-devel >= 3.1.17-3
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	popt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A port of Debian's apt tools for RPM based distributions. It provides
the apt-get utility that provides a simpler, safer way to install and
upgrade packages. APT features complete installation ordering,
multiple source capability and several other unique features.

%description -l pl
Port debianowego narz�dzia APT dla dystrybucji bazuj�cych na zarz�dcy
pakiet�w RPM. APT dostarcza narz�dzie apt-get, kt�re umo�liwia prost�
bezpieczn� instalacj� i aktualizacj� pakiet�w. Mo�liwo�ci APT to wyb�r
kolejno�ci instalacji, mo�liwo�� ustawienia kilku �r�de� pakiet�w itp.

%description -l pt_BR
Um porte das ferramentas apt do Debian para distribui��es baseadas no
RPM. Sob desenvolvimento, use por sua pr�pria conta e risco.

%package -n libapt-pkg
Summary:        libapt-pkg library
Summary(pl):    Biblioteka libapt-pkg
Group:          Libraries
Group(de):      Libraries
Group(fr):      Librairies
Group(pl):      Biblioteki

%description -n libapt-pkg
libapt-pkg library

%description -l pl -n libapt-pkg
Biblioteka libapt-pkg.

%package -n libapt-pkg-devel
Summary:	Development files for APT's libapt-pkg
Summary(es):	Development files for APT's libapt-pkg
Summary(pl):	Pliki nag��wkowe dla libapt-pkg
Summary(pt_BR):	Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT
Group:		Development
Group(de):	Entwicklung
Group(pl):	Programowanie
Group(pt_BR):	Desenvolvimento
Group(de):	Applikationen/Archivierung
Group(es):	Desarrollo
Group(pl):	Aplikacje/Archiwizacja
Requires:	%{name}-%{version}

%description -n libapt-pkg-devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%description -l es -n libapt-pkg-devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%description -l pl -n libapt-pkg-devel
Pakiet zawiera pliki nag��wkowe potrzebne do tworzenia aplikacji
korzystaj�cych z biblioteki libapt-pkg.

%description -l pt_BR -n libapt-pkg-devel
Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT

%prep
%setup -q
tar xzf docs.tar.gz

%build
%configure \
	--enable-nls \
	--with-gpm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/cache/apt/archives/partial \
	$RPM_BUILD_ROOT/var/state/apt/lists/partial \
	$RPM_BUILD_ROOT{%{_includedir}/apt-pkg,%{_libdir}/apt,%{_mandir}/man{5,8},%{_bindir}} \
	$RPM_BUILD_ROOT/etc/apt

install bin/libapt-pkg.so* $RPM_BUILD_ROOT%{_libdir}

install bin/{apt-{get,cache,config,cdrom},genpkglist,gensrclist} \
	tools/genbasedir $RPM_BUILD_ROOT%{_bindir}

install apt-pkg/{*.h,*/*.h} $RPM_BUILD_ROOT%{_includedir}/apt-pkg

install doc/*.5 $RPM_BUILD_ROOT/%{_mandir}/man5
install doc/*.8 $RPM_BUILD_ROOT/%{_mandir}/man8

install  bin/methods/* $RPM_BUILD_ROOT%{_libdir}/apt

install %{SOURCE1}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf
install %{SOURCE2}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/sources.list
install %{SOURCE3}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/vendors.list
install rpmpriorities	$RPM_BUILD_ROOT%{_sysconfdir}/apt/rpmpriorities

cd po; make install DESTDIR=$RPM_BUILD_ROOT; cd ..

gzip -9fn docs/*.text docs/examples/* README.RPM TODO

%find_lang %{name}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/*.gz docs/examples/*.gz *.gz
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/apt
%config(noreplace) %{_sysconfdir}/apt/apt.conf 
%config(noreplace) %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/apt/vendors.list
%config %{_sysconfdir}/apt/rpmpriorities
%dir %{_libdir}/apt
%config %verify(not mode) %{_libdir}/apt/*
%{_mandir}/man[58]/*
/var/cache/apt
/var/state/apt

%files -n libapt-pkg
%defattr(644,root,root,755)
%{_libdir}/libapt-pkg.so.*.*

%files -n libapt-pkg-devel
%defattr(644,root,root,755)
%{_libdir}/libapt-pkg.so
%{_includedir}/apt-pkg
