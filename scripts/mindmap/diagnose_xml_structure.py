#!/usr/bin/env python3
"""
Diagnostic script to examine the MindManager XML structure and find where text is stored
"""

import base64
import sys
import zipfile
import io
import xml.etree.ElementTree as ET
from pathlib import Path


def extract_and_diagnose(html_path):
    """Extract and diagnose the XML structure"""
    print(f"Reading: {html_path}")
    
    # Extract mmap data
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    pattern = r'<script id="mmap" type="text/plain">(.*?)</script>'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("Could not find mmap data")
        return
    
    base64_data = match.group(1).strip()
    decoded = base64.b64decode(base64_data)
    
    # Extract XML
    with zipfile.ZipFile(io.BytesIO(decoded)) as zf:
        for filename in zf.namelist():
            if 'Document.xml' in filename:
                xml_content = zf.read(filename)
                root = ET.fromstring(xml_content.decode('utf-8'))
                break
    
    print(f"\nRoot element: {root.tag}")
    
    # Find the main topic
    main_topic = None
    for elem in root.iter():
        if 'OneTopic' in elem.tag:
            main_topic = elem
            break
    
    if not main_topic:
        print("Could not find OneTopic")
        return
    
    print(f"\nMain topic tag: {main_topic.tag}")
    print(f"Main topic attributes: {dict(main_topic.attrib)}")
    
    # Show first few levels of structure
    print("\n=== First Topic Structure ===")
    show_element_structure(main_topic, max_depth=3, current_depth=0)
    
    # Find first few topics with different structures
    print("\n=== Sample Topic Nodes ===")
    count = 0
    for elem in root.iter():
        if ('Topic' in elem.tag or 'OneTopic' in elem.tag) and count < 5:
            print(f"\nTopic {count + 1}:")
            print(f"  Tag: {elem.tag}")
            print(f"  Attributes: {dict(elem.attrib)}")
            
            # Look for text in various places
            if elem.text and elem.text.strip():
                print(f"  Direct text: {elem.text.strip()[:50]}...")
            
            # Check children for text elements
            for child in elem:
                tag_name = child.tag.split('}')[-1]
                if 'Text' in tag_name or 'Title' in tag_name or 'Label' in tag_name:
                    print(f"  Found {tag_name}: ", end="")
                    if child.text:
                        print(f"{child.text.strip()[:50]}...")
                    else:
                        # Check grandchildren
                        for grandchild in child:
                            gname = grandchild.tag.split('}')[-1]
                            if grandchild.text:
                                print(f"{gname}: {grandchild.text.strip()[:50]}...")
                                break
            
            count += 1
    
    # Find and show a few topics deeper in the tree
    print("\n=== Deep Topic Examples ===")
    find_deep_topics(root, max_samples=3)


def show_element_structure(elem, max_depth=3, current_depth=0, indent=""):
    """Show element structure recursively"""
    if current_depth > max_depth:
        return
    
    tag_name = elem.tag.split('}')[-1]
    attrs = list(elem.attrib.keys())
    
    print(f"{indent}{tag_name}")
    if attrs:
        print(f"{indent}  Attributes: {', '.join(attrs)}")
    if elem.text and elem.text.strip():
        print(f"{indent}  Text: {elem.text.strip()[:50]}...")
    
    # Show unique child tags
    child_tags = set()
    for child in elem:
        child_tag = child.tag.split('}')[-1]
        child_tags.add(child_tag)
    
    if child_tags:
        print(f"{indent}  Children: {', '.join(sorted(child_tags))}")
        
        # Recurse for first instance of each unique tag
        shown = set()
        for child in elem:
            child_tag = child.tag.split('}')[-1]
            if child_tag not in shown:
                shown.add(child_tag)
                show_element_structure(child, max_depth, current_depth + 1, indent + "    ")


def find_deep_topics(root, max_samples=3):
    """Find topics that are deep in the hierarchy"""
    samples_found = 0
    
    # Use a path to track depth
    def traverse(elem, path=[]):
        nonlocal samples_found
        
        if samples_found >= max_samples:
            return
        
        tag_name = elem.tag.split('}')[-1]
        
        # If we're deep enough and it's a topic
        if len(path) > 5 and ('Topic' in tag_name or 'OneTopic' in tag_name):
            samples_found += 1
            print(f"\nDeep Topic at level {len(path)}:")
            print(f"  Path: {' > '.join(path[-3:])}")
            print(f"  Tag: {elem.tag}")
            
            # Try to find text
            for child in elem:
                child_tag = child.tag.split('}')[-1]
                if 'Text' in child_tag:
                    print(f"  Text element found: {child_tag}")
                    # Check for PlainText
                    for gc in child:
                        gc_tag = gc.tag.split('}')[-1]
                        if 'PlainText' in gc_tag and gc.text:
                            print(f"    PlainText content: {gc.text.strip()[:100]}...")
                            return
                    if child.text:
                        print(f"    Direct text: {child.text.strip()[:100]}...")
        
        # Recurse
        for child in elem:
            traverse(child, path + [tag_name])
    
    traverse(root)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python diagnose_xml_structure.py <html_file>")
        sys.exit(1)
    
    extract_and_diagnose(sys.argv[1])
