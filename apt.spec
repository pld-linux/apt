Summary:	Debian's Advanced Packaging Tool with RPM support
Summary(pl):	Zawansowane narzêdzie do zarz±dzania pakietami
Summary(pt):	Frontend avançado para pacotes rpm e deb
Name:		apt
Version:	0.3.19cnc55
Release:	1
License:	GPL
Group:		Applications/Archiving
Group(de):	Applikationen/Archivierung
Group(es):	Administración
Group(pl):	Aplikacje/Archiwizacja
Source0:	ftp://ftp.conectiva.com/pub/conectiva/EXPERIMENTAL/apt/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}-sources.list
Source3:	vendors.list
Source4:	rpmpriorities
Source5:	%{name}-pl-man-pages.tar.bz2
Patch0:		%{name}-norequires.patch
Patch1:		%{name}-FHS.patch
Patch2:		%{name}-no_PARALLEL_RUN.patch
Patch3:		%{name}-ac_fixes.patch
Patch4:		%{name}-newmethods.patch
Patch5:		%{name}-pld_man.patch
Patch6:		%{name}-man_fixes.patch
Patch7:		%{name}-mirrors.patch
URL:		http://bazar.conectiva.com.br/~godoy/apt-howto/
Requires:	gnupg
Obsoletes:	libapt-pkg
BuildRequires:	rpm-devel >= 3.0.6-2
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
BuildRequires:	db3-devel >= 3.1.17-3
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	popt-devel
BuildRequires:	autoconf
BuildRequires:	automake
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
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
Requires:	%{name} = %{version}
Requires:	rpm-devel
Obsoletes:	libapt-pkg-devel
Obsoletes:	libapt-pkg-static

%description devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%description -l es devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%description -l pl devel
Pakiet zawiera pliki nag³ówkowe potrzebne do tworzenia aplikacji
korzystaj±cych z biblioteki libapt-pkg.

%description -l pt_BR devel
Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT

%prep
%setup -q -a5
%patch0 -p1
tar xzf docs.tar.gz
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

mkdir docs/{pl,pt_BR}
rm -f po/{POTFILES,Makefile}

%build
aclocal -I buildlib
autoconf
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure \
	--enable-nls \
	--with-gpm
%{__make} CC="%{__cc}"  %{?__cxx:CXX=%{__cxx}}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/cache/apt/archives/partial \
	$RPM_BUILD_ROOT/var/lib/apt/lists/partial \
	$RPM_BUILD_ROOT{%{_includedir}/apt-pkg,%{_libdir}/apt} \
	$RPM_BUILD_ROOT{%{_mandir}/{,pl/,pt_BR/}man{5,8},%{_bindir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/apt

install bin/libapt-pkg.so.*.*.* $RPM_BUILD_ROOT%{_libdir}
cp -f bin/libapt-pkg.so $RPM_BUILD_ROOT%{_libdir}

install bin/{apt-{get,cache,config,cdrom},genpkglist,gensrclist} \
	tools/genbasedir $RPM_BUILD_ROOT%{_bindir}

install apt-pkg/{*.h,*/*.h} $RPM_BUILD_ROOT%{_includedir}/apt-pkg

for a in "" pl pt_BR ; do
	if ls doc/*.5 >/dev/null 2>&1 ; then
		install doc/*.5 $RPM_BUILD_ROOT/%{_mandir}/$a/man5
	fi
	install doc/*.8 $RPM_BUILD_ROOT/%{_mandir}/$a/man8
done

install  bin/methods/* $RPM_BUILD_ROOT%{_libdir}/apt

install %{SOURCE1}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf
install %{SOURCE3}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/vendors.list
install %{SOURCE4}	$RPM_BUILD_ROOT%{_sysconfdir}/apt/rpmpriorities
# bzip2 -dc %{SOURCE5} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

sed -e s/@ARCH@/%{_target_cpu}/ %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/apt/sources.list

cd po; make install DESTDIR=$RPM_BUILD_ROOT; cd ..

gzip -9fn docs/*.text docs/examples/* README.RPM TODO

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/*.gz docs/examples/*.gz *.gz
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/apt
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/apt/apt.conf 
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/apt/sources.list
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/apt/vendors.list
%config %{_sysconfdir}/apt/rpmpriorities
%dir %{_libdir}/apt
%attr(755,root,root) %{_libdir}/apt/*
%{_mandir}/man[58]/*
%lang(pl) %{_mandir}/pl/man8/*
%lang(pt) %{_mandir}/pt_BR/man[58]/*
/var/cache/apt
/var/lib/apt
%attr(755,root,root) %{_libdir}/libapt-pkg.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libapt-pkg.so
%{_includedir}/apt-pkg
