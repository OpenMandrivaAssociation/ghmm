%define with_atlas	1
%define with_gsl	1
%define name		ghmm
# use this until version 1.0, instead of a date to avoid the need of Epoch
# and still make upgrades work correctly from 0.20090317 t0 0.9-rc1
%define version		0.90000001
%define upstream	0.9-rc1

%define libname		%mklibname %{name}
%define libname_devel	%mklibname %{name} -d
%define libname_static	%mklibname %{name} -d -s

Name:		%{name}
Version:	%{version}
Release:	%mkrel 3
Group:		Sciences/Mathematics
License:	LGPL
Summary:	General Hidden Markov Model library
Source:		%{name}-%{upstream}.tar.gz
URL:		https://ghmm.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{upstream}-buildroot

%if %{with_atlas}
BuildRequires:	libatlas-devel
%endif

%if %{with_gsl}
BuildRequires:	libgsl-devel
%endif
BuildRequires:	libxml2-devel
BuildRequires:	python-devel
BuildRequires:	swig

Requires:	python-Gato
Requires:	python-%{name}

%description
The General Hidden Markov Model library (GHMM) is a freely available
LGPL-ed C library implementing efficient data structures and algorithms
for basic and extended HMMs.

The GHMM is developed by the Algorithmics group at the Max Planck
Institute for Molecular Genetics.

%package	-n %{libname}
Summary:	General Hidden Markov Model library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}

%description -n %{libname}
The General Hidden Markov Model library (GHMM) is a freely available
LGPL-ed C library implementing efficient data structures and algorithms
for basic and extended HMMs.

The GHMM is developed by the Algorithmics group at the Max Planck
Institute for Molecular Genetics.

%package	-n %{libname_devel}
Summary:	%{name} development files
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}

%description -n %{libname_devel}
This package provides the %{name} development files.

%package	-n %{libname_static}
Summary:	%{name} development files
Group:		Development/C
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%{name}-static-devel < %{version}-%{release}

%description -n %{libname_static}
This package provides the %{name} static libraries.

%package -n	python-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python

%description	-n python-%{name} 
This package contains Python bindings for %{name}.

%prep
%setup -q -n %{name}-%{upstream}

%build
sed -i 's|setup.py install|setup.py install --root=%{buildroot}|'	\
    ghmmwrapper/Makefile.am HMMEd/Makefile.am

sh autogen.sh

CFLAGS="%{optflags} -fPIC"				\
%if %{with_atlas}
	LAPACK_LIBS="-L%{_libdir}/atlas -llapack"	\
%endif
%configure						\
%if %{with_atlas}
	--enable-atlas					\
%else
	--disable-atlas					\
%endif
%if %{with_gsl}
	--enable-gsl					\
%else
	--with-rng=bsd					\
%endif

%make

%install
%makeinstall_std

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/%{name}/ghmm.dtd.1.0

%files		-n %{libname}
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.*

%files		-n %{libname_devel}
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.la
%{_libdir}/lib%{name}.so

%files		-n python-%{name}
%defattr(-,root,root)
%{py_platlibdir}/*
%{py_sitedir}/*

%files		-n %{libname_static}
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}.a
