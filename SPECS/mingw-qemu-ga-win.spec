%{?mingw_package_header}

%define with_vss 1
%define qemu_version 10.0.0
%define ga_manufacturer "RedHat"
%define ga_distro "RHEL"

Name: mingw-qemu-ga-win
Version: 110.0.2
Release: 1%{?dist}
Summary: Qemus Guest agent for Windows

Group: System Environment/Daemons
License: Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND FSFAP AND GPL-1.0-or-later AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-2.0-or-later WITH GCC-exception-2.0 AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND MIT AND LicenseRef-Fedora-Public-Domain AND CC-BY-3.0
URL: http://www.qemu.org/
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Source0: https://gitlab.com/qemu-project/qemu/-/archive/v%{qemu_version}/qemu-v%{qemu_version}.tar.bz2

Patch0001: 0001-Change-Version.patch
Patch0002: v2_20250324_kkostiuk_qga_add_guest_get_load_command.mbx
Patch0003: v2_20250618_eashurov_qga_vss_win32_add_vss_provider_unregistration_retry.mbx
Patch0004: 20250620_kkostiuk_qga_vss_exit_with_non_zero_code_when_register_fail.mbx
Patch0005: 2025_07_17_kkostiuk_util_win32_write_hex_value_when_can_t_get_error_message.patch
Patch0006: 0002-qga-win-Add-additional-VSS-logs.patch
Patch0007: 0001-Revert-qga-Don-t-daemonize-before-channel-is-initial.patch

BuildArch: noarch
# RHEL-57753 - mingw-qemu-ga-win failed to build on s390x
ExclusiveArch: x86_64

Provides: bundled(mingw-gcc)
Provides: bundled(mingw-gcc-c++)
Provides: bundled(mingw-gettext)
Provides: bundled(mingw-glib2)
Provides: bundled(mingw-pcre)
Provides: qemu-ga-win = %{version}
Obsoletes: qemu-ga-win < 105.0.0
# based on https://gitlab.com/qemu-project/qemu/-/blob/v7.1.0/qga/installer/qemu-ga.wxs

BuildRequires: libtool
BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: python3-devel
BuildRequires: gettext
BuildRequires: gettext-devel
BuildRequires: mingw32-gcc >= 7.4.0
BuildRequires: mingw32-gcc-c++ >= 7.4.0
BuildRequires: mingw64-gcc >= 7.4.0
BuildRequires: mingw64-gcc-c++ >= 7.4.0
BuildRequires: mingw32-glib2 >= 2.78.0
BuildRequires: mingw64-glib2 >= 2.78.0
BuildRequires: mingw64-headers >= 10.0.0
BuildRequires: mingw32-headers >= 10.0.0
BuildRequires: mingw-w64-tools >= 10.0.0
BuildRequires: msitools >= 0.93.93
BuildRequires: meson
BuildRequires: ninja-build

%description
Qemu Guest Agent for Windows.

qemu-kvm is an open source virtualizer that provides hardware emulation for
the KVM hypervisor.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%prep
%setup -q -n qemu-v%{qemu_version}
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1

%build

rm -rf $RPM_BUILD_ROOT

export QEMU_GA_MANUFACTURER="%{ga_manufacturer}"
export QEMU_GA_DISTRO="%{ga_distro}"
export QEMU_GA_VERSION="%{version}"

#Build for Win32
%{mingw32_env}
./configure \
   --disable-docs \
   --disable-system \
   --disable-user \
   --cross-prefix=i686-w64-mingw32- \
   --enable-guest-agent \
   --enable-guest-agent-msi \
%if %{with_vss}
   --enable-qga-vss \
%endif
   || cat %{_builddir}/qemu-%{qemu_version}/build/config.log

make -j$(nproc) qemu-ga

mkdir -p $RPM_BUILD_ROOT%{mingw32_bindir}
#cp build/qga/qemu-ga.exe $RPM_BUILD_ROOT%{mingw32_bindir}
cp build/qga/qemu-ga-i386.msi $RPM_BUILD_ROOT%{mingw32_bindir}

#Build for Win64
%{mingw64_env}
./configure \
   --disable-docs \
   --disable-system \
   --disable-user \
   --cross-prefix=x86_64-w64-mingw32- \
   --enable-guest-agent \
   --enable-guest-agent-msi \
%if %{with_vss}
   --enable-qga-vss \
%endif
   || cat %{_builddir}/qemu-%{qemu_version}/build/config.log

