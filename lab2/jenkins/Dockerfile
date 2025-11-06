# jenkins/Dockerfile
FROM jenkins/jenkins:lts-jdk21

# Копируем файл с плагинами
COPY --chown=jenkins:jenkins plugins.txt /usr/share/jenkins/ref/plugins.txt

# Устанавливаем плагины через Jenkins CLI
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

# Копируем скрипты инициализации
COPY --chown=jenkins:jenkins init.groovy.d/ /usr/share/jenkins/ref/init.groovy.d/

# Пробрасываем переменные окружения
ENV JENKINS_OPTS --prefix=/jenkins
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

USER jenkins