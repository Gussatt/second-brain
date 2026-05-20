# inbox-fetcher

Use when you need to fetch content from a URL and save it to the `00 Inbox` directory using specific Obsidian Web Clipper templates. This skill ensures that content is formatted correctly according to the site type (YouTube, GitHub, etc.), prevents duplicate notes, and adds the `unread: true` property to new notes.

## Core Pattern

1. **Identify URLs**: Extract all URLs from the input text or provided source.
2. **Execute Fetcher**: Run the `inbox_fetcher.py` script to process the URLs.
   ```bash
   python3 inbox_fetcher.py "<text_containing_urls>"
   ```
3. **Template Mapping**: The script automatically selects the best template from `_Assets/` based on the URL's trigger patterns.
4. **Duplicate Check**: The script skips URLs that would result in a file that already exists in the target directory.
5. **Unread Tracking**: Every new note created by the script includes `unread: true` in its frontmatter.

## When to Use

- When a user provides a list of links to "process" or "add to the vault".
- As a pre-processing step for skills like `summarize` or `wiki-ingest` when they are given a URL instead of a local file.
- To ensure consistent metadata and formatting for all incoming web content.

## Examples

### Processing a single link
User: "Save this video to my inbox: https://www.youtube.com/watch?v=zjkBMFhNj_g"
Assistant: Runs `python3 inbox_fetcher.py "https://www.youtube.com/watch?v=zjkBMFhNj_g"`

### Processing multiple links from text
User: "Here are some articles I found: [Link 1](...), [Link 2](...)"
Assistant: Runs `python3 inbox_fetcher.py "..."` (passing the full text)
