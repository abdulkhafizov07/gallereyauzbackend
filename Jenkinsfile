pipeline {
  agent {
    label "python-agent"
  }

  environment {
    VENV = "${WORKSPACE}/env"
    PYTHON = "${WORKSPACE}/env/bin/python"
    UVICORN = "${WORKSPACE}/env/bin/uvicorn"
    ENTRYPOINT = "main:app"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install Dependencies') {
      steps {
        sh '''
          echo "Searching for virtualenv"
          echo "System python version $(python3 --version)"
          if [ ! -d env ]; then
            echo "Can not find virtualenv\nCreating it env"
            python3 -m venv env
          fi
          echo "Virtualenv python version $(env/bin/python3 --version)"
          env/bin/pip install --upgrade pip
          env/bin/pip install -r requirements.txt
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          if [ -d tests ]; then
            env/bin/python -m pytest || true
          fi
        '''
      }
    }

    stage('Deploy') {
      steps {
          sshagent (credentials: ['deploy-local-server-1823']) {
            sh '''
            ssh -o StrictHostKeyChecking=no a@10.0.18.23 << EOF
              DEPLOY_FOLDER="/home/a/gallereya/backend"
              GITHUB_URL="git@github.com:abdulkhafizov07/gallereyauzbackend.git"

              mkdir -p "$DEPLOY_FOLDER"
              if [ -d "$DEPLOY_FOLDER/.git" ]; then
                echo "Repo already exists at $DEPLOY_FOLDER - skipping clone."
              else
                echo "Clonning for the first time"
                git clone "$GITHUB_URL" "$GITHUB_URL"
              fi
          '''
        }
      }
    }
  }
}
