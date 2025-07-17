pipeline {
  agent {
    label "docker-agent"
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
          if [ ! -d env ]; then
            python3 -m venv env
          fi
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
        sh '''
          pkill -f "uvicorn ${ENTRYPOINT}" || true
          nohup ${UVICORN} ${ENTRYPOINT} --host 0.0.0.0 --port 8000 &
        '''
      }
    }
  }
}

