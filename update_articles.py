import os
import re
import html

homepage = "index.html"

excluded = {
    "index.html",
    "tentang.html",
    "privasi.html",
    "syarat.html",
    "kontak.html",
}

articles = []

for filename in os.listdir("."):
    if not filename.endswith(".html"):
        continue

    if filename in excluded:
        continue

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        continue

    # Hanya mengambil halaman yang memiliki struktur artikel
    if '<article class="article">' not in content:
        continue

    title_match = re.search(
        r"<title>(.*?)</title>",
        content,
        re.I | re.S
    )

    description_match = re.search(
        r'<meta\s+name="description"\s+content="(.*?)"',
        content,
        re.I | re.S
    )

    category_match = re.search(
        r'<span\s+class="category">(.*?)</span>',
        content,
        re.I | re.S
    )

    title = (
        title_match.group(1).strip()
        if title_match
        else filename.replace(".html", "")
    )

    description = (
        description_match.group(1).strip()
        if description_match
        else "Panduan praktis dari PanduanUsaha."
    )

    category = (
        category_match.group(1).strip()
        if category_match
        else "Artikel"
    )

    title = re.sub(
        r"\s*\|\s*PanduanUsaha\s*$",
        "",
        title
    )

    articles.append({
        "file": filename,
        "title": title,
        "description": description,
        "category": category
    })


articles.sort(key=lambda x: x["file"])


cards = []

for article in articles:
    filename = html.escape(
        article["file"],
        quote=True
    )

    title = html.escape(article["title"])
    description = html.escape(article["description"])
    category = html.escape(article["category"])

    cards.append(f"""
      <article class="article-card">
        <span class="article-category">{category}</span>
        <h3>{title}</h3>
        <p>{description}</p>
        <a href="{filename}">Baca selengkapnya →</a>
      </article>""")


generated = "\n".join(cards)


with open(homepage, "r", encoding="utf-8") as f:
    index = f.read()


marker = '<div id="article-list" class="articles">'

if marker not in index:
    raise Exception(
        "Bagian article-list tidak ditemukan di index.html"
    )


start = index.index(marker) + len(marker)

# Cari penutup div article-list.
end = index.find("</div>", start)

if end == -1:
    raise Exception(
        "Penutup article-list tidak ditemukan"
    )


new_index = (
    index[:start]
    + "\n"
    + generated
    + "\n\n    "
    + index[end:]
)


with open(homepage, "w", encoding="utf-8") as f:
    f.write(new_index)


print(
    f"Berhasil menemukan {len(articles)} artikel."
      )
