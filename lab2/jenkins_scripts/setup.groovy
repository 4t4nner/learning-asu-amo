# jenkins_scripts/setup.groovy
import jenkins.model.*
import hudson.security.*
import org.jenkinsci.plugins.workflow.libs.*

def instance = Jenkins.getInstance()

def jobName = "ml_pipeline"
def repoPath = "/var/jenkins_home/workspace/lab1"

// Б безопасность
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount("admin", "admin")
instance.setSecurityRealm(hudsonRealm)

def strategy = new GlobalMatrixAuthorizationStrategy()
strategy.add(Jenkins.ADMINISTER, "admin")
instance.setAuthorizationStrategy(strategy)

// можно из интерфейса но всё равно создал груви
def job = instance.getItemByFullName(jobName)
if (job == null) {
    job = instance.createProject(org.jenkinsci.plugins.workflow.job.WorkflowJob.class, jobName)
}

// Настраиваем Jenkinsfile
def flowDef = """
pipeline {
    agent any
    stages {
        stage('Run ML Pipeline') {
            steps {
                script {
                    dir('${repoPath}') {
                        sh './pipeline.sh'
                    }
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'models/**/*,data/**/*', fingerprint: true
        }
    }
}
"""
job.setDefinition(new org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition(flowDef, true))

instance.save()