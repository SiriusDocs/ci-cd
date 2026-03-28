pipeline {
    agent any
    
    environment {
        GIT_CREDENTIALS_ID = 'git-credentials'
        REGISTRY_CREDENTIALS_ID = 'registry-credentials'
        REGISTRY_URL = 'registry.certsirius.ru'
        IMAGE_NAME = 'frontend-prod'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/SiriusDocs/frontend.git',
                        credentialsId: env.GIT_CREDENTIALS_ID
                    ]]
                ])
            }
        }
        
        stage('Build & Push') {
            steps {
                script {
                    docker.withRegistry("https://${REGISTRY_URL}", env.REGISTRY_CREDENTIALS_ID) {
                        def customImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                        customImage.push()
                        customImage.push('latest')
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}