# TODO
# - webapps support: lighttpd
# - find nice way to split it into 3 parts: user, admin and common
# - package css and templates as config.
# - put config part of vacation.pl into separate file (there is configuration part in that).
# - what to do with upgrade.php?
# - setup.php and upgrade.php should be marked as "missingok"
Summary:	Web Based Management tool created for Postfix
Summary(pl.UTF-8):	Narzędzie WWW do zarządzania Postfiksem
Name:		postfixadmin
Version:	2.3.5
Release:	2
License:	GPL v2+
Group:		Networking/Mail
Source0:	http://downloads.sourceforge.net/project/postfixadmin/postfixadmin/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9a72ed8d827fa2c7f641001f2aa87814
Source1:	%{name}.conf
URL:		http://postfixadmin.com/
BuildRequires:	rpmbuild(macros) >= 1.264
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/groupadd
Requires:	php(pcre)
Requires:	php(session)
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Suggests:	php(imap)
Suggests:	webserver(indexfile)
Conflicts:	apache-base < 2.4.0-1
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

%description -l pl.UTF-8
Postfix Admin to oparte na WWW narzędzie do zarządzania Postfiksem.
Jest to oparta na PHP aplikacja obsługująca wirtualne domeny i
użytkowników w stylu Postfiksa zapisane w bazie MySQL.

Postfix Admin obsługuje:
- wirtualne skrzynki, wirtualne aliasy, przekazywanie
- przekazywanie z domeny do domeny, przechwytywanie ("catch-all")
- autoresponder (vacation) dla skrzynek wirtualnych
- quoty, ograniczenia aliasów i skrzynek dla domen
- zapasowe MX-y
- komunikaty w ponad 25 języków (podziękowania za przysłanie ich!)

%package vacation
Summary:	Vacations script for Postfix
Summary(pl.UTF-8):	Skrypt wakacje dla Postfiksa
Group:		Networking/Utilities
# too bad, script is installed (and possibly configured inside) in /var/spool,
# so perlprov won't detect it :/
Requires:	perl-Email-Valid
Requires:	perl-MIME-Charset
Requires:	perl-MIME-EncWords
Requires:	perl-Mail-Sendmail
Suggests:	perl-DBD-Pg
Suggests:	perl-DBD-mysql

%description vacation
Vacations script for Postfix.

%description vacation -l pl.UTF-8
Skrypt wakacje dla Postfiksa.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{admin,css,images,languages,model,templates,users},/var/spool/vacation}

install *.php $RPM_BUILD_ROOT%{_appdir}
install admin/*.php $RPM_BUILD_ROOT%{_appdir}/admin
install css/*.css $RPM_BUILD_ROOT%{_appdir}/css
install images/* $RPM_BUILD_ROOT%{_appdir}/images
install languages/* $RPM_BUILD_ROOT%{_appdir}/languages
install model/* $RPM_BUILD_ROOT%{_appdir}/model
install templates/* $RPM_BUILD_ROOT%{_appdir}/templates
install users/* $RPM_BUILD_ROOT%{_appdir}/users
install VIRTUAL_VACATION/vacation.pl $RPM_BUILD_ROOT/var/spool/vacation

# config:
install config.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

# MOTD should be empty by default?
for motd in motd-admin.txt motd-users.txt motd.txt; do
	:> $RPM_BUILD_ROOT%{_sysconfdir}/$motd
	ln -s %{_sysconfdir}/$motd $RPM_BUILD_ROOT%{_appdir}
done

# We don't need it:
rm -f $RPM_BUILD_ROOT%{_appdir}/VIRTUAL_VACATION/index.php

%clean
rm -rf $RPM_BUILD_ROOT

%pre vacation
%groupadd -g 219 vacation
%useradd -u 219 -d /var/spool/vacation/ -s /bin/false -c "Vacation scripts" -g vacation vacation

%postun vacation
if [ "$1" = "0" ]; then
	%userremove vacation
	%groupremove vacation
fi

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc ADDITIONS CHANGELOG.TXT INSTALL.TXT motd*.txt
%dir %attr(750,root,http) %{_sysconfdir}
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/motd*
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/motd*
%{_appdir}/admin
%{_appdir}/css
%{_appdir}/images
%{_appdir}/languages
%{_appdir}/model
%{_appdir}/templates
%{_appdir}/users

%files vacation
%defattr(644,root,root,755)
%doc VIRTUAL_VACATION
%attr(700,vacation,vacation) %dir /var/spool/vacation
%attr(700,vacation,vacation) %config(noreplace) %verify(not md5 mtime size) /var/spool/vacation/vacation.pl
