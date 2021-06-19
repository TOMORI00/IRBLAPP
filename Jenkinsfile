pipeline {
    agent any

    stages {
        stage('pull code') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/develop']], extensions: [], userRemoteConfigs: [[credentialsId: 'c95a2f8d-c4c3-429e-b3c2-1c47b84f2a39', url: 'http://212.129.149.40/cdwx/backend-irblapp.git']]])
            }
        }
        stage('build') {
            steps {
                script{
                    dir("${env.WORKSPACE}/irblapp"){
                        sh'mvn clean package -Dmaven.test.skip=false'
                    }
                }

                 }
        }
        stage('coverage report'){
            steps{
                jacoco execPattern: '**/target/**.exec'
            }
        }
        stage('publish') {
            steps {
                deploy adapters: [tomcat8(credentialsId: 'ae10adcb-d29d-4735-93f7-6d769dfe1a34', path: '', url: 'http://81.70.101.44:8088/')], contextPath: 'irblapp', war: '**/target/*.war'
          }
        }
    }
}
