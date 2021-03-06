#
# Conditional build:
%bcond_with	javadoc		# don't build javadoc
%bcond_with	tests		# don't build and run tests


%define		srcname		commons-chain
Summary:	"Chain of Responsibility" pattern implemention
Name:		java-commons-chain
Version:	1.2
Release:	6
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/commons/chain/source/commons-chain-%{version}-src.tar.gz
# Source0-md5:	a94fef07630d88c859fb8397ddbcb6ba
Patch0:		%{name}-notests.patch
URL:		http://commons.apache.org/chain
BuildRequires:	ant
BuildRequires:	java(jsf) = 1.1
BuildRequires:	java-commons-digester >= 1.8
BuildRequires:	java-commons-logging
BuildRequires:	java-pluto
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %{with tests}
BuildRequires:	ant-junit
BuildRequires:	java-commons-beanutils
BuildRequires:	java-commons-collections
BuildRequires:	java-junit
%endif
BuildRequires:	java(servlet)
BuildRequires:	sed >= 4
Requires:	java(jsf) = 1.1
Requires:	java(servlet)
Requires:	java-commons-digester >= 1.8
Requires:	java-commons-logging
Requires:	java-pluto
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
"Chain of Responsibility" pattern implemention.

%package doc
Summary:	Manual for %{name}
Summary(fr.UTF-8):	Documentation pour %{name}
Summary(it.UTF-8):	Documentazione di %{name}
Summary(pl.UTF-8):	Podręcznik dla %{name}
Group:		Documentation

%description doc
Documentation for %{name}.

%description doc -l fr.UTF-8
Documentation pour %{name}.

%description doc -l it.UTF-8
Documentazione di %{name}.

%description doc -l pl.UTF-8
Dokumentacja do %{name}.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%package demo
Summary:	Demo for %{name}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{name}
Group:		Development/Languages/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{name}.

%package manual
Summary:	Tutorial for %{name}
Group:		Documentation

%description manual
Manual for %{name}.

%prep
%setup -q -n %{srcname}-%{version}-src

%{__sed} -i -e 's,\r$,,' build.xml
%patch0 -p1

%build
export JAVA_HOME="%{java_home}"

required_jars="servlet-api commons-logging commons-digester portlet-api-1.0 faces-api-1.1"
%if %{with tests}
required_jars=$required_jars" junit commons-collections commons-beanutils-core"
%endif

CLASSPATH=$(build-classpath $required_jars):target/classes:target/test-classes

export LC_ALL=en_US # source code not US-ASCII

%ant -Dbuild.sysclasspath=only %{?with_tests:test} jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a target/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
