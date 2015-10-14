		
Fluent-Specs
=================== 

FluentSpecs is a Java API for fluent unit-level specification using a BDD/Gherkin format, similar to ScalaTest. It provides a thin uniform interface for
mocking, behaviour and state verification around Mockito and Hamcrest. 

Inspired by Hamcrest, Mockito, Fest-Assertions, RSpec and Narrative.

The current version only provides the most common subset of the functionality present in Hamcrest and Mockito. 


To use as Maven dependency, download [jar](https://github.com/JoseLlarena/FluentSpecs/raw/master/dist/fluent-specs-2.0.0.jar) and run:

```shell
mvn install:install-file -DgroupId=com.fluent -DartifactId=fluent-specs -Dpackaging=jar -Dversion=2.0.0 -Dfile=fluent-specs-2.0.0.jar -DgeneratePom=true
```

then you can reference it in your pom.xml as

```xml
<dependency>
  <groupId>com.fluent</groupId>
  <artifactId>fluent-specs</artifactId>
  <version>2.0.0</version>
  <scope>test</test>
</dependency>
```
