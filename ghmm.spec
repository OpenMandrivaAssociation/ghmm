%define with_gsl	1
%define name		ghmm
%define version		0.20090317

%define libname		%mklibname %{name}
%define libname_devel	%mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%mkrel 5
Group:		Sciences/Mathematics
License:	LGPL
Summary:	General Hidden Markov Model library
# svn co https://ghmm.svn.sourceforge.net/svnroot/ghmm/trunk/ghmm
# tar jcvf ghmm-0.`date +%\Y%\m%\d`.tar.bz2 ghmm
Source:		%{name}-%{version}.tar.bz2
URL:		http://ghmm.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	python-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python

%description	-n python-%{name} 
This package contains Python bindings for %{name}.

%prep
%setup -q -n %{name}

%build
sed -i 's|setup.py install|setup.py install --root=%{buildroot}|'	\
    ghmmwrapper/Makefile.am HMMEd/Makefile.am

sh autogen.sh

CFLAGS="%{optflags} -fPIC"	\
%configure		\
%if %{with_gsl}
	--enable-gsl	\
%else
	--with-rng=bsd
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
