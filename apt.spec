Summary:	Debian's Advanced Packaging Tool with RPM support
Summary(pl):	Zawansowane narz�dzie do zarz�dzania pakietami
Summary(pt):	Frontend avan�ado para pacotes rpm e deb
Name:		apt
Version:	0.5.4cnc4
Release:	0.1

License:	GPL
Group:		Applications/Archiving
Source0:	http://moin.conectiva.com.br/files/AptRpm/attachments/%{name}-%{version}.tar.bz2
Source1:	%{name}.conf
Source2:	%{name}-sources.list
Source3:	vendors.list
Source4:	rpmpriorities
Source5:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-pl-man-pages.tar.bz2
Patch0:		%{name}-norequires.patch
Patch1:		%{name}-FHS.patch
Patch2:		%{name}-no_PARALLEL_RUN.patch
Patch3:		%{name}-ac_fixes.patch
Patch5:		%{name}-pld_man.patch
Patch6:		%{name}-man_fixes.patch
Patch7:		%{name}-mirrors.patch
Patch8:		%{name}-es_it.patch
URL:		http://moin.conectiva.com.br/files/AptRpm/
Requires:	gnupg
Obsoletes:	libapt-pkg
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	db3-devel >= 3.1.17-3
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
BuildRequires:	popt-devel
BuildRequires:	rpm-devel >= 3.0.6-2
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A port of Debian's apt tools for RPM based distributions. It provides
the apt-get utility that provides a simpler, safer way to install and
upgrade packages. APT features complete installation ordering,
multiple source capability and several other unique features.

%description -l pl
Port debianowego narz�dzia APT dla dystrybucji bazuj�cych na zarz�dcy
pakiet�w RPM. APT dostarcza narz�dzie apt-get, kt�re umo�liwia prost�,
bezpieczn� instalacj� i aktualizacj� pakiet�w. Mo�liwo�ci APT to wyb�r
kolejno�ci instalacji, mo�liwo�� ustawienia kilku �r�de� pakiet�w itp.

%description -l pt_BR
Um porte das ferramentas apt do Debian para distribui��es baseadas no
RPM. Sob desenvolvimento, use por sua pr�pria conta e risco.

%package devel
Summary:	Development files for APT's libapt-pkg
Summary(pl):	Pliki nag��wkowe dla libapt-pkg
Summary(pt):	Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT
Group:		Development/Libraries
Requires:	%{name} = %{version}
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
Pakiet zawiera pliki nag��wkowe potrzebne do tworzenia aplikacji
korzystaj�cych z biblioteki libapt-pkg.

%description devel -l pt_BR
Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT

%prep
%setup -q -a5
#%patch0 -p1
# probably unneeded
#%patch1 -p1
%patch2 -p1
%patch3 -p1
# need review
#%patch5 -p1
# need review
#%patch6 -p1
%patch8 -p1 -b .wiget

%build
mv po/es_ES.po po/es.po
mv po/it_IT.po po/it.po

aclocal -I buildlib
#need patching
#autoheader
%{__autoconf}
CPPFLAGS="-Wno-deprecated"
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
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
	$RPM_BUILD_ROOT%{_sysconfdir}/apt

install bin/libapt*.so.*.*.* $RPM_BUILD_ROOT%{_libdir}
cp -f bin/libapt*.so $RPM_BUILD_ROOT%{_libdir}

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
ln -s ./gzip $RPM_BUILD_ROOT%{_libdir}/apt/bzip2
ln -s ./rsh $RPM_BUILD_ROOT%{_libdir}/apt/ssh

install %{SOURCE1}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf
install %{SOURCE3}   	$RPM_BUILD_ROOT%{_sysconfdir}/apt/vendors.list
install %{SOURCE4}	$RPM_BUILD_ROOT%{_sysconfdir}/apt/rpmpriorities
# bzip2 -dc %{SOURCE5} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

sed -e s/@ARCH@/%{_target_cpu}/ %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/apt/sources.list

cd po; make install DESTDIR=$RPM_BUILD_ROOT; cd ..


%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/examples/* README.RPM TODO
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
#%lang(pt) %{_mandir}/pt_BR/man[58]/*
/var/cache/apt
/var/lib/apt
%attr(755,root,root) %{_libdir}/libapt*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libapt*.so
%{_includedir}/apt-pkg
