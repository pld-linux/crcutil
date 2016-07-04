#
# Conditional build:
%bcond_with	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	High performance CRC implementation
Name:		crcutil
Version:	1.0
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/crcutil/%{name}-%{version}.tar.gz
# Source0-md5:	94cb7014d4078c138d3c9646fcf1fec5
Patch0:		detect-mcrc32.patch
Patch1:		build-fix-tests.patch
Patch2:		automake.patch
Patch3:		library.patch
Patch4:		build-unclobber.patch
Patch5:		x32.patch
URL:		https://code.google.com/archive/p/crcutil/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Crcutil library provides efficient implementation of CRC algorithms.

It includes reference implementation of a novel Multiword CRC
algorithm invented by Andrew Kadatch and Bob Jenkins in early 2007.
The new algorithm is heavily tuned towards modern Intel and AMD
processors and is substantially faster than almost all other software
CRC algorithms.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation

%description apidocs
API documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p3

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS
%attr(755,root,root) %{_libdir}/libcrcutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcrcutil.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/crc.pdf INSTALL ChangeLog NEWS
%{_libdir}/libcrcutil.so
%{_includedir}/crcutil
%{_pkgconfigdir}/libcrcutil.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcrcutil.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs/*
%endif
