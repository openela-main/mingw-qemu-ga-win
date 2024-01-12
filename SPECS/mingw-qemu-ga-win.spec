%{?mingw_package_header}

%define with_vss 1
%define qemu_version 8.0.0
%define ga_manufacturer "RedHat"
%define ga_distro "RHEL"

Name: mingw-qemu-ga-win
Version: 106.0.0
Release: 1%{?dist}
Summary: Qemus Guest agent for Windows

Group: System Environment/Daemons
License: GPLv2+ and LGPLv2+ and BSD
URL: http://www.qemu.org/
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Source0: http://wiki.qemu.org/download/qemu-%{qemu_version}.tar.bz2

Patch0001: 0001-Change-Version.patch

BuildArch: noarch

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
BuildRequires: mingw32-pixman
BuildRequires: mingw64-pixman
BuildRequires: mingw32-gcc >= 7.4.0
BuildRequires: mingw64-gcc >= 7.4.0
BuildRequires: mingw32-glib2
BuildRequires: mingw64-glib2
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
%setup -q -n qemu-%{qemu_version}
%patch0001 -p1

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
