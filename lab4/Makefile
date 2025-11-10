push-dvc-titanic:
	dvc add datasets/titanic.csv && \
	git add .
	git add ../.dvc/
	git commit -m "Добавлен датасет Титаника" && \
	dvc push