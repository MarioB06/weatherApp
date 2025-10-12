pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Backend Tests') {
      steps {
        sh 'docker compose run --rm test'
      }
      post {
        always { sh 'docker compose rm -f test || true' }
      }
    }
    stage('Frontend Build') {
      steps {
        sh 'docker compose run --rm frontend npm run build'
      }
      post {
        always { sh 'docker compose rm -f frontend || true' }
      }
    }
    stage('Build Images') {
      steps { sh 'docker compose build api frontend' }
    }
    stage('Deploy API (optional)') {
      when { expression { return params?.DEPLOY ?: false } }
      steps {
        sh 'docker compose down'
        sh 'docker compose up -d api'
      }
    }
  }
  environment {
    OPENWEATHER_API_KEY = credentials('1ae22c96f65feed51923e80599a286f5')
  }
  parameters {
    booleanParam(name: 'DEPLOY', defaultValue: false, description: 'API nach erfolgreichem Build starten')
  }
  options { timestamps() }
}
