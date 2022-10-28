# api_yatube
api_yatube

## Автор:
Дровнин Павел

### О чем проект:

Создание API для учебной социальной сети Yatube, с помощью которой можно будет смотеть, создавать, изменять и удалять посты и комментарии.

### Как развернуть:

```
git clone git@github.com:pashpiter/api_yatube.git
```

```
Открыть папку с проектом
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

