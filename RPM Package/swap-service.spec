
%define relabel_files() \
restorecon -R -v /usr/bin; \
restorecon -R -v /usr/lib/systemd/system; \

%define selinux_policyver 3.13.1-266

Name:          swap-service
Version:       1.0
Release:       1%{?dist}
Summary:       Swap service
Group:         Testing
License:       GPL
URL:           https://github.com/SvetlanaGolub/swap_service
Source0:       %{name}-%{version}.tar.gz
Source1:	swap_service.pp
Source2:	swap_service.if
BuildRequires: /bin/rm, /bin/mkdir, /bin/cp
Requires:      /bin/bash, policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch:     noarch

%description
Service for swap control and SELinux policy module
Authors: Andryushin, Gerasimov, Golub, Grubach, Rudik, Zorichev

%prep
%setup -q

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 swapcontrol.sh %{buildroot}%{_bindir}
install -d %{buildroot}%{_exec_prefix}/lib/systemd/system/
install -m 644 swapcontrol.service %{buildroot}%{_exec_prefix}/lib/systemd/system/swapcontrol.service
install -d %{buildroot}%{_mandir}/man8/
install -m 644 swapcontrol.8 %{buildroot}%{_mandir}/man8/swapcontrol.8
#For SELinux module
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}/etc/selinux/targeted/contexts/users/

#Install our policy
%post
semodule -n -i %{_datadir}/selinux/packages/swap_service.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

#Delet SELinux module
%postun
if [ $1 -eq 0 ]; then
    semodule -n -r swap_service
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%{_bindir}/swapcontrol.sh 
%{_exec_prefix}/lib/systemd/system/swapcontrol.service
%{_mandir}/man8/swapcontrol.8*
%attr(0600,root,root) %{_datadir}/selinux/packages/swap_service.pp
%{_datadir}/selinux/devel/include/contrib/swap_service.if

%changelog
* Sat May 30 2020 Swap-service
- Added swap-service
