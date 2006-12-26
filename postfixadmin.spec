# TODO
# - %%lang for language files
Summary:	Web Based Management tool created for Postfix
Summary(pl):	Narzêdzie WWW do zarz±dzania Postfiksem
Name:		postfixadmin
Version:	2.1.0
Release:	0.1
License:	freely usable and distributable with restrictions (see URL)
Group:		Networking/Utilities
Source0:	http://high5.net/page7_files/%{name}-%{version}.tgz
# Source0-md5:	89043e52796298f44a06d65eaddaef09
#Source1:	%{name}.conf
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.TXT ADDITIONS VIRTUAL_VACATION
%dir %attr(750,root,http) %{_sysconfdir}
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/admin
%{_appdir}/images
%{_appdir}/languages
%{_appdir}/templates
%{_appdir}/users
