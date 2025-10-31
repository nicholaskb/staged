#!/usr/bin/env python3
"""
Extract MindMap structure from HTML file and convert to ontology instances
"""

import base64
import json
import re
import sys
import zipfile
import io
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class MindMapExtractor:
    """Extract and process MindMap data from HTML viewer file"""
    
    def __init__(self, html_path: str):
        self.html_path = Path(html_path)
        self.nodes = []
        self.relationships = []
        self.node_counter = 0
        
    def extract_mmap_data(self) -> str:
        """Extract base64-encoded mmap data from HTML file"""
        print(f"Reading HTML file: {self.html_path}")
        
        with open(self.html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find the mmap script tag
        pattern = r'<script id="mmap" type="text/plain">(.*?)</script>'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            base64_data = match.group(1).strip()
            print(f"Found mmap data: {len(base64_data)} characters")
            return base64_data
        else:
            raise ValueError("Could not find mmap data in HTML file")
    
    def decode_mmap(self, base64_data: str) -> bytes:
        """Decode base64 mmap data"""
        try:
            decoded = base64.b64decode(base64_data)
            print(f"Decoded {len(decoded)} bytes")
            return decoded
        except Exception as e:
            print(f"Error decoding base64: {e}")
            raise
    
    def extract_xml_from_mmap(self, mmap_bytes: bytes) -> str:
        """Extract XML content from mmap file (which is a zip archive)"""
        try:
            # Try to read as zip file
            with zipfile.ZipFile(io.BytesIO(mmap_bytes)) as zf:
                # List files in the archive
                file_list = zf.namelist()
                print(f"Files in mmap archive: {file_list}")
                
                # Look for the main document file
                for filename in file_list:
                    if 'Document.xml' in filename or filename.endswith('.xml'):
                        print(f"Extracting: {filename}")
                        xml_content = zf.read(filename)
                        return xml_content.decode('utf-8')
                        
        except zipfile.BadZipFile:
            # If not a zip, try as raw XML
            try:
                return mmap_bytes.decode('utf-8')
            except:
                return mmap_bytes.decode('latin-1')
                
        return None
    
    def parse_mindmap_xml(self, xml_content: str) -> Dict:
        """Parse MindMap XML structure"""
        try:
            # Parse XML
            root = ET.fromstring(xml_content)
            
            # Extract namespace
            namespace = root.tag.split('}')[0].strip('{') if '}' in root.tag else ''
            
            print(f"Root element: {root.tag}")
            print(f"Namespace: {namespace}")
            
            # Create structure dict
            structure = {
                'root': None,
                'nodes': [],
                'relationships': []
            }
            
            # Process based on MindManager format
            # This will vary based on the actual XML structure
            self._process_mindmanager_xml(root, structure, namespace)
            
            return structure
            
        except ET.ParseError as e:
            print(f"XML parse error: {e}")
            # Try alternative parsing approaches
            return self._parse_fallback(xml_content)
    
    def _process_mindmanager_xml(self, root, structure, namespace):
        """Process MindManager-specific XML format"""
        # MindManager uses different namespaces
        ns = {'ap': namespace} if namespace else {}
        
        # Find topics in various possible locations
        topics = []
        
        # Try different patterns for MindManager topics
        patterns = [
            './/{http://schemas.mindjet.com/MindManager/Core/2003}Topic',
            './/ap:OneTopic',
            './/ap:Topic', 
            './/Topic',
            './/{*}Topic',
            './/{*}OneTopic',
            './/topic',
            './/node'
        ]
        
        for pattern in patterns:
            found = root.findall(pattern, ns) if ':' in pattern else root.findall(pattern)
            if found:
                topics = found
                print(f"Found {len(topics)} topic nodes using pattern: {pattern}")
                break
        
        if not topics:
            # Try to find the root topic
            if root.tag.endswith('Map'):
                # Look for immediate children
                for child in root:
                    print(f"Root child: {child.tag}")
                    if 'Topic' in child.tag or 'OneTopic' in child.tag:
                        topics = [child]
                        # Also get its children
                        topics.extend(child.findall('.//{*}Topic'))
                        topics.extend(child.findall('.//{*}OneTopic'))
                        break
        
        print(f"Found {len(topics)} topic nodes total")
        
        for topic in topics:
            node_data = self._extract_node_data(topic)
            if node_data:
                structure['nodes'].append(node_data)
    
    def _extract_node_data(self, element) -> Dict:
        """Extract data from a node element"""
        node_id = element.get('id', f'node_{self.node_counter}')
        self.node_counter += 1
        
        # Extract text content - MindManager stores text in Text element
        text = element.get('text', '')
        if not text:
            # Look for Text element (MindManager format)
            text_patterns = [
                './/{http://schemas.mindjet.com/MindManager/Core/2003}Text',
                './/Text',
                './/{*}Text',
                './/text',
                './/{*}text',
                './/PlainText',
                './/{*}PlainText'
            ]
            
            for pattern in text_patterns:
                text_elem = element.find(pattern)
                if text_elem is not None:
                    # Get all text content including PlainText
                    if text_elem.text:
                        text = text_elem.text
                    else:
                        # Look for PlainText child
                        plain_text = text_elem.find('.//{*}PlainText') or text_elem.find('.//PlainText')
                        if plain_text is not None and plain_text.text:
                            text = plain_text.text
                    if text:
                        break
        
        # If still no text, try the element's text directly
        if not text and element.text:
            text = element.text.strip()
        
        # Extract other attributes
        node_data = {
            'id': node_id,
            'text': text or f"Node_{self.node_counter}",
            'type': element.tag.split('}')[-1],  # Remove namespace
            'attributes': dict(element.attrib)
        }
        
        # Process children - look for SubTopics container or direct Topic children
        children = []
        
        # Look for SubTopics container first
        subtopics = element.find('.//{*}SubTopics') or element.find('.//SubTopics')
        if subtopics is not None:
            # Get topics from SubTopics
            child_topics = subtopics.findall('.//{*}Topic') or subtopics.findall('.//Topic')
            child_topics.extend(subtopics.findall('.//{*}OneTopic') or subtopics.findall('.//OneTopic') or [])
        else:
            # Look for direct child topics
            child_topics = []
            for child in element:
                if 'Topic' in child.tag or 'OneTopic' in child.tag:
                    child_topics.append(child)
        
        for child_topic in child_topics:
            child_data = self._extract_node_data(child_topic)
            if child_data:
                children.append(child_data['id'])
                # Add parent-child relationship
                self.relationships.append({
                    'parent': node_id,
                    'child': child_data['id'],
                    'type': 'hasChild'
                })
                # Also add the child to the main nodes list
                self.nodes.append(child_data)
        
        if children:
            node_data['children'] = children
            
        return node_data
    
    def _parse_fallback(self, content: str) -> Dict:
        """Fallback parsing for non-standard formats"""
        structure = {
            'root': 'fallback_root',
            'nodes': [],
            'relationships': []
        }
        
        # Try to extract any hierarchical structure
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['stage', 'gate', 'protein', 'cgt']):
                structure['nodes'].append({
                    'id': f'node_{i}',
                    'text': line.strip(),
                    'type': 'extracted_line'
                })
        
        return structure
    
    def generate_ttl(self, structure: Dict, output_path: str):
        """Generate TTL ontology file from extracted structure"""
        print(f"Generating TTL file: {output_path}")
        
        ttl_lines = [
            '@prefix ex: <https://w3id.org/cmc-stagegate#> .',
            '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .',
            '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .',
            '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
            '',
            '# MindMap Structure extracted from HTML viewer',
            f'# Generated: {datetime.now().isoformat()}',
            f'# Source: {self.html_path.name}',
            '',
            '# MindMap Structure Instance',
            'ex:mindmap_structure_2023Q3 a ex:MindMapStructure ;',
            '    rdfs:label "LM Stage Gates MindMap Q3 2023" ;',
            '    rdfs:comment "Visual hierarchy of stage gates from MindManager" .',
            ''
        ]
        
        # Process nodes
        for node in structure['nodes']:
            node_id = node['id'].replace(' ', '_').replace('-', '_')
            text = node.get('text', '').replace('"', '\\"')
            
            # Determine if this is a Protein or CGT node
            modality = None
            if 'protein' in text.lower():
                modality = 'Protein'
                node_class = 'ex:ProteinStageGate'
            elif 'cgt' in text.lower() or 'cell' in text.lower() or 'gene' in text.lower():
                modality = 'CGT'
                node_class = 'ex:CGTStageGate'
            else:
                node_class = 'ex:MindMapNode'
            
            ttl_lines.append(f'# Node: {text[:50]}...' if len(text) > 50 else f'# Node: {text}')
            ttl_lines.append(f'ex:mm_{node_id} a {node_class} ;')
            ttl_lines.append(f'    rdfs:label "{text}" ;')
            
            if modality:
                ttl_lines.append(f'    ex:modality "{modality}" ;')
            
            # Add visual metadata
            metadata = {
                'originalId': node['id'],
                'type': node.get('type', 'unknown')
            }
            ttl_lines.append(f'    ex:visualMetadata """{json.dumps(metadata)}""" ;')
            
            # Add children relationships
            if 'children' in node:
                child_refs = ', '.join([f'ex:mm_{c.replace(" ", "_").replace("-", "_")}' 
                                       for c in node['children']])
                ttl_lines.append(f'    ex:hasChildNode {child_refs} ;')
            
            ttl_lines[-1] = ttl_lines[-1].rstrip(' ;') + ' .'
            ttl_lines.append('')
        
        # Add relationships
        if self.relationships:
            ttl_lines.append('# Parent-Child Relationships')
            for rel in self.relationships:
                parent_id = rel['parent'].replace(' ', '_').replace('-', '_')
                child_id = rel['child'].replace(' ', '_').replace('-', '_')
                ttl_lines.append(f'ex:mm_{child_id} ex:hasParentNode ex:mm_{parent_id} .')
            ttl_lines.append('')
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ttl_lines))
        
        print(f"Generated {len(structure['nodes'])} nodes in TTL file")
        return len(structure['nodes'])
    
    def extract_and_convert(self, output_path: str = None):
        """Main method to extract MindMap and convert to TTL"""
        if output_path is None:
            output_path = self.html_path.parent / 'mindmap_structure.ttl'
        
        try:
            # Extract mmap data from HTML
            base64_data = self.extract_mmap_data()
            
            # Decode base64
            mmap_bytes = self.decode_mmap(base64_data)
            
            # Extract XML
            xml_content = self.extract_xml_from_mmap(mmap_bytes)
            
            if xml_content:
                print(f"Extracted XML: {len(xml_content)} characters")
                
                # Parse XML structure
                structure = self.parse_mindmap_xml(xml_content)
                
                # Generate TTL
                node_count = self.generate_ttl(structure, output_path)
                
                print(f"Successfully generated ontology with {node_count} nodes")
                return True
            else:
                print("Could not extract XML content from mmap file")
                return False
                
        except Exception as e:
            print(f"Error during extraction: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python extract_mindmap_data.py <html_file> [output_ttl]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    extractor = MindMapExtractor(html_file)
    success = extractor.extract_and_convert(output_file)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
