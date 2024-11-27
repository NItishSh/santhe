pipeline {
    agent any

    parameters {
        string(name: 'DOCKER_IMAGE', defaultValue: 'your-image-name', description: 'Docker image name')
    }

    environment {
        SEMVER_FILE = "semver.txt"
        GIT_COMMIT_SHORT = "${env.GIT_COMMIT.take(7)}"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        ansiColor('xterm')
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

                    def preRelease = env.BRANCH_NAME == "main" ? "" :
                                     env.BRANCH_NAME == "develop" ? "-beta.${env.BUILD_NUMBER}" :
                                     env.BRANCH_NAME.startsWith("feature/") ? "-alpha.${env.BUILD_NUMBER}" :
                                     "-rc.${env.BUILD_NUMBER}"

                    def newVersion = "${major}.${minor}.${patch}${preRelease}"
                    writeFile file: SEMVER_FILE, text: newVersion
                    echo "New version determined: ${newVersion}"
                }
            }
        }

        stage('Lint') {
            steps {
                script {
                    echo "Running lint checks using Docker..."
                    sh "docker build --target lint -t ${params.DOCKER_IMAGE}:${env.BUILD_NUMBER}-lint ."
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    echo "Building the application using Docker..."
                    sh "docker build --target build -t ${params.DOCKER_IMAGE}:${env.BUILD_NUMBER}-build ."
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "Running tests using Docker..."
                    sh "docker build --target test -t ${params.DOCKER_IMAGE}:${env.BUILD_NUMBER}-test ."
                }
            }
            post {
                always {
                    junit '**/target/test-reports/*.xml' // Adjust the path based on your project
                    echo 'Tests completed'
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                script {
                    echo "Running static code analysis using Docker..."
                    sh "docker build --target static-analysis -t ${params.DOCKER_IMAGE}:${env.BUILD_NUMBER}-static-analysis ."
                }
            }
        }

        stage('Package') {
            steps {
                script {
                    def version = readFile(SEMVER_FILE).trim()
                    echo "Packaging version: ${version}"
                    sh "docker build --target production -t ${params.DOCKER_IMAGE}:${version} ."
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
                    sh "docker push ${params.DOCKER_IMAGE}:${version}"

                    sh "git tag -a ${version} -m 'Release ${version}'"
                    sh "git push origin ${version}"
                }
            }
        }
    }

    post {
        success {
            echo 'Build completed successfully!'
            // Add notification logic here (e.g., Slack or email)
        }
        failure {
            echo 'Build failed.'
            // Add notification logic here (e.g., Slack or email)
        }
        always {
            cleanWs()
        }
    }
}
