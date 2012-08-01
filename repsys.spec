Name: repsys
Version: 1.11
Epoch: 1
Release: 7
Summary: Tools for Mandriva Linux repository access and management
Group: Development/Other
Source0: %{name}-%{version}.tar.bz2
Source1: mdk-rebrand-mdk
Source2: repsys.conf
Patch0: repsys-1.9-new-ssh-url.patch
Patch1: repsys-1.11-undeclared-variable.patch
Patch2: repsys-1.11-fix-undefined-function.patch
Patch3: repsys-1.11-changelog-encode-utf8.patch
Patch4: repsys-1.11-unpack-use-nodeps.patch
License: GPL
URL: http://gitorious.org/repsys
Requires: python-cheetah subversion openssh-clients python-rpm
BuildArch: noarch

%description
Tools for Mandriva Linux repository access and management.

<http://wiki.mandriva.com/en/Development/Packaging/RepositorySystem>

%package ldap
Group: Development/Other
Summary: Repsys plugin to retrieve maintainer information from LDAP
Requires: repsys >= 1.6.16 python-ldap

%description ldap
A Repsys plugin that allows retrieving maintainer information shown in
changelogs from a LDAP server. 

See repsys --help-plugin ldapusers for more information. Also see
http://qa.mandriva.com/show_bug.cgi?id=30549

%prep
%setup -q
install -m 0644 %_sourcedir/repsys.conf %_builddir/%name-%version
%patch0 -p1 -b .new-ssh-url
%patch1 -p1 -b .undeclared-variable
%patch2 -p1 -b .undeclared-function
%patch3 -p1 -b .changelog-encode-utf8
%patch4 -p1 -b .unpack-use-nodeps

%build
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --root=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_datadir}/repsys/
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 %{SOURCE1} %{buildroot}%{_datadir}/repsys/rebrand-mdk
install -m 0755 create-srpm %{buildroot}%{_datadir}/repsys/create-srpm
install -m 0755 repsys-ssh %{buildroot}%{_bindir}/repsys-ssh
install -m 0644 repsys.conf %{buildroot}%{_sysconfdir}

%files
%defattr(-,root,root)
%doc CHANGES repsys-example.conf
%attr(0644,root,root) %{_sysconfdir}/repsys.conf
%{_bindir}/repsys
%{_bindir}/repsys-ssh
%{_datadir}/repsys
%{_mandir}/*/*
%{py_puresitedir}/RepSys
%exclude %{py_puresitedir}/RepSys/plugins/ldapusers.py*
%{py_puresitedir}/*.egg-info

%files ldap
%doc README.LDAP
%{py_puresitedir}/RepSys/plugins/ldapusers.py*
