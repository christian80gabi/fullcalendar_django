pipeline {
  agent any
  stages {
    stage('Checkout Code') {
      steps {
        git(url: 'https://github.com/christian80gabi/fullcalendar_django', branch: 'main')
      }
    }

    stage('Print out list of files') {
      steps {
        sh 'ls -la'
      }
    }

  }
}