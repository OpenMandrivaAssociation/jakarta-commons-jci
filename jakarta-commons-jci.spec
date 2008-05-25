# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

#TODO enable groovy
%define gcj_support 0
## If you don't want to build with maven, and use straight ant instead,
## give rpmbuild option '--without maven'
%define _without_maven 1
%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section   free
%define base_name commons-jci

Name:           jakarta-%{base_name}
Version:        1.0
Release:        %mkrel 1.0.1
Epoch:          0
Summary:        Commons Java Compiler Interface
License:        Apache License 2.0
Url:            http://commons.apache.org/jci/
Group:          Development/Java
Source0:        http://www.apache.org/dist/commons/jci/source/commons-jci-1.0-src.tar.gz
Source1:        %{base_name}-settings.xml
Source2:        %{base_name}-%{version}-jpp-depmap.xml
Source3:        %{base_name}-autogenerated-files.tar.gz
Patch0:         commons-jci-1.0-JaninoJavaCompiler.patch
Patch1:         commons-jci-1.0-JaninoCompilationProblem.patch
Patch2:         commons-jci-1.0-JavacClassLoader.patch
Patch3:         commons-jci-1.0-pom.patch
Patch4:         commons-jci-1.0-site_xml.patch

BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-devel = 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
BuildRequires:  junit
%if %{with_maven}
BuildRequires:  maven2-common-poms
BuildRequires:  maven2 
BuildRequires:  maven2-default-skin
BuildRequires:  maven2-plugin-ant
BuildRequires:  maven2-plugin-antrun
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-idea
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-jxr
BuildRequires:  maven2-plugin-pmd
BuildRequires:  maven2-plugin-project-info-reports
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-site
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven2-plugin-surefire-report
BuildRequires:  mojo-maven2-plugin-cobertura
BuildRequires:  mojo-maven2-plugin-taglist
BuildRequires:  jetty6-maven2-plugins
%endif

BuildRequires:  asm2
BuildRequires:  jakarta-commons-cli
BuildRequires:  jakarta-commons-io
BuildRequires:  jakarta-commons-lang
BuildRequires:  jakarta-commons-logging
#BuildRequires:  groovy-jsr
BuildRequires:  ecj
BuildRequires:  janino
BuildRequires:  rhino
BuildRequires:  servletapi5
BuildRequires:  vafer-dependency

Requires:       jakarta-commons-io
Requires:       jakarta-commons-lang
Requires:       jakarta-commons-logging

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot

%description
JCI is a java compiler interface featuring a compiling classloader.
The current implementation supports compilation via the following 
compilers:
* eclipse
* janino
* javac
* groovy-jsr
* rhino


%package compiler-eclipse
Summary:        ECJ Module for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       ecj

%description compiler-eclipse
%{summary}.

%if 0
%package compiler-groovy
Summary:        Groovy JSR Module for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       groovy-jsr

%description compiler-groovy
%{summary}.
%endif

%package compiler-janino
Summary:        Janino Module for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       janino

%description compiler-janino
%{summary}.

%package compiler-rhino
Summary:        Rhino Module for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       rhino

%description compiler-rhino
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%if %{with_maven}
%package manual
Summary:        Documents for %{name}
Group:          Development/Java

%description manual
%{summary}.
%endif

%package demo
Summary:        Examples for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{name}-compilers-eclipse = %{epoch}:%{version}-%{release}
Requires:       jakarta-commons-cli
Requires:       servlet_2_4_api

%description demo
%{summary}.

%prep
%setup -q -n %{base_name}-%{version}-src
#find . -name "*.jar" -exec rm -f {} \;
for j in $(find . -name "*.jar"); do
    mv $j $j.no
done
%if %{without_maven}
gzip -dc %{SOURCE3} | tar xf -
%endif

%patch0 -b .sav0
%patch1 -b .sav1
%patch2 -b .sav2
# patch3 patches out findbugs reporting
%patch3 -b .sav3
%patch4 -b .sav4

cp %{SOURCE1} settings.xml
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml



%build
export JAVA_HOME=%{_jvmdir}/java-rpmbuild

%if %{with_maven}
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL/JPP/maven2/default_poms/

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

export M2_SETTINGS=$(pwd)/settings.xml
mvn-jpp \
        -e \
        -s $M2_SETTINGS \
        -Dmaven.test.failure.ignore=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install
mvn-jpp \
        -e \
        -s $M2_SETTINGS \
        -Dmaven.test.failure.ignore=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        ant:ant site

%else
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath \
commons-io \
commons-lang \
commons-logging-api \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd fam
ant -Dmaven.settings.offline=true -Dbuild.sysclasspath=only jar javadoc
popd

