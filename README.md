# What would PG do? 🤔

A comprehensive collection of Paul Graham's essays scraped and organized for easy AI-assisted analysis and inspiration.

## Who is Paul Graham?

**Paul Graham** is a legendary figure in the startup and technology world. He's an English-American computer scientist, writer, essayist, entrepreneur, and investor who co-founded [Y Combinator](https://www.ycombinator.com/), the most successful startup accelerator in history.

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
- **Automated scraping and processing scripts** for maintaining the collection
- **Two AI system prompts** for different interaction styles with the knowledge base
- **Clean, organized structure** for easy browsing and analysis
- **Complete essay collection** spanning decades of influential writing

## How to Use

### The AI-Powered Way (Recommended)

**Current Recommended Method: Raycast Chat Presets**

The most effective way to interact with this knowledge base is through **Raycast Chat Presets** using:
- **Model**: Google Gemini 2.5 Flash (excellent for quick queries and reasoning)
- **Thinking Setting**: Maximum (enables deeper analytical reasoning)
- **System Prompt**: Load from `SYS_PROMPT/system_prompt.md` or `SYS_PROMPT/system_prompt_G.md`
- **Knowledge Base**: Import relevant essays or the complete knowledge base as context

**Alternative: Direct AI IDE Integration**

While you *could* set up RAG (Retrieval-Augmented Generation) for this dataset, **direct context loading is more effective** with modern large context windows.

If you prefer IDE integration:

