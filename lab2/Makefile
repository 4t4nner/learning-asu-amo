# Makefile
.DEFAULT_GOAL := all

# Пути к данным и моделям
DATA_GEN_DIR := ../lab1/data_gen
DATA_DIR := ../lab1/data
MODELS_DIR := ../lab1/models
JENKINS_DIR := ./jenkins
JENKINS_HOME := ./jenkins_home

all: setup start-jenkins wait-for-jenkins run-pipeline

setup: create-dirs copy-requirements build-jenkins build-ml

create-dirs:
	@mkdir -p $(DATA_GEN_DIR) $(DATA_DIR) $(MODELS_DIR) $(JENKINS_HOME)
	@mkdir -p $(JENKINS_DIR)/init.groovy.d
	@echo "✅ Директории созданы"

copy-requirements:
	@cp ../lab1/requirements.txt .
	@echo "✅ requirements.txt скопирован"

build-jenkins:
	@docker compose build jenkins
	@echo "✅ Jenkins образ успешно собран"

build-ml:
	@docker compose build ml-pipeline
	@echo "✅ ML pipeline образ успешно собран"

start-jenkins:
	@docker compose up -d jenkins
	@echo "🚀 Jenkins запускается в фоновом режиме..."

wait-for-jenkins:
	@echo "⏳ Ожидание полной инициализации Jenkins (120 секунд)..."
	@for i in {1..12}; do \
		sleep 10; \
		echo "⏳ Ожидание... $$(($$i * 10)) секунд из 120"; \
		if curl -s http://localhost:8089/jenkins/login > /dev/null; then \
			echo "✅ Jenkins готов к работе"; \
			break; \
		fi; \
	done
	@echo "🔗 Jenkins доступен по адресу: http://localhost:8089/jenkins"
	@echo "🔑 Логин: admin, Пароль: admin"

run-pipeline:
	@docker compose up --force-recreate --no-deps ml-pipeline
	@echo "✅ ML Pipeline успешно выполнен"

jenkins-logs:
	@docker compose logs -f jenkins

ml-logs:
	@docker compose logs -f ml-pipeline

jenkins-console:
	@docker exec -it jenkins_lab2 bash

clean-data:
	@echo "🧹 Очистка данных..."
	@rm -rf $(DATA_GEN_DIR)/* $(DATA_DIR)/* $(MODELS_DIR)/* 2>/dev/null || true
	@echo "✅ Данные очищены"

clear-all: clean-data
	@echo "🔥 Полная очистка..."
	@docker compose down -v --remove-orphans
	@docker image prune -f
	@rm -rf $(JENKINS_HOME) $(JENKINS_DIR)/init.groovy.d/*.groovy
	@rm -f requirements.txt
	@echo "✅ Все контейнеры, образы и данные удалены"

.PHONY: all setup create-dirs copy-requirements build-jenkins build-ml start-jenkins wait-for-jenkins run-pipeline jenkins-logs ml-logs jenkins-console clean-data clear-all