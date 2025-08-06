%global commit0 d4deb7c371aac2a304522ffc297fcb71e6507699
%global date 20250806
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

Name:           egl-wayland2
Version:        1.0.0%{!?tag:~%{date}git%{shortcommit0}}
Release:        2%{?dist}
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
* Wed Aug 06 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0~20250806gitd4deb7c-2
- Update to latest snapshot.

* Wed Aug 06 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0~20250805git33c9941-1
- First import based on Fedora egl-wayland2.
