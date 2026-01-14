---
name: web-search
description: Efficiently search the web and scrape pages using local SearXNG + Crawl4AI services, with natural language responses and optional compression
---

# Web Search & Scrape (Local Services)

Search the web and scrape page content using locally-running services via a proxy on port 8001.

## Prerequisites

Docker services must be running from `~/Documents/repos/sketch-claude-search-skill`:

```bash
cd ~/Documents/repos/sketch-claude-search-skill && docker compose up -d
```

Services:
- Proxy: http://localhost:8001 (use this)
- SearXNG: http://localhost:8080 (direct)
- Crawl4AI: http://localhost:8000 (direct)

## Search the Web

```bash
curl -s "http://localhost:8001/search?q=QUERY&format=json" | jq '.results[:10] | .[] | {title, url, content}'
```

Replace `QUERY` with URL-encoded search terms. Use `+` for spaces.

Add `&compress=true&instruction=YOUR+INSTRUCTION` to have a cheap LLM process the results. The instruction is natural language, e.g.:
- `brief summary of key facts`
- `detailed analysis preserving all information`
- `just the URLs and titles`
- `extract only pricing information`

### Search Examples

```bash
# Basic search
curl -s "http://localhost:8001/search?q=rust+async+tutorial&format=json" | jq '.results[:10]'

# Compressed search with natural language instruction
curl -s "http://localhost:8001/search?q=rust+async+tutorial&format=json&compress=true&instruction=summarize+the+top+results+with+links"

# Detailed compression
curl -s "http://localhost:8001/search?q=weather+london&format=json&compress=true&instruction=extract+temperature+and+conditions+for+today+and+tomorrow"

# Page 2 of results
curl -s "http://localhost:8001/search?q=query&format=json&pageno=2" | jq '.results'

# Search specific category (images, news, videos, science, files, it)
curl -s "http://localhost:8001/search?q=query&format=json&categories=science" | jq '.results'

# Time filter (day, week, month, year)
curl -s "http://localhost:8001/search?q=query&format=json&time_range=week" | jq '.results'
```

## Scrape a URL

```bash
curl -s -X POST "http://localhost:8001/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' | jq '.markdown'
```

Add `"compress": true, "instruction": "your instruction"` to the JSON body to have a cheap LLM process the page content.

### Scrape Examples

```bash
# Full response with metadata
curl -s -X POST "http://localhost:8001/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' | jq '{markdown, metadata, links}'

# Compressed scrape with brief summary
curl -s -X POST "http://localhost:8001/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "compress": true, "instruction": "brief summary"}'

# Compressed scrape with detailed extraction
curl -s -X POST "http://localhost:8001/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.example.com", "compress": true, "instruction": "extract all API endpoints and their parameters"}'

# Target specific CSS selector
curl -s -X POST "http://localhost:8001/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "css_selector": "article"}' | jq '.markdown'

# Longer timeout for slow sites
curl -s -X POST "http://localhost:8001/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "timeout": 60}' | jq '.markdown'
```

## Health Check

```bash
curl -s "http://localhost:8001/health" | jq
```

## Troubleshooting

```bash
# Check container status
docker ps | grep -E "searxng|crawl4ai|redis|proxy"

# Restart services
cd ~/Documents/repos/sketch-claude-search-skill && docker compose restart

# View logs
docker logs search-proxy
docker logs searxng
docker logs crawl4ai-service
```

## When to Use This

- Searching for current information beyond your knowledge cutoff
- Getting full content from a URL (not just snippets)
- Researching topics that need multiple sources
- Scraping JavaScript-heavy sites that WebFetch can't handle
- Use compression with specific instructions to control how much detail you get back
