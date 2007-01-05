# TODO
# - webapps support: apache1, lighttpd
# - *motd.txt should marked as config and placed in /etc ?
# - maybe split into 3 subpackages: admin, users, common?
Summary:	Web Based Management tool created for Postfix
Summary(pl):	Narzêdzie WWW do zarz±dzania Postfiksem
Name:		postfixadmin
Version:	2.1.0
Release:	0.3
License:	freely usable and distributable with restrictions (see URL)
Group:		Networking/Utilities
Source0:	http://high5.net/page7_files/%{name}-%{version}.tgz
# Source0-md5:	89043e52796298f44a06d65eaddaef09
Source1:	%{name}.conf
URL:		http://high5.net/postfixadmin/
BuildRequires:	rpmbuild(macros) >= 1.264
Requires:	php(pcre)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Postfix Admin is a Web Based Management tool created for Postfix. It
is a PHP based application that handles Postfix Style Virtual Domains
and Users that are stored in MySQL.

Postfix Admin supports:
- Virtual Mailboxes / Virtual Aliases / Forwarders.
- Domain to Domain forwarding / Catch-All.
- Vacation (auto-response) for Virtual Mailboxes.
- Quota / Alias & Mailbox limits per domain.
- Backup MX.
- Packaged with over 25 languages... (Thank you all for sending them!)

%description -l pl
Postfix Admin to oparte na WWW narzêdzie do zarz±dzania Postfiksem.
Jest to oparta na PHP aplikacja obs³uguj±ca wirtualne domeny i
u¿ytkowników w stylu Postfiksa zapisane w bazie MySQL.

Postfix Admin obs³uguje:
- wirtualne skrzynki, wirtualne aliasy, przekazywanie
- przekazywanie z domeny do domeny, przechwytywanie ("catch-all")
- autoresponder (vacation) dla skrzynek wirtualnych
- quoty, ograniczenia aliasów i skrzynek dla domen
- zapasowe MX-y
- komunikaty w ponad 25 jêzyków (podziêkowania za przys³anie ich!)

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{admin,images,languages,templates,users}}

install *.php $RPM_BUILD_ROOT%{_appdir}
install admin/*.php $RPM_BUILD_ROOT%{_appdir}/admin
install images/* $RPM_BUILD_ROOT%{_appdir}/images
install languages/* $RPM_BUILD_ROOT%{_appdir}/languages
install templates/* $RPM_BUILD_ROOT%{_appdir}/templates
install users/* $RPM_BUILD_ROOT%{_appdir}/users

# config:
install config.inc.php.sample $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc *.TXT ADDITIONS VIRTUAL_VACATION
%dir %attr(750,root,http) %{_sysconfdir}
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/admin
%{_appdir}/images
%dir %{_appdir}/languages
%{_appdir}/languages/index.php
%lang(bg) %{_appdir}/languages/bg.lang
%lang(ca) %{_appdir}/languages/ca.lang
%lang(cn) %{_appdir}/languages/cn.lang
%lang(cs) %{_appdir}/languages/cs.lang
%lang(da) %{_appdir}/languages/da.lang
%lang(de) %{_appdir}/languages/de.lang
%lang(en) %{_appdir}/languages/en.lang
%lang(es) %{_appdir}/languages/es.lang
%lang(et) %{_appdir}/languages/et.lang
%lang(eu) %{_appdir}/languages/eu.lang
%lang(fi) %{_appdir}/languages/fi.lang
%lang(fo) %{_appdir}/languages/fo.lang
%lang(fr) %{_appdir}/languages/fr.lang
%lang(hu) %{_appdir}/languages/hu.lang
%lang(is) %{_appdir}/languages/is.lang
%lang(it) %{_appdir}/languages/it.lang
%lang(mk) %{_appdir}/languages/mk.lang
%lang(nl) %{_appdir}/languages/nl.lang
%lang(nn) %{_appdir}/languages/nn.lang
%lang(pl) %{_appdir}/languages/pl.lang
%lang(pt_BR) %{_appdir}/languages/pt-br.lang
%lang(ru) %{_appdir}/languages/ru.lang
%lang(sl) %{_appdir}/languages/sl.lang
%lang(sv) %{_appdir}/languages/sv.lang
%lang(tr) %{_appdir}/languages/tr.lang
%lang(tw) %{_appdir}/languages/tw.lang
%{_appdir}/templates
%{_appdir}/users
