# Сервис для парсинга и хранения новостей
Сервис в фоном режиме пополянет базу данных новостей. Реализована возможность выгрузки данных по средствам API.

Для запуска:

```sh
python app.py
```

## Метод для получения списка новостей

`GET /posts` вернет список новостей.

##### Поля новостей

Название| Описание
------- | ---------------
id      | Идентификатор
title   | Заголовок новости
url     | Ссылка на новость
created | Дата создания записи

##### Аргументы запроса

Название| Описание
------- | ---------------
order   |  Поля для сортирвки (id, title, url, created)
desc    |  Флаг сортировки по убыванию (по умолчанию false)
limit   |  Максимальное количество новостей в запросе (не более 500)
offset  |  Необходимое количество новостей для пропуска


##### Результат запроса

```json
[
    {
        "id": 1,
        "title": "Announcing Rust 1.33.0",
        "url": "https://example.com",
        "created": "ISO 8601"
    },
    {
        "id": 2,
        "title": "Redesigning GitHub Repository Page",
        "url": "https://example.com",
        "created": "ISO 8601"
    }
]
```

### Пример запроса с аругментами

`GET /posts?order=title&desc=true` сортировка по заглоловку новостей.

##### Результат запроса с аругментами

```json
[
    {
        "id": 2,
        "title": "Redesigning GitHub Repository Page",
        "url": "https://example.com",
        "created": "ISO 8601"
    },
    {
        "id": 1,
        "title": "Announcing Rust 1.33.0",
        "url": "https://example.com",
        "created": "ISO 8601"
    }
]
```

### Метод выгрузки текущих новостей с интернет-страницы.

`GET /posts/update` пополняет базу данных ивозвращает найденные новости..

##### Результат запроса

```json
[
    {
        "title": "Announcing Rust 1.33.0",
        "url": "https://example.com",
        "created": "ISO 8601"
    },
    {
        "title": "Redesigning GitHub Repository Page",
        "url": "https://example.com",
        "created": "ISO 8601"
    }
]
```

### Формат получения ошибки запроса

* `error` - категория ошибки.
* `message` - описание ошибки (необязательное поле).

```json
{
    "error": 'Bad request',
    "message": 'Field "order" is incorrect'
}
```
