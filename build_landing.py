"""Сборка резервного лендинга Станэксперт на daisyUI 5 + Tailwind 4 (CDN).

Источники контента (MASTER_RULES): «База по станкам СТАНЭКСПЕРТ.md» ->
products.json (14 карточек, фото, цены, ГИСП, ключевые характеристики,
тип для фильтра). Палитра: primary 004D76, base-content 001F45,
accent FF2D2D. Заявки: Авито / телефон / Telegram / MAX, цели Метрики
110756129. Временный URL -> noindex.

Сборка: python3 build_landing.py && python3 publish.py
"""
import html
import json
from pathlib import Path

LAND = Path(__file__).parent
P = json.loads((LAND / "products.json").read_text(encoding="utf-8"))

AVITO = "https://www.avito.ru/brands/stanexpert"
TG = "https://web.telegram.org/a/#6133689782"
MAXL = "https://max.ru/u/f9LHodD0cOKKnEkQ-OuwQODb6MmyTcu8QxrKx0motQ51KIXyZGDBHsPsAXU"
PHONE_DISP = "8 (800) 100-72-49"
PHONE_TEL = "tel:+78001007249"
EMAIL = "info@stanexpert.com"
METRIKA = "110756129"

# Телеграм-бот для приёма заявок с формы (АВАРИЙНЫЙ РЕЖИМ).
# ВНИМАНИЕ: токен попадает в публичный JS-файл страницы. Бот выделенный
# (@leadreservestan_bot), продажные боты не затронуты. После восстановления
# stanexpert.com токен ОБЯЗАТЕЛЬНО отозвать: @BotFather -> /revoke.
TG_TOKEN = "9225468750:AAHwd4UYLr9Le7dOPigtpY4fk3faXo9dU5Y"
# chat_id группы + топик для заявок (задан владельцем: t.me/c/4300610435/244).
TG_CHAT_ID = "-1004300610435"
TG_THREAD_ID = "244"


def esc(s):
    return html.escape(str(s), quote=False)


def short_name(full):
    n = full.replace("СТАНЭКСПЕРТ®", "СТАНЭКСПЕРТ").strip()
    for pre in ("МОБИЛЬНЫЙ РАСТОЧНО-НАПЛАВОЧНЫЙ КОМПЛЕКС СТАНЭКСПЕРТ",
                "МОБИЛЬНЫЙ РАСТОЧНО-НАПЛАВОЧНЫЙ СТАНОК СТАНЭКСПЕРТ",
                "МОБИЛЬНЫЙ РАСТОЧНОЙ СТАНОК СТАНЭКСПЕРТ",
                "МОБИЛЬНЫЙ НАПЛАВОЧНЫЙ СТАНОК СТАНЭКСПЕРТ"):
        if n.upper().startswith(pre):
            n = n[len(pre):].strip(" ,")
            break
    return n[:1].upper() + n[1:]


def split_desc(desc):
    parts = [x.strip() for x in desc.split("\n\n") if x.strip()]
    return (parts[0] if parts else "", " ".join(parts[1:]))


hero_img = "img/hero_bg.jpg"

# ---------------- карточки каталога ----------------
TYPE_LABEL = {"rastochny": "Расточной", "naplavka": "Наплавочный",
              "complex": "Расточно-наплавочный"}

# Короткие описания (без выдуманных фактов: только диапазоны из specs).
SHORT_TEXT = [
    "МНС59 ЦПУ позволяет выполнять внутреннюю наплавку в диапазоне от 25 до 1000 мм и наружную наплавку поверхностей диаметром от 100 до 1000 мм, без демонтажа крупногабаритной детали.",
    "МРНК ПИОНЕР ЦПУ ПЛЮС выполняет расточку отверстий от 25 до 220 мм, внутреннюю наплавку от 25 до 400 мм и наружную наплавку поверхностей от 100 до 500 мм — без демонтажа детали.",
    "МРНК ПИОНЕР-2 ЦПУ БАЗА ПЛЮС выполняет расточку отверстий от 25 до 400 мм, внутреннюю наплавку от 25 до 400 мм и наружную наплавку поверхностей от 50 до 1000 мм — без демонтажа детали.",
    "МРНК ТАРМАН 400 ЦПУ БАЗА ПЛЮС выполняет расточку отверстий от 25 до 600 мм, внутреннюю наплавку от 25 до 600 мм и наружную наплавку поверхностей от 100 до 1000 мм — без демонтажа детали.",
    "МРНК-59 ЦПУ БАЗА выполняет расточку отверстий от 25 до 800 мм, внутреннюю наплавку от 45 до 500 мм и наружную наплавку поверхностей от 50 до 500 мм — без демонтажа детали.",
    "ТАРМАН 200 выполняет расточку отверстий от 25 до 220 мм, внутреннюю наплавку от 25 до 220 мм и наружную наплавку поверхностей от 100 до 500 мм — без демонтажа детали.",
    "ТАРМАН 600 с двухскоростным приводом и консольной подачей выполняет расточку отверстий от 25 до 600 мм, внутреннюю наплавку от 25 до 600 мм и наружную наплавку поверхностей от 100 до 500 мм — без демонтажа детали.",
    "МРНК 59 ЦПУ выполняет расточку отверстий от 25 до 800 мм, внутреннюю наплавку от 45 до 500 мм и наружную наплавку поверхностей от 50 до 500 мм — без демонтажа детали.",
    "МРНК ПИОНЕР-2 ЦПУ ПЛЮС выполняет расточку отверстий от 25 до 400 мм, внутреннюю наплавку от 25 до 400 мм и наружную наплавку поверхностей от 50 до 1000 мм — без демонтажа детали.",
    "МРНК ТАРМАН 400 ЦПУ ПЛЮС выполняет расточку отверстий от 25 до 600 мм, внутреннюю наплавку от 25 до 600 мм и наружную наплавку поверхностей от 100 до 1000 мм — без демонтажа детали.",
    "ПИОНЕР БАЗА ПЛЮС выполняет расточку изношенных цилиндрических и соосных отверстий от 25 до 220 мм — без демонтажа детали.",
    "ПИОНЕР с автоподачей выполняет расточку изношенных отверстий и соосных посадочных мест от 25 до 220 мм — без демонтажа детали.",
    "Станок ВАЛА 59993 применяется для райберовки соосных отверстий в сопрягаемых деталях — чтобы обеспечить точное взаимное положение элементов после сборки.",
    "ПИОНЕР-2 ЦПУ ПЛЮС выполняет расточку изношенных отверстий и соосных посадочных мест от 25 до 400 мм — без демонтажа детали.",
]