make -j$(nproc) qemu-ga

mkdir -p $RPM_BUILD_ROOT%{mingw64_bindir}
# cp build/qga/qemu-ga.exe $RPM_BUILD_ROOT%{mingw64_bindir}
cp build/qga/qemu-ga-x86_64.msi $RPM_BUILD_ROOT%{mingw64_bindir}


%files
%defattr(-,root,root)
%{mingw32_bindir}/qemu-ga*
%{mingw64_bindir}/qemu-ga*

%changelog
* Mon Aug 4 2025 Kostiantyn Kostiuk <kkostiuk@redhat.com> 110.0.2-1
- RHEL-107174 QGA can't be installed before vioserial driver or without serial port configured

* Thu Jul 17 2025 Kostiantyn Kostiuk <kkostiuk@redhat.com> 110.0.1-1
- RHEL-104252 QAPI error desc does not contain Windows error

* Fri Jun 20 2025 Kostiantyn Kostiuk <kkostiuk@redhat.com> 110.0.0-1
- RHEL-83547 - Rebase mingw-qemu-ga-win to QEMU 10.0.0 
- RHEL-96980 - mingw-qga: Drop mingw-pixman build deps
- RHEL-98947 - [mingw-qemu-ga-win] MSI installer ignore VSS installation result 
- RHEL-11824 - [QGA] VSS installation retry, if previously VSS service was not un-registered correctly 

* Mon Mar 17 2025 Konstantin Kostiuk <kkostiuk@redhat.com> 109.1.0-8
- RHEL-71884 - [qemu-guest-agent][RFE] Report CPU load average for Windows VMs

* Mon Jan 20 2025 Konstantin Kostiuk <kkostiuk@redhat.com> 109.1.0-7
- RHEL-74469 - Rebuild mingw-qemu-ga-win package due to deps update

* Tue Jan 7 2025 Konstantin Kostiuk <kkostiuk@redhat.com> 109.1.0-6
- Fix version release
- RHEL-70468 - win server 2k25 guest agent shows wrong output os version

* Thu Dec 12 2024 Dehan Meng <demeng@redhat.com> 109.1.0-5
- RHEL-70468 - win server 2k25 guest agent shows wrong output os version

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 109.1.0-4
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Wed Sep 11 2024 Konstantin Kostiuk <kkostiuk@redhat.com> 109.1.0-3
- RHEL-57753 - mingw-qemu-ga-win failed to build on s390x
- Rebuild

* Fri Sep 6 2024 Konstantin Kostiuk <kkostiuk@redhat.com> 109.1.0-2
- RHEL-57753 - mingw-qemu-ga-win failed to build on s390x
 
* Wed Sep 4 2024 Konstantin Kostiuk <kkostiuk@redhat.com> 109.1.0
- RHEL-57014 - Rebase qemu-ga to 9.1.0
- RHEL-32297 - guest agent public ssh injection api support for Windows
- RHEL-36718 - The version of mingw-qemu-ga-win doesn't match inside query and via command 'guest-info'
- Set version to 109.1.0

* Tue May 7 2024 Konstantin Kostiuk <kkostiuk@redhat.com> 108.0.2
- Set version to 108.0.2
- RHEL-35692 - Update gating.yaml for RHEL 10

* Tue Apr 30 2024 Konstantin Kostiuk <kkostiuk@redhat.com> 108.0.1
- Set version to 108.0.1
- RHEL-34770 - Gatting rpminspect SPDX license expressions validate failed

* Wed Apr 24 2024 Konstantin Kostiuk <kkostiuk@redhat.com> 108.0.0
- Set version to 108.0.0
- RHEL-23026 - Rebase qemu-ga to 9.0.0

* Mon Apr 1 2024 Dehan Meng <demeng@redhat.com> 107.0.2
- Set version to 107.0.2
- RHEL-26205 - [QGA] Add Windows Server 2025 to guest-osinfo command

* Mon Jan 15 2024 Konstantin Kostiuk <kkostiuk@redhat.com> 107.0.1
- Set version to 107.0.1
- RHEL-21655 - Fix mingw-qemu-ga-win licenses 

* Mon Jan 15 2024 Konstantin Kostiuk <kkostiuk@redhat.com> 107.0.0
- Set version to 107.0.0
- RHEL-15491 - Rebase qemu-ga to 8.2.0

