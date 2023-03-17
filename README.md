# Учебный проект - Сайт для онлайн-игры в камень-ножницы-бумага
Ссылка на рабочую версию сайта https://rock-paper-scissors-bl9y.onrender.com/
## Особенности проекта:
- Реализация онлайн игры и чата на технологии WebSocket
- Фронтенд на JavaScript + Bootstrap
- Бэкнд django + django channels

## Инструкция по поднятию dev версии на локальном компьютере:
- клонировать репозиторий
```
$ git clone https://github.com/Tren-123/rock_paper_scissors
```
- установить зависимости
```
$ pip install -r requirements.txt
```
- создать бд
```
$ python3 manage.py migrate

- создать нескольких пользователей на сайте в разделе регистрации или командой консоли:
```
$ python3 manage.py createsuperuser
```
- запустить сайт на локальном компьютетере
```
$ python3 manage.py runserver
```
- ссылка на сайт http://127.0.0.1:8000/

