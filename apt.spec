# TODO:
# - use system lua
# NOTE: apt is currently not supported as PLD package manager;
#       apt 0.5.x was never supported because of too greedy Obsoletes handling
#
# Conditional build:
%bcond_without	python	# Python binding
#
Summary:	Debian's Advanced Packaging Tool with RPM support
Summary(pl.UTF-8):	Zaawansowane narzędzie do zarządzania pakietami
Summary(pt.UTF-8):	Frontend avançado para pacotes rpm e deb
Name:		apt
Version:	0.5.15lorg3.94a
Release:	0.1
License:	GPL v2+
Group:		Applications/Archiving
Source0:	http://apt-rpm.org/testing/%{name}-%{version}.tar.bz2
# Source0-md5:	c1f3702c0a91a31132c1019d559e2ae3
Source1:	%{name}.conf
Source2:	%{name}-sources.list
Source3:	vendors.list
Source4:	rpmpriorities
Source5:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-pl-man-pages.tar.bz2
# Source5-md5:	a3e9b7fd3dbf243d63cbfcc78cb20c1c
Patch0:		%{name}-rpm5.patch
Patch1:		%{name}-pld_man.patch
Patch2:		%{name}-man_fixes.patch
Patch3:		%{name}-includes.patch
Patch4:		%{name}-filed.patch
Patch5:		%{name}-pld_user_in_ftp_pass.patch
Patch6:		%{name}-format.patch
URL:		http://apt-rpm.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9.5
BuildRequires:	bzip2-devel
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils
BuildRequires:	gettext-tools >= 0.14.5
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= 5
BuildRequires:	sqlite3-devel
BuildRequires:	zlib-devel
%if %{with python}
BuildRequires:	python-devel >= 2
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
%endif
Requires:	gnupg
Requires:	libxml2 >= 1:2.6
Requires:	rpm
Obsoletes:	libapt-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A port of Debian's apt tools for RPM based distributions. It provides
the apt-get utility that provides a simpler, safer way to install and
upgrade packages. APT features complete installation ordering,
multiple source capability and several other unique features.

%description -l pl.UTF-8
Port debianowego narzędzia APT dla dystrybucji bazujących na zarządcy
pakietów RPM. APT dostarcza narzędzie apt-get, które umożliwia prostą,
bezpieczną instalację i aktualizację pakietów. Możliwości APT to wybór
kolejności instalacji, możliwość ustawienia kilku źródeł pakietów itp.

%description -l pt_BR.UTF-8
Um porte das ferramentas apt do Debian para distribuições baseadas no
RPM. Sob desenvolvimento, use por sua própria conta e risco.

%package devel
Summary:	Development files for APT's libapt-pkg
Summary(pl.UTF-8):	Pliki nagłówkowe dla libapt-pkg
Summary(pt.UTF-8):	Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	libxml2-devel >= 1:2.6
Requires:	rpm-devel >= 5
Obsoletes:	libapt-pkg-devel

%description devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%description devel -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe potrzebne do tworzenia aplikacji
korzystających z biblioteki libapt-pkg.

%description devel -l pt_BR.UTF-8
Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT

%package static
Summary:	Static libapt-pkg library
Summary(pl.UTF-8):	Statyczna biblioteka libapt-pkg
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	libapt-pkg-static

%description static
Static libapt-pkg library.

%description static -l pl.UTF-8
Statyczna biblioteka libapt-pkg.

%package -n python-apt
Summary:	Python bindings for libapt-pkg library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libapt-pkg
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-apt
Python bindings for libapt-pkg library.

%description -n python-apt -l pl.UTF-8
Wiązania Pythona do biblioteki libapt-pkg.

%prep
%setup -q -a5
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# swig rebuild doesn't work (plain swig cannot cope with class Class::SubClass { })
#%{__rm} python/{apt.py,apt_wrap.cxx}

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4 -I buildlib
%{__autoconf}
%{__autoheader}
%{__automake}
CXXFLAGS="%{rpmcxxflags} -fpermissive"
bash %configure