* Mon Jul 10 2023 Konstantin Kostiuk <kkostiuk@redhat.com> 106.0.1
- Set version to 106.0.1
- RHELPLAN-147763 - [mingw-qemu-ga-win] VSS DLL: Add logging mechanism
- RHEL-581 - Use the SPDX vocabulary to specify the license

* Sun Apr 23 2023 Konstantin Kostiuk <kkostiuk@redhat.com> 106.0.0
- Set version to 106.0.0
- RHEL-408 - Add provides, obsoletes for mingw-qemu-ga-win
- RHEL-385 - Rebase mingw-qemu-ga-win to QEMU 8.0

* Wed Feb 15 2023 Konstantin Kostiuk <kkostiuk@redhat.com> 105.0.4
- Set version to 105.0.4
- BZ#2167436

* Mon Dec 26 2022 Konstantin Kostiuk <kkostiuk@redhat.com> 105.0.3
- Set version to 105.0.3
- BZ#2090250 - mingw-qemu-ga-win: Add Provides: bundled() to rpm packages [rhel-9]

* Tue Dec 6 2022 Konstantin Kostiuk <kkostiuk@redhat.com> 105.0.2
- Set version to 105.0.2
- Fix wrong requires
- Fix missing patch0002
- Remove extra Summary
- BZ#2090333 - [mingw-qemu-ga-win] qga command 'guest-get-fsinfo' can't query bus-type of USB

* Tue Dec 6 2022 Konstantin Kostiuk <kkostiuk@redhat.com> 105.0.1
- Set version to 105.0.1
- Remove redundant package
- BZ#2090333 - [mingw-qemu-ga-win] qga command 'guest-get-fsinfo' can't query bus-type of USB

* Mon Oct 24 2022 Konstantin Kostiuk <kkostiuk@redhat.com> 105.0.0
- Set version to 105.0.0
- BZ#2137262 - qemu-ga-win: Rebase qemu-ga to 7.1.0

* Tue May 17 2022 Konstantin Kostiuk <kkostiuk@redhat.com> 104.0.2
- Set version to 104.0.2
- BZ#2084608 - Fix mismatched allocation function
- BZ#2084613 - qga-win: race condition in build

* Thu May 12 2022 Konstantin Kostiuk <kkostiuk@redhat.com> 104.0.1
- Set version to 104.0.1
- BZ#2084493 - qemu-ga can't be installed

* Mon Apr 25 2022 Konstantin Kostiuk <kkostiuk@redhat.com> 104.0.0
- Set version to 104.0.0
- BZ#2078384 - Rebase QEMU Guest Agent Windows to 7.0.0
- Rebase to qemu-7.0.0

* Mon Jan 24 2022 Konstantin Kostiuk <kkostiuk@redhat.com> 103.0.0
- Set version to 103.0.0
- BZ#1992643 - Add mingw-qemu-ga-win package to CentOS stream
- Rebase to qemu-6.2.0

* Mon Dec 27 2021 Yan Vugenfirer <yvugenfi@redhat.com> 102.10.0
- Set version to 102.10.0
- BZ#2026167 - Add Windows11 version support for mingw-qemu-ga
- Dynamically link mingw-glib2 library

* Thu Dec 23 2021 Yan Vugenfirer <yvugenfi@redhat.com> 102.9.0
- Set version to 102.9.0
- BZ#2026167 - Add Windows11 version support for mingw-qemu-ga
- Use mingw-glib2-2.70.1

* Thu Nov 25 2021  Yan Vugenfirer <yvugenfi@redhat.com> 102.8.8
- Set version to 102.8.0
- BZ#2026167 - Add Windows11 version support for mingw-qemu-ga

* Wed Jul 21 2021 Yan Vugenfirer <yvugenfi@redhat.com> 102.7.0
- Set version to 102.7.0
- BZ#1958825 - Memory leak in qemu-ga for Windows

* Tue Jul 13 2021 Yan Vugenfirer <yvugenfi@redhat.com> 102.6.0
- Set version to 102.6.0
- BZ#1978859 - The qemu-ga-win build version in MSI is different between checking inside guest and qga command
- BZ#1981302 - QGA version can't be upgrade directly without uninstalling old version

* Tue Jun 22 2021 Yan Vugenfirer <yvugenfi@redhat.com> 102.5.0
- Set version to 102.5.0
- Bug 1972070 - RFE: Add Windows Server 2022 version support for mingw-qemu-ga

