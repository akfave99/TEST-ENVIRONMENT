"""
Fix the choropleth embedding by removing nested HTML tags
"""
import re
import os

def fix_html_file(filepath):
    """Fix a single HTML file by removing nested HTML tags."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find and remove nested <html><head>...</head><body>...</body></html> tags
    # Keep only the inner content (div and script)
    pattern = r'<html>\s*<head>.*?</head>\s*<body>\s*(.*?)\s*</body>\s*</html>'
    
    def replace_nested_html(match):
        # Return just the inner content
        return match.group(1)
    
    # Replace all nested HTML documents
    new_content = re.sub(pattern, replace_nested_html, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

# Fix all chart files
docs_dir = 'docs'
files_to_fix = [
    'chart3-defense-systems.html',
    'chart4-multi-country-radar.html',
    'chart5-priorities-heatmap.html'
]

for filename in files_to_fix:
    filepath = os.path.join(docs_dir, filename)
    if os.path.exists(filepath):
        if fix_html_file(filepath):
            print(f"✅ Fixed {filename}")
        else:
            print(f"⚠️  No nested HTML found in {filename}")
    else:
        print(f"❌ File not found: {filename}")

print("\n✅ All files fixed!")
