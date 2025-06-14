# What would PG do? 🤔

A comprehensive collection of Paul Graham's essays scraped and organized for easy AI-assisted analysis and inspiration.

## Who is Paul Graham?

For those who've been living under a rock, **Paul Graham** is a legendary figure in the startup and tech world. He's an English-American computer scientist, writer, essayist, entrepreneur, and investor who co-founded [Y Combinator](https://www.ycombinator.com/), the most successful startup accelerator in history.

**Key accomplishments:**
- Co-founded **Y Combinator** (funded companies like Airbnb, Dropbox, Stripe, Reddit, and thousands more)
- Created **Viaweb** (sold to Yahoo for $49M, became Yahoo Store)
- Built **Hacker News**, the premier tech community platform
- Author of influential programming books including *"On Lisp"* and *"Hackers & Painters"*
- PhD in Computer Science from Harvard

**Connect with PG:**
- 🐦 Twitter: [@paulg](https://twitter.com/paulg)
- 📝 Famous Blog: [paulgraham.com](https://paulgraham.com)

His essays are considered essential reading for entrepreneurs, programmers, and anyone interested in startups, technology, and thoughtful commentary on society.

## What's in this repo?

This repository contains:

- **200+ Paul Graham essays** scraped from his website and converted to markdown
- **Automated scraping script** using the `fabric` utility
- **Clean, organized structure** for easy browsing and analysis
- **Complete essay collection** from his decades of writing

## How to Use

### The AI-Powered Way (Recommended)

Sure, you *could* set up RAG (Retrieval-Augmented Generation) for this dataset, but honestly? **That's overkill.**

Here's what I recommend instead:

1. **Open your favorite AI-powered IDE** (mine is [Zed](https://zed.dev/) 🚀)
2. **Select Google Gemini 2.0 Flash or 2.5 Pro** which has a massive **1M token context window**
3. **Load all the markdown files** directly into your prompt
4. **Ask anything** - Who needs RAG when you have 1 million tokens?

#### Why This Approach Works

- **[Google Gemini 2.0 Flash](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-0-flash)** can handle 1M+ tokens in a single context window
- **1M tokens ≈ 50,000 lines of code or 8 novels worth of text**
- **[Zed Editor](https://zed.dev/)** provides seamless AI integration with multiple providers
- **No indexing delays, no vector databases, no complexity** - just pure context

### Example Prompts to Try

```
"Based on PG's essays, what would he say about [your startup idea]?"

"Find all of PG's advice about hiring and summarize the key principles"

"What are PG's thoughts on [current tech trend] based on his writing patterns?"

"Create a PG-style essay about [your topic] using his voice and insights"
```

## Repository Structure

```
PG/
├── README.md                 # This file
├── scrape_pg.sh             # Bash script for scraping essays
├── pg_data.json            # URLs and titles of all essays
├── scrape_log.txt          # Scraping activity log
└── posts/                  # All essays in markdown format
    ├── Founder Mode.md
    ├── How to Do Great Work.md
    ├── How to Get Startup Ideas.md
    └── ... (200+ more essays)
```

## Technical Details

### Scraping Script Features

- **Robust error handling** with colored output
- **Rate limiting** to be respectful of PG's servers
- **File sanitization** for clean, readable filenames
- **Progress tracking** with detailed logging
- **Resume capability** for interrupted scrapes

### Prerequisites

If you want to run the scraper yourself:

```bash
# Install required tools
brew install jq                    # JSON parsing
# Install fabric utility (path configured in script)
```

### Running the Scraper

```bash
./scrape_pg.sh
```

The script will:
1. Read URLs from `pg_data.json`
2. Download each essay using the `fabric` utility
3. Convert to clean markdown format
4. Save in the `posts/` directory
5. Log all activity to `scrape_log.txt`

## Why This Matters

Paul Graham's essays represent decades of wisdom about:

- **Startups & Entrepreneurship** - From idea to IPO
- **Programming & Technology** - Insights from a master craftsman
- **Writing & Communication** - Clear thinking made manifest
- **Life & Philosophy** - Thoughtful takes on society and human nature

Having this knowledge instantly accessible in your AI workflow means you can:
- **Get PG's perspective** on any business decision
- **Learn from patterns** across his extensive writing
- **Generate PG-style insights** for your own work
- **Reference specific essays** without endless googling

## Contributing

Found an essay that's missing? Want to improve the scraper? PRs welcome!

## License

This repository contains scraped content from [paulgraham.com](https://paulgraham.com). All essays remain the intellectual property of Paul Graham. This collection is intended for personal learning and analysis purposes.

---

*"The way to get startup ideas is not to try to think of startup ideas. It's to look for problems, preferably problems you have yourself."* - Paul Graham

**Now go build something people want! 🚀**
