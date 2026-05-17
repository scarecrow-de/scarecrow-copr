## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global xdg_desktop_portal_version 1.19.1

Name:           xdg-desktop-portal-scarecrow
Version:        1.15.3
Release:        %autorelease
Summary:        Backend implementation for xdg-desktop-portal using GTK+

License:        LGPL-2.0-or-later
URL:            https://github.com/scarecrow-de/%{name}
Source0:        https://github.com/scarecrow-de/%{name}/archive/refs/heads/main.tar.gz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
BuildRequires:  pkgconfig(gtk+-unix-print-3.0)
BuildRequires:  pkgconfig(xdg-desktop-portal) >= %{xdg_desktop_portal_version}
BuildRequires:  systemd-rpm-macros
Requires:       dbus
Requires:       gsettings-desktop-schemas
Requires:       xdg-desktop-portal >= %{xdg_desktop_portal_version}

# https://github.com/containers/composefs/pull/229#issuecomment-1838735764
%if 0%{?rhel} >= 10
ExcludeArch:    %{ix86}
%endif

# This portal is recommended if you have installed any app that uses GTK. (It's
# also recommended if you have any such app installed via flatpak or snap, but
# that is impossible to detect here.)
Supplements:    gtk3
Supplements:    gtk4

%description
A backend implementation for xdg-desktop-portal that is used in Scarecrow.


%prep
%autosetup -p1 -n %{name}-main


%build
# All backends that are disabled are instead provided by
# xdg-desktop-portal-gnome, to keep this package free of GNOME dependencies.
# The appchooser and settings backends are enabled for non-GNOME GTK
# applications.
%meson \
    -Dappchooser=enabled \
    -Dsettings=enabled \
    -Dlockdown=disabled \
    -Dwallpaper=disabled \
    %{nil}
%meson_build


%install
%meson_install
%find_lang %{name}


%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service


%files -f %{name}.lang
%license COPYING
%doc NEWS README.md
%{_libexecdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.scarecrow.service
%{_datadir}/xdg-desktop-portal/portals/scarecrow.portal
%{_userunitdir}/%{name}.service



%changelog
* Sun May 17 2026 Marcel Mrówka <micro.mail88@gmail.com> - 1.15.3-1
- Initial xdg-desktop-portal-scarecrow release
