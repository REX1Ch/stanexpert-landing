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


hero_img = next((ph for p in P for ph in p["photos"]
                 if "пионерцпуплюс" in ph), P[0]["photos"][0])

# ---------------- карточки каталога ----------------
TYPE_LABEL = {"rastochny": "Расточной", "naplavka": "Наплавочный",
              "complex": "Расточно-наплавочный"}
cards, ld_items = [], []
for i, p in enumerate(P):
    name = short_name(p["name"])
    lead, rest = split_desc(p["desc"])
    specs = " · ".join(p.get("specs") or [])
    typ = p.get("type", "complex")
    gisp = ('<span class="badge badge-accent text-white">ГИСП Минпромторга · '
            'полная комплектация</span>' if p["gisp"] else "")
    imgs = "".join(
        f'<div class="carousel-item w-full"><img src="{esc(src)}" '
        f'alt="{esc(name)}" class="w-full aspect-4/3 object-cover" '
        f'loading="lazy"></div>' for src in p["photos"])
    price_num = "".join(ch for ch in p["price"] if ch.isdigit())
    cards.append(f"""
<article class="card bg-base-100 shadow-sm filter-item" data-type="{typ}">
  <div class="carousel w-full">{imgs}</div>
  <div class="card-body gap-2">
    <div class="flex flex-wrap gap-1">{gisp}
      <span class="badge badge-outline">{TYPE_LABEL[typ]}</span></div>
    <h3 class="card-title text-base leading-snug">{esc(name)}</h3>
    <p class="text-xl font-extrabold text-accent">{esc(p['price'])}</p>
    <p class="text-sm opacity-80">{esc(specs)}</p>
    <p class="text-sm">{esc(lead)}</p>
    <div class="collapse collapse-arrow bg-base-200 rounded-box">
      <input type="checkbox" aria-label="Подробнее">
      <div class="collapse-title text-sm font-semibold">Подробнее</div>
      <div class="collapse-content text-sm opacity-90"><p>{esc(rest)}</p></div>
    </div>
    <div class="card-actions">
      <a class="btn btn-primary btn-sm js-goal" data-goal="avito_click"
         href="{AVITO}?utm_source=landing&utm_medium=card&utm_campaign=reserve_landing"
         target="_blank" rel="noopener">Уточнить на Авито</a>
    </div>
  </div>
</article>""")
    ld_items.append({
        "@type": "Product", "name": f"СТАНЭКСПЕРТ {name}",
        "description": lead, "image": p["photos"][0] if p["photos"] else "",
        "offers": {"@type": "Offer", "priceCurrency": "RUB",
                   "price": price_num or "0",
                   "availability": "https://schema.org/InStock"},
    })

catalog_html = "".join(cards)

# ---------------- сегменты ----------------
SEGMENTS = [
    ("Строительная и дорожная техника",
     "Проушины ковша экскаватора, отверстия стрелы и рукояти под пальцы и втулки, шарниры каретки."),
    ("Сельскохозяйственная техника",
     "Задняя навеска МТЗ, шарниры рам К-700/701, шкворневые узлы и оси качания мостов."),
    ("Горнодобывающая и карьерная техника",
     "Станины щёковых и конусных дробилок, посадки под бронзовые втулки, цапфы мельниц."),
    ("Грузоподъёмная и буровая техника",
     "Корневые оси стрел автокранов, гильзы КМУ, цилиндры подъёма кузова, ОПУ платформ."),
    ("Нефтегаз",
     "Станки-качалки: опоры балансиров, головки шатунов, траверсы — знакопеременные нагрузки."),
    ("Ремонтные и судоремонтные предприятия",
     "Корпуса редукторов, гнёзда под обоймы подшипников, наружная проточка фланцев и валов."),
]
segments_html = "".join(f"""
<div class="card bg-base-100 shadow-sm">
  <div class="card-body">
    <h3 class="card-title text-base">{esc(t)}</h3>
    <p class="text-sm opacity-80">{esc(d)}</p>
  </div>
</div>""" for t, d in SEGMENTS)

# ---------------- FAQ ----------------
FAQ = [
    ("Какой диаметр отверстий можно восстановить?",
     "В зависимости от модели — расточка и внутренняя наплавка Ø25–800 мм, наружная наплавка поверхностей до Ø1000 мм. Точность обработки H7. Полные диапазоны — в карточках станков выше и в характеристиках на Авито."),
    ("Можно ли расточить проушину ковша без демонтажа узла?",
     "Да. Комплексы мобильные и работают непосредственно на месте ремонта: проушина ковша, стрела, шкворень моста, корпус редуктора — демонтаж и вывоз детали не нужны. Это основной сценарий использования оборудования."),
    ("Что значит «комплектация ГИСП» и в чём отличие от базовой?",
     "Полные комплектации включены в каталог ГИСП Минпромторга: станок поставляется в составе, готовом к работе, поэтому цена выше. Базовые версии — для тех, кто комплектуется сам. Что входит в каждую позицию, менеджер подтвердит по конкретной модели."),
    ("Как купить станок в лизинг и что для этого нужно?",
     "Льготный лизинг для юридических лиц: ставка от 4,6%, первоначальный взнос от 0%, срок до 36 месяцев. Напишите нам на Авито или позвоните — подготовим расчёт платежа под вашу модель и поможем с оформлением."),
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
</style>
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org",
             "@graph": [{"@type": "ItemList", "name": "Каталог станков СТАНЭКСПЕРТ",
                         "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "item": it}
    for i, it in enumerate(ld_items)]}, ld_faq]}, ensure_ascii=False, indent=1)}
</script>
</head>
<body class="bg-base-100 text-base-content">

