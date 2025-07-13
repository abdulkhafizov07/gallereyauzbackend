pipeline {
    agent any

    environment {
        VENV_PATH = "${env.WORKSPACE}/env"
        DEPLOY_USER = "a"
        DEPLOY_HOST = "195.158.4.211"
        DEPLOY_PATH = "/home/a/Projects/gallereya/backend"
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-ssh-key', url: 'git@github.com:abdulkhafizov07/gallereyauzbackend.git', branch: 'main'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh "python3 -m venv ${VENV_PATH}"
                sh "${VENV_PATH}/bin/pip install --upgrade pip"
                sh "${VENV_PATH}/bin/pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                sh "${VENV_PATH}/bin/python -m pytest tests"
            }
        }

        stage('Deploy to Server') {
            steps {
                sshagent(credentials: ['your-ssh-credentials-id']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} << 'EOF'
                    cd ${DEPLOY_PATH}
                    git pull origin main
                    source env/bin/activate
                    pip install -r requirements.txt
                    sudo systemctl restart gallereya-backend.service
                    EOF
                    """
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

