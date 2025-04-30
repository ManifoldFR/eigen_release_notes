import json
import re
from collections import defaultdict

def extract_pr_number(text):
    """Extract PR number from markdown entry like [#123](...): Description"""
    match = re.search(r'\[#(\d+)\]', text)
    if match:
        return int(match.group(1))
    return 0  # Default value if no match

def jsonl_to_markdown(jsonl_file, output_file):
    # Dictionary to store categories and their items
    categories = defaultdict(lambda: defaultdict(list))
    
    # Read and parse the JSONL file
    num_lines = 0
    with open(jsonl_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            for mr_id, category_dict in data.items():
                for category_path, content in category_dict.items():
                    # Split the category path into main category and subcategory
                    main_category, subcategory = category_path.split('/')
                    categories[main_category][subcategory].append(content)
            num_lines += 1
    print(f"Processed {num_lines} lines")
    
    # Sort items within each subcategory by PR number
    for main_category in categories:
        for subcategory in categories[main_category]:
            categories[main_category][subcategory].sort(key=extract_pr_number)
    
    # Generate the markdown content
    markdown_content = []
    
    # Sort categories for consistent output
    for main_category in sorted(categories.keys()):
        markdown_content.append(f"# {main_category.capitalize()}")
        markdown_content.append("")  # Empty line after main heading
        
        # First handle normal subcategories
        for subcategory in sorted([s for s in categories[main_category].keys() if not s.startswith('other_')]):
            markdown_content.append(f"## {subcategory.replace('_', ' ').capitalize()}")
            markdown_content.append("")  # Empty line after subheading
            
            # Add list items
            for item in categories[main_category][subcategory]:
                markdown_content.append(f"- {item}")
            
            markdown_content.append("")  # Empty line after list
        
        # Then handle other_xxx subcategories in a specific order
        other_subcategories = [s for s in categories[main_category].keys() if s.startswith('other_')]
        if other_subcategories:
            markdown_content.append("## Other")
            markdown_content.append("")  # Empty line after subheading
            
            # Define preferred order for other subcategories
            preferred_order = ["other_fixed", "other_improved", "other_added", "other_removed", "other_changed"]
            
            # Sort other subcategories based on preferred order
            def get_order_index(subcategory):
                try:
                    return preferred_order.index(subcategory)
                except ValueError:
                    return len(preferred_order)  # Put unknown categories at the end
            
            for subcategory in sorted(other_subcategories, key=get_order_index):
                # Extract the action part (e.g., "fixed" from "other_fixed")
                action = subcategory.split('_')[1].capitalize()
                markdown_content.append(f"### {action}")
                markdown_content.append("")  # Empty line after action label
                
                # Add list items
                for item in categories[main_category][subcategory]:
                    markdown_content.append(f"- {item}")
                
                markdown_content.append("")  # Empty line after list
    
    # Write to output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(markdown_content))
    
    print(f"Markdown file generated successfully: {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = "mr_release_notes.jsonl"
    jsonl_to_markdown(input_file, "changelog.md")
