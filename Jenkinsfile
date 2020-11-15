def withDockerNetwork(Closure inner) {
  try {
    networkId = UUID.randomUUID().toString()
    sh "docker network create ${networkId}"
    inner.call(networkId)
  } finally {
    sh "docker network rm ${networkId}"
  }
}


pipeline {
    
    agent {
       node { label 'master' } 
    }
    
   environment {
        registry = "paleontolog/go_bot"
        registryCredential = 'dockerhub'
        apikey = credentials('apikey')
   }
   
   stages {
         stage('Build') {
            agent {
                docker { 
                    image 'golang' 
                  // args '-v $HOME/.cache/go-build:/.cache/go-build'
                }
            } 
            steps {
              git branch: 'master', credentialsId: 'github', url: 'https://github.com/Paleontolog/TelegramBot.git'
              sh 'go get -d -v  github.com/Syfaro/telegram-bot-api'
              sh 'go get -d -v  github.com/lib/pq'
              sh 'env XDG_CACHE_HOME=/tmp/.cache env CGO_ENABLED=0 go build -o ./target/main  bot/main.go '
              stash includes: 'target/main', name: 'mainFile'
              stash includes: 'Dockerfile', name: 'dockerfile'
            }
        }
        
        stage('Build docker image') {
            steps {
                unstash 'dockerfile'
                unstash 'mainFile'
                script {
                  def dockerHome = tool 'myDocker'
                  env.PATH = "${dockerHome}/bin:${env.PATH}"    
                   
                  def myDocker = docker.build("${registry}:${env.BUILD_ID}")
                  docker.withRegistry('', registryCredential ) {
                        myDocker.push()
                  }   
                }
            }
        }
        
        stage('Remove container') {
            steps {
                script {
                    try {
                        sh "docker rmi ${registry}:${env.BUILD_ID}"
                    } catch (exc) {
                        print("Container not found")
                    }
                }
            }
        }
        
        
//   stage('Pull container') {
//             steps {
//                 script {
//                     try {
//                         withDockerNetwork{ n ->
//                             docker.image("${registry}:23").withRun("--network ${n} -e ${apikey} --name gotest") { c ->
//                               docker.image('curlimages/curl').inside("""--network ${n} --entrypoint=''""") {
                                   
//                                     sh '''
//                                         set +x;
//                                          x=0; 
//                                          while [ $x -lt 100 ] && ! curl gotest:8080/-_-api/v1/hello  --output /dev/null; 
//                                          do 
//                                             x=$(( $x + 1 )); 
//                                             sleep 1; 
//                                          done
//                                     '''
                                    
//                                     def response = sh(
//                                         script: '''
//                                             $(curl --write-out '%{http_code}' \
//                                                 --silent --output /dev/null gotest:8080)
//                                         ''', 
//                                         returnStdout: true).trim()
//                                     print(response)
                                    
//                                     assert response == '200'
//                               }
//                             }
//                         } 
//                     } catch(ex){
//                         print(ex)
//                     }
//                 }
//             }
//   }    
        
        
    stage('Pull container') {
            steps {
                script {
                    try {
                        sh "docker run -d -e ${apikey} -p 80:80 --name gotest ${registry}:${env.BUILD_ID}"
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
