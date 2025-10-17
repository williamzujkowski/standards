#!/bin/bash
set -euo pipefail

# Kotlin Project Setup Script
# Sets up a Gradle Kotlin project with testing, linting, and best practices

PROJECT_NAME="${1:-kotlin-app}"
PACKAGE_NAME="${2:-com.example.app}"
KOTLIN_VERSION="1.9.20"
COROUTINES_VERSION="1.7.3"
JUNIT_VERSION="5.10.0"
MOCKK_VERSION="1.13.8"

echo "Setting up Kotlin project: $PROJECT_NAME"
echo "Package: $PACKAGE_NAME"

# Create project structure
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Create directory structure
mkdir -p src/{main,test}/kotlin
mkdir -p src/{main,test}/resources
mkdir -p buildSrc/src/main/kotlin

# Convert package name to directory path
PACKAGE_PATH="${PACKAGE_NAME//./\/}"
mkdir -p "src/main/kotlin/$PACKAGE_PATH"
mkdir -p "src/test/kotlin/$PACKAGE_PATH"

echo "✓ Created directory structure"

# Create settings.gradle.kts
cat > settings.gradle.kts << SETTINGS
rootProject.name = "$PROJECT_NAME"
SETTINGS

echo "✓ Created settings.gradle.kts"

# Create build.gradle.kts
cat > build.gradle.kts << 'BUILD'
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.9.20"
    id("io.gitlab.arturbosch.detekt") version "1.23.1"
    id("org.jlleitschuh.gradle.ktlint") version "11.6.1"
    application
}

group = "com.example"
version = "1.0.0"

repositories {
    mavenCentral()
}

dependencies {
    // Kotlin stdlib
    implementation(kotlin("stdlib"))
    
    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-jdk8:1.7.3")
    
    // Testing
    testImplementation(kotlin("test"))
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    testImplementation("io.mockk:mockk:1.13.8")
    
    // Logging (optional)
    implementation("ch.qos.logback:logback-classic:1.4.11")
    implementation("io.github.microutils:kotlin-logging-jvm:3.0.5")
}

tasks.test {
    useJUnitPlatform()
    
    testLogging {
        events("passed", "skipped", "failed")
        showStandardStreams = false
    }
}

tasks.withType<KotlinCompile> {
    kotlinOptions {
        jvmTarget = "17"
        freeCompilerArgs = listOf(
            "-Xjsr305=strict",
            "-opt-in=kotlin.RequiresOptIn"
        )
    }
}

detekt {
    buildUponDefaultConfig = true
    allRules = false
    config.setFrom(files("$projectDir/config/detekt.yml"))
    baseline = file("$projectDir/config/detekt-baseline.xml")
}

ktlint {
    version.set("0.50.0")
    debug.set(false)
    verbose.set(false)
    android.set(false)
    outputToConsole.set(true)
    ignoreFailures.set(false)
    
    filter {
        exclude("**/generated/**")
        include("**/kotlin/**")
    }
}

application {
    mainClass.set("com.example.app.MainKt")
}

// Custom tasks
tasks.register("check-all") {
    group = "verification"
    description = "Run all checks (test, detekt, ktlint)"
    dependsOn("test", "detekt", "ktlintCheck")
}

tasks.register("format") {
    group = "formatting"
    description = "Format code with ktlint"
    dependsOn("ktlintFormat")
}
BUILD

echo "✓ Created build.gradle.kts"

# Create gradle.properties
cat > gradle.properties << PROPS
kotlin.code.style=official
kotlin.incremental=true
kotlin.caching.enabled=true

org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
PROPS

echo "✓ Created gradle.properties"

# Create config directory
mkdir -p config

# Create basic detekt.yml
cat > config/detekt.yml << 'DETEKT'
build:
  maxIssues: 0

complexity:
  active: true
  ComplexMethod:
    threshold: 15
  LongMethod:
    threshold: 60
  LongParameterList:
    functionThreshold: 6

style:
  active: true
  MaxLineLength:
    maxLineLength: 120
  MagicNumber:
    active: true
    ignoreNumbers: ['-1', '0', '1', '2']

naming:
  active: true
  FunctionNaming:
    functionPattern: '[a-z][a-zA-Z0-9]*'
  ClassNaming:
    classPattern: '[A-Z][a-zA-Z0-9]*'

potential-bugs:
  active: true
DETEKT

echo "✓ Created detekt.yml"

# Create .editorconfig
cat > .editorconfig << EDITOR
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{kt,kts}]
indent_style = space
indent_size = 4
max_line_length = 120

[*.gradle.kts]
indent_size = 4

[*.md]
trim_trailing_whitespace = false
EDITOR

echo "✓ Created .editorconfig"

# Create .gitignore
cat > .gitignore << GITIGNORE
# Gradle
.gradle/
build/
!gradle-wrapper.jar

# IDE
.idea/
*.iml
*.ipr
*.iws
.vscode/

# OS
.DS_Store
Thumbs.db

# Test
*.log
*.class

# Local config
local.properties
GITIGNORE

echo "✓ Created .gitignore"

# Create sample Main.kt
cat > "src/main/kotlin/$PACKAGE_PATH/Main.kt" << MAIN
package $PACKAGE_NAME

import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    println("Hello, Kotlin!")
    
    val app = Application()
    app.run()
}

class Application {
    suspend fun run() {
        println("Application started")
        // Your application logic here
    }
}
MAIN

echo "✓ Created Main.kt"

# Create sample test
cat > "src/test/kotlin/$PACKAGE_PATH/ApplicationTest.kt" << TEST
package $PACKAGE_NAME

import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.Assertions.*

class ApplicationTest {
    @Test
    fun \`application runs successfully\`() = runTest {
        val app = Application()
        
        assertDoesNotThrow {
            app.run()
        }
    }
}
TEST

echo "✓ Created ApplicationTest.kt"

# Create README
cat > README.md << README
# $PROJECT_NAME

Kotlin project with coroutines, testing, and code quality tools.

## Build

\`\`\`bash
./gradlew build
\`\`\`

## Test

\`\`\`bash
./gradlew test
\`\`\`

## Run

\`\`\`bash
./gradlew run
\`\`\`

## Code Quality

\`\`\`bash
# Run all checks
./gradlew check-all

# Format code
./gradlew format

# Static analysis
./gradlew detekt

# Lint check
./gradlew ktlintCheck
\`\`\`

## Project Structure

- \`src/main/kotlin\` - Source code
- \`src/test/kotlin\` - Tests
- \`config/\` - Configuration files
- \`build.gradle.kts\` - Build configuration

## Technologies

- Kotlin $KOTLIN_VERSION
- Coroutines $COROUTINES_VERSION
- JUnit $JUNIT_VERSION
- MockK $MOCKK_VERSION
- Detekt (static analysis)
- ktlint (code formatting)
README

echo "✓ Created README.md"

# Initialize Gradle wrapper
echo "Initializing Gradle wrapper..."
gradle wrapper --gradle-version=8.4 --distribution-type=bin

echo ""
echo "✅ Project setup complete!"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  ./gradlew build"
echo "  ./gradlew test"
echo "  ./gradlew run"
echo ""
echo "Code quality:"
echo "  ./gradlew check-all  # Run all checks"
echo "  ./gradlew format     # Format code"
