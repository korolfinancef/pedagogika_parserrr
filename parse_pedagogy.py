
!pip install -q beautifulsoup4 lxml


from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import json

# Для загрузки файла через диалог (если pedsovet_main.html ещё нет в файловой системе)
try:
    from google.colab import files
except ImportError:
    files = None  


BASE_URL = "https://pedsovet.org"


def looks_like_article_href(href: str) -> bool:
    # Фильтруем только ссылки на статьи с карточек
    if not href:
        return False

    href = href.strip()

    # якоря / почта / телефоны / js
    if href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return False

    # внешние сайты не нужны
    if href.startswith("http") and "pedsovet.org" not in href:
        return False

    # страница статьи всегда содержит /article/
    return "/article/" in href


SERVICE_TITLES = {
    "к другим статьям",
    "к другим новостям",
    "больше статей по теме",
}


def parse_articles_from_html(html: str):
    # Возвращает список словарей {title, url} для всех карточек на главной
    soup = BeautifulSoup(html, "lxml")

    articles = []
    seen_urls = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not looks_like_article_href(href):
            continue

        title = a.get_text(" ", strip=True)
        if not title:
            continue

        if title.lower() in SERVICE_TITLES:
            # сервисные ссылки «к другим статьям» и т.п.
            continue

        url = urljoin(BASE_URL, href)

        if url in seen_urls:
            # если одна и та же статья встречается несколько раз — пропускаем дубликат
            continue
        seen_urls.add(url)

        articles.append({"title": title, "url": url})

    # отсортируем по заголовку типа для красоты)0
    articles.sort(key=lambda x: x["title"].lower())
    return articles


html_path = Path("pedsovet_main.html")

if html_path.is_file():
    print("[INFO] Используем файл pedsovet_main.html из файловой системы Colab")
    html = html_path.read_text(encoding="utf-8", errors="ignore")
else:
    if files is None:
        raise SystemExit(
            "Файл pedsovet_main.html не найден\n"
        )
    print("[INFO] Файл pedsovet_main.html не найден. Выбери сохранённый HTML главной страницы.")
    uploaded = files.upload()  # откроется диалог выбора файла
    if not uploaded:
        raise SystemExit("Файл не был выбран.")
    # берём первый загруженный файл
    name, content = next(iter(uploaded.items()))
    print(f"[INFO] Используем загруженный файл: {name}")
    html = content.decode("utf-8", errors="ignore")

# === ПАРСИНГ И ВЫВОД ===

articles = parse_articles_from_html(html)

# вывод в консоль
print(json.dumps(articles, ensure_ascii=False, indent=2))
print("\nНайдено статей:", len(articles))

# --- сохранение в JSON-файл ---
out_path = Path("articles.json")
out_path.write_text(
    json.dumps(articles, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"\n[INFO] Результат сохранён в файле {out_path}")


