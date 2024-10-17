#
# please keep this file backportable on the system running on kenobi
#
%define my_py_ver %(echo %py_ver | tr -d -c '[:digit:]')
%if "%my_py_ver" == ""
# Assume 2.6 if we don't have python at src.rpm creation time
%define my_py_ver 26
%endif

Name: repsys
Version: 1.10
Epoch: 1
Release: 7
Summary: Tools for Mandriva Linux repository access and management
Group: Development/Other
Source: %{name}-%{version}.tar.bz2
Source1: mdk-rebrand-mdk
Source2: repsys.conf
Patch0: repsys-1.9-new-ssh-url.patch
License: GPL
URL: https://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/build_system/repsys/
Requires: python-cheetah subversion openssh-clients python-rpm
%py_requires -d
BuildRoot: %{_tmppath}/%{name}-%{version}-root
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

See repsys --help-plugin ldapusers for more information. Also see
http://qa.mandriva.com/show_bug.cgi?id=30549

%prep
%setup -q
install -m 0644 %{SOURCE2} %_builddir/%name-%version
%patch0 -p1 -b .new-ssh-url

%build
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --root=%{buildroot}
# Using compile inline since niemeyer's python macros still not available on mdk rpm macros
find %{buildroot}%{py_puresitedir} -name '*.pyc' -exec rm -f {} \; 
python -c "import sys, os, compileall; br='%{buildroot}'; compileall.compile_dir(sys.argv[1], ddir=br and 
(sys.argv[1][len(os.path.abspath(br)):]+'/') or None)" %{buildroot}%{py_sitedir}

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_datadir}/repsys/
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 %{SOURCE1} %{buildroot}%{_datadir}/repsys/rebrand-mdk
install -m 0755 create-srpm %{buildroot}%{_datadir}/repsys/create-srpm
install -m 0755 repsys-ssh %{buildroot}%{_bindir}/repsys-ssh
install -m 0644 repsys.conf %{buildroot}%{_sysconfdir}

