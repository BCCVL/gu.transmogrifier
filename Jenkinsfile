pipeline {

    agent {
        docker {
            image 'python:2'
        }
    }

    stages {

        stage('Build') {

            steps {
                // environment {} is executed in node context, and there is no WORKSPACE defined
                withPyPi() {
                    // clean up workenv but keep cached eggs
                    sh 'git clean -x -d -f -e "eggs"'
                    // get pip
                    sh 'easy_install pip'
                    // install build env
                    sh "pip install -r requirements.txt"
                    // build everything
                    sh 'buildout'
                }
            }

        }
        stage('Test') {

            steps {
                withPyPi() {
                    sh(script: './bin/test',
                       returnStatus: true)
                }
                // capture test result
                step([
                    $class: 'XUnitBuilder',
                    thresholds: [
                        [$class: 'FailedThreshold', failureThreshold: '0',
                                                    unstableThreshold: '1']
                    ],
                    tools: [
                        [$class: 'JUnitType', deleteOutputFiles: true,
                                              failIfNotNew: true,
                                              pattern: 'parts/test/testreports/*.xml',
                                              stopProcessingIfError: true]
                    ]
                ])
            }

        }

        stage('Package') {
            when {
                expression {
                    // check if we want to publish a package
                    return publishPackage(currentBuild.result, env.BRANCH_NAME)
                }
            }
            steps {
                withPyPi() {
                    // Build has to happen in correct folder or setup.py won't find MANIFEST.in file and other files
                    sh 'python setup.py register -r devpi sdist bdist_wheel upload -r devpi'
                }
            }
        }

    }

    post {
        always {
            echo "This runs always"

            // does this plugin get committer emails by themselves?
            // alternative would be to put get commiter email ourselves, and list of people who need to be notified
            // and put mail(...) step into each appropriate section
            // => would this then send 2 emails? e.g. changed + state email?
            step([
                $class: 'Mailer',
                notifyEveryUnstableBuild: true,
                recipients: 'gerhard.weis@gmail.com ' + emailextrecipients([
                    [$class: 'CulpritsRecipientProvider'],
                    [$class: 'RequesterRecipientProvider']
                ])
            ])
        }
        success {
            echo 'This will run only if successful'
            //triggerDownstream('org.bccvl.movelib', env.BRANCH_NAME)
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, the Pipeline was previously failing but is now successful'
        }
    }

}
