pipeline {
  agent any

  parameters {
    string(
      name: 'LOCALES_DIR',
      defaultValue: 'locales',
      description: 'Directory of locale JSON files to validate'
    )
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Validate') {
      steps {
        sh 'bash tools/run_checks.sh --locales-dir "${LOCALES_DIR}"'
      }
    }

    stage('Report') {
      steps {
        archiveArtifacts artifacts: 'reports/locale-report.txt', fingerprint: true
      }
    }
  }

  post {
    success {
      echo 'Locale QA passed. All locale files match English keys and placeholders.'
    }
    failure {
      echo 'Locale QA failed. Open the archived locale-report.txt and fix missing/extra/empty/placeholder issues.'
    }
    unstable {
      echo 'Locale QA is unstable (warnings only).'
    }
    always {
      echo "Build result: ${currentBuild.currentResult}"
    }
  }
}