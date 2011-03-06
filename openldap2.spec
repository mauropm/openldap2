#
# spec file for package openldap2 (Version 2.3.35)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           openldap2
BuildRequires:  cyrus-sasl-devel db-devel openslp-devel openssl-devel tcpd-devel
%if %sles_version == 9
BuildRequires: -pwdutils
%endif
%if %sles_version == 10
BuildRequires: -pwdutils -db-devel libdb-4_5-devel
%endif
URL:            http://www.openldap.org
License:        BSD; openldap 2.8
Version:        2.3.43
Release:        0
%if "%{name}" == "openldap2"
Group:          Productivity/Networking/LDAP/Servers
Provides:       ldap2 openldap2-back-ldap openldap2-back-monitor
Requires:       libldap-2_3-0 = %{version}
Obsoletes:      openldap2-back-ldap openldap2-back-monitor
Conflicts:      openldap
PreReq:         %insserv_prereq %fillup_prereq /usr/sbin/useradd /usr/sbin/groupadd /usr/bin/strings /usr/bin/awk /usr/bin/grep
Summary:        The New OpenLDAP Server (LDAPv3)
%else
Group:          Productivity/Networking/LDAP/Servers
Conflicts:      openldap-client
Summary:        The New OpenLDAP Server (LDAPv3)
%endif
Autoreqprov:    on
Source:         openldap-%{version}.tar.bz2
Source1:        openldap-rc.tgz
Source2:        openldap-admin-guide.tar.bz2
Source3:        addonschema.tar.gz
Source4:        DB_CONFIG
Source5:        sasl-slapd.conf
Patch:          openldap2.dif
Patch1:         secpatch.dif
Patch2:         slapd_conf.dif
Patch3:         ldap_conf.dif
Patch4:         ldapi_url.dif
Patch5:         openldap-ntlm.diff
Patch6:         libldap-gethostbyname_r.dif
Patch7:         pie-compile.dif
Patch9:         slapd_chain_return_error.dif
Patch10:        openldap-2.3.43-modrdn-segfault.patch
Patch11:	openldap-2.3.43-rh620621.patch
Patch12:        openldap-2.3.43-rwm-cleanup.patch
Patch98:        mp-bind.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Prefix:         %{_prefix}

%description
The Lightweight Directory Access Protocol (LDAP) is used to access
online directory services. It runs directly over TCP and can be used to
access a stand-alone LDAP directory service or to access a directory
service that has an X.500 back-end.



Authors:
--------
    The OpenLDAP Project <project@openldap.org>
%if "%{name}" == "openldap2"
%package      -n openldap2-back-perl
Summary:        OpenLDAP Perl Back-End
Requires:       openldap2 = %{version}
Autoreqprov:    on
Group:          Productivity/Networking/LDAP/Servers

%description -n openldap2-back-perl
The OpenLDAP Perl back-end allows you to execute Perl code specific to
different LDAP operations.



Authors:
--------
    The OpenLDAP Project <project@openldap.org>

%package      -n openldap2-back-meta
Summary:        OpenLDAP Meta Back-End
Requires:       openldap2 = %{version}
Autoreqprov:    on
Group:          Productivity/Networking/LDAP/Servers
Provides:       openldap2:/usr/share/man/man5/slapd-meta.5.gz

%description -n openldap2-back-meta
The OpenLDAP Meta back-end is able to perform basic LDAP proxying with
respect to a set of remote LDAP servers. The information contained in
these servers can be presented as belonging to a single Directory
Information Tree (DIT).



Authors:
--------
    The OpenLDAP Project <project@openldap.org>
%else
%package      -n openldap2-devel
Summary:        Libraries, Header Files and Documentation for OpenLDAP2
Autoreqprov:    on
Conflicts:      openldap-devel 
Requires:       openldap2-client = %{version}  cyrus-sasl-devel openssl-devel
Group:          Development/Libraries/C and C++

%description -n openldap2-devel
This package provides the OpenLDAP2 libraries, header files, and
documentation.



Authors:
--------
    The OpenLDAP Project <project@openldap.org>

%package      -n libldap-2_3-0
License:        BSD 3-Clause; openldap 2.8
Summary:        The OpenLDAP libraries
AutoReqProv:    on
Group:          Development/Libraries/C and C++

%description -n libldap-2_3-0
This package contains the OpenLDAP client libraries.



Authors:
--------
    The OpenLDAP Project <project@openldap.org>

%endif

%prep
%setup -q -n openldap-%{version} -a1 -a2 -a3 
%patch
%patch1
%patch2
%patch3
%patch4
%patch5
%patch6
%if %suse_version > 920
%patch7
%endif
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch98 -p1
#%patch99 -p1 

%build
%{?suse_update_config:%{suse_update_config -f build}}
libtoolize --force
autoreconf
export CFLAGS="-g $RPM_OPT_FLAGS -fno-strict-aliasing -DLDAP_DEPRECATED -DLDAP_CONNECTIONLESS"
./configure --prefix=/usr \
        --exec-prefix=/usr \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=/var/run/slapd \
        --libexecdir=/usr/lib/openldap \
        --libdir=%{_libdir} \
        --mandir=%{_mandir} \
        --enable-wrappers \
        --enable-aclgroups \
        --enable-spasswd \
        --enable-modules \
        --enable-shared \
        --enable-dynamic \
        --with-tls \
        --with-cyrus-sasl \
        --enable-crypt \
        --enable-ipv6=yes \
