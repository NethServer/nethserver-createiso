Name:           nethserver-createiso
Version:        0.0.1
Release:        1%{?dist}
Summary:        Create NethServer ISO file
BuildArch:	noarch

License:        GPLv3
URL:            http://www.nethserver.org
Source0:        https://github.com/nethesis/nethserver-createiso/%{version}/%{name}-%{version}.tar.gz

Requires: mock => 1.2.3
Requires: fuse
Requires: fuse-iso
Requires: genisoimage
Requires: intltool
Requires: isomd5sum
Requires: mock
Requires: syslinux
Requires: tar
Requires: yum-plugin-downloadonly


%description
Create NethServer ISO file starting from CentOS minimal ISO

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -vp  %{buildroot}/%{_bindir} %{buildroot}/%{_sysconfdir}/mock %{buildroot}/%{_datadir}/%{name}
install -vp src/bin/createiso %{buildroot}/%{_bindir}
install -vp src/mock/nethserver-iso-6.6-x86_64.cfg %{buildroot}/%{_sysconfdir}/mock
install -vp src/mock/nethserver-enterprise-iso-6.6-x86_64.cfg %{buildroot}/%{_sysconfdir}/mock
install -vp src/lib/isolinux.cfg %{buildroot}/%{_datadir}/%{name}
install -vp src/lib/RPM-GPG-KEY-NethServer-6 %{buildroot}/%{_datadir}/%{name}

LIB_FILES="
nethserver-enterprise/splash.png
nethserver-enterprise/splash.jpg
nethserver-enterprise/brand_packages
nethserver-enterprise/mock_config
nethserver/splash3.xcf
nethserver/splash.xcf
nethserver/splash4.xcf
nethserver/splash.xpm.gz
nethserver/convert.sh
nethserver/splash.png
nethserver/splash2.xcf
nethserver/splash.jpg
nethserver/mock_config
ks/ks-crypted.cfg
ks/start.ks
ks/ks-unattended.cfg
ks/end.ks
ks/installer
"

for F in $LIB_FILES; do
    DESTDIR="%{buildroot}/%{_datadir}/%{name}/$(dirname $F)" 
    if ! test -d $DESTDIR; then
      echo '%%dir' %{_datadir}/%{name}/$(dirname $F) >> filelist-%{name}-%{version}
      mkdir -vp $DESTDIR;
    fi
    echo %{_datadir}/%{name}/$F >> filelist-%{name}-%{version}
    install -vp src/lib/$F %{buildroot}/%{_datadir}/%{name}/$F
done

%files -f filelist-%{name}-%{version}
%defattr(-,root,root,-)
%{_bindir}/createiso
%{_datadir}/%{name}/isolinux.cfg
%{_datadir}/%{name}/RPM-GPG-KEY-NethServer-6
%config(noreplace) %{_sysconfdir}/mock/nethserver-iso-6.6-x86_64.cfg
%config(noreplace) %{_sysconfdir}/mock/nethserver-enterprise-iso-6.6-x86_64.cfg
%doc COPYING

%changelog
* Mon Jan 19 2015 Davide Principi <davide.principi@nethesis.it> - 0.0.1-1
- Initial version

