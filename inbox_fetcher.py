import re
import subprocess
import sys
import os
import json
from datetime import datetime

class TemplateEngine:
    def __init__(self, templates_dir):
        self.templates = []
        for filename in os.listdir(templates_dir):
            if filename.endswith(".json"):
                path = os.path.join(templates_dir, filename)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        tpl = json.load(f)
                        tpl['_filename'] = filename
                        self.templates.append(tpl)
                except Exception as e:
                    print(f"Warning: Could not load template {filename}: {e}", file=sys.stderr)
        
        # Identify default template
        self.default_template = next((t for t in self.templates if "default-raw-clipper" in t['_filename'].lower()), None)
        if not self.default_template:
            self.default_template = next((t for t in self.templates if t.get('name') == "Default Raw Clipper"), None)
        if not self.default_template and self.templates:
            self.default_template = self.templates[0]

    def find_template(self, url):
        best_match = self.default_template
        max_trigger_len = -1
        
        for t in self.templates:
            if t == self.default_template:
                continue
            for trigger in t.get('triggers', []):
                if url.startswith(trigger):
                    if len(trigger) > max_trigger_len:
                        max_trigger_len = len(trigger)
                        best_match = t
        return best_match

    def resolve_placeholder(self, placeholder_expr, data, url):
        # Handle literal strings: {{ "literal text" }}
        if (placeholder_expr.startswith('"') and placeholder_expr.endswith('"')) or \
           (placeholder_expr.startswith("'") and placeholder_expr.endswith("'")):
            return placeholder_expr[1:-1]

        parts = placeholder_expr.split('|')
        expr = parts[0].strip()
        filters = parts[1:]

        value = ""
        # Common top-level properties
        if expr == "title":
            value = data.get('title', '')
        elif expr == "url":
            value = url
        elif expr == "content":
            value = data.get('contentMarkdown', data.get('content', ''))
        elif expr == "description":
            value = data.get('description', '')
        elif expr == "domain":
            value = data.get('domain', '')
        elif expr == "author":
            value = data.get('author', '')
        elif expr == "site":
            value = data.get('site', '')
        elif expr == "image" or expr == "thumbnailUrl":
            value = data.get('image', data.get('thumbnailUrl', ''))
        elif expr == "published":
            value = data.get('published', '')
        elif expr == "date":
            value = datetime.now().strftime("%Y-%m-%d")
        elif expr == "time":
            value = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        elif expr == "words":
            value = str(data.get('wordCount', 0))
        elif expr.startswith("meta:name:"):
            name = expr[len("meta:name:"):]
            for tag in data.get('metaTags', []):
                if tag.get('name') == name:
                    value = tag.get('content', '')
                    break
        elif expr.startswith("meta:property:"):
            prop = expr[len("meta:property:"):]
            for tag in data.get('metaTags', []):
                if tag.get('property') == prop:
                    value = tag.get('content', '')
                    break
        elif expr.startswith("schema:"):
            # schema:@VideoObject:name or schema:@Book:author[0].name
            schema_path = expr[len("schema:"):].split(':')
            if len(schema_path) >= 2:
                target_type = schema_path[0].lstrip('@')
                prop_expr = schema_path[1]
                
                found_in_schema = False
                for obj in data.get('schemaOrgData', []):
                    obj_type = obj.get('@type', '').lstrip('@')
                    if obj_type == target_type:
                        # Follow property path with potential indexing
                        current = obj
                        path_parts = re.split(r'\.|\b(?=\[)', prop_expr)
                        for part in path_parts:
                            if not part: continue
                            idx_match = re.match(r'\[(\d+)\]', part)
                            if idx_match:
                                idx = int(idx_match.group(1))
                                if isinstance(current, list) and idx < len(current):
                                    current = current[idx]
                                else:
                                    current = ""
                                    break
                            else:
                                if isinstance(current, dict):
                                    current = current.get(part, "")
                                else:
                                    current = ""
                                    break
                        value = current
                        if value:
                            found_in_schema = True
                        break
                
                # Fallback to top-level properties
                if not found_in_schema:
                    if prop_expr.endswith("name") or prop_expr == "title":
                        value = data.get('title', '')
                    elif prop_expr == "author":
                        value = data.get('author', '')
                    elif prop_expr == "uploadDate" or prop_expr == "datePublished":
                        value = data.get('published', '')
                    elif prop_expr == "description":
                        value = data.get('description', '')
                    elif prop_expr == "thumbnailUrl":
                        value = data.get('thumbnailUrl', data.get('image', ''))
                    elif prop_expr == "embedUrl" or prop_expr == "url":
                        value = url

        elif expr.startswith("selector"):
            # We don't have a real DOM, but we can try to guess from common properties
            if "title" in expr.lower() or "repo-title" in expr.lower():
                # For GitHub title, it's often user/repo
                value = data.get('title', '').split(':')[0].strip()
            elif "author" in expr.lower():
                value = data.get('author', '')
            elif "content" in expr.lower() or "body" in expr.lower() or "article" in expr.lower():
                value = data.get('contentMarkdown', data.get('content', ''))
            elif "date" in expr.lower() or "published" in expr.lower():
                value = data.get('published', '')
            elif "sidebar" in expr.lower() or "description" in expr.lower():
                value = data.get('description', '')
            else:
                value = ""
        elif expr == "transcript":
            content = data.get('content', '')
            match = re.search(r'<div class="youtube transcript">(.*?)</div>', content, re.DOTALL)
            if match:
                transcript_html = match.group(1)
                transcript = re.sub(r'<h[1-6].*?>(.*?)</h[1-6]>', r'### \1', transcript_html)
                transcript = re.sub(r'<p.*?>(.*?)</p>', r'\1\n', transcript)
                transcript = re.sub(r'<span class="timestamp".*?>(.*?)</span>', r'**\1**', transcript)
                transcript = re.sub(r'<.*?>', '', transcript)
                value = transcript.strip()
        
        # Apply filters
        for f in filters:
            value = self.apply_filter(value, f)
        
        return str(value)

    def apply_filter(self, value, filter_expr):
        f_match = re.match(r'^(\w+)(?::(.*))?$', filter_expr.strip())
        if not f_match:
            return value
        
        name = f_match.group(1)
        args_str = f_match.group(2)
        args = []
        if args_str:
            args = re.findall(r'"([^"]*)"', args_str)
            if not args:
                args = args_str.split(',')

        if name == "safe_name":
            value = re.sub(r'[\\/*?:"<>|]', '', str(value))
        elif name == "trim":
            value = str(value).strip()
        elif name == "wikilink":
            value = f"[[{value}]]" if value else ""
        elif name == "date":
            fmt = args[0] if args else "%Y-%m-%d"
            fmt = fmt.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d").replace("HH", "%H").replace("mm", "%M").replace("ss", "%S")
            try:
                if value and isinstance(value, str) and not value.startswith('"'):
                    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    value = dt.strftime(fmt)
                else:
                    value = datetime.now().strftime(fmt)
            except:
                value = datetime.now().strftime(fmt)
        elif name == "replace":
            if len(args) >= 2:
                value = str(value).replace(args[0], args[1])
        elif name == "join":
            sep = args[0] if args else ", "
            if isinstance(value, list):
                value = sep.join(map(str, value))
        elif name == "first":
            if isinstance(value, list) and value:
                value = value[0]
        elif name == "markdown":
            pass
        elif name == "remove_tags" or name == "remove_html" or name == "strip_tags":
            value = re.sub(r'<.*?>', '', str(value))
        elif name == "split":
            sep = args[0] if args else ","
            value = str(value).split(sep)
        elif name == "calc":
            if args:
                expr = args[0]
                try:
                    num = float(value)
                    if expr.startswith("/"): value = num / float(expr[1:])
                    elif expr.startswith("*"): value = num * float(expr[1:])
                except: pass
        elif name == "round":
            try: value = round(float(value))
            except: pass

        return value

    def render(self, template, data, url):
        # 1. Properties (Frontmatter)
        properties = {}
        for prop in template.get('properties', []):
            prop_name = prop.get('name')
            prop_value_expr = prop.get('value')
            val = re.sub(r'{{(.*?)}}', lambda m: self.resolve_placeholder(m.group(1), data, url), prop_value_expr)
            properties[prop_name] = val
        
        # Always add unread: true
        properties['unread'] = True
        
        # 2. Content
        content_fmt = template.get('noteContentFormat', '{{content}}')
        body = re.sub(r'{{(.*?)}}', lambda m: self.resolve_placeholder(m.group(1), data, url), content_fmt)
        
        # 3. Handle 'context' if present
        if 'context' in template:
            context_val = re.sub(r'{{(.*?)}}', lambda m: self.resolve_placeholder(m.group(1), data, url), template['context'])
            body = body.replace('{{context}}', context_val)

        yaml_frontmatter = "---\n"
        for k, v in properties.items():
            if ":" in str(v) or "\"" in str(v) or "\n" in str(v):
                v_safe = json.dumps(v)
            else:
                v_safe = v
            yaml_frontmatter += f"{k}: {v_safe}\n"
        yaml_frontmatter += "---\n\n"
        
        final_output = yaml_frontmatter + body
        
        name_fmt = template.get('noteNameFormat', '{{title}}')
        filename = re.sub(r'{{(.*?)}}', lambda m: self.resolve_placeholder(m.group(1), data, url), name_fmt)
        filename = re.sub(r'[\\/*?:"<>|]', '', filename).strip()
        if not filename:
            filename = "Untitled"
        filename += ".md"
        
        return filename, final_output