def spec_table(specs, specs_full):
    """Двухстолбцовая таблица: параметр | значение.
    Приоритет — полная таблица из «Базы по станкам» (specs_full)."""
    rows = []
    if specs_full:
        for param, val in specs_full:
            rows.append(f'<tr><td class="opacity-80">{esc(param)}</td>'
                        f'<td class="text-right font-semibold">{esc(val)}</td></tr>')
    else:  # фолбэк: разбор коротких строк specs
        import re
        for s in specs or []:
            m = re.match(r"^(.*?)(\d.*)$", s.strip())
            if m:
                param, val = m.group(1).strip(" ."), m.group(2).strip()
            else:
                param, val = s.strip(), ""
            rows.append(f'<tr><td class="opacity-80">{esc(param)}</td>'
                        f'<td class="text-right font-semibold whitespace-nowrap">{esc(val)}</td></tr>')
    return "".join(rows)


cards, ld_items = [], []
for i, p in enumerate(P):
    name = short_name(p["name"])
    short = SHORT_TEXT[i] if i < len(SHORT_TEXT) else split_desc(p["desc"])[0]
    typ = p.get("type", "complex")
    gisp = ('<span class="badge badge-accent text-white">ГИСП Минпромторга · '
            'полная комплектация</span>' if p["gisp"] else "")
    # квадратное окно фото, без рамок
    imgs = "".join(
        f'<div class="carousel-item w-full"><img src="{esc(src)}" '
        f'alt="{esc(name)}" class="w-full aspect-square object-cover" '
        f'loading="lazy"></div>' for src in p["photos"])
    price_num = "".join(ch for ch in p["price"] if ch.isdigit())
    cards.append(f"""
<article class="card bg-base-100 shadow-sm filter-item relative overflow-visible" data-type="{typ}">
  <div class="carousel w-full">{imgs}</div>
  <div class="card-body gap-2">
    <div class="flex flex-wrap gap-1">{gisp}
      <span class="badge badge-outline">{TYPE_LABEL[typ]}</span></div>
    <h3 class="card-title text-xl leading-snug">{esc(name)}</h3>
    <p class="text-base text-accent mt-1">{esc(p['price'])}</p>
    <p class="text-sm opacity-90">{esc(short)}</p>
    <button type="button" class="btn btn-outline btn-primary btn-sm w-full mt-1 spec-toggle"
            data-spec="spec-{i}">Технические характеристики</button>
    <button type="button" class="btn btn-accent text-white w-full offer-open js-goal"
            data-goal="offer_click" data-model="{esc(name)}">Получить предложение</button>
  </div>
  <div id="spec-{i}" class="spec-panel hidden absolute inset-x-2 top-2 bottom-2 z-20 rounded-box bg-base-100 shadow-2xl border border-base-300 flex flex-col">
    <div class="flex items-center justify-between gap-2 p-3 border-b border-base-300">
      <span class="font-bold text-sm leading-snug">Характеристики · {esc(name)}</span>
      <button type="button" class="btn btn-ghost btn-sm px-2 spec-close" aria-label="Закрыть">✕</button>
    </div>
    <div class="overflow-y-auto p-2 grow">
      <table class="table table-sm text-sm">
        <tbody>{spec_table(p.get("specs"), p.get("specs_full"))}</tbody>
      </table>
    </div>
  </div>
</article>""")
    ld_items.append({
        "@type": "Product", "name": f"СТАНЭКСПЕРТ {name}",
        "description": short, "image": p["photos"][0] if p["photos"] else "",
        "offers": {"@type": "Offer", "priceCurrency": "RUB",
                   "price": price_num or "0",
                   "availability": "https://schema.org/InStock"},
    })

