%{!?fc18: %define fc18 0}

%if %{fc18}
%define majorminor  1.0
%define gstreamer gstreamer1
%else
%define majorminor  0.10
%define gstreamer gstreamer
%endif

%{expand:%%define meego %(test -e /etc/meego-release && echo 1 || echo 0)}

Name:		%{gstreamer}-fluendo-mp3
Version:	0.10.32
Release:	1.flu
Summary:	Fluendo GStreamer plug-in for mp3 support

Group:		Applications/Multimedia
License:	MIT
URL:		http://www.fluendo.com/
Source:		gst-fluendo-mp3-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{gstreamer}-devel
%if ! %{meego}
BuildRequires:  %{gstreamer}-plugins-base-devel
%else
BuildRequires:  gst-plugins-base-devel
%endif
BuildRequires:  intel-ipp

%description
Fluendo GStreamer plug-in for mp3 support.

%prep
%setup -q -n gst-fluendo-mp3-%{version}

%build
%if %{meego}
%configure --enable-cpu-tune-atom --with-ipp-arch=11
%else
%configure
%endif
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# Remove unneeded .la and .a files
rm -rf $RPM_BUILD_ROOT/%{_libdir}/gstreamer-%{majorminor}/*.a
rm -rf $RPM_BUILD_ROOT/%{_libdir}/gstreamer-%{majorminor}/*.la

%post
semanage 2>/dev/null >/dev/null
if [ "$?" -eq 1 ]; then
        semanage fcontext -a -t textrel_shlib_t %{_libdir}/gstreamer-%{majorminor}/libgstflump3dec.so
        if [ "$?" -eq 0 ]; then
                echo "Changed local file context in SELinux"
        else
                echo "Failed to run semanage"
        fi
fi
restorecon 2>/dev/null >dev/null
if [ "$?" -eq 1 ]; then
        restorecon %{_libdir}/gstreamer-%{majorminor}/libgstflump3dec.so
        if [ "$?" -eq 0 ]; then
                echo "Changed SELinux permissions for" %{_libdir}/gstreamer-%{majorminor}/libgstflump3dec.so
        else
                echo "Failed to change SELinux permissions for " %{_libdir}/gstreamer-%{majorminor}/libgstflump3dec.so
        fi  
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root, -)
%doc README ChangeLog COPYING AUTHORS NEWS TODO LICENSE
%{_libdir}/gstreamer-%{majorminor}/libgstflump3dec.so

%changelog
* Mon Feb 11 2013 Julien Moutte <julien@fluendo.com>
- Add support for GStreamer 1.0

* Thu Aug 25 2011 Julien Moutte <julien@fluendo.com>
- IPP packages now have a common name.
- Meego specific configure optimizations.

* Fri Dec 14 2007 Christophe Eymard <ceymard@fluendo.com>
- persistent settings across reboots and SELinux disabling/reenabling.

* Tue Oct 04 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- removed -register

* Fri Jul 08 2005 Christian F.K. Schaller <christian@fluendo.com>
- First attempt at spec
