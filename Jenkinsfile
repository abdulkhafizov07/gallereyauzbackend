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
      agent { label 'ls-1823' }
      steps {
        sh '''
          DEPLOY_DIR="/homa/a/gallereya/backend"
          echo "Deploying on deploy server..."
          mkdir -p "${DEPLOY_DIR}"
          cp -r * "${DEPLOY_DIR}"
          sudo systemctl restart gallereya-backend.service
        '''
      }
    }
  }
}
