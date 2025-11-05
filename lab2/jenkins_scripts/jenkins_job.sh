#!/bin/bash
# jenkins_job.sh

# Запускаем pipeline из lab1
cd /var/jenkins_home/workspace/lab1 || exit 1

# Копируем скрипты в текущую директорию для запуска
cp /app/*.py .
cp /app/pipeline.sh .

# Даем права на выполнение
chmod +x pipeline.sh

# Запускаем pipeline
./pipeline.sh

# Копируем результаты обратно для сохранения в артефактах
mkdir -p /var/jenkins_home/artifacts
cp -r data_gen data models /var/jenkins_home/artifacts/

echo "Pipeline успешно завершен"