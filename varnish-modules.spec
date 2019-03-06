%global varnishver 4.1.11
%global modulesver 0.13.0
# To get vabi and vabistrict, run rpm -qip --provides <varnish-rpm-package>
# For the varnish version you are building against.
%global vabi 3.2
%global vabistrict 61367ed17d08a9ef80a2d42dc84caef79cdeee7a
#% global vplus  -plus
#% global vbranch .v4.1plus
%global vbranch .v4.1

Name: varnish-modules
Summary: Collection of varnish modules.
Version: %{varnishver}_%{modulesver}
Release: 1%{?dist}
License: BSD
Group: System Environment/Daemons
URL: https://github.com/varnish/varnish-modules
Source0: https://download.varnish-software.com/%{name}/%{name}-%{modulesver}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: varnish = %varnishver
Requires: varnishabi-%vabi
Requires: varnishabi-strict-%vabistrict
Buildrequires: varnish = %varnishver
Buildrequires: varnish-devel = %varnishver

%description
Collection of Varnish modules to add functionality to Varnish cache server.
Includes: vmod-cookie, vmod-header, vmod-saintmode, vmod-softpurge,
vmod-tcp, vmod-var, vmod-vsthrottle, and vmod-xkey.

%prep
%setup -q -n %{name}-%{modulesver}

%build
export RST2MAN=/bin/true
%configure \
  --docdir=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
# We have to remove rpath - not allowed in Fedora
# (This problem only visible on 64 bit arches)
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g;
        s|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%check
make check


%install
# Clean buildroot on older el variants
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# None of these for fedora/epel
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'
find %{buildroot}/%{_libdir}/ -name  '*.a' -exec rm -f {} ';'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/varnish*/vmods/
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%license LICENSE
%endif
%doc AUTHORS CHANGES.rst README.rst COPYING docs/*.rst
%{_mandir}/man3/*.3*

%changelog
* Sun Apr 15 2018 Jeff Sheltren <jeff@tag1consulting.com> - 4.1.9_0.13.0-1
- Update modules to 0.13.0
- Build for Varnish 4.1.9

* Fri Jun 23 2017 Jeff Sheltren <jeff@tag1consulting.com> - 4.1.6_0.12.1-3
- Update for Varnish 4.1.6, bump strict ABI

* Tue Jun 13 2017 Jeff Sheltren <jeff@tag1consulting.com> - 4.1.5_0.12.1-2
- Update versioning to contain varnish version built against.
 
* Fri Jun  9 2017 Jeff Sheltren <jeff@tag1consulting.com> - 0.12.1-1
- Update to 0.12.1

* Thu Apr 20 2017 Jeff Sheltren <jeff@tag1consulting.com> - 0.11.0-1
- Initial packaging of varnish-modules based on vmod-memcached spec.

* Wed Dec 07 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> - 1.0.0-2
- Rebuild for varnish-4.1.1

* Tue Sep 13 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> - 1.0.0-1
- Wrap for fedora/epel/copr

