# TODO:
# - build python bindings
Summary:	Debian's Advanced Packaging Tool with RPM support
Summary(pl):	Zaawansowane narzêdzie do zarz±dzania pakietami
Summary(pt):	Frontend avançado para pacotes rpm e deb
Name:		apt
Version:	0.5.5cnc4.1
Release:	0.1
License:	GPL
Group:		Applications/Archiving
Source0:	http://moin.conectiva.com.br/files/AptRpm/attachments/%{name}-%{version}.tar.bz2
# Source0-md5:	cde405f21583ea6f8e012dc3d62412aa
Source1:	%{name}.conf
Source2:	%{name}-sources.list
Source3:	vendors.list
Source4:	rpmpriorities
Source5:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-pl-man-pages.tar.bz2
# Source5-md5:	a3e9b7fd3dbf243d63cbfcc78cb20c1c
Patch0:		%{name}-no_PARALLEL_RUN.patch
Patch1:		%{name}-ac_fixes.patch
Patch2:		%{name}-pld_man.patch
Patch3:		%{name}-man_fixes.patch
Patch5:		%{name}-es_it.patch
Patch6:		%{name}-filed.patch
Patch7:		%{name}-pld_user_in_ftp_pass.patch
Patch8:		%{name}-assert.patch
URL:		http://moin.conectiva.com.br/files/AptRpm/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
BuildRequires:	popt-devel
BuildRequires:	rpm-devel >= 3.0.6-2
BuildRequires:	zlib-devel
Requires:	gnupg
Requires:	rpm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	libapt-pkg

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
Requires:	%{name} = %{version}
Requires:	libstdc++-devel
Requires:	rpm-devel
Obsoletes:	libapt-pkg-devel
Obsoletes:	libapt-pkg-static

%description devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%description devel -l es
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
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
mv po/es_ES.po po/es.po
mv po/it_IT.po po/it.po
mv po/de_DE.po po/de.po

%{__aclocal} -I buildlib
#need patching
#autoheader
%{__autoconf}
CPPFLAGS="-Wno-deprecated"
CXXFLAGS="%{rpmcflags} -fno-exceptions"
%configure \
	--enable-nls \
	--with-gpm
%{__make} CC="%{__cc}"  CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/cache/apt/archives/partial \
	$RPM_BUILD_ROOT/var/lib/apt/lists/partial \
	$RPM_BUILD_ROOT{%{_includedir}/apt-pkg,%{_libdir}/apt} \
	$RPM_BUILD_ROOT{%{_mandir}/{,pl/,pt_BR/}man{5,8},%{_bindir}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/apt,%{_datadir}}


install bin/libapt*.so.*.*.* $RPM_BUILD_ROOT%{_libdir}
cp -df bin/libapt*.so $RPM_BUILD_ROOT%{_libdir}

install -m755 bin/apt-* bin/gen* bin/hd* \
	$RPM_BUILD_ROOT%{_bindir}
install -m755 tools/genbasedir $RPM_BUILD_ROOT%{_bindir}	

install apt-pkg/{*.h,*/*.h} $RPM_BUILD_ROOT%{_includedir}/apt-pkg

for a in "" pl ; do
	if ls doc/$a/*.5 >/dev/null 2>&1 ; then
		install -m644 doc/*.5 $RPM_BUILD_ROOT%{_mandir}/$a/man5
	fi
	install -m644 doc/$a/*.8 $RPM_BUILD_ROOT%{_mandir}/$a/man8
done

install  bin/methods/* $RPM_BUILD_ROOT%{_libdir}/apt
rm -f $RPM_BUILD_ROOT%{_libdir}/apt/bzip2
rm -f $RPM_BUILD_ROOT%{_libdir}/apt/ssh
ln -sf ./gzip $RPM_BUILD_ROOT%{_libdir}/apt/bzip2
ln -sf ./rsh $RPM_BUILD_ROOT%{_libdir}/apt/ssh

install %{SOURCE1}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf
install %{SOURCE3}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/vendors.list
install %{SOURCE4}	$RPM_BUILD_ROOT%{_sysconfdir}/apt/rpmpriorities

sed -e s/@ARCH@/%{_target_cpu}/ %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/apt/sources.list

cp -a locale $RPM_BUILD_ROOT%{_datadir}/

%find_lang %{name}
%find_lang libapt-pkg3.3
cat libapt-pkg3.3.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/examples/* TODO
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
/var/cache/apt
/var/lib/apt
%attr(755,root,root) %{_libdir}/libapt*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/libapt-pkg2_to_3.txt 
%{_libdir}/libapt*.so
%{_includedir}/apt-pkg
