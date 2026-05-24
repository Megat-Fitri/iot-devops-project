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
        
        stage('Test App') {
            steps {
                echo 'Running automated tests...'
                script {
                    // Remove old test container if exists
                    sh 'docker rm -f test-container || true'
                    
                    // Start test container
                    sh 'docker run -d --name test-container -p 5001:5000 ${DOCKER_IMAGE}:v${BUILD_NUMBER}'
                    
                    // Wait for Flask to be ready
                    sh '''
                        echo "Waiting for Flask to start..."
                        for i in $(seq 1 30); do
                            if curl -s -f http://localhost:5001/health > /dev/null 2>&1; then
                                echo "Flask is ready!"
                                break
                            fi
                            echo "Attempt $i: not ready yet..."
                            sleep 1
                        done
                    '''
                    
                    // Install requests and run tests
                    sh 'pip3 install requests --break-system-packages'
                    sh 'python3 test_app.py'
                }
            }
            post {
                always {
                    sh 'docker stop test-container || true'
                    sh 'docker rm test-container || true'
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Tests passed! Pushing image to Docker Hub...'
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
            echo '✅ SUCCESS! All tests passed, image pushed to Docker Hub!'
        }
        failure {
            echo '❌ FAILED! Either tests failed or push failed. Check logs above.'
        }
    }
}