1. **Open your favorite AI-powered IDE** (mine is [Zed](https://zed.dev/) 🚀)
2. **Select Google Gemini 2.0 Flash or 2.5 Pro** which has a massive **1M token context window**
3. **Load all the markdown files** directly into your prompt
4. **Ask anything** - Who needs RAG when you have 1 million tokens?

#### Why This Approach Works

- **Large Context Windows**: Google Gemini models can handle 1M+ tokens in a single context window
- **Massive Capacity**: 1M tokens ≈ 50,000 lines of code or 8 novels worth of text
- **AI-Native IDEs**: Tools like [Zed](https://zed.dev/) provide seamless AI integration with multiple providers
- **Simplicity**: No indexing delays, no vector databases, no complexity - just pure contextual understanding
- **Real-time Analysis**: Direct access to the complete knowledge base for instant insights

### Example Prompts to Try

**Startup & Business Advice:**
```
"Based on PG's essays, what would he say about [your startup idea]?"
"What does PG recommend for early-stage startups struggling with product-market fit?"
"Analyze my business model using Paul Graham's principles"
```

**Research & Analysis:**
```
"Find all of PG's advice about hiring and summarize the key principles"
"What are the common patterns in PG's thoughts on successful founders?"
"Compare PG's views on venture capital from different time periods"
```

**Writing & Communication:**
```
"Help me write a PG-style essay about [your topic]"
"What would PG say about [current tech trend] based on his writing patterns?"
"Critique my startup pitch using Paul Graham's communication principles"
```

## Repository Structure

```
PG/
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── scrape_pg.sh                   # Bash script for scraping essays
├── pg_data.json                   # Essay URLs and metadata
├── scrape_log.txt                 # Scraping activity log
├── SYS_PROMPT/                    # AI system prompts and knowledge base
│   ├── system_prompt.md           # Analytical advisor persona
│   ├── system_prompt_G.md         # Paul Graham persona
│   ├── pg_knowledge_base.md       # Complete knowledge base
│   └── KNOWLEDGE_INDEX.md         # Structured essay index
├── posts/                         # Original essays (raw format)
│   ├── Founder Mode.md
│   ├── How to Do Great Work.md
│   ├── How to Get Startup Ideas.md
│   └── ... (200+ more essays)
├── posts_clean/                   # Cleaned and formatted essays
│   └── ... (processed essays)
├── concatenator.py                # Combine essays into knowledge base
├── indexmaker.py                  # Generate structured essay index
├── pg_parser.py                   # Essay parsing and cleanup (v1)
└── pg_parser_V2.py                # Essay parsing and cleanup (v2)

Generated files (git ignored):
├── .env                           # Your API keys (DO NOT COMMIT)
└── pg_env/                        # Python virtual environment
```

## System Prompts & AI Personas

This repository includes two carefully crafted system prompts in the `SYS_PROMPT/` directory:

### `system_prompt.md` - The Analytical Advisor
This prompt creates a **straightforward startup and technology advisor** persona that:
- Provides direct, analytical insights grounded in PG's essays
- Requires verbatim quotes and specific essay references
- Focuses on practical, actionable advice
- Maintains intellectual rigor with systematic knowledge retrieval

### `system_prompt_G.md` - The Paul Graham Persona  
This prompt creates a more **immersive Paul Graham persona** that:
- Embodies PG's distinctive voice, thinking patterns, and communication style
- Uses first-person perspective ("I" statements) as if PG himself is responding
- Incorporates his characteristic rhetorical patterns and analogical reasoning
- References personal experiences (Viaweb, Y Combinator) when relevant

**Key Difference in User Experience:** 
- **Analytical Advisor** (`system_prompt.md`): Provides **insights about** Paul Graham's ideas with academic rigor and specific citations
- **Paul Graham Persona** (`system_prompt_G.md`): Delivers insights **from** Paul Graham's perspective with his distinctive voice and thinking patterns

Choose based on whether you want analytical distance or immersive persona interaction.

## Running the Scripts

### Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv pg_env
source pg_env/bin/activate  # On Windows: pg_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# Or install manually:
# pip install python-dotenv requests

# Set up your API key
cp .env.example .env
# Edit .env and add your Google API key
```

### Index Generation

```bash
# Generate knowledge index from essays
python indexmaker.py
```

### Essay Parsing and Cleanup

```bash
# Parse and clean essay formats
python pg_parser.py
# or
python pg_parser_V2.py
```

### Content Concatenation

```bash
# Combine essays into single knowledge base
python concatenator.py
```

## Technical Details

### Scraping Script Features

- **Robust error handling** with colored output
- **Rate limiting** to be respectful of PG's servers
- **File sanitization** for clean, readable filenames
- **Progress tracking** with detailed logging
- **Resume capability** for interrupted scrapes

### Prerequisites

**For scraping essays (optional):**
```bash
# Install required tools
brew install jq                    # JSON parsing utility
# Install fabric utility (path configured in script)
```

**For processing and analysis:**
```bash
# Python 3.7+ required
python3 --version

# Google Gemini API key (for indexing)
# Get yours at: https://console.cloud.google.com/apis/credentials
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

Paul Graham's essays represent **decades of battle-tested wisdom** across multiple domains:

### Core Areas of Expertise
- **🚀 Startups & Entrepreneurship**: From initial idea validation to IPO strategies
- **💻 Programming & Technology**: Insights from a master craftsman and language designer
- **✍️ Writing & Communication**: Clear thinking made manifest through precise language
- **🧠 Philosophy & Life**: Thoughtful commentary on society, human nature, and decision-making

### Practical Benefits
Having this knowledge instantly accessible in your AI workflow enables you to:
- **Get PG's perspective** on critical business decisions and strategic challenges
- **Identify patterns** across decades of writing to inform your own thinking
- **Generate insights** using proven mental models and frameworks
- **Access specific examples** and case studies without manual research
- **Develop intuition** for startup thinking and technology trends

## Contributing & Feedback

We welcome contributions and suggestions! Here are ways you can help:

### System Prompt Improvements
- **Refine the personas** - Found better ways to capture PG's voice or analytical framework?
- **Add new prompt variations** - Different use cases might need different approaches
- **Test and iterate** - Try the prompts with various AI models and share results

### Content & Scripts
- **Missing essays** - Found an essay that's not in the collection?
- **Script enhancements** - Improve the scraper, parser, or indexing tools
- **Documentation** - Help others understand and use the tools better

### Suggestions Welcome
- **New features** - Ideas for better ways to interact with the knowledge base
- **Bug reports** - If something doesn't work as expected
- **Use case examples** - Share how you're using this in your workflow

**Submit issues or PRs on GitHub!**

## License & Attribution

This repository contains content scraped from [paulgraham.com](https://paulgraham.com) for educational and research purposes. 

**Important Notes:**
- All essays remain the intellectual property of **Paul Graham**
- This collection is intended for **personal learning and analysis only**
- Commercial use requires permission from the original author
- The scraping and processing scripts are provided under MIT license
- Please respect the original author's work and link back to [paulgraham.com](https://paulgraham.com) when sharing insights

**Attribution**: Original essays by Paul Graham • Collection and processing tools by this repository's contributors

---

**⭐ Star this repo if you find it useful!** • **🍴 Fork it to customize for your needs** • **📧 Share your use cases and feedback**

---

*"The way to get startup ideas is not to try to think of startup ideas. It's to look for problems, preferably problems you have yourself."* - Paul Graham

**Now go build something people want! 🚀**
