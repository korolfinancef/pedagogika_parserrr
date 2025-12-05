# Парсинг карточек статей (педагогика) с pedsovet.org

Учебный проект по парсингу HTML с помощью **BeautifulSoup**.

Цель — извлечь названия статей и ссылки на них из небольших прямоугольных
«карточек» на главной странице сайта [pedsovet.org](https://pedsovet.org/).

---

## Что делает программа

Скрипт `parse_pedagogy.py`:

1. Читает **сохранённый HTML-файл** главной страницы `https://pedsovet.org/`.
2. Находит «малые карточки» статей:
   - ориентируется на ссылки, которые ведут на путь вида `/article/...`;
   - корректно обрабатывает относительные ссылки.
3. Для каждой карточки извлекает:
   - **название статьи** (заголовок / подпись на карточке);
   - **ссылку на полную статью** (приводится к абсолютному виду).
4. Собирает результат в структуру Python — список словарей:
   ```python
   [
     {
       "title": "Название статьи",
       "url": "https://pedsovet.org/article/..."
     },
     ...
   ]
Установка и запуск
1. Создать и активировать виртуальное окружение (рекомендуется)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

2. Установить зависимости
pip install -r requirements.txt

3. Запуск парсера

Вывести результат в консоль:

python parse_pedagogy.py pedsovet_main.html


Сохранить результат в файл articles.json:

python parse_pedagogy.py pedsovet_main.html -o articles.json


После запуска вы увидите JSON со списком статей и строку с количеством найденных карточек:

[
  {
    "title": "15 минут, которые изменили школу: как организовать видеозарядку в каждом классе",
    "url": "https://pedsovet.org/article/15-minut-kotorye-izmenili-skolu-kak-organizovat-videozaradku-v-kazdom-klasse"
  },
  {
    "title": "5 идей для новогоднего утренника",
    "url": "https://pedsovet.org/article/5-idej-dla-novogodnego-utrennika"
  }
  ...
]

Найдено статей: 42
