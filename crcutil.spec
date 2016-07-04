#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	High performance CRC implementation
Name:		crcutil
Version:	1.0
Release:	0.1
License:	Apache v2.0
Group:		Libraries
Source0:	https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/crcutil/%{name}-%{version}.tar.gz
# Source0-md5:	94cb7014d4078c138d3c9646fcf1fec5
Patch0:		detect-mcrc32.patch
Patch1:		http://storage.googleapis.com/google-code-attachments/crcutil/issue-9/comment-0/build-fix-tests.patch
# Patch1-md5:	6b88d4eeef7e418c1eb6fc0ab729dca2
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

%build
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

# if library provides pkgconfig file containing proper {Requires,Libs}.private
# then remove .la pollution
#%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS
%attr(755,root,root) %{_libdir}/%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.N

%files devel
%defattr(644,root,root,755)
%doc devel-doc/* ChangeLog NEWS TODO
%attr(755,root,root) %{_libdir}/%{name}.so
# if no pkgconfig support, or it misses .private deps, then include .la file
#%{_libdir}/libFOO.la
%{_includedir}/%{name}
%{_aclocaldir}/%{name}.m4
%{_pkgconfigdir}/%{name}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs/*
%endif