export CLASSPATH=$(build-classpath \
asm2/asm2 \
commons-io \
commons-lang \
commons-logging-api \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/fam/target/%{base_name}-fam-%{version}.jar
pushd core
%ant -Dmaven.settings.offline=true -Dbuild.sysclasspath=only jar javadoc
popd

pushd compilers

export CLASSPATH=$(build-classpath \
ecj \
commons-logging-api \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/%{base_name}-core-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/test-classes
pushd eclipse
%ant -Dmaven.settings.offline=true -Dbuild.sysclasspath=only jar javadoc
popd

export CLASSPATH=$(build-classpath \
janino \
commons-logging-api \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/%{base_name}-core-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/test-classes
pushd janino
%ant -Dmaven.settings.offline=true -Dbuild.sysclasspath=only jar javadoc
popd

export CLASSPATH=$(build-classpath \
groovy-jsr-all \
commons-logging-api \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/%{base_name}-core-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/test-classes
%if 0
pushd groovy
%ant -Dmaven.settings.offline=true -Dbuild.sysclasspath=only jar javadoc
popd
%endif

export CLASSPATH=$(build-classpath \
asm2/asm2 \
asm2/asm2-analysis \
asm2/asm2-util \
commons-logging-api \
vafer-dependency \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/%{base_name}-core-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/test-classes
pushd javac
%ant -Dmaven.settings.offline=true -Dbuild.sysclasspath=only jar javadoc
popd

export CLASSPATH=$(build-classpath \
commons-logging-api \
js \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/%{base_name}-core-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/../core/target/test-classes
pushd rhino
%ant -Dmaven.settings.offline=true -Dbuild.sysclasspath=only jar javadoc
popd

popd

export CLASSPATH=$(build-classpath \
commons-cli \
servletapi5 \
)
CLASSPATH=$CLASSPATH:$(pwd)/fam/target/%{base_name}-fam-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/core/target/%{base_name}-core-%{version}.jar
pushd examples
%ant -Dmaven.settings.offline=true -Dbuild.sysclasspath=only jar javadoc
popd

%endif

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
%add_to_maven_depmap org.apache.commons %{base_name} %{version} JPP %{base_name}

install -m 644 fam/target/%{base_name}-fam-%{version}.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-fam-%{version}.jar
%add_to_maven_depmap org.apache.commons %{base_name}-fam %{version} JPP %{base_name}-fam
install -m 644 core/target/%{base_name}-core-%{version}.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-core-%{version}.jar
install -m 644 core/target/%{base_name}-core-%{version}-tests.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-core-tests-%{version}.jar
%add_to_maven_depmap org.apache.commons %{base_name}-core %{version} JPP %{base_name}-core

install -m 644 compilers/javac/target/%{base_name}-javac-%{version}.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-javac-%{version}.jar
%add_to_maven_depmap org.apache.commons %{base_name}-javac %{version} JPP %{base_name}-javac
install -m 644 compilers/eclipse/target/%{base_name}-eclipse-%{version}.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-eclipse-%{version}.jar
%add_to_maven_depmap org.apache.commons %{base_name}-eclipse %{version} JPP %{base_name}-eclipse
%if 0
install -m 644 compilers/groovy/target/%{base_name}-groovy-%{version}.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-groovy-%{version}.jar
%add_to_maven_depmap org.apache.commons %{base_name}-groovy %{version} JPP %{base_name}-groovy
%endif
install -m 644 compilers/janino/target/%{base_name}-janino-%{version}.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-janino-%{version}.jar
%add_to_maven_depmap org.apache.commons %{base_name}-janino %{version} JPP %{base_name}-janino
install -m 644 compilers/rhino/target/%{base_name}-rhino-%{version}.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-rhino-%{version}.jar
%add_to_maven_depmap org.apache.commons %{base_name}-rhino %{version} JPP %{base_name}-rhino
install -m 644 examples/target/%{base_name}-examples-%{version}.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-examples-%{version}.jar
%add_to_maven_depmap org.apache.commons %{base_name}-examples %{version} JPP %{base_name}-examples

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in jakarta-*; do \
ln -sf ${jar} ${jar/jakarta-/}; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{base_name}.pom
install -m 644 fam/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{base_name}-fam.pom
install -m 644 core/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{base_name}-core.pom
install -m 644 compilers/javac/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{base_name}-javac.pom
install -m 644 compilers/eclipse/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{base_name}-eclipse.pom
#install -m 644 compilers/groovy/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{base_name}-groovy.pom
install -m 644 compilers/janino/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{base_name}-janino.pom
install -m 644 compilers/rhino/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{base_name}-rhino.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf target/site/apidocs
%else
install -d -m 755 \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/fam
cp -pr fam/target/site/apidocs/* \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/fam
install -d -m 755 \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/core
cp -pr core/target/site/apidocs/* \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/core
install -d -m 755 \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-eclipse
cp -pr compilers/eclipse/target/site/apidocs/* \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-eclipse
%if 0
install -d -m 755 \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-groovy
cp -pr compilers/groovy/target/site/apidocs/* \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-groovy
%endif
install -d -m 755 \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-janino
cp -pr compilers/janino/target/site/apidocs/* \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-janino
install -d -m 755 \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-javac
cp -pr compilers/javac/target/site/apidocs/* \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-javac
install -d -m 755 \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-rhino
cp -pr compilers/rhino/target/site/apidocs/* \
       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compiler-rhino
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

## manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%if %{with_maven}
cp -pr target/site $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/*fam*.jar
%{_javadir}/*core*.jar
%{_javadir}/*javac*.jar
%{_datadir}/maven2
%{_mavendepmapfragdir}

%files compiler-eclipse
%defattr(0644,root,root,0755)
%{_javadir}/*eclipse*.jar

%if 0
%files compiler-groovy
%defattr(0644,root,root,0755)
%{_javadir}/*groovy*.jar
%endif

%files compiler-janino
%defattr(0644,root,root,0755)
%{_javadir}/*janino*.jar

%files compiler-rhino
%defattr(0644,root,root,0755)
%{_javadir}/*rhino*.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%if %{with_maven}
%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/site
%endif

%files demo
%defattr(0644,root,root,0755)
%{_javadir}/*examples*.jar
