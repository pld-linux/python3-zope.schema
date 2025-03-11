#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests (installed package required)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	zope.schema
Summary:	zope.interface extension for defining data schemas
Summary(pl.UTF-8):	Rozszerzenie zope.interface do definiowania schematów danych
Name:		python-%{module}
# keep 6.x here for python2 support
Version:	6.2.1
Release:	3
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.schema/zope.schema-%{version}.tar.gz
# Source0-md5:	4def0eb61a3d69a4ae262965bfded3a1
URL:		https://www.zope.dev/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-zope.event
BuildRequires:	python-zope.i18nmessageid
BuildRequires:	python-zope.interface >= 5.0.0
BuildRequires:	python-zope.testing
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.event
BuildRequires:	python3-zope.i18nmessageid
BuildRequires:	python3-zope.interface >= 5.0.0
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
zope.interface extension for defining data schemas.

%description -l pl.UTF-8
Rozszerzenie zope.interface do definiowania schematów danych.

%package -n python3-%{module}
Summary:	zope.interface extension for defining data schemas
Summary(pl.UTF-8):	Rozszerzenie zope.interface do definiowania schematów danych
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
zope.interface extension for defining data schemas.

%description -n python3-%{module} -l pl.UTF-8
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

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-2 --test-path=src -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/zope/schema/tests
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/schema/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py_sitescriptdir}/zope/schema
%{py_sitescriptdir}/zope.schema-%{version}-py*.egg-info
%{py_sitescriptdir}/zope.schema-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/zope/schema
%{py3_sitescriptdir}/zope.schema-%{version}-py*.egg-info
%{py3_sitescriptdir}/zope.schema-%{version}-py*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
