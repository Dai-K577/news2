# 📰 NEWSLINE — 無料ニュースまとめサイト

GitHub Pages + GitHub Actions + RSS で動く完全無料のニュースアグリゲーター。

## 🗂 ファイル構成

```
.
├── index.html                  # フロントエンド（GitHub Pagesで公開）
├── fetch_news.py               # RSS取得スクリプト
├── news.json                   # 自動生成されるデータ（コミット不要）
└── .github/workflows/
    └── update.yml              # 3時間ごとに自動実行
```

## 🚀 セットアップ手順

### 1. リポジトリ作成 & push

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_NAME/YOUR_REPO.git
git push -u origin main
```

### 2. GitHub Pages を有効化

`Settings → Pages → Source: Deploy from branch → main / (root)`

### 3. 初回 news.json を生成

```bash
python fetch_news.py
git add news.json
git commit -m "add news.json"
git push
```

または GitHub の Actions タブから手動で `Run workflow` を実行。

### 4. 完了！

`https://YOUR_NAME.github.io/YOUR_REPO/` でアクセス可能。  
以降は **3時間ごとに自動更新** されます。

## 📡 ニュースソースの追加・変更

`fetch_news.py` の `RSS_FEEDS` リストを編集するだけ：

```python
RSS_FEEDS = [
    {"name": "表示名", "url": "RSSのURL", "category": "カテゴリ名"},
    ...
]
```

### 主なRSSフィード例

| メディア | URL |
|----------|-----|
| NHK 総合 | `https://www.nhk.or.jp/rss/news/cat0.xml` |
| NHK 国際 | `https://www.nhk.or.jp/rss/news/cat6.xml` |
| 朝日新聞 | `https://www.asahi.com/rss/asahi/newsheadlines.rdf` |
| Reuters JP | `https://jp.reuters.com/rssFeed/topNews` |
| ITmedia | `https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml` |
| Gigazine  | `https://gigazine.net/news/rss_2.0/` |

## ⚙️ 更新頻度の変更

`.github/workflows/update.yml` の `cron` を変更：

```yaml
- cron: "0 */6 * * *"   # 6時間ごと
- cron: "0 8,12,18 * * *"  # 8時・12時・18時
```

## 💰 コスト

| 項目 | コスト |
|------|--------|
| GitHub Pages | 無料 |
| GitHub Actions | 無料（月2,000分） |
| RSS フィード | 無料 |
| **合計** | **¥0** |
