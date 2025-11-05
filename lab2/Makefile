# по-умолчанию первая явно
.DEFAULT_GOAL := all

# Пути к данным и моделям
DATA_GEN_DIR := ../lab1/data_gen
DATA_DIR := ../lab1/data
MODELS_DIR := ../lab1/models

all: setup run-pipeline

setup: create-dirs
	@docker compose build
	@echo "Docker-образы успешно собраны"

create-dirs:
	@mkdir -p $(DATA_GEN_DIR) $(DATA_DIR) $(MODELS_DIR) jenkins_home jenkins_scripts
	@echo "Директории созданы"

start-jenkins:
	@docker compose up -d jenkins
	@echo "Ожидание запуска Jenkins (30 секунд)..."
	@sleep 30
	@echo "Jenkins запущен и доступен по адресу: http://localhost:8089/jenkins"
	@echo "Логин: admin, Пароль: admin"

run-pipeline:
	@docker compose up --build --force-recreate ml-pipeline
	@echo "ML Pipeline успешно выполнен"

run-jenkins-pipeline:
	@echo "Запуск Jenkins pipeline..."
	@docker exec jenkins_lab2 curl -s -X POST http://localhost:8080/jenkins/job/ml_pipeline/build \
		--user admin:admin \
		-H "Content-Type: application/x-www-form-urlencoded"
	@echo "Jenkins pipeline запущен: http://localhost:8089/jenkins"

jenkins: start-jenkins
	@echo ""
	@echo "Инструкции по настройке Jenkins job:"
	@echo "   1. Откройте http://localhost:8089/jenkins"
	@echo "   2. Создайте новый Pipeline job с именем 'ml_pipeline'"
	@echo "   3. В настройках Pipeline выберите 'Pipeline script from SCM'"
	@echo "   4. Укажите путь к Jenkinsfile в ../lab1/"
	@echo "   5. Сохраните и запустите job"

clean-data:
	@rm -rf $(DATA_GEN_DIR)/* $(DATA_DIR)/* $(MODELS_DIR)/* 2>/dev/null || true
	@echo "Данные очищены"

clear-all: clean-data
	@docker compose down -v --remove-orphans
	@docker image prune -f
	@rm -rf jenkins_home jenkins_scripts
	@echo "Все контейнеры, образы и данные удалены"

.PHONY: all setup create-dirs start-jenkins run-pipeline run-jenkins-pipeline jenkins clean-data clear-all