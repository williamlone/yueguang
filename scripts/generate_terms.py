# -*- coding: utf-8 -*-
"""
generate_terms.py —— 生成 Hugo 用的分区词条映射 data/terms.json

做法：
    1. 从 mdb 目录下六个 Access 库读取 blog_Tag.tag_URL / blog_Category.cate_Url，
       得到「中文词条 -> 英文 slug」的映射（保留原始大小写）。
    2. 扫描 content 下六个分区的 md 文件，只保留实际用到的中文词条。
    3. 输出 data/terms.json，供模板和 content/_content.gotmpl 使用。

运行：
    python scripts/generate_terms.py

新增文章后重跑本脚本即可补上新的词条。
"""

import json
import os
import sys

import pyodbc
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content")
MDB_DIR = os.path.join(ROOT, "mdb")
OUT_FILE = os.path.join(ROOT, "data", "terms.json")

ODBC_DRIVER = "Microsoft Access Driver (*.mdb, *.accdb)"

# 分区 -> (数据库文件, 文章目录)
SECTIONS = {
    "main": ("myblog2007.mdb", os.path.join(CONTENT_DIR, "archives")),
    "weibo": ("blog2007.mdb", os.path.join(CONTENT_DIR, "weibo", "archives")),
    "google": ("google2007.mdb", os.path.join(CONTENT_DIR, "google", "archives")),
    "movie": ("movie2007.mdb", os.path.join(CONTENT_DIR, "movie", "archives")),
    "info": ("info2007.mdb", os.path.join(CONTENT_DIR, "info", "archives")),
    "apps": ("apps2007.mdb", os.path.join(CONTENT_DIR, "apps", "archives")),
}


def read_db_rows(db_path):
    """返回 (tag 行, 分类行)，每行是 (中文名, slug)，按数据库 ID 排序。"""
    conn = pyodbc.connect(
        "Driver={%s};DBQ=%s;" % (ODBC_DRIVER, os.path.abspath(db_path))
    )
    cur = conn.cursor()

    def rows(sql):
        result = []
        for row in cur.execute(sql):
            name = (row[0] or "").strip()
            slug = (row[1] or "").strip()
            if name and slug:
                result.append((name, slug))
        return result

    tags = rows("SELECT tag_Name, tag_URL FROM blog_Tag ORDER BY tag_ID")
    cats = rows("SELECT cate_Name, cate_Url FROM blog_Category ORDER BY cate_ID")
    conn.close()
    return tags, cats


def read_front_matter(path):
    """读取 md 的 YAML front matter，返回 dict；没有 front matter 时返回空 dict。"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        print("  ! front matter 解析失败：%s (%s)" % (path, exc))
        return {}


def collect_articles(article_dir):
    """扫描目录下所有 md，返回 [(tag 列表, 分类列表), ...]。"""
    articles = []
    if not os.path.isdir(article_dir):
        return articles
    for name in os.listdir(article_dir):
        if not name.endswith(".md"):
            continue
        fm = read_front_matter(os.path.join(article_dir, name))
        tags = [str(v).strip() for v in (fm.get("tags") or []) if v]
        cats = [str(v).strip() for v in (fm.get("categories") or []) if v]
        articles.append((tags, cats))
    return articles


def build_terms(used, db_rows, kind, articles, index, page_size=40):
    """
    把实际用到的中文词条整理成：
        name_map : 中文名 -> slug（给文章里的标签链接用）
        pages    : [{slug, title, names, page_count}]
                   （每个 slug 只产出一个词条，page_count 是它需要的分页数）

    数据库里可能有两个中文名共用一个 slug（如 澳洲 / 澳大利亚 -> Australia），
    这时词条页需要一个 names 列表，把两种写法的文章都收进来。
    """
    groups = {}
    canonical = {}
    titles = {}
    for name, slug in db_rows:
        canonical.setdefault(name, slug)
        titles.setdefault(slug, name)

    missing = []
    for name, slug in db_rows:
        if name in used:
            group = groups.setdefault(
                slug, {"slug": slug, "title": titles[slug], "names": []}
            )
            if name not in group["names"]:
                group["names"].append(name)
    for name in sorted(used):
        if name not in canonical:
            missing.append(name)
            groups[name] = {"slug": name, "title": name, "names": [name]}

    if missing:
        print("  ! %s 中有 %d 个词条在数据库里找不到 slug：%s" % (kind, len(missing), "、".join(missing)))

    for group in groups.values():
        names = set(group["names"])
        count = sum(1 for article in articles if names & set(article[index]))
        group["article_count"] = count
        group["page_count"] = max(1, (count + page_size - 1) // page_size)

    name_map = {}
    for group in groups.values():
        for name in group["names"]:
            name_map[name] = group["slug"]
    pages = sorted(groups.values(), key=lambda g: g["title"])
    return name_map, pages


def main():
    if not os.path.isdir(MDB_DIR):
        sys.exit("找不到 mdb 目录：%s" % MDB_DIR)

    output = {}
    for key, (db_file, article_dir) in SECTIONS.items():
        print("== %s" % key)
        tags_db, cats_db = read_db_rows(os.path.join(MDB_DIR, db_file))
        articles = collect_articles(article_dir)
        used_tags = set(t for tags, _ in articles for t in tags)
        used_cats = set(c for _, cats in articles for c in cats)
        tags, tag_pages = build_terms(used_tags, tags_db, "tag", articles, 0)
        cats, cat_pages = build_terms(used_cats, cats_db, "category", articles, 1)
        output[key] = {
            "article_count": len(articles),
            "list_page_count": max(1, (len(articles) + 39) // 40),
            "tags": tags,
            "tag_pages": tag_pages,
            "cats": cats,
            "cat_pages": cat_pages,
        }
        print("   tag %d 个（页面 %d 个），分类 %d 个" % (len(tags), len(tag_pages), len(cats)))

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("已写入 %s" % OUT_FILE)


if __name__ == "__main__":
    main()
