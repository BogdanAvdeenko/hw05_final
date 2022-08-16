# Django-проект Yatube — это платформа для публикаций, блог.

В проекте реализована система подписки на авторов и создание ленты их постов.
Написана система комментирования записей.

Для оформления веб-страниц был использован программный язык HTML.
HTML-код вынесен в отдельные файлы - HTML-шаблоны.
Django ORM применен  для работы с данными реляционной БД посредством классов.
Проект использует драйвер баз данных SQLite.

Использованы контекст-процессоры - анонимные посетители видят сайт иным, чем авторизованные пользователи.
Авторизованным пользователям доступны ссылки на выход и смены пароля, а анонимным — ссылки на регистрацию и авторизацию.

Добавление картинок к постам реализованно с помощью Pillow.
С помощью sorl-thumbnail выведены иллюстрации к постам.

Настроено кеширование главной страницы - список постов на главной странице сайта хранится в кэше и обновляется раз в 20 секунд.

Написаны Unittest в Django для тестирование моделей, URLs, Views, Forms.

Проверено:
- Что во view-функциях используются правильные html-шаблоны.
- Что словарь context, передаваемый в шаблон при вызове,  соответствует ожиданиям.
- Что если при создании поста указать группу, то этот пост появляется:
    - на главной странице сайта,
    - на странице выбранной группы,
    - в профайле пользователя.
    - пост не попал в группу, для которой не был предназначен.
- Что при выводе поста с картинкой изображение передаётся в словаре context:
    - на главную страницу,
    - на страницу профайла,
    - на страницу группы,
    - на отдельную страницу поста.
- Так же:
    - Что при отправке поста с картинкой через форму PostForm создаётся запись в базе данных.
    - Авторизованный пользователь может подписываться на других пользователей и удалять их из подписок.
    - Новая запись пользователя появляется в ленте тех, кто на него подписан и не появляется в ленте тех, кто не подписан.
    - При отправке валидной формы со страницы создания поста reverse('posts:create_post') создаётся новая запись в базе данных.
    - При отправке валидной формы со страницы редактирования поста reverse('posts:post_edit', args=('post_id',)) происходит изменение поста с post_id в базе данных.

Переопределены шаблона страницы входа и другие шаблоны управления доступом.

## Как запустить проект:

- [x] 1) Клонировать репозиторий и перейти в него в командной строке.
- [x] 2) Cоздать и активировать виртуальное окружение:

```
py -m venv venv
```

```
source venv/Scripts/activate
```

```
py -m pip install --upgrade pip
```

- [x] 3) Установить все необходимые пакеты из requirements.txt:

```
pip install -r requirements.txt
```

- [x] 4) Выполнить миграции:

```
python manage.py migrate
```

- [x] 5) Запустить проект:

```
python manage.py runserver
```

## Автор:
Богдан Авдеенко. Студент факультета Бэкенд. Когорта №33. Яндекс Практикум.
