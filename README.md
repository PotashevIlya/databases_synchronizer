# «databases_synchronizer»

## Описание проекта: 
databases_synchronizer - это скрипт, написанный на языке Python, который позволяет синхронизировать состояния двух баз данных MySQL (например, тестовую и продовую). Скрипт синхронизизирует как структуру, так и данные. 
ВАЖНО: Структура базы-образца должна либо повторять структуру обновлямой базы, либо быть шире за счёт новых таблиц или столбцов с данными, НО не наоборот. То есть скрипт заточен под обновление целевой базы с сохранением уже существующих в ней данных. 

## Как запустить скрипт у себя:
1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/PotashevIlya/databases_synchronizer
cd databases_synchronizer
```
2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```
3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
4. Создать .env файл и заполнить его по образцу .env.example
5. Запутить скрипт командой
```
python databases_synchronizer.py
```
### Технологический стек :bulb:
Python, SQLAlchemy, MySQL
___  
#### Автор проекта:  
:small_orange_diamond: [Поташев Илья](https://github.com/PotashevIlya) 
