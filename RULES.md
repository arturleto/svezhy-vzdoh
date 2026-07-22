# RULES.md — Свежий Вздох (GitHub Pages)

> Последнее обновление: 2026-07-22 (сессия 3)

## СТРУКТУРА ПРОЕКТА
- `index.html` = копия `offer.html` — корневой URL открывает полную страницу напрямую (без отдельной видео-страницы)
- `offer.html` — оригинал; при изменениях редактировать offer.html и `cp offer.html index.html`
- `img-*.png` — иллюстрации, генерируются через nano-banana (Gemini 2.5 Flash Image)

### Архитектура первого блока
- `video-block` + `hero-intro` обёрнуты в `.top-hero-wrap` с единым градиентом; сами блоки — `background:transparent`
- Если разделить на два блока с разными градиентами — будет видимая линия стыка (грабля!)
- `.hi-pillar` карточки: `background:rgba(255,255,255,.06)` — НУЖЕН тёмный фон-родитель, иначе белый текст невидим на белом

## КРИТИЧНЫЕ ПРАВИЛА

### Git / деплой
- **Перед пушем PNG-файлов** всегда делать: `git config http.postBuffer 52428800` — иначе HTTP 400
- Деплой = `git push origin main` → GitHub Pages обновляется автоматически (~1-2 мин)
- Кэш Telegram не сбрасывается сам — добавлять `?v=N` к URL для принудительного обновления превью

### Изображения
- Все PNG генерируются через `mcp__nano-banana__generate_image` (Gemini 2.5 Flash Image)
- Gemini всегда выдаёт квадрат 1024×1024; для 2:1 кадра — кроп через PIL
- Ресайз на macOS: `sips -Z <px> input.png --out output.png`
- **Для PNG-стикеров (без рамки):** генерировать на белом фоне → убирать фон flood-fill от углов (thresh=40), НЕ threshold по всему изображению — иначе съедает белые части арта
- **Для «бесшовного» наложения на тёмный фон:** генерировать с фоном точно #0D3826 — картинка сливается с фоном страницы

### Кириллица в Gemini
- Русский текст генерируется, но модель часто переносит слова на новую строку даже при явном запрете
- Лайфхак: перечислять буквы через дефис «С-В-Е-Ж-И-Й В-З-Д-О-Х» и просить «wide horizontal banner», «like a marquee sign»

## ССЫЛКИ
- Сайт: https://arturleto.github.io/svezhy-vzdoh/
- Тест-версия: https://arturleto.github.io/svezhy-vzdoh/test1/
- Оффер: https://arturleto.github.io/svezhy-vzdoh/offer.html
- Instagram: @leto.s.v

### Tribute — ссылки оплаты по тирам (TG-бот, НЕ web)
- 950 ₽/мес (первые 2ч): https://t.me/tribute/app?startapp=s11nt
- 990 ₽/мес (до 24ч):    https://t.me/tribute/app?startapp=sVVm
- 1 450 ₽/мес (до 7д):   https://t.me/tribute/app?startapp=s11nv
- 4 900 ₽/мес (базовая): https://t.me/tribute/app?startapp=s11nx

### PNG — очистка внутренних белых
- После flood-fill внешнего фона оставшиеся белые opaque-пиксели = внутренность букв
- Убирать через numpy: `data[(a>30) & (r>200) & (g>200) & (b>200), 3] = 0`
- Апскейл логотипа: `img.resize((w*3, h*3), Image.LANCZOS)` — гладкие края без AI

## АРХИТЕКТУРА ТАЙМЕРА (test1/index.html)
- Таймер работает на `localStorage` — при первом визите пишет timestamp, каждую секунду считает elapsed
- TIERS массив: `{ until, price, note, link }` — у каждого тира своя Tribute-ссылка
- Кнопка покупки: `id="buy-btn"` — href обновляется в `tick()` через `bb.href = tier.link`
- Все остальные кнопки на сайте → якорь `#price`, только одна кнопка ведёт на Tribute
- Таймер vs редирект: localStorage-подход лучше для GitHub Pages (без сервера); редирект не даёт защиты сильнее
- `.compare-col-title` — стиль заголовков колонок сравнения (строка ~282): font-size и opacity

## ГРАБЛИ
- `<title>` влияет на Telegram-превью, не только `<h1>` — при переименовании менять оба
- `img-hero-backup.png` — бэкап заглавной картинки (не коммитить если не нужен)
- Два блока с разными градиентами = резкая линия стыка → всегда оборачивать в общий контейнер с одним фоном
- Нельзя читать chatgpt.com/share через WebFetch (SPA) — использовать curl с Mozilla user-agent + Python regex (см. memory reference_chatgpt_links)
