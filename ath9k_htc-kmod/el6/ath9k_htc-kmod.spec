# Define the kmod package name here.
%define kmod_name ath9k_htc

# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 2.6.32-358.el6.%{_target_cpu}}

Name:    %{kmod_name}-kmod
Version: 0.0
Release: 4%{?dist}
Group:   System Environment/Kernel
License: GPLv2
Summary: %{kmod_name} kernel module(s)
URL:     http://www.kernel.org/

BuildRequires: redhat-rpm-config
ExclusiveArch: i686 x86_64

# Sources.
# The source tarball comes from the RHEL6_4 kernel-2.6.32-358.14.1.el6
# drivers/net/wireless/ath
Source0:  ath.tar.bz2
Source1:  ath9k_htc-Makefile
Source5:  GPL-v2.0.txt
Source10: kmodtool-%{kmod_name}-el6.sh

# Patches.
Patch1:	ath9k_htc_rhel6_4.patch

# Magic hidden here.
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
This package provides the %{kmod_name} kernel module(s).
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -n ath
patch -p2 < %{PATCH1}
%{__rm} -f ath9k/Makefile
%{__cp} -a %{SOURCE1} ath9k/Makefile
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
KSRC=%{_usrsrc}/kernels/%{kversion}
pushd ath9k
%{__make} -C "${KSRC}" %{?_smp_mflags} modules M=$PWD
popd

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}
pushd ath9k
KSRC=%{_usrsrc}/kernels/%{kversion}
%{__make} -C "${KSRC}" modules_install M=$PWD
popd
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} %{SOURCE5} %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;
# Remove the unrequired files.
%{__rm} -f %{buildroot}/lib/modules/%{kversion}/modules.*

%clean
%{__rm} -rf %{buildroot}

%changelog
* Mon Aug 05 2013 Philip J Perry <phil@elrepo.org> - 0.0-4
- Rebase driver to RHEL6_4 kernel-2.6.32-358.14.1.el6 source code.

* Tue Apr 23 2013 Alan Bartlett <ajb@elrepo.org> - 20130307-2
- Adjusted to the ELRepo Project standards.

* Fri Apr 19 2013 Gary Benson <gbenson@redhat.com> - 20130307-1
- Repackaged for ath9k_htc.

* Mon Mar 11 2013 Paul Hampson <Paul.Hampson@Pobox.com> - 0.0-3
- Update to compat-drivers release 2013-03-07-u with EL6-specific patches.
  [http://elrepo.org/bugs/view.php?id=361]

* Sat Dec 22 2012 Philip J Perry <phil@elrepo.org> - 0.0-2
- Add missing modules
  [http://elrepo.org/bugs/view.php?id=306]

* Mon Oct 15 2012 Philip J Perry <phil@elrepo.org> - 0.0-1
- Initial el6 build of the kmod package from nightly snapshot 2012-10-03-pc.
  [http://elrepo.org/bugs/view.php?id=306]
