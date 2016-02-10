Name:           nethserver-createiso
Version: 1.2.0
Release: 1%{?dist}
Summary:        Create NethServer ISO file
BuildArch:	noarch

License:        GPLv3
URL:            http://www.nethserver.org
Source0:        %{name}-%{version}.tar.gz

Requires: mock => 1.2.3
Requires: fuseiso
Requires: genisoimage
Requires: intltool
Requires: isomd5sum
Requires: syslinux
Requires: tar
Requires: createrepo
Requires: yum-plugin-downloadonly


%description
Create NethServer ISO file starting from CentOS minimal ISO

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -vp  %{buildroot}/%{_bindir} %{buildroot}/%{_sysconfdir}/mock %{buildroot}/%{_datadir}/%{name}
install -m 0755 -vp src/bin/createiso %{buildroot}/%{_bindir}
install -m 0644 -vp src/mock/nethserver-iso-7-x86_64.cfg %{buildroot}/%{_sysconfdir}/mock
install -m 0644 -vp src/lib/isolinux.cfg %{buildroot}/%{_datadir}/%{name}
install -m 0644 -vp src/lib/RPM-GPG-KEY-NethServer-7 %{buildroot}/%{_datadir}/%{name}

LIB_FILES="
nethserver-enterprise/splash.png
nethserver-enterprise/splash.jpg
nethserver-enterprise/config
nethserver/splash.xcf
nethserver/splash.xpm.gz
nethserver/convert.sh
nethserver/splash.png
nethserver/splash.jpg
nethserver/config
ks/ks-unattended.cfg
"

for F in $LIB_FILES; do
    DESTDIR="%{buildroot}/%{_datadir}/%{name}/$(dirname $F)" 
    if ! test -d $DESTDIR; then
      echo '%%dir' %{_datadir}/%{name}/$(dirname $F) >> filelist-%{name}-%{version}
      mkdir -vp $DESTDIR;
    fi
    echo %{_datadir}/%{name}/$F >> filelist-%{name}-%{version}
    install -m 0644 -vp src/lib/$F %{buildroot}/%{_datadir}/%{name}/$F
done

%files -f filelist-%{name}-%{version}
%defattr(-,root,root,-)
%{_bindir}/createiso
%{_datadir}/%{name}/isolinux.cfg
%{_datadir}/%{name}/RPM-GPG-KEY-NethServer-7
%config(noreplace) %{_sysconfdir}/mock/nethserver-iso-7-x86_64.cfg
%config %{_datadir}/%{name}/nethserver/config
%config %{_datadir}/%{name}/nethserver-enterprise/config
%doc COPYING

%changelog
* Wed Aug 26 2015 Davide Principi <davide.principi@nethesis.it> - 1.2.0-1
- Mock configuration for NethServer 6.7 ISO - Enhancement #3245 [NethServer]

* Wed Mar 18 2015 Davide Principi <davide.principi@nethesis.it> - 1.1.1-1
- Install dependencies from nethesis-updates.
- Print out extra RPMs list and additional disk size.
- Fix missing yum-plugin-downloadonly dependency in final systems.

* Tue Mar 17 2015 Davide Principi <davide.principi@nethesis.it> - 1.1.0-1
- Honour nethserver-iso group definition from YUM repositories.
- Removed old splash screen files.

* Thu Mar 05 2015 Davide Principi <davide.principi@nethesis.it> - 1.0.1-1
- Put YUM groups from nethserver-updates into ISO

* Thu Mar 05 2015 Davide Principi <davide.principi@nethesis.it> - 1.0.0-1
- Interactive installer: show ethernet mac addresses - Enhancement #3047 [NethServer]
- nethserver-devbox replacements - Feature #3009 [NethServer]
- YUM groups read from nethserver-updates
- Changed repositories URLs to mirrorlist.nethserver.org

* Tue Mar  3 2015 Davide Principi <davide.principi@nethesis.it> - 0.0.2-3
- Added Requires: createrepo

* Tue Jan 27 2015 Davide Principi <davide.principi@nethesis.it> - 0.0.2-1
- Use YUM mirrorlist plugin

* Mon Jan 19 2015 Davide Principi <davide.principi@nethesis.it> - 0.0.1-1
- Initial version