%if "%{name}" == "openldap2"
        --enable-aci \
        --enable-bdb \
        --enable-hdb \
        --enable-ldbm \
        --enable-rewrite \
        --enable-ldap=yes \
        --enable-meta=mod \
        --enable-monitor=yes \
        --enable-perl=mod \
        --enable-slp \
        --enable-overlays=yes \
        --enable-proxycache=yes \
%else
        --disable-slapd \
%endif
        --enable-lmpasswd \
        --with-yielding-select
make depend
make %{?jobs:-j%jobs}
rm tests/scripts/test022-ppolicy
rm tests/scripts/test036-meta-concurrency
rm tests/scripts/test039-glue-ldap-concurrency

%check
# calculate the base port to be use in the test-suite
SLAPD_BASEPORT=10000
if [ -f /.buildenv ] ; then
    . /.buildenv
    SLAPD_BASEPORT=$(($SLAPD_BASEPORT + $BUILD_INCARNATION * 10))
fi
export SLAPD_BASEPORT
%if %suse_version < 1100
%ifnarch %arm alpha
make test
%endif
%endif

%install
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/usr/sbin
make DESTDIR=$RPM_BUILD_ROOT install
install -m 755 rc.ldap $RPM_BUILD_ROOT/etc/init.d/ldap
install -m 755 rc.slurpd $RPM_BUILD_ROOT/etc/init.d/slurpd
ln -sf ../../etc/init.d/ldap $RPM_BUILD_ROOT/usr/sbin/rcldap
ln -sf ../../etc/init.d/slurpd $RPM_BUILD_ROOT/usr/sbin/rcslurpd
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sasl2
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/sasl2/slapd.conf
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/apparmor/profiles/extras/
install -m 644 apparmor/usr.lib.openldap.slapd $RPM_BUILD_ROOT/%{_sysconfdir}/apparmor/profiles/extras/usr.lib.openldap.slapd
install -m 755 -d $RPM_BUILD_ROOT/var/lib/ldap
install -m 700 -d $RPM_BUILD_ROOT/var/lib/slurpd
chmod a+x $RPM_BUILD_ROOT/%{_libdir}/liblber.so*
chmod a+x $RPM_BUILD_ROOT/%{_libdir}/libldap_r.so*
chmod a+x $RPM_BUILD_ROOT/%{_libdir}/libldap.so*
%if "%{name}" == "openldap2"
mkdir -p $RPM_BUILD_ROOT/var/adm/fillup-templates
install -m 644 sysconfig.openldap $RPM_BUILD_ROOT/var/adm/fillup-templates/sysconfig.openldap
install -m 644 *.schema $RPM_BUILD_ROOT/etc/openldap/schema
install -m 644 $RPM_SOURCE_DIR/DB_CONFIG $RPM_BUILD_ROOT/var/lib/ldap/DB_CONFIG
install -m 644 $RPM_BUILD_ROOT/etc/openldap/DB_CONFIG.example $RPM_BUILD_ROOT/var/lib/ldap/DB_CONFIG.example
install -d $RPM_BUILD_ROOT/etc/sysconfig/SuSEfirewall2.d/services/
install -m 644 SuSEfirewall2.openldap $RPM_BUILD_ROOT/etc/sysconfig/SuSEfirewall2.d/services/openldap
rm -f $RPM_BUILD_ROOT/etc/openldap/DB_CONFIG.example
rm -f $RPM_BUILD_ROOT/var/run/slapd/openldap-data/DB_CONFIG.example
%endif
rm -f $RPM_BUILD_ROOT/usr/lib/openldap/modules/*.a
rm -f $RPM_BUILD_ROOT/usr/share/man/man5/slapd-dnssrv.5
rm -f $RPM_BUILD_ROOT/usr/share/man/man5/slapd-null.5
rm -f $RPM_BUILD_ROOT/usr/share/man/man5/slapd-passwd.5
rm -f $RPM_BUILD_ROOT/usr/share/man/man5/slapd-shell.5
rm -f $RPM_BUILD_ROOT/usr/share/man/man5/slapd-sql.5
rm -f $RPM_BUILD_ROOT/usr/share/man/man5/slapd-tcl.5
# Remove *.la files, libtool does not handle this correct
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la
#
#put filelists into files
cat >openldap2.filelist <<EOF
/var/adm/fillup-templates/sysconfig.openldap
%dir %attr(-, root, root) %{_sysconfdir}/apparmor/
%dir %attr(-, root, root) %{_sysconfdir}/apparmor/profiles/
%dir %attr(-, root, root) %{_sysconfdir}/apparmor/profiles/extras/
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/apparmor/profiles/extras/usr.lib.openldap.slapd
%config /etc/init.d/ldap
%config /etc/init.d/slurpd
%config /etc/sysconfig/SuSEfirewall2.d/services/openldap
/usr/sbin/rcldap
/usr/sbin/rcslurpd
/usr/sbin/slap*
%dir /etc/openldap
/etc/openldap/schema
%config(noreplace) %attr(640, root, ldap) /etc/openldap/slapd.conf
%config(noreplace) /var/lib/ldap/DB_CONFIG
%config(noreplace) /var/lib/ldap/DB_CONFIG.example
%attr(640, root, ldap) /etc/openldap/slapd.conf.default
%config(noreplace) /etc/sasl2/slapd.conf
%dir /usr/lib/openldap
%dir /usr/lib/openldap/modules
/usr/lib/openldap/slapd
/usr/lib/openldap/slurpd
%dir %attr(0700, ldap, ldap) /var/lib/ldap
%dir %attr(0700, ldap, ldap) /var/run/slapd
/var/lib/slurpd
%doc %{_mandir}/man8/sl*
%doc %{_mandir}/man5/slapd.*
%doc %{_mandir}/man5/slapd-bdb.*
%doc %{_mandir}/man5/slapd-hdb.*
%doc %{_mandir}/man5/slapd-ldbm.*
%doc %{_mandir}/man5/slapd-ldap.*
%doc %{_mandir}/man5/slapd-ldif.*
%doc %{_mandir}/man5/slapd-monitor.*
%doc %{_mandir}/man5/slapd-relay.*
%doc %{_mandir}/man5/slapo-*
%doc ANNOUNCEMENT COPYRIGHT INSTALL LICENSE README CHANGES
%doc doc/drafts doc/install doc/admin-guide
EOF
#
cat > openldap2-client.filelist <<EOF
%dir /etc/openldap
%config(noreplace) /etc/openldap/ldap.conf
/etc/openldap/ldap.conf.default
/usr/bin/ldapadd
/usr/bin/ldapcompare
/usr/bin/ldapdelete
/usr/bin/ldapmodify
/usr/bin/ldapmodrdn
/usr/bin/ldapsearch
/usr/bin/ldappasswd
/usr/bin/ldapwhoami
%doc %{_mandir}/man1/ldap*
%doc %{_mandir}/man5/ldap.conf*
%doc %{_mandir}/man5/ldif.*
EOF
cat > libldap.filelist <<EOF
%{_libdir}/liblber*.so.*
%{_libdir}/libldap*.so.*
EOF
cat > openldap2-devel.filelist <<EOF
/usr/include/lber.h
/usr/include/lber_types.h
/usr/include/ldap*.h
/usr/include/slapi-plugin.h
%{_libdir}/liblber.a
%{_libdir}/liblber.so
%{_libdir}/libldap.a
%{_libdir}/libldap.so
%{_libdir}/libldap_r.a
%{_libdir}/libldap_r.so
%doc %{_mandir}/man3/ber*
%doc %{_mandir}/man3/lber*
%doc %{_mandir}/man3/ld_errno*
%doc %{_mandir}/man3/ldap*
EOF
cat > openldap2-back-perl.filelist <<EOF
/usr/lib/openldap/modules/back_perl*
%doc %{_mandir}/man5/slapd-perl.*
EOF
cat > openldap2-back-meta.filelist <<EOF
/usr/lib/openldap/modules/back_meta*
%doc %{_mandir}/man5/slapd-meta.*
EOF
#remove files from other spec file
%if "%{name}" == "openldap2"
cat openldap2-client.filelist libldap.filelist openldap2-devel.filelist |    
%else
cat openldap2.filelist openldap2-back-perl.filelist openldap2-back-meta.filelist |
%endif
  grep -v "%dir " |sed -e "s|^.* ||" |grep "^/" |while read name ; do
    rm -rf $RPM_BUILD_ROOT$name
  done
%if "%{name}" == "openldap2"

%pre
/usr/sbin/groupadd -g 70 -o -r ldap 2> /dev/null || :
/usr/sbin/useradd -r -o -g ldap -u 76 -s /bin/bash -c "User for OpenLDAP" -d \
/var/lib/ldap ldap 2> /dev/null || :

%post
if [ ${1:-0} -gt 1 ] && [ -f %{_libdir}/sasl2/slapd.conf ] ; then
  cp /etc/sasl2/slapd.conf /etc/sasl2/slapd.conf.rpmnew
  cp %{_libdir}/sasl2/slapd.conf /etc/sasl2/slapd.conf
fi
%{fillup_and_insserv -n -s openldap ldap START_LDAP slurpd START_SLURPD}
%{remove_and_set -n openldap OPENLDAP_RUN_DB_RECOVER}

%preun
%stop_on_removal ldap slurpd

%postun
%restart_on_update ldap slurpd
%insserv_cleanup

%files -f openldap2.filelist
%defattr(-,root,root)

%files -n openldap2-back-perl -f openldap2-back-perl.filelist
%defattr(-,root,root)

%files -n openldap2-back-meta -f openldap2-back-meta.filelist
%defattr(-,root,root)
%else

%post -n libldap-2_3-0 -p /sbin/ldconfig

%postun -n libldap-2_3-0 -p /sbin/ldconfig

%files -f openldap2-client.filelist
%defattr(-,root,root)

%files -n libldap-2_3-0 -f libldap.filelist
%defattr(-,root,root)

%files -n openldap2-devel -f openldap2-devel.filelist
%defattr(-,root,root)
%endif

%changelog -n openldap2
* Mon Feb 26 2007 - rhafer@suse.de
Updated to Version 2.3.34. Most important changes:
  * Fixed libldap missing get_option(TLS CipherSuite) (ITS#4815)
  * Fixed ldapmodify printing error from ldap_result() (ITS#4812)
  * Fixed slapadd LDIF parsing (ITS#4817)
  * Fixed slapd libltdl link ordering (ITS#4830)
  * Fixed slapd syncrepl memory leaks (ITS#4805)
  * Fixed slapd dynacl/ACI compatibility with 2.1
  * Fixed slapd-bdb/hdb be_entry_get with aliases/referrals
    (ITS#4810)
  * Fixed slapd-ldap more response handling bugs (ITS#4782)
  * Fixed slapd-ldap C-API code tests (ITS#4808)
  * Fixed slapd-monitor NULL printf (ITS#4811)
  * Fixed slapo-chain spurious additional info in response
    (ITS#4828)
  * Fixed slapo-syncprov presence list (ITS#4813)
  * Fixed slapo-syncprov contextCSN checkpoint again (ITS#4720)
  * Added slapo-ppolicy cn=config support (ITS#4836)
  * Added slapo-auditlog cn=config support
* Fri Jan 26 2007 - rhafer@suse.de
- Updated to Version 2.3.33. Most importan changes:
  * Fixed slapd-ldap chase-referrals switch (ITS#4557)
  * Fixed slapd-ldap bind behavior when idassert is always used 
    (ITS#4781)
  * Fixed slapd-ldap response handling bugs (ITS#4782)
  * Fixed slapd-ldap idassert mode=self anonymous ops (ITS#4798)
  * Fixed slapd-ldap/meta privileged connections handling 
    (ITS#4791)
  * Fixed slapd-meta retrying (ITS#4594, 4762)
  * Fixed slapo-chain referral DN use (ITS#4776)
  * Fixed slapo-dynlist dangling pointer after entry free 
    (ITS#4801)
  * Fixed libldap ldap_pvt_put_filter syntax checks (ITS#4648)
* Tue Nov 14 2006 - rhafer@suse.de
- Updated to Version 2.3.30
* Wed Oct 30 2006 - rhafer@suse.de
- Updated to Version 2.3.28
* Wed Oct 04 2006 - rhafer@suse.de
- Add $network to Should-Start/Should-Stop in init scripts
  (Bug: #206823)
- Imported latest back-perl changes from CVS, to fix back-perl
  initialization (Bug: #207618)
* Tue Aug 22 2006 - rhafer@suse.de
- Updated to Version 2.3.27
  * Fixed libldap dnssrv bug with "not present" positive statement
  (ITS#4610)
  * Fixed libldap dangling pointer issue (ITS#4405)
  * Fixed slapd incorrect rebuilding of replica URI (ITS#4633)
  * Fixed slapd DN X.509 normalization crash (ITS#4644)
  * Fixed slapd-monitor operations order via callbacks (ITS#4631)
  * Fixed slapo-accesslog purge task during shutdown
  * Fixed slapo-ppolicy handling of default policy (ITS#4634)
  * Fixed slapo-ppolicy logging verbosity when using default policy
  * Fixed slapo-syncprov incomplete sync on restart issues (ITS#4622)
* Wed Aug 02 2006 - rhafer@suse.de
- Updated to Version 2.3.25
  * Add libldap_r TLS concurrency workaround (ITS#4583)
  * Fixed slapd acl selfwrite bug (ITS#4587)
  * Fixed various syncrepl and slapo-syncprov bugs (ITS#4582, 4622,
  4534,4613, 4589)
  * Fixed slapd-bdb/hdb lock bug with virtual root (ITS#4572)
  * Fixed slapd-bdb/hdb modrdn new entry disappearing bug (ITS#4616)
  * Fixed slapd-bdb/hdb cache job issue
  * Fixed slapo-ppolicy password hashing bug (ITS#4575)
  * Fixed slapo-ppolicy password modify pwdMustChange reset bug (ITS#4576)
  * Fixed slapo-ppolicy control can be critical (ITS#4596)
- Enabled CLDAP (LDAP over UDP) support
* Mon Jun 26 2006 - rhafer@suse.de
- Updated to Version 2.3.24
  * Fixed slapd syncrepl timestamp bug (delta-sync/cascade)
  (ITS#4567)
  * Fixed slapd-bdb/hdb non-root users adding suffix/root entries
  (ITS#4552)
  * Re-fixed slapd-ldap improper free bug in exop (ITS#4550)
  * Fixed slapd-ldif assert bug (ITS#4568)
  * Fixed slapo-syncprov crash under glued database (ITS#4562)
- cleaned up SLES10 update specific stuff
- added "chain-return-error" feature from HEAD to chain overlay
  (ITS#4570)
* Thu Jun 22 2006 - schwab@suse.de
- Don't use automake macros without using automake.
* Wed May 24 2006 - rhafer@suse.de
- Updated to Version 2.3.23
  * obsoletes the patches: libldap_ads-sasl-gssapi.dif,
  slapd-epollerr.dif
  * Fixed slapd-ldap improper free bug (ITS#4550)
  * Fixed libldap referral input destroy issue (ITS#4533)
  * Fixed libldap ldap_sort_entries tail bug (ITS#4536)
  * Fixed slapd runqueue use of freed memory (ITS#4517)
  * Fixed slapd thread pool init issue (ITS#4513)
  * Fixed slapd-bdb/hdb pre/post-read freeing (ITS#4532)
  * Fixed slapd-bdb/hdb pre/post-read unavailable issue (ITS#4538)
  * Fixed slapd-bdb/hdb referral issue (ITS#4548)
  * Fixed slapo-ppolicy BER tags issue (ITS#4528)
  * Fixed slapo-ppolicy rebind bug (ITS#4516)
  * For more details see the CHANGES file
- Install CHANGES file to /usr/share/doc/packages/openldap2
* Wed May 10 2006 - rhafer@suse.de
- Really apply the patch for Bug#160566
- slapd could crash while processing queries with pre-/postread
  controls (Bug#173877, ITS#4532)
* Fri Mar 24 2006 - rhafer@suse.de
- Backported fix from CVS for occasional crashes in referral
  chasing code (as used in e.g. back-meta/back-ldap).
  (Bug: #160566, ITS: #4448)
* Mon Mar 13 2006 - rhafer@suse.de
- openldap2 must obsolete -back-monitor and -back-ldap to have them
  removed during update (Bug: #157576)
* Fri Feb 17 2006 - rhafer@suse.de
- Add "external" to the list of supported SASL mechanisms
  (Bug: #151771)
* Thu Feb 16 2006 - rhafer@suse.de
- Error out when conversion from old configfile to config database
  fails (Bug: #135484,#135490 ITS: #4407)
* Mon Feb 13 2006 - rhafer@suse.de
- Don't ignore non-read/write epoll events (Bug: #149993,
  ITS: #4395)
- Added update message to /usr/share/update-messages/en/ and enable
  it, when update did not succeed.
* Thu Feb 09 2006 - rhafer@suse.de
- OPENLDAP_CHOWN_DIRS honors databases defined in include files
  (Bug: #135473)
- Fixed version numbers in README.update
- Fixed GSSAPI binds against Active Directory (Bug: #149390)
* Thu Feb 09 2006 - rhafer@suse.de
- OPENLDAP_CHOWN_DIRS honors databases defined in include files
  (Bug: #135473)
- Fixed version numbers in README.update
- Fixed GSSAPI binds against Active Directory (Bug: #149390)
* Fri Feb 03 2006 - rhafer@suse.de
- Cleaned up update procedure
- man-pages updates and fixes (Fate: #6365)
* Fri Jan 27 2006 - rhafer@suse.de
- Updated to 2.3.19 (Bug #144371)
* Fri Jan 27 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Jan 25 2006 - rhafer@suse.de
- Updated Admin Guide to latest version
- build slapcat from openldap-2.2.24 and install it to
  /usr/sbin/openldap-2.2-slapcat to be able to migrate from
  OpenLDAP 2.2.
- removed slapd-backbdb-dbupgrade which is no longer needed
- attempt to dump/reload bdb databases in %%{post}
- Update notes in README.update
* Fri Jan 13 2006 - rhafer@suse.de
- New sysconfig variable OPENLDAP_KRB5_KEYTAB
- Cleanup in default configuration and init scripts
* Wed Jan 11 2006 - rhafer@suse.de
- Updated to 2.3.17
- Remove OPENLDAP_RUN_DB_RECOVER from sysconfig file in %%post
  slapd does now automatically recover the database if needed
- Removed unneeded README.SuSE
- Small adjustments to the default DB_CONFIG file
* Mon Jan 09 2006 - rhafer@suse.de
- Updated to 2.3.16
* Mon Dec 19 2005 - rhafer@suse.de
- Fixed filelist (slapd-hdb man-page was missing)
* Fri Dec 09 2005 - rhafer@suse.de
- Fixed build on x86_64
* Wed Dec 07 2005 - rhafer@suse.de
- Merged -back-ldap and -back-monitor subpackages into the main
  package and don't build them as dynamic modules anymore.
- updated to OpenLDAP 2.3.13
* Mon Nov 28 2005 - rhafer@suse.de
- updated to OpenLDAP 2.3.12
* Wed Oct 26 2005 - rhafer@suse.de
- updated to OpenLDAP 2.3.11
- removed the "LDAP_DEPRECATED" workaround
* Mon Sep 26 2005 - rhafer@suse.de
- Add "LDAP_DEPRECATED" to ldap.h for now
* Fri Sep 23 2005 - rhafer@suse.de
- updated to OpenLDAP 2.3.7
* Tue Aug 16 2005 - rhafer@suse.de
- allow start_tls while chasing referrals (Bug #94355, ITS #3791)
* Mon Jul 04 2005 - rhafer@suse.de
- devel-subpackage requires openldap2-client of the same version
  (Bugzilla: #93579)
* Thu Jun 30 2005 - uli@suse.de
- build with -fPIE (not -fpie) to avoid GOT overflow on s390*
* Wed Jun 22 2005 - rhafer@suse.de
- build the server packages with -fpie/-pie
* Wed Jun 15 2005 - rhafer@suse.de
- updated to 2.2.27
* Wed May 25 2005 - rhafer@suse.de
- libldap-gethostbyname_r.dif: Use gethostbyname_r instead of
  gethostbyname in libldap. Should fix host lookups through
  nss_ldap (Bugzilla: #76173)
* Fri May 13 2005 - rhafer@suse.de
- Updated to 2.2.26
- made /%%{_libdir}]/sasl2/slapd.conf %%config(noreplace)
* Thu Apr 28 2005 - rhafer@suse.de
- Added /%%{_libdir}]/sasl2/slapd.conf to avoid warnings about
  unconfigured OTP mechanism (Bugzilla: #80588)
* Tue Apr 12 2005 - rhafer@suse.de
- added minimal timeout to startproc in init-script to let it
  report the "failed" status correctly in case of misconfiguration
  (Bugzilla: #76393)
* Mon Apr 04 2005 - rhafer@suse.de
- crl-check.dif: Implements CRL checking on client and server side
- use different base ports for differnt values of BUILD_INCARNATION
  (/.buildenv) to allow parallel runs of the test-suite on a single
  machine
* Mon Apr 04 2005 - uli@suse.de
- force yielding-select test to yes (test occasionally hangs QEMU)
* Fri Apr 01 2005 - uli@suse.de
- disable test suite on ARM (hangs QEMU)
* Tue Mar 29 2005 - rhafer@suse.de
- updated to 2.2.24
- enabled back-hdb
* Wed Mar 02 2005 - rhafer@suse.de
- syncrepl.dif: merged latest syncrepl fixes (Bugzilla: #65928)
- libldap-reinit-fdset.dif: Re-init fd_sets when select is
  interupted (Bugzilla #50076, ITS: #3524)
* Thu Feb 17 2005 - rhafer@suse.de
- checkproc_before_recover.dif: Check if slapd is stopped before
  running db_recover from the init script. (Bugzilla: #50962)
* Tue Feb 01 2005 - rhafer@suse.de
- Cleanup back-bdb databases in %%post, db-4.3 changed the
  transaction log format again.
- cosmetic fixes in init script
* Tue Jan 25 2005 - rhafer@suse.de
- updated to 2.2.23
- cleaned up #neededforbuild
- package should also build on older SuSE Linux releases now
- increased killproc timeout in init-script (Bugzilla: #47227)
* Thu Jan 13 2005 - rhafer@suse.de
- updated to 2.2.20
- Removed unneeded dependencies
* Fri Dec 10 2004 - kukuk@suse.de
- don't install *.la files
* Wed Nov 10 2004 - rhafer@suse.de
- updated to 2.2.18
- use kerberos-devel-packages in neededforbuild
* Fri Sep 24 2004 - ro@suse.de
- re-arranged specfile to sequence (header (package/descr)* rest)
  so the checking parser is not confused ...
* Fri Sep 24 2004 - rhafer@suse.de
- Added pre_checkin.sh to generate a separate openldap2-client
  spec-file from which the openldap2-client and openldap2-devel
  subpackages are built. Should reduce build time for libldap as
  the test-suite is only executed in openldap2.spec.
* Fri Sep 10 2004 - rhafer@suse.de
- libldap-result.dif: ldapsearch was hanging in select() when
  retrieving results from eDirectory through a StartTLS protected
  connection (Bugzilla #44942)
* Mon Aug 09 2004 - dobey@suse.de
- added ntlm support
* Tue Aug 03 2004 - rhafer@suse.de
- updated to 2.2.16
- Updated ACLs in slapd_conf.dif to disable default read access
  to the "userPKCS12" Attribute
- rc-check-conn.diff: When starting slapd wait until is accepts
  connections, or 10 seconds at maximum (Bugzilla #41354)
- Backported -o slp={on|off} feature from OpenLDAP Head and added
  new sysconfig variable (OPENLDAP_REGISTER_SLP) to be able
  to switch SLP registration on and off. (Bugzilla #39865)
- removed unneeded README.update
* Fri Apr 30 2004 - rhafer@suse.de
- updated to 2.2.11
- remove SLES8 update specific stuff
- Bugzilla #39652: Updated slapd_conf.dif to contain basic access
  control
- Bugzilla #39468: Added missing items to yast.schema
- fixed strict-aliasing compiler warnings (strict-aliasing.dif)
* Thu Apr 29 2004 - coolo@suse.de
- build with several jobs if available
* Mon Apr 19 2004 - rhafer@suse.de
- ldapi_url.dif: Fixed paths for LDAPI-socket, pid-file and
  args-file (Bugzilla #38790)
- ldbm_modrdn.dif: Fixed back-ldbm modrdn indexing bug (ITS #3059,
  Bugzilla #38915)
- modify_check_duplicates.dif: check for duplicate attribute
  values in modify requests (ITS #3066/#3097, Bugzilla #38607)
- updated and renamed yast2userconfig.schema to yast.schema as it
  contains more that only user configuration now
- syncrepl.dif: addtional fixes for syncrepl (ITS #3055, #3056)
- test_syncrepl_timeout: increased sleep timeout in syncrepl
  testsuite
* Thu Apr 01 2004 - rhafer@suse.de
- added "TLS_REQCERT allow" to /etc/openldap/ldap.conf, to make
  START_TLS work without access to the CA Certificate.
  (Bugzilla: #37393)
* Fri Mar 26 2004 - rhafer@suse.de
- fixed filelist
- check-build.sh (build on kernel >= 2.6.4 hosts only)
- yast2user.schema / slapd.conf fixed (#37076)
- don't check for TLS-options is init-script anymore (#33560)
- fixed various typos in README.update
* Wed Mar 17 2004 - rhafer@suse.de
- fixed build of openldap-2.1-slapcat (using correct db41 include
  files, build backends as on sles8)
- attempt to update bdb database and reindex ldbm database in %%{post}
- Update notes in README.update
- better default configuration (including default DB_CONFIG file)
- misc updates for the YaST schema
- fixed crasher in syncrepl-code (syncrepl.dif)
* Tue Mar 16 2004 - schwab@suse.de
- Fix type mismatch.
* Tue Mar 02 2004 - rhafer@suse.de
- updated to 2.2.6
- build a openldap-2.1-slapcat from 2.1.25 sources  to be able to
  migrate from SLES8 and SL 9.0
* Thu Feb 19 2004 - ro@suse.de
- added check-build.sh (build on 2.6 hosts only)
* Thu Feb 05 2004 - rhafer@suse.de
- updated to 2.2.5
- adjusted rfc2307bis.schema to support UTF-8 values in most
  attributes
- enabled proxycache-overlay (wiht fix to work with back-ldbm)
* Tue Jan 13 2004 - rhafer@suse.de
- updated to 2.2.4
- updated Admin Guide to most recent version
* Sat Jan 10 2004 - adrian@suse.de
- add %%defattr
- fix build as user
* Mon Dec 08 2003 - rhafer@suse.de
- updated to 2.1.25
- small fixes for the YaST user schema
* Tue Nov 11 2003 - rhafer@suse.de
- enabled SLP-support
* Fri Oct 17 2003 - kukuk@suse.de
- Remove unused des from neededforbuild
* Tue Sep 02 2003 - mt@suse.de
- Bugzilla #29859: fixed typo in sysconfig metadata,
  usage of OPENLDAP_LDAPS_INTERFACES in init script
- added /usr/lib/sasl2/slapd.conf permissions handling
- added sysconfig variable OPENLDAP_SLAPD_PARAMS=""
  to support additional slapd start parameters
- added sysconfig variable OPENLDAP_START_LDAPI=NO/yes
  for ldapi:/// (LDAP over IPC) URLs
* Thu Aug 14 2003 - rhafer@suse.de
- added activation metadata to sysconfig template (Bugzilla #28911)
- removed lint from specfile
* Thu Aug 07 2003 - rhafer@suse.de
- added %%stop_on_removal and %%restart_on_update calls
- bdb_addcnt.dif fixes a possible endless loop in id2entry()
- addonschema.tar.gz: some extra Schema files (YaST, RFC2307bis)
* Wed Jul 16 2003 - rhafer@suse.de
- removed fillup_only and call fillup_and_insserv correctly
- new Options in sysconfig.openldap: OPENLDAP_LDAP_INTERFACES,
  OPENLDAP_LDAPS_INTERFACES and OPENLDAP_RUN_DB_RECOVER
* Tue Jul 01 2003 - rhafer@suse.de
- updated to 2.1.22
- updated Admin Guide to most recent version
- build librewrite with -fPIC
* Mon Jun 16 2003 - rhafer@suse.de
- updated to 2.1.21
* Wed Jun 11 2003 - ro@suse.de
- fixed requires lines
* Mon May 26 2003 - rhafer@suse.de
- don't link back-ldap against librewrite.a, it's already linked
  into slapd (package should build on non-i386 Archs again)
* Fri May 23 2003 - rhafer@suse.de
- fixed dynamic build of back-ldap
- new subpackage back-ldap
* Tue May 20 2003 - rhafer@suse.de
- updated to version 2.1.20
- enabled dynamic backend modules
- new subpackages back-perl, back-meta and back-monitor
- remove unpacked files from BuildRoot
* Fri May 09 2003 - rhafer@suse.de
- updated to version 2.1.19
* Wed Apr 16 2003 - ro@suse.de
- fixed requires for devel-package ...
* Tue Apr 15 2003 - ro@suse.de
- fixed neededforbuild
* Thu Feb 13 2003 - kukuk@suse.de
- Enable IPv6 again
* Tue Feb 11 2003 - rhafer@suse.de
- added /etc/openldap to filelist
* Mon Feb 03 2003 - rhafer@suse.de
- switch default backend to ldbm
* Sun Feb 02 2003 - ro@suse.de
- fixed requires for devel package (cyrus-sasl2-devel)
* Fri Jan 31 2003 - rhafer@suse.de
- liblber.dif: Fixes two bugs in liblber by which remote attackers
  could crash the LDAP server (Bugzilla #22469, OpenLDAP ITS #2275
  and #2280)
* Tue Jan 14 2003 - choeger@suse.de
- build using sasl2
* Mon Jan 13 2003 - rhafer@suse.de
- updated to version 2.1.12
- added metadata to sysconfig template (Bug: #22666)
* Thu Nov 28 2002 - rhafer@suse.de
- updated to version 2.1.8
- added additional fix of 64bit archs
- added secpatch.dif to fix setuid issues in libldap
* Fri Sep 06 2002 - rhafer@suse.de
- fix for Bugzilla ID #18981, chown to OPENLDAP_USER didn't work
  with multiple database backend directories
* Mon Sep 02 2002 - rhafer@suse.de
- removed damoenstart_ipv6.diff and disabled IPv6 support due to
  massive problems with nss_ldap
* Mon Aug 26 2002 - rhafer@suse.de
- ldap_user.dif: slapd is now run a the user/group ldap (Bugzilla
  ID#17697)
* Fri Aug 23 2002 - rhafer@suse.de
- updated to version 2.1.4, which fixes tons of bugs
- added damoenstart_ipv6.diff (slapd was not starting when
  configured to listen on IPv4 and IPv6 interfaces, as done by the
  start script)
- added README.SuSE with some hints about the bdb-backend
- updated filelist to include only the man pages of the backends,
  that were built
* Thu Aug 15 2002 - rhafer@suse.de
- removed termcap and readline from neededforbuild
* Thu Aug 08 2002 - rhafer@suse.de
- enabled {CRYPT} passwords
- update filelist (added new manpages)
* Thu Jul 25 2002 - rhafer@suse.de
- patches for 64 bit architectures
* Fri Jul 19 2002 - rhafer@suse.de
- update to 2.1.3
* Fri Jul 05 2002 - kukuk@suse.de
- fix openldap2-devel requires
* Thu Jul 04 2002 - rhafer@suse.de
- switched back from cyrus-sasl2 to cyrus-sasl
* Wed Jul 03 2002 - rhafer@suse.de
- updated to OpenLDAP 2.1.2
- added the OpenLDAP Administration Guide
- enabled additional backends (ldap, meta, monitor)
* Mon Jun 10 2002 - olh@suse.de
- hack build/ltconfig to build shared libs on ppc64
* Wed Jun 05 2002 - rhafer@suse.de
- created /etc/sysconfig/openldap and OPENLDAP_START_LDAPS variable
  to enable ldap over ssl support
* Thu Mar 07 2002 - rhafer@suse.de
- Fix for Bugzilla ID#14569 (added cyrus-sasl-devel openssl-devel
  to the "Requires" Section of the -devel subpackage)
* Mon Feb 18 2002 - rhafer@suse.de
- updated to the latest STABLE release (2.0.23) which fixes some
  nasty bugs see ITS #1562,#1582,#1577,#1578
* Thu Feb 07 2002 - rhafer@suse.de
- updated to the latest release (which fixes a index corruption
  bug)
- cleanup in neededforbuild
- small fixes for the init-scripts
* Thu Jan 17 2002 - rhafer@suse.de
- updated to the latest stable release (2.0.21)
* Wed Jan 16 2002 - egmont@suselinux.hu
- removed periods and colons from startup/shutdown messages
* Tue Jan 15 2002 - rhafer@suse.de
- updated to v2.0.20 (which fixes a security hole in ACL
  processing)
* Fri Jan 11 2002 - rhafer@suse.de
- converted archive to bzip2
- makes use of %%{_libdir} now
- set CFLAGS to -O0 for archs ia64, s390(x) and alpha otherwise
  the test suite fails on these archs
- changed slapd.conf to store the database under /var/lib/ldap
  (this patch was missing in the last versions by accident)
* Mon Jan 07 2002 - rhafer@suse.de
- update to v2.0.19
* Thu Dec 06 2001 - rhafer@suse.de
- eliminated START_LDAP, START_SLURPD variables in rc.config
- created separate init script for slurpd
- moved init scripts from dif to separate source tgz
* Fri Oct 26 2001 - choeger@suse.de
- update to v2.0.18
* Mon Oct 15 2001 - choeger@suse.de
- update to v2.0.17
  added a sleep to the restart section
  moved some manpages to the client package
* Mon Oct 01 2001 - choeger@suse.de
- update to v2.0.15
* Wed Sep 12 2001 - choeger@suse.de
- backported the full bugfix from openldap-2.0.14
* Tue Sep 11 2001 - choeger@suse.de
- Bugfix for slurpd millionth second bug (ITS#1323)
* Mon Sep 10 2001 - choeger@suse.de
- moved ldapfilter.conf ldaptemplates.conf ldapsearchprefs.conf
  to openldap2-client package
* Mon Sep 03 2001 - choeger@suse.de
- update to version 2.0.12
* Mon Jul 02 2001 - choeger@suse.de
- bugfix: init script was not LSB compliant, Bugzilla ID#9072
* Tue Jun 19 2001 - ro@suse.de
- fixed for autoconf again
* Fri Jun 15 2001 - choeger@suse.de
- update to 2.0.11
- removed autoconf in specfile, because it doesn't work
* Wed May 23 2001 - choeger@suse.de
- update to version 2.0.10 (minor fixes)
* Tue May 22 2001 - choeger@suse.de
- update to version 2.0.9
* Mon Apr 23 2001 - choeger@suse.de
- removed kerberos support
- added aci support
* Fri Apr 20 2001 - choeger@suse.de
- added kerberos support
* Thu Apr 05 2001 - choeger@suse.de
- moved section 5 and 8 manpages to the server part of package
* Wed Mar 14 2001 - kukuk@suse.de
- Move *.so links into -devel package
- -devel requires -client
* Thu Mar 08 2001 - choeger@suse.de
- split up into openldap2-client and -devel
* Tue Feb 27 2001 - ro@suse.de
- changed neededforbuild <cyrus-sasl> to <cyrus-sasl cyrus-sasl-devel>
* Fri Feb 23 2001 - ro@suse.de
- added readline/readline-devel to neededforbuild (split from bash)
* Thu Jan 04 2001 - choeger@suse.de
- bugfix: slapd.conf rename /var/lib/openldap-ldbm to
  /var/lib/ldap
  init script: use $remote_fs
* Tue Jan 02 2001 - olh@suse.de
- use script name in %%post
* Thu Dec 07 2000 - choeger@suse.de
- bugfix from Andreas Jaeger:
  workaround for glibc2.2, detach
* Fri Dec 01 2000 - ro@suse.de
- hacked configure for apparently broken pthread
* Fri Dec 01 2000 - ro@suse.de
- fixed spec
* Thu Nov 23 2000 - choeger@suse.de
- made configs %%config(noreplace) (Bug 4112)
- fixed neededforbuild
* Wed Nov 22 2000 - choeger@suse.de
- adopted new init scheme
* Wed Nov 15 2000 - choeger@suse.de
- fixed neededforbuild
* Fri Nov 10 2000 - choeger@suse.de
- added buildroot
* Tue Nov 07 2000 - choeger@suse.de
- long package name
- new version, 2.0.7
* Fri Oct 06 2000 - choeger@suse.de
- first package of openldap2 (v2.0.6)
