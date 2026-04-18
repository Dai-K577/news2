import json
import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime, timezone

RSS_FEEDS = [
    {"name": "朝日新聞",           "url": "https://www.asahi.com/rss/asahi/newsheadlines.rdf", "category": "総合"},
    {"name": "Reuters Japan",      "url": "https://jp.reuters.com/rssFeed/topNews",      "category": "国際"},
]

def fetch_rss(feed):
    try:
        req = urllib.request.Request(feed["url"], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            xml_data = res.read()
        root = ET.fromstring(xml_data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        items = []

        # RSS 2.0
        for item in root.findall(".//item")[:10]:
            title = item.findtext("title", "").strip()
            link  = item.findtext("link", "").strip()
            desc  = item.findtext("description", "").strip()
            pub   = item.findtext("pubDate", "").strip()
            if title and link:
                items.append({"title": title, "link": link, "description": desc[:200], "pubDate": pub, "source": feed["name"], "category": feed["category"]})

        # Atom
        if not items:
            for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry")[:10]:
                title = entry.findtext("{http://www.w3.org/2005/Atom}title", "").strip()
                link_el = entry.find("{http://www.w3.org/2005/Atom}link")
                link  = link_el.get("href", "") if link_el is not None else ""
                desc  = entry.findtext("{http://www.w3.org/2005/Atom}summary", "").strip()
                pub   = entry.findtext("{http://www.w3.org/2005/Atom}updated", "").strip()
                if title and link:
                    items.append({"title": title, "link": link, "description": desc[:200], "pubDate": pub, "source": feed["name"], "category": feed["category"]})

        return items
    except Exception as e:
        print(f"[ERROR] {feed['name']}: {e}")
        return []

def main():
    all_news = []
    for feed in RSS_FEEDS:
        print(f"Fetching: {feed['name']}")
        items = fetch_rss(feed)
        all_news.extend(items)
        print(f"  -> {len(items)} items")

    output = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "total": len(all_news),
        "news": all_news
    }

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ news.json updated: {len(all_news)} articles")

if __name__ == "__main__":
    main()
