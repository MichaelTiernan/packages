Name:      atop
Version:   2.0.2
Release:   1%{?dist}
URL:       http://www.atoptool.nl
Summary:   Advanced System and Process Monitor
License:   GPL
Group:     System Environment

BuildRequires: ncurses-devel
BuildRequires: systemd

# Sources
Source0:   http://www.atoptool.nl/download/atop-2.0.2.tar.gz
Source1:   atopd.service

%description
The program atop is an interactive monitor to view the load on
a Linux-system. It shows the occupation of the most critical
hardware-resources (from a performance point of view) on system-level,
i.e. cpu, memory, disk and network. It also shows which processess
(and threads) are responsible for the indicated load (again cpu-,
memory-, disk- and network-load on process-level).
The program atop can also be used to log system- and process-level
information in raw format for long-term analysis.

The program atopsar can be used to view system-level statistics
as reports.

%prep
%setup -q

%build
make

%install
rm    -rf 			  $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/
install -Dp -m 04711 atop 	  $RPM_BUILD_ROOT/usr/bin/atop
ln -s atop                        $RPM_BUILD_ROOT/usr/bin/atopsar
install -Dp -m 0644 man/atop.1 	  $RPM_BUILD_ROOT/usr/share/man/man1/atop.1
install -Dp -m 0644 man/atopsar.1 $RPM_BUILD_ROOT/usr/share/man/man1/atopsar.1
install -Dp -m 0644 man/atoprc.5  $RPM_BUILD_ROOT/usr/share/man/man5/atoprc.5
install -Dp -m 0711 atop.daily	  $RPM_BUILD_ROOT/etc/atop/atop.daily
install -Dp -m 0711 45atoppm	  $RPM_BUILD_ROOT/etc/atop/45atoppm
install -Dp -m 0644 atop.cron 	  $RPM_BUILD_ROOT/etc/cron.d/atop
install -Dp -m 0644 psaccs_atop	  $RPM_BUILD_ROOT/etc/logrotate.d/psaccs_atop
install -Dp -m 0644 psaccu_atop	  $RPM_BUILD_ROOT/etc/logrotate.d/psaccu_atop
install -d  -m 0755 		  $RPM_BUILD_ROOT/var/log/atop

%clean
rm -rf    $RPM_BUILD_ROOT

%post
# Configure atop for systemd
/bin/systemctl daemon-reload >/dev/null 2>&1
/bin/systemctl enable atopd.service >/dev/null 2>&1
/bin/systemctl start atopd.service >/dev/null 2>&1

# save today's logfile (format might be incompatible)
mv /var/log/atop/atop_`date +%Y%m%d` /var/log/atop/atop_`date +%Y%m%d`.save \
					2> /dev/null || :
# create dummy files to be rotated
touch /var/log/atop/dummy_before /var/log/atop/dummy_after

# install Power Management for suspend/hibernate
if [ -d /usr/lib/pm-utils/sleep.d ]
then
	cp /etc/atop/45atoppm /usr/lib/pm-utils/sleep.d
fi

if [ -d /usr/lib64/pm-utils/sleep.d ]
then
	cp /etc/atop/45atoppm /usr/lib64/pm-utils/sleep.d
fi

# activate daily logging for today
/etc/atop/atop.daily

%preun
systemctl stop atopd.service

rm -f /usr/lib/pm-utils/sleep.d/45atoppm    2> /dev/null
rm -f /usr/lib64/pm-utils/sleep.d/45atoppm  2> /dev/null

# atop-2.0.2 and atopsar-2.0.2 will remain for old logfiles
cp -f  /usr/bin/atop 		/usr/bin/atop-2.0.2
ln -sf /usr/bin/atop-2.0.2 	/usr/bin/atopsar-2.0.2

%files
%defattr(-,root,root)
%doc README COPYING AUTHOR ChangeLog
/usr/bin/atop
/usr/bin/atopsar
/usr/share/man/man1/atop.1*
/usr/share/man/man1/atopsar.1*
/usr/share/man/man5/atoprc.5*
%{_unitdir}/atopd.service
/etc/atop/atop.daily
/etc/atop/45atoppm
/etc/cron.d/atop
/etc/logrotate.d/psaccs_atop
/etc/logrotate.d/psaccu_atop
%dir /var/log/atop/


%changelog
* Wed Aug 6 2014 Rob Mokkink <rob@mokkinksystems.com> 2.0.2-1
- Initial Rebuild for elrepo
- Added buildrequirement ncurses-devel
- Added buildrequirement systemd
- Added systemd service file atopd.service