catalog_html = "".join(cards)

# ---------------- сегменты ----------------
SEGMENTS = [
    ("Строительная и дорожная техника", "строительная.jpg",
     "Проушины ковша экскаватора, отверстия стрелы и рукояти под пальцы и втулки, шарниры каретки."),
    ("Сельскохозяйственная техника", "сельхоз.jpg",
     "Задняя навеска МТЗ, шарниры рам К-700/701, шкворневые узлы и оси качания мостов."),
    ("Горнодобывающая и карьерная техника", "горная.jpg",
     "Станины щёковых и конусных дробилок, посадки под бронзовые втулки, цапфы мельниц."),
    ("Грузоподъёмная и буровая техника", "грузоподьемная.jpg",
     "Корневые оси стрел автокранов, гильзы КМУ, цилиндры подъёма кузова, ОПУ платформ."),
    ("Нефтегаз", "нефтегаз.jpg",
     "Станки-качалки: опоры балансиров, головки шатунов, траверсы — знакопеременные нагрузки."),
    ("Ремонтные и судоремонтные предприятия", "судоремонт.jpg",
     "Корпуса редукторов, гнёзда под обоймы подшипников, наружная проточка фланцев и валов."),
]
segments_html = "".join(f"""
<div class="card bg-base-100 shadow-sm">
  <figure><img src="img/{esc(img)}" alt="{esc(t)}" class="w-full aspect-16/10 object-cover" loading="lazy"></figure>
  <div class="card-body">
    <h3 class="card-title text-base">{esc(t)}</h3>
    <p class="text-sm opacity-80">{esc(d)}</p>
  </div>
</div>""" for t, img, d in SEGMENTS)

# ---------------- FAQ (по топ-20 вопросов чата расточников от 03.11,
# только то, что касает СТАНЭКСПЕРТ как производителя станков) ----------------
FAQ = [
    ("Сколько стоит станок СТАНЭКСПЕРТ?",
     "Цены с НДС — от 137 820 ₽ за расточной станок ПИОНЕР БАЗА ПЛЮС до 1 680 420 ₽ за МРНК 59 ЦПУ. Актуальные цены всех 14 моделей — в карточках выше. Для юридических лиц доступен льготный лизинг: ставка от 4,6%, первоначальный взнос от 0%, срок до 36 месяцев."),
    ("Какой минимальный и максимальный диаметр обработки?",
     "Расточка отверстий — от Ø25 до 800 мм в зависимости от модели. Внутренняя наплавка — от 25 мм (у МНС59 ЦПУ — до Ø1000 мм), наружная наплавка поверхностей — до Ø1000 мм. Точность обработки — Н7. Точные диапазоны каждой модели — в таблице характеристик в карточке."),
    ("Станки производятся в России или собираются в Китае?",
     "СТАНЭКСПЕРТ — производитель: мобильные расточно-наплавочные комплексы производим сами. Мы не дилер и не посредник — за поставку и гарантию отвечает завод."),
    ("Чем ваши станки отличаются от Авантехно, Сирмеханики и китайских аналогов?",
     "Собственное производство, цены с НДС от 137 820 ₽, питание обычной сети 220 В, пульт управления, полные комплектации включены в каталог ГИСП Минпромторга. Поставляем по всей России, в Казахстан и Беларусь — с запуском под ключ."),
    ("Можно ли наплавлять чугун?",
     "Да, оборудование применяется для восстановления отверстий и посадочных мест в деталях из стали и чугуна — в том числе кареток, корпусов редукторов, проушин. Чугун требует особых режимов наплавки: стартовые параметры под марку материала подберем при обращении."),
    ("Какое электропитание нужно для работы станка?",
     "Все модели работают от обычной сети 220 В, 50 Гц — промышленная сеть 380 В не требуется. Это позволяет работать прямо на объекте: в поле, в карьере, в цеху."),
    ("Сколько весит станок и как его перевозить?",
     "Основной агрегат весит от 34 до 129 кг в зависимости от модели — станок перевозится в багажнике легкового автомобиля или на заднем сиденье. Габариты каждой модели — в таблице характеристик."),
    ("Есть ли модели с ЦПУ и автоподачей?",
     "Да. Модели с ЦПУ: МНС59 ЦПУ, МРНК ПИОНЕР ЦПУ ПЛЮС, ТАРМАН ЦПУ и другие. Модель ПИОНЕР С АВТОПОДАЧЕЙ БАЗА ПЛЮС — с механизированной подачей. Пульт управления входит в комплектацию моделей с ЦПУ."),
    ("Можно ли восстановить гильзу гидроцилиндра или посадку под подшипник без демонтажа?",
     "Да. Комплексы мобильные и работают непосредственно на месте ремонта: гильза гидроцилиндра, посадочное место под обойму подшипника, проушина ковша, соосные отверстия корпусов — демонтаж и вывоз детали не нужны."),
    ("Где купить станок и какие сроки поставки?",
     "Нажмите «Получить предложение» в карточке модели или напишите нам на Авито — подтвердим комплектацию, цену и сроки. Точная комплектация и сроки поставки определяются после согласования технического задания. Доставляем по России, в Казахстан и Беларусь."),
]
faq_html = "".join(f"""
<div class="collapse collapse-arrow bg-base-100 shadow-sm">
  <input type="radio" name="faq"{' checked="checked"' if i == 0 else ''}>
  <div class="collapse-title font-semibold">{esc(q)}</div>
  <div class="collapse-content text-sm opacity-80"><p>{esc(a)}</p></div>
</div>""" for i, (q, a) in enumerate(FAQ))

