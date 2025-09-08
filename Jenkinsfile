pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Build image') {
      steps { sh 'docker compose build' }
    }
    stage('Unit tests') {
      steps { sh 'docker compose run --rm test' }
      post { always { sh 'docker compose rm -f test || true' } }
    }
    stage('Deploy API') {
      steps {
        sh 'docker compose down'
        sh 'docker compose up -d api'
      }
    }
  }
  environment {
    OPENWEATHER_API_KEY = credentials('1ae22c96f65feed51923e80599a286f5')
  }
  options { timestamps() }
}
