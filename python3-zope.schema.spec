#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests (installed package required)

%define module	zope.schema
Summary:	zope.interface extension for defining data schemas
Summary(pl.UTF-8):	Rozszerzenie zope.interface do definiowania schematów danych
Name:		python3-%{module}
Version:	7.0.1
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.schema/zope.schema-%{version}.tar.gz
# Source0-md5:	d938af4000a89fa101d2f48f7a8fdd75
Patch0:		zope.schema-intersphinx.patch
URL:		https://www.zope.dev/
BuildRequires:	python3 >= 1:3.7
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.event
BuildRequires:	python3-zope.i18nmessageid
BuildRequires:	python3-zope.interface >= 5.0.0
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
zope.interface extension for defining data schemas.

%description -l pl.UTF-8
Rozszerzenie zope.interface do definiowania schematów danych.

%package apidocs
Summary:	API documentation for Python zope.schema module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.schema
Group:		Documentation

%description apidocs
API documentation for Python zope.schema module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.schema.

%prep
%setup -q -n %{module}-%{version}
%patch -P0 -p1

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/schema/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/zope/schema
%{py3_sitescriptdir}/zope.schema-%{version}-py*.egg-info
%{py3_sitescriptdir}/zope.schema-%{version}-py*-nspkg.pth

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
