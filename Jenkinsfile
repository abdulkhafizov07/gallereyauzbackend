pipeline {
  agent {
    label "python-agent"
  }

  environment {
    VENV = "${WORKSPACE}/venv"
    PYTHON = "${VENV}/bin/python"
    UVICORN = "${VENV}/bin/uvicorn"
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
         if [ ! -d venv ]; then
            echo "Creating virtual environment"
            python3 -m venv venv
          fi
          make install-dev
        '''
      }
    }

    stage('Format & Lint') {
      steps {
        sh 'make format lint'
      }
    }

    stage('Build') {
      steps {
        sh 'make build'
      }
    }

    stage('Run Tests') {
      steps {
        sh 'make test'
      }
    }

    stage('Clean') {
      steps  {
        sh 'make clean'
      }
    }

    stage('Deploy') {
      when {
        branch 'main'
      }
      steps {
        sshagent(['deploy-local-server-1823']) {
          sh './deploy.sh'
        }
      }
    }
  }
}
