Name: apt
Version: 0.3.19cnc21
Release: 1cl
Summary: Debian's Advanced Packaging Tool with RPM support
Summary(pt_BR): Frontend avançado para pacotes rpm e deb
Summary(es): Advanced Packaging Tool frontend for rpm and dpkg
Group: Administration
Group(pt_BR): Administração
Group(es): Administración
License: GPL
Source0: ftp://ftp.conectiva.com/pub/conectiva/.0/EXPERIMENTAL/apt/%{name}-%{version}.tar.gz
Source1: %{name}.conf
Source2: sources.list
Source3: vendors.list
Requires: rpm >= 3.0.5
BuildPreReq: rpm-devel >= 3.0.5
BuildRequires: db1-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
A port of Debian's apt tools for RPM based distributions,
or at least for Conectiva. It provides the apt-get utility that
provides a simpler, safer way to install and upgrade packages.
APT features complete installation ordering, multiple source
capability and several other unique features.

Under development, use at your own risk!

%description -l pt_BR
Um porte das ferramentas apt do Debian para distribuições
baseadas no RPM. Ou pelo menos para o Conectiva.
Sob desenvolvimento, use por sua própria conta e risco.

%description -l es
A port of Debian's apt tools for RPM based distributions.
Or at least for Conectiva. 
Under development, use at your own risk!!!

%package -n libapt-pkg-devel
Summary: Development files for APT's libapt-pkg
Summary(pt_BR): Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT
Summary(es): Development files for APT's libapt-pkg
Group: Development
Group(pt_BR): Desenvolvimento
Group(es): Desarrollo
Requires: apt

%description -n libapt-pkg-devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

Under development, use at your own risk!

%description -l pt_BR -n libapt-pkg-devel
Arquivos de desenvolvimento para a biblioteca libapt-pkg do APT

%description -l es -n libapt-pkg-devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

Under development, use at your own risk!

%package -n libapt-pkg-doc
Summary: Documentation for APT development
Summary(pt_BR): Documentação para o APT (desenvolvimento)
Summary(es): Documentation for APT development
Group: Documentation
Group(pt_BR): Documentação
Group(es): Documentación

%description -n libapt-pkg-doc
This package contains documentation for development of the APT
package manipulation program and its libraries.

%description -l pt_BR -n libapt-pkg-doc
Documentação para quem deseja desenvolver com o APT e suas
bibliotecas.

%description -l es -n libapt-pkg-doc
This package contains documentation for development of the APT
package manipulation program and its libraries.

%prep
%setup -q

%build
%configure
make
tar xzf docs.tar.gz
gzip docs/*.text

%install
rm -fr %{buildroot}
mkdir -p %{buildroot}%{_localstatedir}/cache/%{name}/archives/partial
mkdir -p %{buildroot}%{_localstatedir}/state/%{name}/lists/partial

mkdir -p %{buildroot}%{_libdir}/
cp -a bin/libapt-pkg.so.* %{buildroot}%{_libdir}/
cp -a bin/libapt-pkg.so %{buildroot}%{_libdir}/

install -D bin/apt-get %{buildroot}%{_bindir}/apt-get
install -D bin/apt-cache %{buildroot}%{_bindir}/apt-cache
install -D bin/apt-config %{buildroot}%{_bindir}/apt-config
install -D bin/apt-cdrom %{buildroot}%{_bindir}/apt-cdrom
install -D bin/genpkglist %{buildroot}%{_bindir}/genpkglist
install -D bin/gensrclist %{buildroot}%{_bindir}/gensrclist
install -D tools/genbasedir %{buildroot}%{_bindir}/genbasedir

mkdir -p %{buildroot}%{_includedir}/apt-pkg/
install -D apt-pkg/*.h %{buildroot}%{_includedir}/apt-pkg/
install -D apt-pkg/*/*.h %{buildroot}%{_includedir}/apt-pkg/

mkdir -p %{buildroot}/%{_mandir}/man5/
mkdir -p %{buildroot}/%{_mandir}/man8/
install -D doc/apt.conf.5 %{buildroot}/%{_mandir}/man5/apt.conf.5
install -D doc/sources.list.5 %{buildroot}/%{_mandir}/man5/sources.list.5
install -D doc/vendors.list.5 %{buildroot}/%{_mandir}/man5/vendors.list.5
install -D doc/apt-cache.8 %{buildroot}/%{_mandir}/man8/apt-cache.8
install -D doc/apt-config.8 %{buildroot}/%{_mandir}/man8/apt-config.8
install -D doc/apt.8 %{buildroot}/%{_mandir}/man8/apt.8
install -D doc/apt-cdrom.8 %{buildroot}/%{_mandir}/man8/apt-cdrom.8
install -D doc/apt-get.8 %{buildroot}/%{_mandir}/man8/apt-get.8
install -D doc/apt-get.8 %{buildroot}/%{_mandir}/man8/apt-get.8

