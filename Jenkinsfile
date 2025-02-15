pipeline {
    agent any
    environment {
        AWS_REGION = "${env.AWS_REGION}"
        DOCKER_IMAGE = "${env.DOCKER_IMAGE}" 
        DOCKER_CREDENTIALS_ID = 'DOCKER_TOKEN'
    }
    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                        apt update -y
                        apt install -y python3-pip pylint jq zip python3-venv docker.io
                    '''
                }
            }
        }
        stage('Identify Changed Lambda Files') {
            steps {
                script {
                    env.CHANGED_LAMBDA_FILES = sh(
                        script: 'git diff --name-only HEAD~1 HEAD | grep "^lambda_handler/" | grep ".py$"',
                        returnStdout: true
                    ).trim()
                    if (!env.CHANGED_LAMBDA_FILES) {
                        echo "No Lambda files changed."
                        currentBuild.result = 'SUCCESS'
                        return
                    }
                    echo "Changed Lambda files: ${env.CHANGED_LAMBDA_FILES}"
                }
            }
        }
        stage('Run Pylint on Lambda Functions') {
            when {
                expression { env.CHANGED_LAMBDA_FILES }
            }
            steps {
                script {
                    sh "pylint --fail-under=3 ${env.CHANGED_LAMBDA_FILES}"
                }
            }
        }
        stage('Unit-test') {
            when {
                expression { env.CHANGED_LAMBDA_FILES }
            }
            steps {
                script {
                    def lambdaFiles = env.CHANGED_LAMBDA_FILES.split('\n')
                    for (lambdaFile in lambdaFiles) {
                        def functionName = lambdaFile.tokenize('/').last().replace('.py', '')
                        echo "This is functionName: ${functionName}"

                        catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                            sh """
                                ls -l
                                cd lambda_handler/tests
                                python3 -m venv env
                                ls -l
                                . env/bin/activate
                                ls -l
                                pip install -r requirements.txt
                                python -m unittest ${functionName}_test.py
                            """
                        }
                    }
                }
            }
        }
        stage('Package Lambda Functions') {
            when {
                expression { env.CHANGED_LAMBDA_FILES }
            }
            steps {
                script {
                    def lambdaFiles = env.CHANGED_LAMBDA_FILES.split('\n')
                    for (lambdaFile in lambdaFiles) {
                        def functionName = lambdaFile.tokenize('/').last().replace('.py', '')
                        def lambdaFilename = lambdaFile.tokenize('/').last()
                        def zipFileName = "${functionName}.zip"

                        echo "Processing Lambda function: ${functionName}"
                        echo "Lambda file name: ${lambdaFilename}"
                        echo "Zip file name: ${zipFileName}"

                        if (fileExists("lambda_handler/${functionName}/requirements.txt")) {
                            echo "Installing dependencies for ${functionName} from requirements.txt"

                            if (!fileExists("lambda_handler/${functionName}/package")) {
                                echo "Package directory does not exist. Creating directory for ${functionName}."
                                sh """
                                    mkdir -p lambda_handler/${functionName}/package
                                """
                            } else {
                                echo "Package directory already exists. Skipping directory creation for ${functionName}."
                            }

                            sh """
                                pip install --target lambda_handler/${functionName}/package -r lambda_handler/${functionName}/requirements.txt
                                cd lambda_handler/${functionName}/package
                                zip -r ../${zipFileName} .
                                cd ..
                                zip -g ${zipFileName} ${lambdaFilename}
                                ls -lh
                            """
                        } else {
                            echo "No requirements.txt found for ${functionName}. Skipping dependency installation."
                        }
                    }
                }
            }
        }
        stage('Deploy Lambda Function') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    script {
                        def lambdaFiles = env.CHANGED_LAMBDA_FILES.split('\n')
                        for (lambdaFile in lambdaFiles) {
                            def functionName = lambdaFile.tokenize('/').last().replace('.py', '')
                            def zipFileName = "${functionName}.zip"
                            def artifactPath = "lambda_handler/${functionName}/${zipFileName}"

                            echo "Deploying Lambda function: ${functionName}"
                            echo "This is the zip: ${zipFileName}"
                            sh 'ls -l'
                            deployLambda(
                                functionName: functionName,
                                artifactLocation: "/var/jenkins_home/workspace/lambda-jenkin/lambda_handler/${functionName}/${zipFileName}",
                                updateMode: 'code',
                                awsAccessKeyId: "${AWS_ACCESS_KEY_ID}",
                                awsSecretKey: "${AWS_SECRET_ACCESS_KEY}",
                                awsRegion: env.AWS_REGION
                            )
                        }
                    }
                }
            }
        }
        stage('Run Pylint on Website') {
            steps {
                script {
                    sh 'pylint --fail-under=5 src/http_app/app.py'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                sh' ls -l'
                    docker.build("${env.DOCKER_IMAGE}", ".")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', env.DOCKER_CREDENTIALS_ID) {
                        def image = docker.image("${env.DOCKER_IMAGE}")
                        image.push('latest')
                    }
                }
            }
        }
    }
}