%{__make}

%if %{with python}
%{__make} -C python \
	CC="%{__cxx} %{rpmcxxflags} %{rpmcppflags}" \
	PYTHON="%{__python}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/cache/apt/archives/partial \
	$RPM_BUILD_ROOT/var/lib/apt/lists/partial \
	$RPM_BUILD_ROOT{%{_includedir}/apt-pkg,%{_libdir}/apt} \
	$RPM_BUILD_ROOT{%{_mandir}/{,pl/,pt_BR/}man{5,8},%{_bindir}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/apt,%{_datadir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
install -d $RPM_BUILD_ROOT%{py_sitedir}
install python/_apt.so $RPM_BUILD_ROOT%{py_sitedir}
cp -p python/apt.py $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

install doc/pl/*.8 $RPM_BUILD_ROOT%{_mandir}/pl/man8

%{__rm} $RPM_BUILD_ROOT%{_libdir}/apt/methods/bzip2
%{__rm} $RPM_BUILD_ROOT%{_libdir}/apt/methods/ssh
ln -sf gzip $RPM_BUILD_ROOT%{_libdir}/apt/methods/bzip2
ln -sf rsh $RPM_BUILD_ROOT%{_libdir}/apt/methods/ssh

install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf
install %{SOURCE3}	$RPM_BUILD_ROOT%{_sysconfdir}/apt/vendors.list
install %{SOURCE4}	$RPM_BUILD_ROOT%{_sysconfdir}/apt/rpmpriorities

sed -e s/@ARCH@/%{_target_cpu}/ %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/apt/sources.list

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{de_DE,de}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{es_ES,es}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{it_IT,it}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
# COPYING contains general notes; GPL text is in COPYING.GPL
%doc AUTHORS AUTHORS.RPM COPYING ChangeLog TODO doc/examples/*
%attr(755,root,root) %{_bindir}/apt-cache
%attr(755,root,root) %{_bindir}/apt-cdrom
%attr(755,root,root) %{_bindir}/apt-config
%attr(755,root,root) %{_bindir}/apt-get
%attr(755,root,root) %{_bindir}/apt-shell
%attr(755,root,root) %{_bindir}/countpkglist
%attr(755,root,root) %{_bindir}/genbasedir
%attr(755,root,root) %{_bindir}/genpkglist
%attr(755,root,root) %{_bindir}/gensrclist
%attr(755,root,root) %{_libdir}/libapt-pkg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libapt-pkg.so.3
%dir %{_libdir}/apt
%dir %{_libdir}/apt/methods
%attr(755,root,root) %{_libdir}/apt/methods/*
%dir %{_sysconfdir}/apt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apt/apt.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apt/sources.list
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apt/vendors.list
%config %{_sysconfdir}/apt/rpmpriorities
%dir %{_sysconfdir}/apt/apt.conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apt/apt.conf.d/multilib.conf
%{_mandir}/man5/apt.conf.5*
%{_mandir}/man5/apt_preferences.5*
%{_mandir}/man5/sources.list.5*
%{_mandir}/man5/vendors.list.5*
%{_mandir}/man8/apt.8*
%{_mandir}/man8/apt-cache.8*
%{_mandir}/man8/apt-cdrom.8*
%{_mandir}/man8/apt-config.8*
%{_mandir}/man8/apt-get.8*
%lang(pl) %{_mandir}/pl/man8/apt.8*
%lang(pl) %{_mandir}/pl/man8/apt-cache.8*
%lang(pl) %{_mandir}/pl/man8/apt-cdrom.8*
%lang(pl) %{_mandir}/pl/man8/apt-get.8*
/var/cache/apt
/var/lib/apt

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libapt-pkg.so
%{_libdir}/libapt-pkg.la
%{_includedir}/apt-pkg
%{_pkgconfigdir}/libapt-pkg.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libapt-pkg.a

%if %{with python}
%files -n python-apt
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_apt.so
%{py_sitedir}/apt.py[co]
%endif
