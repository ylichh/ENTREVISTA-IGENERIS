pipeline {
    agent any

    environment {
        IMAGE_NAME = 'mi-app-python'
    }

    stages {
        stage('Clone') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Smoke Test') {
            steps {
                sh 'docker run --rm $IMAGE_NAME python3 -c "import src.main; print(\"OK\")"'
            }
        }
    }

    post {
        always {
            sh 'docker rmi $IMAGE_NAME || true'
        }
    }
}
