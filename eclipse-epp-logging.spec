%{?scl:%scl_package eclipse-epp-logging}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

%global git_tag NEON_R

Name:           %{?scl_prefix}eclipse-epp-logging
Version:        2.0.1
Release:        1.%{baserelease}%{?dist}
Summary:        Eclipse Error Reporting tool
License:        EPL
URL:            http://www.eclipse.org/epp/

Source0:        http://git.eclipse.org/c/epp/org.eclipse.epp.logging.git/snapshot/org.eclipse.epp.logging-%{git_tag}.tar.xz

Patch0:		feature-cleanup.patch
Patch1:		guava-upgrade.patch
Patch2:		lucene-upgrade.patch

BuildArch:      noarch

BuildRequires: %{?scl_prefix}tycho
BuildRequires: %{?scl_prefix}tycho-extras
BuildRequires: %{?scl_prefix}eclipse-pde
BuildRequires: %{?scl_prefix}eclipse-license
BuildRequires: %{?scl_prefix}eclipse-emf-runtime
BuildRequires: %{?scl_prefix}eclipse-mylyn
BuildRequires: %{?scl_prefix_maven}apache-commons-lang3
BuildRequires: %{?scl_prefix}guava
BuildRequires: %{?scl_prefix_java_common}google-gson
BuildRequires: %{?scl_prefix_java_common}httpcomponents-client
BuildRequires: %{?scl_prefix_maven}maven-enforcer-plugin

Requires:       %{?scl_prefix}eclipse-platform >= 1:4.6.0

%description
EPP Logging provides a set of logging plugins for the Eclipse IDE.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n org.eclipse.epp.logging-%{git_tag}
%patch0 -p1
%patch1 -p1
%patch2 -p0 -b.orig

sed -i -e "s/org.hamcrest;/org.hamcrest.core;/g" `find . -name MANIFEST.MF`
sed -i -e "s/id=\"org.hamcrest\"/id=\"org.hamcrest.core\"/g" `find . -name feature.xml`
sed -i -e "s/org.mockito;/org.mockito.mockito-core;/g"  `find . -name MANIFEST.MF`
sed -i -e "s/org.mockito/org.mockito.mockito-core/g"  `find . -name feature.xml`

# Delete anything prebuilt or bundled
find -name *.jar -delete
find -name *.class -delete

pushd features/
%pom_disable_module org.eclipse.epp.logging.3rd.feature
%pom_disable_module org.eclipse.epp.logging.aeri.tests.feature
%pom_disable_module org.eclipse.epp.logging.sdk.feature
popd

%pom_disable_module releng
%pom_disable_module tests
%pom_disable_module examples

%pom_remove_plugin org.eclipse.tycho:target-platform-configuration
%pom_remove_plugin org.apache.maven.plugins:maven-checkstyle-plugin
%pom_remove_plugin com.mycila.maven-license-plugin:maven-license-plugin
%pom_remove_plugin org.eclipse.tycho:tycho-packaging-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-enforcer-plugin
%pom_remove_plugin org.codehaus.mojo:tidy-maven-plugin
%pom_remove_plugin org.codehaus.mojo:animal-sniffer-maven-plugin bundles/
%pom_remove_plugin org.jacoco:jacoco-maven-plugin tests/
%pom_remove_plugin org.apache.maven.plugins:maven-enforcer-plugin bundles/

%mvn_package "::pom::" __noinstall
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_build -j
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc %{_datadir}/eclipse/droplets/epp-logging/eclipse/features/org.eclipse.epp.logging.aeri.feature_*/*.html

%changelog
* Tue Aug 02 2016 Mat Booth <mat.booth@redhat.com> - 2.0.1-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Tue Aug 02 2016 Mat Booth <mat.booth@redhat.com> - 2.0.1-1
- Port to latest lucene
- Use tagged Neon release

* Thu Jun 30 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.100.0-0.6.gitc6ce9f2
- Add missing BR on maven-enforcer-plugin

* Thu Mar 24 2016 Sopot Cela <scela@redhat.com> - 1.100.0-0.5.gitc6ce9f2
- Added symlinks to lucene3 artifacts

* Thu Mar 24 2016 Sopot Cela <scela@redhat.com> - 1.100.0-0.4.gitc6ce9f2
- Added dropins support

* Mon Mar 21 2016 Sopot Cela <scela@redhat.com> - 1.100.0-0.3.gitc6ce9f2
- Added %license statement

* Fri Mar 18 2016 Sopot Cela <scela@redhat.com> - 1.100.0-0.2.gitc6ce9f2
- Disabled examples module

* Wed Mar 16 2016 Sopot Cela <scela@redhat.com> - 1.100.0-0.1.gitc6ce9f2
- Initial packaging