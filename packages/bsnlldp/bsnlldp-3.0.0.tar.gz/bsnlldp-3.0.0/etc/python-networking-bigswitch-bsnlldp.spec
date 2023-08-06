%global pypi_name bsnlldp
%global rpm_name networking-bigswitch-bsnlldp

Name:           python-%{rpm_name}
Version:        3.0.0
Release:        1%{?dist}
Summary:        Big Switch Networks LLDP agent

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools

%description
This package contains the LLDP agent that periodically
sends out LLDP packages with Big Switch OUI

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
/etc/systemd/system/bsnlldp.service
/usr/bin/bsnlldp

%changelog
* Fri Aug 22 2015 Xin Wu <xin.wu@bigswitch.com> - 3.0.0-1
- Initial package.