%clean
rm -rf %{buildroot}

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
%if %my_py_ver >= 25
%{py_puresitedir}/*.egg-info
%endif

%files ldap
%doc README.LDAP
%{py_puresitedir}/RepSys/plugins/ldapusers.py*



%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.10-2
+ Revision: 669418
- mass rebuild

* Wed Mar 16 2011 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.10-1
+ Revision: 645663
- new version 1.10:
  o allow setting the port used to connect to the submit host
  o allow using submit -r REV, without package name
  o allow using target macros in getsrpm as in submit (via the -d option)
  o abort when no submit host is defined, less chance of obscure errors
  o added option in configuration to allow disabling submits temporarily

* Fri Nov 26 2010 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.9-5mdv2011.0
+ Revision: 601603
- added patch updating the URL on authentication errors

* Thu Nov 11 2010 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.9-4mdv2011.0
+ Revision: 596164
- removed noreplace for /etc/repsys.conf in order to allow bringing new urls
  and fixes in configuration; personal config should go to ~/.repsys/config

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 1:1.9-3mdv2011.0
+ Revision: 590093
- rebuild for python 2.7

* Thu Mar 18 2010 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.9-2mdv2011.0
+ Revision: 525093
- disabled mirror use, it will be reenabled when mdvsys reads it correctly
  (without cooker/)

* Fri Mar 05 2010 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.9-1mdv2010.1
+ Revision: 514360
- new version 1.9

  + Michael Scherer <misc@mandriva.org>
    - fix build on a 64 bit host
    - fix comment and mirror option with the proper url for mdvsys

* Tue Jan 12 2010 Pascal Terjan <pterjan@mandriva.org> 1:1.8-4mdv2010.1
+ Revision: 490215
- Really allow recreating src.rpm without python
- Allow recreating src.rpm without python

  + Bogdano Arendartchuk <bogdano@mandriva.com>
    - changed configuration to use the mirror repository by default, so that
      anonymous users can checkout packages without changing repsys.conf
      (authenticated users either have to user 'repsys switch' or disable it in
      the configuration)

* Thu Sep 24 2009 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.8-1mdv2010.0
+ Revision: 448508
- version 1.8

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:1.7-8mdv2010.0
+ Revision: 426906
- rebuild

* Tue Feb 17 2009 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.7-7mdv2009.1
+ Revision: 342254
- fixed submit to allow specifying only the package name
- the patch advertised on the previous release was not being applied

* Mon Feb 16 2009 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.7-6mdv2009.1
+ Revision: 341081
- added patch to make the -M option work again

* Wed Dec 24 2008 Michael Scherer <misc@mandriva.org> 1:1.7-5mdv2009.1
+ Revision: 318445
- rebuild for new python

* Wed Dec 24 2008 Funda Wang <fwang@mandriva.org> 1:1.7-4mdv2009.1
+ Revision: 318358
- rebuild for new python
- simplify BR

* Mon Nov 17 2008 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.7-3mdv2009.1
+ Revision: 303959
- added patch fixing putsrpm changelog stripping and spec renaming

* Thu Nov 13 2008 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.7-2mdv2009.1
+ Revision: 302695
- leave the configuration file open in the package
- added default_parent back to repsys.conf

* Tue Nov 11 2008 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.7-1mdv2009.1
+ Revision: 302259
- new version 1.7

* Fri Jul 11 2008 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.6.90-1mdv2009.0
+ Revision: 233872
- added patch to make it compatible with create-srpm from repsys < 1.6.90
- new testing version 1.6.90
- added patch to fix incompatibility with urlparse on python-2.4

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 12 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.6.19.2-1mdv2008.1
+ Revision: 118027
- new version 1.6.19.2

* Wed Nov 14 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.6.19.1-2mdv2008.1
+ Revision: 108874
- new version 1.6.19.1

* Thu Nov 08 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.6.19-2mdv2008.1
+ Revision: 106971
- new version 1.6.19

* Mon Jul 02 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.6.18-2mdv2008.0
+ Revision: 47244
- should require openssh-clients instead of ssh

* Mon Jun 18 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.6.18-1mdv2008.0
+ Revision: 41040
- new version 1.6.18
- added requires to python-rpm, as noted by mrl
- added requires to ssh
- requires to subversion

* Wed May 09 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.6.17.1-1mdv2008.0
+ Revision: 25791
- upgrade to 1.7.17.1 bugfix release for 2007.0

* Tue May 08 2007 Andreas Hasenack <andreas@mandriva.com> 1:1.6.17-3mdv2008.0
+ Revision: 25107
- ldap plugin should *only* be in the ldap subpackage

* Tue May 08 2007 Gustavo De Nardin <gustavodn@mandriva.com> 1:1.6.17-2mdv2008.0
+ Revision: 24985
- updated URL and description

* Mon May 07 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1:1.6.17-1mdv2008.0
+ Revision: 24954
- upgrade to 1.6.17
- moved the plugin ldapusers to the package repsys-ldap
- updated to 1.6.16


* Wed Feb 28 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1.6.14-1mdv2007.0
+ Revision: 127256
- 1.6.14

* Tue Jan 16 2007 Andreas Hasenack <andreas@mandriva.com> 1:1.6.13-1mdv2007.1
+ Revision: 109634
- updated to version 1.6.13

* Wed Jan 03 2007 Andreas Hasenack <andreas@mandriva.com> 1:1.6.12-1mdv2007.1
+ Revision: 103724
- version 1.6.12: small fix for the silent feature
- updated to version 1.6.11 (new silent feature)

* Fri Dec 01 2006 Andreas Hasenack <andreas@mandriva.com> 1:1.6.10-1mdv2007.1
+ Revision: 89695
- only package egg file if in newer python
- updated to version 1.6.10:
- use svn export instead of checkout, saves 50%% disk space (part of #27423)
- fixed repsys changed
- using getsrpm-mdk from the tarball
- removed old source

* Tue Nov 28 2006 Michael Scherer <misc@mandriva.org> 1:1.6.9-2mdv2007.1
+ Revision: 87853
- add the .egg-info file to the file listing

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild against python2.5

* Mon Nov 13 2006 Olivier Blin <oblin@mandriva.com> 1:1.6.9-1mdv2007.0
+ Revision: 83823
- 1.6.9
- use 1.6 branch as default in cooker

  + Andreas Hasenack <andreas@mandriva.com>
    - use py_requires for correct python requires (we also need python: python-base
      is not enough for this package)

* Thu Oct 19 2006 Olivier Blin <oblin@mandriva.com> 1:1.5.10-1mdv2007.1
+ Revision: 70681
- 1.5.10
- 1.5.9

* Sun Aug 20 2006 Andreas Hasenack <andreas@mandriva.com> 1:1.5.8-1mdv2007.0
+ Revision: 56843
- updated to 1.5.8

* Sat Aug 05 2006 Andreas Hasenack <andreas@mandriva.com> 1:1.5.7-2mdv2007.0
+ Revision: 51785
- removed bogus requires: python-cheetah is only needed by
  repsys-1.6.x+

* Wed Jul 19 2006 Andreas Hasenack <andreas@mandriva.com> 1:1.5.7-1mdv2007.0
+ Revision: 41543
- updated to version 1.5.7

* Tue Jul 18 2006 Andreas Hasenack <andreas@mandriva.com> 1:1.5.6-1mdv2007.0
+ Revision: 41506
- updated to version 1.5.6

* Thu Jul 13 2006 Andreas Hasenack <andreas@mandriva.com> 1:1.5.5-1mdv2007.0
+ Revision: 41001
- updated to version 1.5.5
- removed moredefines patch: already applied upstream

* Sat Jun 24 2006 Andreas Hasenack <andreas@mandriva.com> 1:1.5.4-2mdv2007.0
+ Revision: 37986
- using mkrel
- define a more complete rpm environment for constructing the .src.rpm
  so all the files end up being where we expect them to be
- renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

* Tue Feb 14 2006 Andreas Hasenack <andreas@mandriva.com> 1:1.5.4-1mdk
+ Revision: 1737
- downgraded to version 1.5.4: 1.6.0 is not ready for prime time
  (bumped epoch)
- removed patch that was already applied in version 1.5.4 (wasn't being
  applied to 1.6.0 either)

* Thu Feb 02 2006 Andreas Hasenack <andreas@mandriva.com> 1.6.0-1mdk
+ Revision: 1563
- added new requires for python-cheetah
- updated to version 1.6.0 which has the new %%changelog mechanism
- dropped patches already applied upstream
- install config file

* Sat Oct 01 2005 Andreas Hasenack <andreas@mandriva.com> 1.5.3.1-4mdk
+ Revision: 979
- releasing 1.5.3.1-4mdk
- fixed author's email
- fixed mandriva logo url
- fixed mime-type of the repsys-mdk.patch

* Wed Jul 27 2005 Helio Chissini de Castro <helio@mandriva.com> 1.5.3.1-3mdk
+ Revision: 441
- Changes on behalf of Oden Eriksson
- update S1
- lib64 fixes
- this is no noarch package
- rpmlint fixes
- Upload new spec
- Fixed ugly type on url type svn+ssh
- Update repsys to match new changelog requirements ( just release keep unchanged )
- Update getsrpm-mdk to genrate srpm with changelog
- Fixed regexp for unicode/color chars in terminal ( thanks to aurelio )
- Start to fix builds on x86_64 archs.
- Fixed patch for get real changelog and version
- Added changelog patch to match mdk style
- Added rebrand script for match release number with svn
- Added wrapper script for get srpms ready for submit to cluster compilation
- Added suggested changes by neoclust
- Added initial users on default
- Added a initial changelog until repsys submit is working
- No bziped patches
- Initial import of repsys package

