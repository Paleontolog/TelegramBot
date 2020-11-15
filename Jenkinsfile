// def withDockerNetwork(Closure inner) {
//   try {
//     networkId = UUID.randomUUID().toString()
//     sh "docker network create ${networkId}"
//     inner.call(networkId)
//   } finally {
//     sh "docker network rm ${networkId}"
//   }
// }


pipeline {
    
    agent {
       node { label 'master' } 
    }
    
   environment {
        registry = "paleontolog/go_bot"
        registryCredential = 'dockerhub'
   }
   
   stages {
        //  stage('Build') {
        //     agent {
        //         docker { 
        //             image 'golang' 
        //           // args '-v $HOME/.cache/go-build:/.cache/go-build'
        //         }
        //     } 
        //     steps {
        //       git branch: 'master', credentialsId: 'github', url: 'https://github.com/Paleontolog/TelegramBot.git'
        //       sh 'go get -d -v  github.com/Syfaro/telegram-bot-api'
        //       sh 'go get -d -v  github.com/lib/pq'
        //       sh 'env XDG_CACHE_HOME=/tmp/.cache env CGO_ENABLED=0 go build -o ./target/main  bot/main.go '
        //       stash includes: 'target/main', name: 'mainFile'
        //       stash includes: 'Dockerfile', name: 'dockerfile'
        //     }
        // }
        
        // stage('Build docker image') {
        //     steps {
        //         unstash 'dockerfile'
        //         unstash 'mainFile'
        //         script {
        //           def dockerHome = tool 'myDocker'
        //           env.PATH = "${dockerHome}/bin:${env.PATH}"    
                   
        //           def myDocker = docker.build("${registry}:${env.BUILD_ID}")
        //           docker.withRegistry('', registryCredential ) {
        //                 myDocker.push()
        //           }   
        //         }
        //     }
        // }
        
        // stage('Remove container') {
        //     steps {
        //         script {
        //             try {
        //                 sh "docker rmi ${registry}:${env.BUILD_ID}"
        //             } catch (exc) {
        //                 print("Container not found")
        //             }
        //         }
        //     }
        // }
        
        
        stage('Pull container') {
            steps {
                script {
                    try {
                        //  docker.image("${registry}:23").inside("-it --rm -e API_KEY=API_KEY=1428953537:AAGXZr4wTMQAUCvjZnyo1-nbEf5QDsT3j3w -p 80:80 --name gotest --entrypoint=''"){
                        //      sh './main'
                        //  }
                        sh "docker run --rm -e API_KEY=1428953537:AAGXZr4wTMQAUCvjZnyo1-nbEf5QDsT3j3w -p 80:80 --name gotest ${registry}:23"
                    } catch(ex){
                        print(ex)
                    }
                }
            }
        }
    }
    post {
        always {
              script {
                    try {
                        sh "docker rmi ${registry}:${env.BUILD_ID}"
                    } catch (exc) {
                        print(exc)
                    }
                }
        }
    }
}
