%define rel 1
%define my_py_ver %(echo %py_ver | tr -d '.')

Name: repsys
Version: 1.6.90
Epoch: 1
Release: %mkrel %rel
Summary: Tools for Mandriva Linux repository access and management
Group: Development/Other
Source: %{name}-%{version}.tar.bz2
Source1: mdk-rebrand-mdk
Patch0: repsys-1.6.90-compat-create-srpm.patch
License: GPL
URL: http://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/build_system/repsys/
Requires: python-cheetah subversion openssh-clients python-rpm
%py_requires
Buildrequires: python-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python 
BuildRequires: python-devel
BuildArch: noarch

%description
Tools for Mandriva Linux repository access and management.

<http://wiki.mandriva.com/en/Development/Packaging/RepositorySystem>

<http://wiki.mandriva.com/en/Development/Packaging/Tools/repsys>


%package ldap
Group: Development/Other
Summary: Repsys plugin to retrieve maintainer information from LDAP
Requires: repsys >= 1.6.16 python-ldap

%description ldap
A Repsys plugin that allows retrieving maintainer information shown in
changelogs from a LDAP server. 

See repsys --help-plugin ldapusers for more information. Also
http://qa.mandriva.com/show_bug.cgi?id=30549

%prep
%setup -q
%patch0 -p0 -b compat-create-srpm

%build
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --root=%{buildroot}
# Using compile inline since niemeyer's python macros still not available on mdk rpm macros
find %{buildroot}%{py_sitedir} -name '*.pyc' -exec rm -f {} \; 
python -c "import sys, os, compileall; br='%{buildroot}'; compileall.compile_dir(sys.argv[1], ddir=br and 
(sys.argv[1][len(os.path.abspath(br)):]+'/') or None)" %{buildroot}%{py_sitedir}

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_datadir}/repsys/
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 %{SOURCE1} %{buildroot}%{_datadir}/repsys/rebrand-mdk
install -m 0755 create-srpm %{buildroot}%{_datadir}/repsys/create-srpm
install -m 0755 getsrpm-mdk %{buildroot}%{_bindir}/getsrpm-mdk
install -m 0644 repsys.conf %{buildroot}%{_sysconfdir}

%post
if [ "$1" = "2" ]; then
	if ! grep -q '^create-srpm' %{_sysconfdir}/repsys.conf; then
		cat >> %{_sysconfdir}/repsys.conf <<EOF

[helper]
create-srpm = %{_datadir}/repsys/create-srpm
EOF
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES repsys-example.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/repsys.conf
%{_bindir}/repsys
%{_bindir}/getsrpm-mdk
%{_datadir}/repsys
%{_mandir}/*/*
%{py_sitedir}/RepSys
%exclude %{py_sitedir}/RepSys/plugins/ldapusers.py*
%if %my_py_ver >= 25
%{py_sitedir}/*.egg-info
%endif

%files ldap
%doc README.LDAP
%{py_sitedir}/RepSys/plugins/ldapusers.py*

