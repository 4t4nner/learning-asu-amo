## Отчет по заданию 4

### Курс "Автоматизация машинного обучения"

<p style="text-align: end;">Выполнил: Артём Кожевников</p>
<p style="text-align: end;">4-406м3</p>

Репозиторий [доступен по ссылке](https://github.com/4t4nner/learning-asu-amo) . Этот отчет [доступен по ссылке](https://github.com/4t4nner/learning-asu-amo/tree/main/lab4) 


### 2. Установите git и dvc
![alt text](image.png)

### 3-5. Создайте папку проекта.
```bash
git clone https://github.com/4t4nner/learning-asu-amo
cd learning-asu-amo
mkcd lab4
```
![alt text](image-1.png)

### 6. Настройте удаленное хранилище файлов, например на Google Disk.
- сделал редактируемую всеми папку на гуглдиске (будет удалена после публикации)

![alt text](image-2.png)

### 7. Создайте датасет о пассажирах “Титаника”, например, catboost.titanic().
- [lab4.py](lab4.py)
```bash
t4nner@w: lab4 code lab4.py
t4nner@w: lab4 source /home/t4nner/.venv         
t4nner@w: lab4 pip install -r requirements.txt 
```
![alt text](image-3.png)



### 
Я так и не смог настроить доступ к gdrive.
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)
![alt text](image-8.png)

С указанием аккаунта консоли в доступе к папке - всё равно не работает.
```bash
GDRIVE_CREDENTIALS_DATA=/mnt/DATA/projects/asu/learning-asu-amo/lab4/asu-amo-***.json dvc push --remote  gdrive
```


**Буду использовать удалённое ssh хранилище**, доступное по ssh ключу:
```bash
dvc remote add -d <branch_name> ssh://user@host<:optional_port>/path
```
![alt text](image-9.png)
![alt text](image-10.png)
![alt text](image-11.png)

