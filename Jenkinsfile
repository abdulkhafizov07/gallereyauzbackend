pipeline {
  agent any

  environment {
    VENV = "${WORKSPACE}/env"
    PYTHON = "${WORKSPACE}/env/bin/python"
    UVICORN = "${WORKSPACE}/env/bin/uvicorn"
    ENTRYPOINT = "main:app"
  }

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/your-user/your-repo.git'
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
            env/bin/python -m unittest discover tests || true
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

