# Claude Search Skill

Local web search and scraping infrastructure for Claude Code, using SearXNG + Crawl4AI.

## Quick Start

```bash
# Start services
docker compose up -d

# Verify
curl "http://localhost:8080/search?q=test&format=json"  # SearXNG
curl http://localhost:8000/health                        # Crawl4AI
```

## Services

| Service | Port | Purpose |
|---------|------|---------|
| SearXNG | 8080 | Meta-search (70+ engines) |
| Crawl4AI | 8000 | Web scraping with Playwright |
| Redis | 6379 | Caching |

## Usage with Claude

Use the `/web-search` skill or ask Claude to search/scrape using the local services.

## Stop

```bash
docker compose down
```

## Attribution

Based on [Bionic-AI-Solutions/open-search](https://github.com/Bionic-AI-Solutions/open-search).
