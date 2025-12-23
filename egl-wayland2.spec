%global commit0 f4a2d326cc2eb32d6cf6c0b64082f1c53c770049
%global date 20251222
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

Name:           egl-wayland2
Version:        1.0.1%{!?tag:~%{date}git%{shortcommit0}}
Release:        9%{?dist}
Summary:        Dma-buf-based Wayland external platform library
# src/wayland/dma-buf.h is GPL 2, rest is Apache 2.0
License:        Apache-2.0 and GPL-2.0
URL:            https://github.com/NVIDIA/%{name}

%if 0%{?tag:1}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
%endif

# Bundle missing Wayland Protocols:
Source1:        https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.45/staging/fifo/fifo-v1.xml
Source2:        https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.45/staging/linux-drm-syncobj/linux-drm-syncobj-v1.xml
Source3:        https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.45/staging/commit-timing/commit-timing-v1.xml
Patch0:         %{name}-missing-protocols.patch

BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  libtool
BuildRequires:  pkgconfig(egl) >= 1.5
BuildRequires:  pkgconfig(eglexternalplatform) >= 1.1
BuildRequires:  pkgconfig(gbm) >= 21.2.0
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl-backend) >= 3
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)

# Required for directory ownership
Requires:       libglvnd-egl%{?_isa}

%description
This is a new implementation of the EGL External Platform Library for Wayland
(EGL_KHR_platform_wayland), using the NVIDIA driver's new platform surface
interface, which simplifies a lot of the library and improves window resizing.

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} src/wayland/

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} -name '*.la' -delete
rm -f %{buildroot}%{_libdir}/libnvidia-egl-wayland2.so

%files
%doc README.md
%license LICENSE
%{_libdir}/libnvidia-egl-wayland2.so.1
%{_libdir}/libnvidia-egl-wayland2.so.1.*
%{_datadir}/egl/egl_external_platform.d/09_nvidia_wayland2.json

%changelog
* Tue Dec 23 2025 Simone Caronni <negativo17@gmail.com> - 1.0.1~20251222gitf4a2d32-9
- Update to latest snapshot.

* Mon Dec 15 2025 Simone Caronni <negativo17@gmail.com> - 1.0.1~20251213gitada1c37-8
- Update to latest snapshot.

* Thu Nov 27 2025 Simone Caronni <negativo17@gmail.com> - 1.0.1~20251124git3e5b643-7
- Update to latest snapshot.

* Mon Nov 17 2025 Simone Caronni <negativo17@gmail.com> - 1.0.1~20251112git0c15809-6
- Update to latest snapshot.

* Wed Oct 22 2025 Simone Caronni <negativo17@gmail.com> - 1.0.1~20251022gite16cb0f-5
- Update to latest snapshot.

* Mon Oct 20 2025 Simone Caronni <negativo17@gmail.com> - 1.0.1~20251018git295712b-4
- Update to latest snapshot.

* Thu Aug 07 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0~20250806gitd4deb7c-3
- Update to latest snapshot.

* Wed Aug 06 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0~20250806gitd4deb7c-2
- Update to latest snapshot.

* Wed Aug 06 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0~20250805git33c9941-1
- First import based on Fedora egl-wayland2.
