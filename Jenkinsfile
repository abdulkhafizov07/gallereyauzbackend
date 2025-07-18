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

    stage('Prepare database') {
      steps {
        sh '''
          env/bin/alembic upgrade head
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          if [ -d tests ]; then
            env/bin/python -m pytest
          fi
        '''
      }
    }

    stage('Deploy') {
      when {
        branch 'main'
      }

      steps {
        sshagent(['deploy-local-server-1823']) {
          sh '''
            mkdir -p ~/.ssh
            ssh-keyscan -H 10.0.18.23 >> ~/.ssh/known_hosts

            rsync -avz --exclude='env' --exclude='.git' ./ a@10.0.18.23:/home/a/gallereya/backend

            ssh a@10.0.18.23 '
              cd /home/a/gallereya/backend

              if [ ! -d "env" ]; then
                python3.12 -m venv env
              fi

              env/bin/pip install -r requirements.txt
              env/bin/alembic upgrade head

              sudo /bin/systemctl restart gallereya-backend.service
            '
          '''
        }
      }
    }
  }
}
