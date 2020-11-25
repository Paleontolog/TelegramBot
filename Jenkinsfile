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
        registry = 'paleontolog/go_bot'
        registryCredential = 'dockerhub'
        apikey = credentials('apikey')
    }

    stages {
        stage('Build docker image') {
            steps {
                git branch: 'master', credentialsId: 'github', url: 'https://github.com/Paleontolog/TelegramBot.git'
                script {
                    def dockerHome = tool 'myDocker'
                    env.PATH = "${dockerHome}/bin:${env.PATH}"

                    def myDocker = docker.build("TelegramBot/${registry}:${env.BUILD_ID}")
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
                        print('Container not found')
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
                    } catch (ex) {
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