mkdir -p %{buildroot}%{_libdir}/apt
install  bin/methods/* %{buildroot}%{_libdir}/apt

install -D %{SOURCE1}    %{buildroot}%{_sysconfdir}/apt/apt.conf
install -D %{SOURCE2}    %{buildroot}%{_sysconfdir}/apt/sources.list
install -D %{SOURCE3}    %{buildroot}%{_sysconfdir}/apt/vendors.list
install -D rpmpriorities %{buildroot}%{_sysconfdir}/apt/rpmpriorities

(cd po;make install DESTDIR=%{buildroot})

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,755)
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
%{_bindir}/apt-get
%{_bindir}/apt-cache
%{_bindir}/apt-cdrom
%{_bindir}/apt-config
%{_bindir}/genpkglist
%{_bindir}/gensrclist
%{_bindir}/genbasedir

%files -n libapt-pkg-devel
%defattr(0644,root,root,755)
%{_libdir}/libapt-pkg.so
%{_includedir}/apt-pkg

%files -n libapt-pkg-doc
%defattr(0644,root,root,755)
%doc docs/*.text.gz docs/*.html

%changelog
* Mon Oct 30 2000 Alfredo K. Kojima <kojima@conectiva.com.br>
- released version 0.3.19cnc21

* Sun Oct 29 2000 Alfredo K. Kojima <kojima@conectiva.com.br>
- released version 0.3.19cnc20

* Sun Oct 29 2000 Alfredo K. Kojima <kojima@conectiva.com.br>
- released version 0.3.19cnc19
- added gensrclist
- support for apt-get source

* Fri Oct 27 2000 Alfredo K. Kojima <kojima@conectiva.com.br>
- released version 0.3.19cnc18

* Thu Oct 26 2000 Alfredo K. Kojima <kojima@conectiva.com.br>
- released version 0.3.19cnc17
- new manpages

* Wed Oct 25 2000 Alfredo K. Kojima <kojima@conectiva.com.br>
- released version 0.3.19cnc16

* Sun Oct 22 2000 Alfredo K. Kojima <kojima@conectiva.com.br>
- released version 0.3.19cnc15

* Sat Oct 21 2000 Alfredo K. Kojima <kojima@conectiva.com.br>
- released version 0.3.19cnc14

* Thu Oct 19 2000 Claudio Matsuoka <claudio@conectiva.com>
- new upstream release: 0.3.9cnc13

* Tue Oct 17 2000 Eliphas Levy Theodoro <eliphas@conectiva.com>
- added rpmpriorities to filelist and install

* Tue Oct 17 2000 Claudio Matsuoka <claudio@conectiva.com>
- updated to 0.3.19cnc12
- fresh CVS snapshot including: support to Acquire::ComprExtension,
  debug messages removed, fixed apt-cdrom, RPM DB path, rpmlib call
  in pkgRpmLock::Close(), package priority kludge removed, i18n
  improvements, and genbasedir/genpkglist updates.
- handling language setting in genpkglist to make aptitude happy

* Wed Oct 11 2000 Alfredo K. Kojima <kojima@conectiva.com>
- released version 0.3.19cnc11
- fixed problem with shard lib symlinks

* Tue Oct 10 2000 Alfredo K. Kojima <kojima@conectiva.com>
- released version 0.3.19cnc10

* Mon Oct  2 2000 Claudio Matsuoka <claudio@conectiva.com>
- fixed brown paper bag bug with method permissions
- added parameter --sign to genbasedir
- added html/text doc files

* Sat Sep 30 2000 Claudio Matsuoka <claudio@conectiva.com>
- bumped to 0.3.19cnc9
- added vendors.list
- added gpg method
- fixed minor stuff to make Aptitude work
- added missing manpages
- fixed shared libs
- split in apt, libapt-pkg, libapt-pkg-devel, libapt-pkg-doc
- rewrote genbasedir in shell script (original was in TCL)
- misc cosmetic changes

* Tue Sep 26 2000 Alfredo K. Kojima <kojima@conectiva.com>
- released version 0.3.19cnc8

* Wed Sep 20 2000 Alfredo K. Kojima <kojima@conectiva.com>
- released version 0.3.19cnc7

* Mon Sep 18 2000 Alfredo K. Kojima <kojima@conectiva.com>
- released version 0.3.19cnc6

* Sat Sep 16 2000 Alfredo K. Kojima <kojima@conectiva.com>
- released version 0.3.19cnc5

* Fri Sep 15 2000 Alfredo K. Kojima <kojima@conectiva.com>
- released version 0.3.19cnc4

* Mon Sep 12 2000 Alfredo K. Kojima <kojima@conectiva.com>
- released version 0.3.19cnc3

* Mon Sep 5 2000 Alfredo K. Kojima <kojima@conectiva.com>
- renamed package to apt, with version 0.3.19cncV

* Mon Sep 5 2000 Alfredo K. Kojima <kojima@conectiva.com>
- 0.10
- added genpkglist and rapt-config
- program names changed back to apt-*

* Mon Sep 4 2000 Alfredo K. Kojima <kojima@conectiva.com>
- 0.9

* Mon Sep 4 2000 Alfredo K. Kojima <kojima@conectiva.com>
- 0.8

* Mon Sep 4 2000 Alfredo K. Kojima <kojima@conectiva.com>
- 0.7

* Fri Sep 1 2000 Alfredo K. Kojima <kojima@conectiva.com>
- fixed typo in sources.list

* Tue Aug 31 2000 Alfredo K. Kojima <kojima@conectiva.com>
- version 0.6

* Tue Aug 31 2000 Alfredo K. Kojima <kojima@conectiva.com>
- version 0.5

* Tue Aug 31 2000 Alfredo K. Kojima <kojima@conectiva.com>
- version 0.4

* Wed Aug 30 2000 Alfredo K. Kojima <kojima@conectiva.com>
- version 0.3

* Thu Aug 28 2000 Alfredo K. Kojima <kojima@conectiva.com>
- second try. new release with direct hdlist handling

* Thu Aug 10 2000 Alfredo K. Kojima <kojima@conectiva.com>
- initial package creation. Yeah, it's totally broken for sure.
