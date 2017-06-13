%global gitdate 20170612
%global commit0 4e663566dda9fea8cbff8e58f65e91863cbf42a4
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           mpv
Epoch:          1
Version:        0.25.0
Release:        3%{?gver}%{dist}
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+
URL:            http://%{name}.io/
Source0:        https://github.com/%{name}-player/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{version}.tar.gz

# set defaults for Fedora
# Patch0:       %{name}-config.patch

BuildRequires:  pkgconfig(alsa)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(dvdread)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(enca)
BuildRequires:  ffmpeg-devel
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libguess)
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libquvi-0.9)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(lua-5.1)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(uchardet) >= 0.0.5
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  waf
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python-docutils

BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  perl(Encode)

Requires:       hicolor-icon-theme
Provides:       mplayer-backend

%description
Mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special
input URL types are available to read input from a variety of sources other
than disk files. Depending on platform, a variety of different video and audio
output methods are supported.

%package libs
Summary: Dynamic library for Mpv frontends
Epoch: 1
Provides: libmpv = 1:%{version}-%{release}
Obsoletes: libmpv < 1:%{version}-%{release}

%description libs
This package contains the dynamic library libmpv, which provides access to Mpv.

%package libs-devel
Summary: Development package for libmpv
Epoch: 1
Requires: mpv-libs%{_isa} = 1:%{version}-%{release}
Provides: libmpv-devel = 1:%{version}-%{release}
Obsoletes: libmpv-devel < 1:%{version}-%{release}

%description libs-devel
Libmpv development header files and libraries.

%prep
%setup -n %{name}-%{commit0}
#%patch0 -p1


%build
CFLAGS="${RPM_OPT_FLAGS}" \
LDFLAGS="${RPM_LD_FLAGS}" \
waf configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_docdir}/%{name} \
    --confdir=%{_sysconfdir}/%{name} \
    --disable-build-date \
    --enable-libmpv-shared \
    --enable-sdl2 \
    --enable-encoding

waf -v build %{?_smp_mflags}

%install
waf install --destdir=%{buildroot}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dpm 644 README.md etc/input.conf etc/mpv.conf -t %{buildroot}%{_docdir}/%{name}

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}
%license LICENSE Copyright
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_mandir}/man1/%{name}.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf

%files libs
%license LICENSE Copyright
%{_libdir}/libmpv.so.*

%files libs-devel
%{_includedir}/%{name}
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc


%changelog

* Mon Jun 12 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.25.0-3.git4e66356
- Updated to 0.25.0-3.git4e66356

* Sun May 21 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.25.0-2
- Rebuilt

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.25.0-1
- Rebuilt for libbluray

* Sun Feb 26 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.24.0-1
- Updated to 0.24.0-1

* Tue Dec 27 2016  Pavlo Rudyi <paulcarroty@riseup.net> - 0.23.0-1
- Updated to 0.23-2

* Wed Nov 23 2016  Pavlo Rudyi <paulcarroty@riseup.net> - 0.22.0-2
- Add Epoch 1 to prevent not-update problem

* Mon Nov 21 2016  Pavlo Rudyi <paulcarroty@riseup.net> - 0.22.0-1
- Updated to 0.22

* Fri Oct 21 2016  Pavlo Rudyi <paulcarroty@riseup.net> - 0.21.0-2
- Mass rebuild

* Fri Oct 21 2016  Pavlo Rudyi <paulcarroty@riseup.net> - 0.21.0-1
- Update to 0.21

* Sat Aug 27 2016  Pavlo Rudyi <paulcarroty@riseup.net> - 0.20.0-1
- Update to 0.20

* Tue Aug 16 2016  Pavlo Rudyi <paulcarroty@riseup.net> - 0.19.0-1
- Update to 0.19

* Thu Aug 04 2016  Pavlo Rudyi <paulcarroty@riseup.net> - 0.18.1-1
- Update to 0.18.1

* Thu Jun 30 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.18.0-6
- Rebuilt for FFmpeg 3.1

* Sun Jun 26 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 0.18.0-5
- Mass rebuild with new ffmpeg

* Sat Jun 25 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 0.18.0-4
- Update to 0.18

* Thu Jun  9 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 0.17.0-4
- Fixed bash completion

