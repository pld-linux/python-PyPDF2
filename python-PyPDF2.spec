#
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	PyPDF2
Summary:	A Pure-Python library built as a PDF toolkit
Summary(pl.UTF-8):	Czysto Pythonowa biblioteka narzędzi dla PDF
Name:		python-%{module}
Version:	1.26.0
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/b4/01/68fcc0d43daf4c6bdbc6b33cc3f77bda531c86b174cac56ef0ffdb96faab/%{module}-%{version}.tar.gz
# Source0-md5:	2301acc0ecbab0633d4c9b883d50ee5e
URL:		http://mstamy2.github.com/PyPDF2
BuildRequires:	rpm-pythonprov
# for the py_build, py_install macros
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
%endif
%if %{with python3}
BuildRequires:	python3-modules
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Pure-Python library built as a PDF toolkit. It is capable of:
extracting document information (title, author, etc) splitting
documents page by page merging documents page by page cropping pages
merging multiple pages into a single page encrypting and decrypting
PDF files and more!

%description -l pl.UTF-8
Czysto Pythonowa bibliotek narzędziowa pozwalająca na: uzyskiwanie
informacji o dokumentach (tytuł, autor itp) dzielenie dokumentów na
strony sklejanie dokumentów z pojedynczych stron elimancje marginesów
sklejanie stron w jedną stronę szyfrowanie i odszyfrowywanie plików
PDF.

%package -n python3-%{module}
Summary:	A Pure-Python library built as a PDF toolkit
Summary(pl.UTF-8):	Czysto Pythonowa biblioteka narzędzi dla PDF
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
A Pure-Python library built as a PDF toolkit. It is capable of:
extracting document information (title, author, etc) splitting
documents page by page merging documents page by page cropping pages
merging multiple pages into a single page encrypting and decrypting
PDF files and more!

%description -n python3-%{module} -l pl.UTF-8
Czysto Pythonowa bibliotek narzędziowa pozwalająca na: uzyskiwanie
informacji o dokumentach (tytuł, autor itp) dzielenie dokumentów na
strony sklejanie dokumentów z pojedynczych stron elimancje marginesów
sklejanie stron w jedną stronę szyfrowanie i odszyfrowywanie plików
PDF.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a Sample_Code/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif

%if %{with python3}
%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a Sample_Code/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG README.md
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