ld_faq = {"@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q,
     "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

page = f"""<!DOCTYPE html>
<html lang="ru" data-theme="stanexpert">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>СТАНЭКСПЕРТ® — мобильные расточно-наплавочные комплексы | Расточка и наплавка отверстий Ø25–1000 мм</title>
<meta name="description" content="Производитель мобильных расточно-наплавочных станков для восстановления изношенных отверстий спецтехники, сельхозмашин и промышленного оборудования без демонтажа. Лизинг от 4,6%, взнос от 0%, до 36 мес. Полные комплектации в каталоге ГИСП Минпромторга. Услуги расточки и наплавки оказывают партнёры по всей России.">
<link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css">
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<style>
[data-theme="stanexpert"] {{
  --color-base-100: #f7fafc; --color-base-200: #edf2f7; --color-base-300: #d9e2ec;
  --color-base-content: #001F45;
  --color-primary: #004D76; --color-primary-content: #ffffff;
  --color-secondary: #2e6e93; --color-secondary-content: #ffffff;
  --color-accent: #FF2D2D; --color-accent-content: #ffffff;
  --color-neutral: #001F45; --color-neutral-content: #ffffff;
  --color-info: #0369a1; --color-info-content: #ffffff;
  --color-success: #2e7d32; --color-success-content: #ffffff;
  --color-warning: #b45309; --color-warning-content: #ffffff;
  --color-error: #c81e1e; --color-error-content: #ffffff;
  --radius-selector: 0.5rem; --radius-field: 0.5rem; --radius-box: 0.75rem;
  --size-selector: 0.25rem; --size-field: 0.25rem; --border: 1px;
  --depth: 0; --noise: 0;
}}
/* Брендовые шрифты СТАНЭКСПЕРТ: заголовки — Magistral Extra Bold,
   основной текст — Futura. Это коммерческие шрифты: где не установлены,
   срабатывает каскад фолбэков. Строго без italic — никакого наклона. */
* {{ font-style: normal !important; }}
body {{ font-family: 'Futura', 'Futura PT', 'Trebuchet MS', 'Segoe UI', Arial, sans-serif; }}
h1, h2, h3, h4, .card-title, .btn, .navbar {{ font-family: 'Magistral Extra Bold', 'Magistral', 'Futura', 'Trebuchet MS', 'Segoe UI', Arial, sans-serif; font-weight: 800; }}
</style>
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org",
             "@graph": [{"@type": "ItemList", "name": "Модельный ряд СТАНЭКСПЕРТ",
                         "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "item": it}
    for i, it in enumerate(ld_items)]}, ld_faq]}, ensure_ascii=False, indent=1)}
</script>
</head>
<body class="bg-base-100 text-base-content">

<div class="navbar bg-primary text-primary-content sticky top-0 z-10">
  <div class="navbar-start">
    <a href="#top" aria-label="СТАНЭКСПЕРТ — наверх">
      <span class="bg-white rounded-md px-2.5 py-1.5 inline-flex items-center">
        <img src="img/logo.png" alt="СТАНЭКСПЕРТ®" class="h-6 w-auto">
      </span>
    </a>
  </div>
  <div class="navbar-center hidden lg:flex">
    <ul class="menu menu-horizontal text-sm">
      <li><a href="#segments">Кому подходит</a></li>
      <li><a href="#catalog">Модельный ряд</a></li>
      <li><a href="#leasing">Лизинг</a></li>
      <li><a href="#faq">Вопросы</a></li>
      <li><a href="#contacts">Контакты</a></li>
    </ul>
  </div>
  <div class="navbar-end gap-1">
    <a class="btn btn-ghost btn-sm btn-circle text-primary-content js-goal" data-goal="tg_click"
       href="{TG}" target="_blank" rel="noopener" aria-label="Telegram" title="Telegram">
      <svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5"><path d="M9.04 15.9l-.38 5.36c.55 0 .79-.24 1.08-.52l2.6-2.48 5.38 3.94c.99.55 1.69.26 1.96-.9L23.9 4.6c.32-1.45-.52-2.02-1.48-1.66L1.7 10.9c-1.4.55-1.38 1.34-.24 1.7l5.28 1.64L18.98 6.5c.58-.38 1.1-.17.67.21z"/></svg>
    </a>
    <a class="btn btn-ghost btn-sm btn-circle text-primary-content js-goal" data-goal="email_click"
       href="mailto:{EMAIL}" aria-label="Email" title="{EMAIL}">
      <svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/></svg>
    </a>
    <a class="btn btn-ghost btn-sm btn-circle text-primary-content js-goal" data-goal="max_click"
       href="{MAXL}" target="_blank" rel="noopener" aria-label="MAX" title="MAX">
      <img src="img/max-white.png" alt="MAX" class="w-5 h-5">
    </a>
    <a class="btn btn-accent btn-sm text-white js-goal" data-goal="call_click"
       href="{PHONE_TEL}">☎ <span class="hidden sm:inline">{PHONE_DISP}</span></a>
  </div>
</div>

<div class="hero min-h-[70vh] bg-cover" style="background-image:url('{esc(hero_img)}'); background-position: 62% center;">
  <div class="hero-overlay bg-neutral/50"></div>
  <div class="hero-content text-neutral-content text-center px-4 py-16">
    <div class="max-w-3xl">
      <h1 class="text-3xl md:text-5xl font-extrabold leading-tight">Мобильные расточные и наплавочные станки</h1>
      <p class="py-6 text-base md:text-lg">Российский завод-изготовитель мобильных станков для расточки, торцовки, наплавки, проточки, нарезания резьбы. Диапазон обработки Ø25–1000 мм. Бесплатная демонстрация онлайн или на производстве</p>
      <div class="flex flex-wrap justify-center gap-2 pb-6">
        <span class="badge badge-lg bg-white/10 text-white h-auto py-1.5 whitespace-normal leading-snug">Лизинг от 4,6% · взнос от 0% · до 36 мес</span>
        <span class="badge badge-lg bg-white/10 text-white h-auto py-1.5 whitespace-normal leading-snug">Более 10 лет производим станки и оснастку</span>
        <span class="badge badge-lg bg-white/10 text-white h-auto py-1.5 whitespace-normal leading-snug">Поставка от 3 дней</span>
        <span class="badge badge-lg bg-white/10 text-white h-auto py-1.5 whitespace-normal leading-snug">Доставка по всей России и ЕАЭС</span>
      </div>
      <div class="flex flex-wrap justify-center gap-3">
        <a class="btn btn-primary btn-lg js-goal" data-goal="hero_offer_click"
           href="#lead-form" id="hero-offer-btn">Получить предложение</a>
        <a class="btn btn-accent btn-lg text-white js-goal" data-goal="call_click"
           href="{PHONE_TEL}">Позвонить: {PHONE_DISP}</a>
      </div>
    </div>
  </div>
</div>

<section id="segments" class="max-w-7xl mx-auto px-4 py-14">
  <h2 class="text-2xl md:text-3xl font-bold mb-2">Какую технику ремонтируют нашими станками</h2>
  <p class="opacity-70 mb-6">Самые частые узлы износа отверстий по данным исследования спроса в сегментах РФ, Казахстана и Беларуси.</p>
  <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">{segments_html}
  </div>
</section>

<section id="catalog" class="max-w-7xl mx-auto px-4 py-6">
  <h2 class="text-2xl md:text-3xl font-bold mb-2">Модельный ряд</h2>
  <p class="opacity-70 mb-4">14 моделей собственного производства. Цены с НДС. Характеристики каждой модели — под кнопкой «Технические характеристики» в карточке.</p>
  <div class="flex flex-wrap gap-2 mb-6" role="group" aria-label="Фильтр по типу станка">
    <button class="btn btn-sm btn-primary filter-btn" data-filter="all">Все</button>
    <button class="btn btn-sm filter-btn" data-filter="complex">Расточно-наплавочные</button>
    <button class="btn btn-sm filter-btn" data-filter="rastochny">Расточные</button>
    <button class="btn btn-sm filter-btn" data-filter="naplavka">Наплавочные</button>
  </div>
  <div id="catalog-grid" class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">{catalog_html}
  </div>
</section>

<section id="leasing" class="bg-base-200 py-14 my-10">
  <div class="max-w-7xl mx-auto px-4">
    <h2 class="text-2xl md:text-3xl font-bold mb-6">Льготный лизинг для предприятий</h2>
    <div class="stats stats-vertical lg:stats-horizontal shadow w-full mb-8">
      <div class="stat"><div class="stat-title">Ставка</div><div class="stat-value text-accent">от 4,6%</div><div class="stat-desc">фиксированная, годовых</div></div>
      <div class="stat"><div class="stat-title">Первоначальный взнос</div><div class="stat-value text-accent">от 0%</div><div class="stat-desc">без отвлечения оборотных средств</div></div>
      <div class="stat"><div class="stat-title">Срок финансирования</div><div class="stat-value text-accent">до 36 мес</div><div class="stat-desc">график под сезонность бизнеса</div></div>
    </div>
    <ul class="steps steps-vertical lg:steps-horizontal w-full">
      <li class="step step-accent">Выбираете модель</li>
      <li class="step step-accent">Получаете расчёт платежа</li>
      <li class="step step-accent">Оформляем лизинг</li>
      <li class="step step-accent">Получаете оборудование</li>
    </ul>
    <div class="mt-8">
      <button type="button" class="btn btn-primary js-goal offer-open" data-goal="leasing_offer_click"
         data-model="Лизинг — расчёт платежа">Получить расчёт платежа</button>
    </div>
  </div>
</section>

<section id="certs" class="bg-base-200 py-14 my-10">
  <div class="max-w-7xl mx-auto px-4">
    <h2 class="text-2xl md:text-3xl font-bold mb-2">Сертификация качества станков Станэксперт</h2>
    <p class="opacity-70 mb-6">Официальные документы на оборудование. Нажмите на превью, чтобы открыть, или скачайте PDF.</p>
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <div class="card bg-base-100 shadow-sm">
        <a href="docs/sert-tarman-pioner.pdf" target="_blank" rel="noopener" aria-label="Открыть сертификат">
          <figure><img src="img/sert-tarman-pioner.jpg" alt="Добровольная сертификация оборудования ТАРМАН и ПИОНЕР" class="w-full aspect-3/4 object-cover object-top" loading="lazy"></figure>
        </a>
        <div class="card-body gap-2">
          <h3 class="card-title text-sm leading-snug">Добровольная сертификация оборудования ТАРМАН и ПИОНЕР</h3>
          <a href="docs/sert-tarman-pioner.pdf" download class="btn btn-outline btn-primary btn-sm">Скачать PDF</a>
        </div>
      </div>
      <div class="card bg-base-100 shadow-sm">
        <a href="docs/sert-prombezopasnost.pdf" target="_blank" rel="noopener" aria-label="Открыть сертификат">
          <figure><img src="img/sert-prombezopasnost.jpg" alt="Соответствие требованиям промышленной безопасности" class="w-full aspect-3/4 object-cover object-top" loading="lazy"></figure>
        </a>
        <div class="card-body gap-2">
          <h3 class="card-title text-sm leading-snug">Соответствие требованиям промышленной безопасности</h3>
          <a href="docs/sert-prombezopasnost.pdf" download class="btn btn-outline btn-primary btn-sm">Скачать PDF</a>
        </div>
      </div>
      <div class="card bg-base-100 shadow-sm">
        <a href="docs/sert-eaes.pdf" target="_blank" rel="noopener" aria-label="Открыть сертификат">
          <figure><img src="img/sert-eaes.jpg" alt="Соответствие требованиям безопасности ЕАЭС" class="w-full aspect-3/4 object-cover object-top" loading="lazy"></figure>
        </a>
        <div class="card-body gap-2">
          <h3 class="card-title text-sm leading-snug">Соответствие требованиям безопасности ЕАЭС</h3>
          <a href="docs/sert-eaes.pdf" download class="btn btn-outline btn-primary btn-sm">Скачать PDF</a>
        </div>
      </div>
      <div class="card bg-base-100 shadow-sm">
        <a href="docs/sert-iso9001.pdf" target="_blank" rel="noopener" aria-label="Открыть сертификат">
          <figure><img src="img/sert-iso9001.jpg" alt="Система менеджмента качества ISO 9001" class="w-full aspect-3/4 object-cover object-top" loading="lazy"></figure>
        </a>
        <div class="card-body gap-2">
          <h3 class="card-title text-sm leading-snug">Система менеджмента качества ISO 9001</h3>
          <a href="docs/sert-iso9001.pdf" download class="btn btn-outline btn-primary btn-sm">Скачать PDF</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="lead-form" class="bg-base-200 py-14 my-10">
  <div class="max-w-xl mx-auto px-4">
    <h2 class="text-2xl md:text-3xl font-bold mb-2 text-center">Оставить заявку</h2>
    <p class="text-center opacity-80 mb-6">Перезвоним и подберём комплектацию под вашу задачу.</p>
    <form id="tg-form" class="card bg-base-100 shadow-md">
      <div class="card-body gap-4">
        <label class="form-control w-full">
          <span class="label-text mb-1 font-medium">Ваше имя *</span>
          <input name="name" type="text" required maxlength="80" placeholder="Иван" class="input input-bordered w-full">
        </label>
        <label class="form-control w-full">
          <span class="label-text mb-1 font-medium">Телефон *</span>
          <input name="phone" type="tel" required maxlength="30" placeholder="+7 (___) ___-__-__" class="input input-bordered w-full">
        </label>
        <label class="form-control w-full">
          <span class="label-text mb-1 font-medium">Комментарий</span>
          <textarea name="msg" rows="3" maxlength="600" placeholder="Какой узел восстанавливаете, регион, интересующая модель" class="textarea textarea-bordered w-full"></textarea>
        </label>
        <!-- анти-спам: скрытое поле, люди его не заполняют -->
        <input name="company" type="text" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
        <label class="flex items-start gap-2 text-xs opacity-80 cursor-pointer">
          <input name="agree" type="checkbox" required class="checkbox checkbox-sm checkbox-primary mt-0.5">
          <span>Согласен(на) на обработку персональных данных</span>
        </label>
        <button type="submit" id="tg-form-btn" class="btn btn-accent text-white w-full">Отправить заявку</button>
        <p id="tg-form-status" class="text-center text-sm min-h-5"></p>
      </div>
    </form>
  </div>
</section>

<section id="faq" class="max-w-4xl mx-auto px-4 py-10">
  <h2 class="text-2xl md:text-3xl font-bold mb-6">Частые вопросы</h2>
  <div class="flex flex-col gap-3">{faq_html}
  </div>
</section>

<dialog id="offer-modal" class="modal">
  <div class="modal-box">
    <h3 class="text-xl font-bold">Получить предложение</h3>
    <p class="py-2 text-sm opacity-80">Запрос: <span id="offer-model" class="font-semibold"></span></p>
    <form id="offer-form" class="flex flex-col gap-3 mt-1">
      <input type="hidden" name="model" id="offer-model-input">
      <label class="form-control w-full">
        <span class="label-text mb-1 font-medium">Телефон *</span>
        <input name="phone" type="tel" required maxlength="30" placeholder="+7 (___) ___-__-__" class="input input-bordered w-full">
      </label>
      <label class="form-control w-full">
        <span class="label-text mb-1 font-medium">Email *</span>
        <input name="email" type="email" required maxlength="120" placeholder="name@company.ru" class="input input-bordered w-full">
      </label>
      <label class="flex items-start gap-2 text-xs opacity-80 cursor-pointer">
        <input name="agree" type="checkbox" required class="checkbox checkbox-sm checkbox-primary mt-0.5">
        <span>Согласен(на) на обработку персональных данных</span>
      </label>
      <button type="submit" id="offer-btn" class="btn btn-accent text-white w-full">Отправить</button>
      <p id="offer-status" class="text-center text-sm min-h-5"></p>
    </form>
  </div>
  <form method="dialog" class="modal-backdrop"><button aria-label="Закрыть">закрыть</button></form>
</dialog>

<footer id="contacts" class="footer footer-center bg-neutral text-neutral-content p-10 gap-4">
  <div>
    <span class="bg-white rounded-md px-3 py-2 inline-flex items-center">
      <img src="img/logo.png" alt="СТАНЭКСПЕРТ®" class="h-7 w-auto">
    </span>
    <p class="opacity-80 mt-3">Производитель мобильных расточно-наплавочных комплексов</p>
  </div>
  <div class="flex flex-wrap justify-center gap-2">
    <a class="btn btn-accent text-white js-goal" data-goal="call_click"
       href="{PHONE_TEL}">☎ {PHONE_DISP}</a>
    <a class="btn btn-ghost btn-circle text-neutral-content js-goal" data-goal="email_click"
       href="mailto:{EMAIL}" aria-label="Email" title="{EMAIL}">
      <svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/></svg>
    </a>
    <a class="btn btn-ghost btn-circle text-neutral-content js-goal" data-goal="tg_click"
       href="{TG}" target="_blank" rel="noopener" aria-label="Telegram" title="Telegram">
      <svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5"><path d="M9.04 15.9l-.38 5.36c.55 0 .79-.24 1.08-.52l2.6-2.48 5.38 3.94c.99.55 1.69.26 1.96-.9L23.9 4.6c.32-1.45-.52-2.02-1.48-1.66L1.7 10.9c-1.4.55-1.38 1.34-.24 1.7l5.28 1.64L18.98 6.5c.58-.38 1.1-.17.67.21z"/></svg>
    </a>
    <a class="btn btn-ghost btn-circle text-neutral-content js-goal" data-goal="max_click"
       href="{MAXL}" target="_blank" rel="noopener" aria-label="MAX" title="MAX">
      <img src="img/max-white.png" alt="MAX" class="w-5 h-5">
    </a>
  </div>
  <p class="text-xs opacity-60 max-w-xl">Резервная страница: основной сайт stanexpert.com временно недоступен по техническим причинам. Цены и комплектации актуальны на дату публикации. Услуги расточки и наплавки оказывают партнёрские сервисы на оборудовании СТАНЭКСПЕРТ.</p>
</footer>

<script>
/* фильтр каталога */
document.querySelectorAll('.filter-btn').forEach(function (b) {{
  b.addEventListener('click', function () {{
    document.querySelectorAll('.filter-btn').forEach(function (x) {{
      x.classList.remove('btn-primary'); }});
    b.classList.add('btn-primary');
    var f = b.dataset.filter;
    document.querySelectorAll('.filter-item').forEach(function (c) {{
      c.style.display = (f === 'all' || c.dataset.type === f) ? '' : 'none'; }});
  }});
}});
</script>
<script>
/* форма заявки -> телеграм-бот (токен виден в коде страницы, см. TG_TOKEN) */
(function () {{
  var form = document.getElementById('tg-form');
  if (!form) return;
  var btn = document.getElementById('tg-form-btn');
  var status = document.getElementById('tg-form-status');
  form.addEventListener('submit', function (e) {{
    e.preventDefault();
    if (form.company.value) return; /* honeypot */
    var name = form.name.value.trim(), phone = form.phone.value.trim(), msg = form.msg.value.trim();
    if (!name || !phone) {{ status.textContent = 'Заполните имя и телефон.'; status.className = 'text-center text-sm min-h-5 text-error'; return; }}
    var text = '🔔 ЗАЯВКА С РЕЗЕРВНОГО ЛЕНДИНГА\\n\\n👤 Имя: ' + name + '\\n📞 Телефон: ' + phone +
               (msg ? '\\n💬 Комментарий: ' + msg : '') +
               '\\n\\n🌐 Страница: ' + location.href;
    btn.disabled = true; btn.textContent = 'Отправляем…';
    fetch('https://api.telegram.org/bot{TG_TOKEN}/sendMessage', {{
      method: 'POST', headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{chat_id: '{TG_CHAT_ID}', message_thread_id: '{TG_THREAD_ID}', text: text, parse_mode: 'HTML'}})
    }}).then(function (r) {{ return r.json(); }}).then(function (d) {{
      if (d.ok) {{
        status.textContent = 'Заявка отправлена! Перезвоним в ближайшее время.';
        status.className = 'text-center text-sm min-h-5 text-success';
        form.reset();
        if (window.ym) ym({METRIKA}, 'reachGoal', 'lead_form_sent');
      }} else {{
        status.textContent = 'Не отправилось. Позвоните нам: {PHONE_DISP}';
        status.className = 'text-center text-sm min-h-5 text-error';
      }}
    }}).catch(function () {{
      status.textContent = 'Нет связи. Позвоните нам: {PHONE_DISP}';
      status.className = 'text-center text-sm min-h-5 text-error';
    }}).finally(function () {{
      btn.disabled = false; btn.textContent = 'Отправить заявку';
    }});
  }});
}})();
</script>

<script>
/* «Технические характеристики»: оверлей поверх карточки, не влияет на сетку */
document.querySelectorAll('.spec-toggle').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var el = document.getElementById(b.dataset.spec);
    if (el) el.classList.toggle('hidden');
  }});
}});
document.querySelectorAll('.spec-close').forEach(function (b) {{
  b.addEventListener('click', function () {{
    b.closest('.spec-panel').classList.add('hidden');
  }});
}});
/* кнопка «Получить предложение» в hero -> скролл к форме + фокус в поле имени */
document.querySelectorAll('#hero-offer-btn').forEach(function (btn) {{
  btn.addEventListener('click', function () {{
    setTimeout(function () {{
      var f = document.querySelector('#tg-form [name=name]');
      if (f) f.focus();
    }}, 600);
  }});
}});

/* «Получить предложение»: модалка с телефоном и email -> тот же бот, топик 244 */
(function () {{
  var modal = document.getElementById('offer-modal');
  var form = document.getElementById('offer-form');
  var btn = document.getElementById('offer-btn');
  var status = document.getElementById('offer-status');
  document.querySelectorAll('.offer-open').forEach(function (b) {{
    b.addEventListener('click', function () {{
      document.getElementById('offer-model').textContent = b.dataset.model;
      document.getElementById('offer-model-input').value = b.dataset.model;
      status.textContent = '';
      modal.showModal();
    }});
  }});
  form.addEventListener('submit', function (e) {{
    e.preventDefault();
    var model = form.model.value.trim(), phone = form.phone.value.trim(), email = form.email.value.trim();
    if (!phone || !email) {{ status.textContent = 'Заполните телефон и email.'; status.className = 'text-center text-sm min-h-5 text-error'; return; }}
    var text = '🔔 ЗАПРОС ПРЕДЛОЖЕНИЯ\\n\\n📌 Запрос: ' + model + '\\n📞 Телефон: ' + phone +
               '\\n✉️ Email: ' + email + '\\n\\n🌐 Страница: ' + location.href;
    btn.disabled = true; btn.textContent = 'Отправляем…';
    fetch('https://api.telegram.org/bot{TG_TOKEN}/sendMessage', {{
      method: 'POST', headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{chat_id: '{TG_CHAT_ID}', message_thread_id: '{TG_THREAD_ID}', text: text, parse_mode: 'HTML'}})
    }}).then(function (r) {{ return r.json(); }}).then(function (d) {{
      if (d.ok) {{
        status.textContent = 'Отправлено! Пришлём предложение на указанный email.';
        status.className = 'text-center text-sm min-h-5 text-success';
        form.reset();
        if (window.ym) ym({METRIKA}, 'reachGoal', 'offer_sent');
        setTimeout(function () {{ modal.close(); }}, 1500);
      }} else {{
        status.textContent = 'Не отправилось. Позвоните нам: {PHONE_DISP}';
        status.className = 'text-center text-sm min-h-5 text-error';
      }}
    }}).catch(function () {{
      status.textContent = 'Нет связи. Позвоните нам: {PHONE_DISP}';
      status.className = 'text-center text-sm min-h-5 text-error';
    }}).finally(function () {{
      btn.disabled = false; btn.textContent = 'Отправить';
    }});
  }});
}})();
</script>

<!-- Yandex.Metrika counter -->
<script>
(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];
k.async=1;k.src=r;a.parentNode.insertBefore(k,a)}})
(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
ym({METRIKA},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:false}});
document.querySelectorAll('.js-goal').forEach(function(el){{el.addEventListener('click',function(){{
  if(window.ym) ym({METRIKA},'reachGoal',el.dataset.goal);}});}});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/{METRIKA}" style="position:absolute;left:-9999px" alt=""></div></noscript>
</body>
</html>
"""

(LAND / "index.html").write_text(page, encoding="utf-8")
print("index.html:", len(page), "символов,", len(P), "карточек, hero:", hero_img)
