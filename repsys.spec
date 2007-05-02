%define rel 1
%define my_py_ver %(echo %py_ver | tr -d '.')

Name: repsys
Version: 1.6.16
Epoch: 1
Release: %mkrel %rel
Summary: Tools for Mandriva Linux repository access and management
Group: Development/Other
Source: %{name}-%{version}.tar.bz2
Source1: mdk-rebrand-mdk
License: GPL
URL: http://qa.mandriva.com/twiki/bin/view/Main/RepositorySystem
Requires: python-cheetah
%py_requires
Buildrequires: python-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python 
BuildRequires: python-devel
BuildArch: noarch

%description
Tools for Mandriva Linux repository access and management.

%prep
%setup -q

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
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/repsys.conf
%{_bindir}/repsys
%{_bindir}/getsrpm-mdk
%{_datadir}/repsys
%{py_sitedir}/RepSys
%if %my_py_ver >= 25
%{py_sitedir}/*.egg-info
%endif


