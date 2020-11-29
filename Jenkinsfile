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
        apikeychecker = credentials('apikeychecker')
        chatid = credentials('chatid')
    }

    stages {
        stage('Build docker image') {
            steps {
                git branch: 'master', credentialsId: 'github', url: 'https://github.com/Paleontolog/TelegramBot.git'
                script {
                    def dockerHome = tool 'myDocker'
                    env.PATH = "${dockerHome}/bin:${env.PATH}"

                    def myDocker = docker.build("${registry}:${env.BUILD_ID}", ".")
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

        stage('Pull container') {
            steps {
                script {
                    try {
                        withDockerNetwork{ n ->
                           docker.image("${registry}:${env.BUILD_ID}").withRun("--network ${n} -e ${apikey} --name gobot") { c ->
                              docker.image('paleontolog/bot_checker').withRun("""--network ${n} -e ${apikeychecker} -e ${chatid} --name testgobot""") { e ->
                                    sleep(10)
                                    sh 'docker cp testgobot:/root/sample.log .'
                                
                                    def response = sh(
                                        script: "grep -c OK sample.log",
                                        returnStdout: true).trim()
                                    
                                    print(response)
                                    assert response != '0'
                                    sh 'rm -rf sample.log'
                              }
                            }
                        }
                    } catch(ex) {
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