* Thu Jun  9 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 0.17.0-3
- Add bash completion

* Tue Apr 26 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 0.17.0-2
- Rebuild for Fedora 24 with new depends

* Mon Apr 11 2016 Maxim Orlov <murmansksity@gmail.com> - 1:0.17.0-1.R
- Update to 0.17.0

* Mon Feb 29 2016 Maxim Orlov <murmansksity@gmail.com> - 1:0.16.0-1.R
- Update to 0.16.0

* Mon Jan 18 2016 Maxim Orlov <murmansksity@gmail.com> - 1:0.15.0-1.R
- Update to 0.15.0

* Mon Dec 14 2015 Maxim Orlov <murmansksity@gmail.com> - 1:0.14.0-1.R
- Update to 0.14.0

* Fri Nov 13 2015 Vasiliy N. Glazov <vascom2@gmail.com> - 0.13.0-2.R
- Clean spec
- Use fedora gcc flags

* Thu Nov 12 2015 Vasiliy N. Glazov <vascom2@gmail.com> - 0.13.0-1.R
- update to 0.13.0

* Wed Nov 11 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.11.0-0.1.R
- update to 0.11.0

* Tue May 05 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.1-3
- Revert patch for reject lua 5.3

* Tue May 05 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.1-2
- Disable SDL2 backend
- Apply patch to fix osc bar

* Mon May 04 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1
- Enable SDL2 backend

* Tue Apr 28 2015 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-3
- Conditionalize old waf patch

* Tue Apr 28 2015 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-2
- Rebuilt

* Mon Apr 13 2015 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-1
- Updated

* Wed Jan 28 2015 Miro Hrončok <mhroncok@redhat.com> - 0.7.3-1
- Updated

* Mon Dec 22 2014 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-3
- Slightly change the waf patch

* Mon Dec 22 2014 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-2
- Add patch to allow waf 1.7

* Sat Dec 13 2014 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-1
- New version 0.7.1
- Rebuilt new lirc (#3450)

* Tue Nov 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.6.0-3
- Rebuilt for vaapi 0.36

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 0.6.0-2
- Rebuilt for FFmpeg 2.4.3

* Sun Oct 12 2014 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-1
- New version 0.6.0

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-2
- Rebuilt for FFmpeg 2.4.x

* Wed Sep 03 2014 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-1
- New version 0.5.1
- Add BR ncurses-devel (#3233)

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.4.0-2
- Rebuilt for ffmpeg-2.3

* Tue Jul 08 2014 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-1
- New version 0.4.0

* Tue Jun 24 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.11-1
- New version 0.3.11

* Tue Mar 25 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.6-2
- Rebuilt for new libcdio and libass

* Thu Mar 20 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.6-1
- New version 0.3.6

* Fri Feb 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.5-2
- Rebuilt for mistake

* Fri Feb 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.5-1
- New version 0.3.5

* Sat Jan 25 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.3-1
- New version 0.3.3

* Wed Jan 01 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Use upstream .desktop file

* Wed Jan 01 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-1
- New version 0.3.0
- Switch to waf
- Add some tricks from openSUSE
- Removed already included patch

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-8
- Added patch for https://fedoraproject.org/wiki/Changes/FormatSecurity

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-7
- Support wayland

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-6
- Rebuilt

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-5
- Fixed wrong license tag (see upstream a5507312)

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-4
- Added libva (#3065)

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-3
- Added lua and libquvi (#3025)

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-2
- Rebuilt for mistakes

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-1
- New version 0.2.4

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-4
- There's no longer AUTHORS file in %%doc
- Install icons

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-3
- Rebased config patch

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-2
- Proper sources for all branches

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-1
- New upstream version

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-4
- Fixing cvs errors

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-3
- Add desktop file

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-2
- Do not use xv as default vo

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-1
- New upstream release

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-4
- Rebuilt

* Mon Sep 09 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-3
- Added BR ffmpeg-libs

* Tue Aug 27 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-2
- Reduced BRs a lot (removed support for various stuff)
- Make smbclient realized
- Changed the description to the text from manual page

* Mon Aug 19 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-1
- Initial spec
- Inspired a lot in mplayer.spec
