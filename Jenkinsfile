pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mefitt/iot-app'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build("${DOCKER_IMAGE}:v${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE}:v${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_IMAGE}:v${BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ SUCCESS! Image pushed to Docker Hub!'
        }
        failure {
            echo '❌ FAILED! Check the logs above.'
        }
    }
}