# TODO
# - webapps support: apache1, lighttpd
# - find nice way to split it into 4 parts: user, admin, domain-admin and common
# - package css and templates as config.
# - put config part of vacation.pl into separate file (there is configuration part in that).
Summary:	Web Based Management tool created for Postfix
Summary(pl.UTF-8):	Narzędzie WWW do zarządzania Postfiksem
Name:		postfixadmin
Version:	2.1.0
Release:	3
License:	freely usable and distributable with restrictions (see URL)
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/postfixadmin/%{name}-%{version}.tgz
# Source0-md5:	89043e52796298f44a06d65eaddaef09
Source1:	%{name}.conf
Patch0:		%{name}-pl.patch
Patch1:		%{name}-pgsql.patch
Patch2:		%{name}-non_local_db.patch
Patch3:		%{name}-pl_typo_fix.patch
Patch4:		%{name}-preg_fix.patch
Patch5:		%{name}-case_insensitive_mailbox.patch
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
Suggests:	webserver(indexfile)
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

%description vacation
Vacations script for Postfix.

%description vacation -l pl.UTF-8
Skrypt wakacje dla Postfiksa.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/templates,%{_appdir}/{admin,images,languages,templates,users},/var/spool/vacation}

install *.php $RPM_BUILD_ROOT%{_appdir}
install admin/*.php $RPM_BUILD_ROOT%{_appdir}/admin
install images/* $RPM_BUILD_ROOT%{_appdir}/images
install languages/* $RPM_BUILD_ROOT%{_appdir}/languages
install templates/*.php $RPM_BUILD_ROOT%{_appdir}/templates
install stylesheet.css $RPM_BUILD_ROOT%{_appdir}
install users/* $RPM_BUILD_ROOT%{_appdir}/users
install VIRTUAL_VACATION/vacation.pl $RPM_BUILD_ROOT/var/spool/vacation

# config:
install config.inc.php.sample $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

# Many things can and should be modified by user:
for file in `ls templates/*.tpl`; do
	install $file $RPM_BUILD_ROOT%{_sysconfdir}/templates
	ln -s %{_sysconfdir}/$file $RPM_BUILD_ROOT%{_appdir}/templates
done

# MOTD should be empty by default?
for motd in motd-admin.txt motd-users.txt motd.txt; do
	:> $RPM_BUILD_ROOT%{_sysconfdir}/$motd
	ln -s %{_sysconfdir}/$motd $RPM_BUILD_ROOT%{_appdir}
done

# We don't need it:
rm -f $RPM_BUILD_ROOT%{_appdir}/setup.php \
	$RPM_BUILD_ROOT%{_appdir}/VIRTUAL_VACATION/index.php

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

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc *.TXT ADDITIONS motd*.txt
%dir %attr(750,root,http) %{_sysconfdir}
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(750,root,http) %dir %{_sysconfdir}/templates
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/templates/*.tpl
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/motd*
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/motd*
%{_appdir}/admin
%{_appdir}/images
%{_appdir}/languages
%{_appdir}/stylesheet.css
%{_appdir}/templates
%{_appdir}/users

%files vacation
%defattr(644,root,root,755)
%doc VIRTUAL_VACATION
%attr(700,vacation,vacation) %dir /var/spool/vacation
%attr(700,vacation,vacation) %config(noreplace) %verify(not md5 mtime size) /var/spool/vacation/vacation.pl