* Wed Jun 16 2021 Yan Vugenfirer <yvugenfi@redhat.com> 102.2.0
- Set version to 102.2.0
- Bug 1958825 - fix memory leak in qemu-ga for Windows

* Mon Jun 7 2021 Yan Vugenfirer <yvugenfi@redhat.com> 102.1.0
- Set version to 102.1.0
- BZ#1957377 - ownstream qemu-ga should report the build number and not QEMU version

* Wed Feb 24 2021 Basil Salman <bsalman@redhat.com> 102.0.0
- rebase to qemu-5.2.0
- Set version to 102.0.0
- BZ#1915198 - Rebase mingw-qemu-ga-win to qemu 5.2
- BZ#1929144 - fix qemu-ga-win resource leaks
- BZ#1920874 - Some changes of qga command "get-devices" should be fix on mingw-qemu-ga-win to qemu 5.2
- BZ#1919535 - Can not get the disks of windows guest via guest agent
- BZ#1909073 - Filesystem freeze on Windows reports errors frequently

* Mon Aug 3 2020 Basil Salman <bsalman@redhat.com> 101.2.0
BZ#1746667 - [qemu-guest-agent]System reserve volume's file system via guest agent is different from it's in guest
BZ#1549425 - Getting response from guest-fsfreeze-thaw need about 90s sometimes

* Thu Mar 5 2020 Basil Salman <bsalman@redhat.com> 101.1.0
BZ#1790455 - Add guest-get-devices command to qemu-ga-win

* Thu Oct 24 2019 Basil Salman <bsalman@redhat.com> 101.0.0
BZ#1733165 - QEMU Guest Agent For Windows Return Garbled NIC Name
BZ#1751431 - "guest-get-memory-block-info" is enabled but in fact it is not currently supported

* Tue Jan 22 2019 Yan Vugenfirer <yvugenfi@redhat.com> 100.0.0
BZ#1651655 -  Rebase mingw-qemu-ga-win to qemu 3.1. Change the versioning scheme to independent scheme for qemu-ga-win

* Mon Dec 24 2018 Sameeh Jubran <sjubran@redhat.com> 8.0.0
BZ#1645018 - CVE-2018-12617 virtio-win: Qemu: qemu-guest-agent: Integer overflow causes segmentation fault in qmp_guest_file_read()

* Sun Dec 23 2018 Sameeh Jubran <sjubran@redhat.com> 8.0.0
BZ#1659071 [RFE]Add "windows 2019 x64" support to OS reporting

* Thu Nov 08 2018 Sameeh Jubran <sjubran@redhat.com> 8.0.0
#rebase mingw-qemu-ga-win to qemu 3.1.0

* Sun Jun 24 2018 Sameeh Jubran <sjubran@redhat.com> 7.6.0
BZ#1565431 - "Disk" is [] in the result of guest-get-fsinfo cmd which is odd
BZ#1594113 - Error returned after issue {"execute":"guest-fstrim" } cmd for win7-32/64 and win2008-32/64/r2 guest
BZ#1536331 - Failed to upgrade qemu-ga without virtio-serial driver installed

* Wed Jan 24 2018 Sameeh Jubran <sjubran@redhat.com> 7.5.0
BZ#1536954 - Issuing guest-fsfreeze-freeze cmd for the first time on a new qemu-ga,can not get response.

* Wed Dec 13 2017 Sameeh Jubran <sjubran@redhat.com> 2.9.5
- Add resolved BZs to changelog
BZ#1514303 - QEMU Guest Agent VSS Provider service is being installed with startup type: Automatic
BZ#990629 - [Windows Guest Tools] QEMU Guest Agent service failed | After post-installation reboot another reboot is needed
BZ#1514382 - [guest-agent]Still can write to freezed file system after run "{ "execute": "guest-fsfreeze-freeze"}" cmd.
BZ#1071499 - qemu guest agent for Windows should support guest-set-time command
BZ#1082999 - [WGT] Win 2008 32bit: Detected circular dependencies demand starting RHEV Spice Agent.
BZ#1470649 - [virtio-win[qemu-ga-win][upstream]]Unable to install qemu-ga on Windows platform : QEMU guest agent -- Error 1722
BZ#1514347 - [qemu-ga-win] QEMU guest agent's version is not correct.
BZ#1515137 - Error window pops up during installing windows qemu-ga-win.msi manually

* Sun Jun 04 2017 Sameeh Jubran <sjubran@redhat.com> - 2.9.0
- First release
