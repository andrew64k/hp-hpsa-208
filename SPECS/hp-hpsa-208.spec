%define module_dir updates

Summary: HPSA Driver HP RAID cards
Name: hp-hpsa-208
Version: 3.4.20.208
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz

Patch0: 0001-makefile.patch
Patch1: 0002-define-kernel.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
HPSA Driver HP RAID cards

%prep
%autosetup -n %{name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{kernel_version}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Fri Dec 20 2024 Andrew Lindh <andrew@netplex.net> - 3.4.20.208-1
- Current version 3.4.20-208 (210 tar package)
- Source https://sourceforge.net/projects/cciss/files/hpsa-3.0-tarballs/

