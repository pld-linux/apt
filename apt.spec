# TODO:
# - build python bindings
# - use system lua
Summary:	Debian's Advanced Packaging Tool with RPM support
Summary(pl):	Zaawansowane narzêdzie do zarz±dzania pakietami
Summary(pt):	Frontend avançado para pacotes rpm e deb
Name:		apt
Version:	0.5.15cnc7
Release:	5
License:	GPL
Group:		Applications/Archiving
#Source0:	https://moin.conectiva.com.br/AptRpm?action=AttachFile&do=get&target=apt-0.5.15cnc7.tar.bz2
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	9e44ec1503fa96832bbd9b532543e4de
Source1:	%{name}.conf
Source2:	%{name}-sources.list
Source3:	vendors.list
Source4:	rpmpriorities
Source5:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-pl-man-pages.tar.bz2
# Source5-md5:	a3e9b7fd3dbf243d63cbfcc78cb20c1c
Patch0:		%{name}-ac_fixes.patch
Patch1:		%{name}-pld_man.patch
Patch2:		%{name}-man_fixes.patch
Patch3:		%{name}-es_it.patch
Patch4:		%{name}-filed.patch
Patch5:		%{name}-pld_user_in_ftp_pass.patch
# do not add slash in URL
URL:		http://moin.conectiva.com.br/AptRpm
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	rpm-devel >= 4.4.1
Requires:	gnupg
Requires:	rpm
Obsoletes:	libapt-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A port of Debian's apt tools for RPM based distributions. It provides
the apt-get utility that provides a simpler, safer way to install and
upgrade packages. APT features complete installation ordering,
multiple source capability and several other unique features.

%description -l pl
Port debianowego narzêdzia APT dla dystrybucji bazuj±cych na zarz±dcy
pakietów RPM. APT dostarcza narzêdzie apt-get, które umo¿liwia prost±,
bezpieczn± instalacjê i aktualizacjê pakietów. Mo¿liwo¶ci APT to wybór
kolejno¶ci instalacji, mo¿liwo¶æ ustawienia kilku ¼róde³ pakietów itp.

%description -l pt_BR
Um porte das ferramentas apt do Debian para distribuições baseadas no
RPM. Sob desenvolvimento, use por sua própria conta e risco.

%package devel
Summary:	Development files for APT's libapt-pkg
Summary(pl):	Pliki nag³ówkowe dla libapt-pkg
Summary(pt):	Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	rpm-devel
Obsoletes:	libapt-pkg-devel
Obsoletes:	libapt-pkg-static

%description devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%description devel -l pl
Pakiet zawiera pliki nag³ówkowe potrzebne do tworzenia aplikacji
korzystaj±cych z biblioteki libapt-pkg.

%description devel -l pt_BR
Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT

%prep
%setup -q -a5
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

mv po/es_ES.po po/es.po
mv po/it_IT.po po/it.po
mv po/de_DE.po po/de.po

%build
%{__libtoolize}
%{__gettextize}
%{__aclocal} -I buildlib
#need patching
#autoheader
%{__autoconf}
CPPFLAGS="-Wno-deprecated"
CXXFLAGS="%{rpmcflags} -fno-exceptions"
%configure \
	--enable-nls \
	--with-gpm
%{__make} CC="%{__cc}" CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/cache/apt/archives/partial \
	$RPM_BUILD_ROOT/var/lib/apt/lists/partial \
	$RPM_BUILD_ROOT{%{_includedir}/apt-pkg,%{_libdir}/apt} \
	$RPM_BUILD_ROOT{%{_mandir}/{,pl/,pt_BR/}man{5,8},%{_bindir}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/apt,%{_datadir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/pl/*.8 $RPM_BUILD_ROOT%{_mandir}/pl/man8

rm -f $RPM_BUILD_ROOT%{_libdir}/apt/methods/bzip2
rm -f $RPM_BUILD_ROOT%{_libdir}/apt/methods/ssh
ln -sf ./gzip $RPM_BUILD_ROOT%{_libdir}/apt/methods/bzip2
ln -sf ./rsh $RPM_BUILD_ROOT%{_libdir}/apt/methods/ssh

install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf
install %{SOURCE3}	$RPM_BUILD_ROOT%{_sysconfdir}/apt/vendors.list
install %{SOURCE4}	$RPM_BUILD_ROOT%{_sysconfdir}/apt/rpmpriorities

sed -e s/@ARCH@/%{_target_cpu}/ %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/apt/sources.list

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/examples/* TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/apt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apt/apt.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apt/sources.list
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apt/vendors.list
%config %{_sysconfdir}/apt/rpmpriorities
%dir %{_libdir}/apt
%attr(755,root,root) %{_libdir}/apt/*
%{_mandir}/man[58]/*
%lang(pl) %{_mandir}/pl/man8/*
/var/cache/apt
/var/lib/apt
%attr(755,root,root) %{_libdir}/libapt*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libapt*.so
%{_libdir}/libapt*.a
%{_libdir}/libapt*.la
%{_includedir}/apt-pkg