def fetch_and_save(url, output_dir, engine):
    print(f"Processing URL: {url}")
    try:
        process = subprocess.run(
            ['defuddle', 'parse', url, '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(process.stdout)
        
        template = engine.find_template(url)
        filename, content = engine.render(template, data, url)
        
        target_dir = template.get('path', output_dir)
        if not os.path.isabs(target_dir):
            target_dir = os.path.join(os.getcwd(), target_dir)
            
        output_path = os.path.join(target_dir, filename)

        if os.path.exists(output_path):
            print(f"Skipping duplicate: {filename} already exists.")
            return

        print(f"Using template: {template.get('name', 'Unknown')}")
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully saved content to {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error processing {url}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}", file=sys.stderr)

def main():
    input_text = ""
    
    if not sys.stdin.isatty():
        input_text = sys.stdin.read()
    elif len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isfile(arg):
            with open(arg, 'r', encoding='utf-8') as f:
                input_text = f.read()
        else:
            input_text = arg
            
    if not input_text:
        print("Usage:")
        print("  1. Pass text as argument: python3 inbox_fetcher.py \"some text with https://links.com\"")
        print("  2. Pass a filename:      python3 inbox_fetcher.py my_links.txt")
        print("  3. Pipe text:           cat my_links.txt | python3 inbox_fetcher.py")
        sys.exit(1)
    
    output_dir = "00 Inbox"
    templates_dir = "_Assets"
    engine = TemplateEngine(templates_dir)

    url_pattern = re.compile(r'https?://[\S]+')
    urls = url_pattern.findall(input_text)
    
    if not urls:
        print("No URLs found in the input text.")
        return

    print(f"Found {len(urls)} URLs. Starting processing...")
    for url in urls:
        cleaned_url = url.rstrip(')').rstrip(']')
        fetch_and_save(cleaned_url, output_dir, engine)

if __name__ == "__main__":
    main()
