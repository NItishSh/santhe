pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-image-name"
        SEMVER_FILE = "semver.txt"
        GIT_COMMIT_SHORT = "${env.GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Determine Version') {
            steps {
                script {
                    sh 'git fetch --tags'
                    def latestTag = sh(script: "git describe --tags --abbrev=0 || echo '0.0.0'", returnStdout: true).trim()
                    def (major, minor, patch) = latestTag.tokenize('.')
                    patch = (patch as Integer) + 1

                    def commitMessage = sh(script: "git log -1 --pretty=%B", returnStdout: true).trim()
                    if (commitMessage.contains("#major")) {
                        major = (major as Integer) + 1
                        minor = 0
                        patch = 0
                    } else if (commitMessage.contains("#minor")) {
                        minor = (minor as Integer) + 1
                        patch = 0
                    }

                    def preRelease = ""
                    if (env.BRANCH_NAME == "main") {
                        preRelease = ""
                    } else if (env.BRANCH_NAME == "develop") {
                        preRelease = "-beta.${env.BUILD_NUMBER}"
                    } else if (env.BRANCH_NAME.startsWith("feature/")) {
                        preRelease = "-alpha.${env.BUILD_NUMBER}"
                    } else {
                        preRelease = "-rc.${env.BUILD_NUMBER}"
                    }

                    def newVersion = "${major}.${minor}.${patch}${preRelease}"
                    writeFile file: SEMVER_FILE, text: newVersion
                    echo "New version determined: ${newVersion}"
                }
            }
        }

        stage('Lint') {
            steps {
                script {
                    echo "Running lint checks..."
                    // Example: For a JavaScript/Node.js project
                    sh 'npm install eslint'
                    sh 'npx eslint .'

                    // Example: For a Python project
                    sh 'pip install flake8'
                    sh 'flake8 .'
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                script {
                    echo "Running static code analysis..."
                    // Example: Using SonarQube for comprehensive analysis
                    withSonarQubeEnv('SonarQube') { // Assuming SonarQube is configured in Jenkins
                        sh 'mvn sonar:sonar -Dsonar.projectKey=your-project-key'
                    }
                    
                    // Example: Running SpotBugs for a Java project
                    sh 'mvn spotbugs:check'
                }
            }
            post {
                success {
                    echo "Static analysis completed successfully!"
                }
                failure {
                    echo "Static analysis failed."
                    error("Static code analysis failed.")
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    def version = readFile(SEMVER_FILE).trim()
                    echo "Building version: ${version}"
                    // Insert your build commands here, e.g., Maven, Gradle, npm, etc.
                    // sh 'mvn clean install'
                    // sh 'gradle build'
                    // sh 'npm install && npm run build'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "Running tests..."
                    // Insert your test commands here
                    // sh 'mvn test'
                    // sh 'gradle test'
                    // sh 'npm test'
                }
            }
            post {
                always {
                    junit '**/target/test-reports/*.xml'
                }
            }
        }

        stage('Package') {
            steps {
                script {
                    def version = readFile(SEMVER_FILE).trim()
                    echo "Packaging version: ${version}"
                    sh "docker build -t ${DOCKER_IMAGE}:${version} ."
                }
            }
        }

        stage('Publish') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    def version = readFile(SEMVER_FILE).trim()
                    echo "Publishing version: ${version}"
                    sh "docker push ${DOCKER_IMAGE}:${version}"

                    sh "git tag -a ${version} -m 'Release ${version}'"
                    sh "git push origin ${version}"
                }
            }
        }
    }

    post {
        success {
            echo 'Build completed successfully!'
        }
        failure {
            echo 'Build failed.'
        }
        always {
            cleanWs()
        }
    }
}