<div class="navbar bg-primary text-primary-content sticky top-0 z-10">
  <div class="navbar-start">
    <span class="text-xl font-extrabold tracking-wide px-2">СТАНЭКСПЕРТ<span class="align-super text-xs">®</span></span>
  </div>
  <div class="navbar-center hidden lg:flex">
    <ul class="menu menu-horizontal text-sm">
      <li><a href="#segments">Кому подходит</a></li>
      <li><a href="#catalog">Каталог</a></li>
      <li><a href="#leasing">Лизинг</a></li>
      <li><a href="#faq">Вопросы</a></li>
      <li><a href="#contacts">Контакты</a></li>
    </ul>
  </div>
  <div class="navbar-end">
    <a class="btn btn-accent btn-sm text-white js-goal" data-goal="call_click"
       href="{PHONE_TEL}">☎ {PHONE_DISP}</a>
  </div>
</div>

<div class="hero min-h-[70vh]" style="background-image:url('{esc(hero_img)}')">
  <div class="hero-overlay bg-neutral/70"></div>
  <div class="hero-content text-neutral-content text-center px-4 py-16">
    <div class="max-w-3xl">
      <h1 class="text-3xl md:text-5xl font-extrabold leading-tight">Мобильные расточно-наплавочные комплексы для восстановления изношенных отверстий</h1>
      <p class="py-6 text-base md:text-lg">Ремонт проушин, ковшей, стрел, редукторов и узлов спецтехники, сельхозмашин и промышленного оборудования — непосредственно на месте ремонта, без демонтажа детали. Диапазон обработки Ø25–1000 мм.</p>
      <div class="flex flex-wrap justify-center gap-2 pb-6">
        <span class="badge badge-lg bg-white/10 text-white h-auto py-1.5 whitespace-normal leading-snug">Лизинг от 4,6% · взнос от 0% · до 36 мес</span>
        <span class="badge badge-lg bg-white/10 text-white h-auto py-1.5 whitespace-normal leading-snug">Полные комплектации — в каталоге ГИСП Минпромторга</span>
        <span class="badge badge-lg bg-white/10 text-white h-auto py-1.5 whitespace-normal leading-snug">Россия · Казахстан · Беларусь</span>
      </div>
      <div class="flex flex-wrap justify-center gap-3">
        <a class="btn btn-primary btn-lg js-goal" data-goal="avito_click"
           href="{AVITO}?utm_source=landing&utm_medium=hero&utm_campaign=reserve_landing"
           target="_blank" rel="noopener">Написать на Авито</a>
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
  <h2 class="text-2xl md:text-3xl font-bold mb-2">Каталог</h2>
  <p class="opacity-70 mb-4">14 моделей собственного производства. Цены с НДС. Все характеристики и комплектации — в объявлениях на Авито.</p>
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
      <a class="btn btn-primary js-goal" data-goal="avito_click"
         href="{AVITO}?utm_source=landing&utm_medium=leasing&utm_campaign=reserve_landing"
         target="_blank" rel="noopener">Получить расчёт платежа на Авито</a>
    </div>
  </div>
</section>

<section class="max-w-7xl mx-auto px-4 py-10">
  <h2 class="text-2xl md:text-3xl font-bold mb-6">Производитель, а не перекуп</h2>
  <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
    <div class="card bg-base-100 shadow-sm"><div class="card-body"><h3 class="card-title text-base">Собственное производство</h3><p class="text-sm opacity-80">Мобильные комплексы производим сами — не дилер и не посредник.</p></div></div>
    <div class="card bg-base-100 shadow-sm"><div class="card-body"><h3 class="card-title text-base">Каталог ГИСП</h3><p class="text-sm opacity-80">Полные комплектации включены в каталог ГИСП Минпромторга.</p></div></div>
    <div class="card bg-base-100 shadow-sm"><div class="card-body"><h3 class="card-title text-base">Сервис партнёров</h3><p class="text-sm opacity-80">Услуги расточки и наплавки на нашем оборудовании оказывают партнёры по всей России.</p></div></div>
    <div class="card bg-base-100 shadow-sm"><div class="card-body"><h3 class="card-title text-base">География поставок</h3><p class="text-sm opacity-80">Россия, Казахстан, Беларусь: доставка и запуск под ключ.</p></div></div>
  </div>
</section>

<section id="faq" class="max-w-4xl mx-auto px-4 py-10">
  <h2 class="text-2xl md:text-3xl font-bold mb-6">Частые вопросы</h2>
  <div class="flex flex-col gap-3">{faq_html}
  </div>
</section>

<footer id="contacts" class="footer footer-center bg-neutral text-neutral-content p-10 gap-4">
  <div>
    <p class="text-2xl font-extrabold">СТАНЭКСПЕРТ®</p>
    <p class="opacity-80">Производитель мобильных расточно-наплавочных комплексов</p>
  </div>
  <div class="flex flex-wrap justify-center gap-3">
    <a class="btn btn-primary js-goal" data-goal="avito_click"
       href="{AVITO}?utm_source=landing&utm_medium=footer&utm_campaign=reserve_landing"
       target="_blank" rel="noopener">Авито</a>
    <a class="btn btn-accent text-white js-goal" data-goal="call_click" href="{PHONE_TEL}">{PHONE_DISP}</a>
    <a class="btn btn-outline btn-neutral-content js-goal" data-goal="tg_click" href="{TG}" target="_blank" rel="noopener">Telegram</a>
    <a class="btn btn-outline btn-neutral-content js-goal" data-goal="max_click" href="{MAXL}" target="_blank" rel="noopener">MAX</a>
    <a class="btn btn-outline btn-neutral-content js-goal" data-goal="email_click" href="mailto:{EMAIL}">{EMAIL}</a>
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
