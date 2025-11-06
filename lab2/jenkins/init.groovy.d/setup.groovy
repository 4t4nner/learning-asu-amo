import jenkins.model.*
import hudson.security.*
import hudson.model.*

println "=== НАЧАЛО АВТОМАТИЧЕСКОЙ ИНИЦИАЛИЗАЦИИ JENKINS ==="
println "Время: ${new Date()}"

// Ждем полной загрузки Jenkins и плагинов
println "Ожидание полной загрузки Jenkins и плагинов (30 секунд)..."
sleep(30 * 1000)

def instance = Jenkins.getInstance()

try {
    println "Пользователь admin/admin :"
    
    // admin/admin
    def hudsonRealm = new HudsonPrivateSecurityRealm(false)
    hudsonRealm.createAccount("admin", "admin")
    instance.setSecurityRealm(hudsonRealm)
    
    def strategy = new GlobalMatrixAuthorizationStrategy()
    strategy.add(Jenkins.ADMINISTER, "admin")
    strategy.add(Jenkins.READ, "anonymous")
    instance.setAuthorizationStrategy(strategy)
    
    println "Безопасность! end"
    
    println "Создание pipeline job 'ml_pipeline'..."
    
    def jobName = "ml_pipeline"
    def job = instance.getItemByFullName(jobName)
    
    if (job == null) {
        // Создаем Pipeline job
        job = instance.createProject(org.jenkinsci.plugins.workflow.job.WorkflowJob.class, jobName)
        
        def pipelineScript = """
        pipeline {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-v /var/jenkins_home/workspace/lab1:/app -v /var/jenkins_home/workspace/lab1/data_gen:/app/data_gen -v /var/jenkins_home/workspace/lab1/data:/app/data -v /var/jenkins_home/workspace/lab1/models:/app/models'
                }
            }
            stages {
                stage('Run ML Pipeline') {
                    steps {
                        script {
                            sh 'cd /app && ls -la && chmod +x pipeline.sh && ./pipeline.sh'
                        }
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'data_gen/**/*, data/**/*, models/**/*', fingerprint: true
                }
            }
        }
        """
        
        // Сохраняем пайплайн
        job.setDefinition(new org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition(pipelineScript, true))
        println "Pipeline job 'ml_pipeline' успешно создан"
    } else {
        println "Job 'ml_pipeline' уже существует, пропускаем"
    }
    
    // Сохраняем все изменения
    instance.save()
    println "настройки end"
    
} catch (Exception e) {
    println "ОШИБКА ПРИ ИНИЦИАЛИЗАЦИИ: ${e.getMessage()}"
    e.printStackTrace()
}

println "=== ИНИЦИАЛИЗАЦИЯ JENKINS ЗАВЕРШЕНА ==="