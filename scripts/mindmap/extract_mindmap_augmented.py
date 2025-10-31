#!/usr/bin/env python3
"""
Enhanced MindMap extractor that properly extracts text content and augments existing ontology
Creates only additional triples to add to existing CMC Stage-Gate ontology
"""

import base64
import json
import re
import sys
import zipfile
import io
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import html


class EnhancedMindMapExtractor:
    """Enhanced extractor that properly handles MindManager XML text extraction"""
    
    def __init__(self, html_path: str):
        self.html_path = Path(html_path)
        self.nodes = {}  # Store as dict for easier access
        self.relationships = []
        self.node_counter = 0
        self.stage_nodes = []  # Track stage-related nodes
        self.protein_nodes = []  # Track protein-specific nodes
        self.cgt_nodes = []  # Track CGT-specific nodes
        
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
    
    def decode_and_extract_xml(self, base64_data: str) -> ET.Element:
        """Decode base64 and extract XML from mmap zip"""
        decoded = base64.b64decode(base64_data)
        
        with zipfile.ZipFile(io.BytesIO(decoded)) as zf:
            # Find Document.xml
            for filename in zf.namelist():
                if 'Document.xml' in filename:
                    print(f"Extracting: {filename}")
                    xml_content = zf.read(filename)
                    # Parse and return root element
                    return ET.fromstring(xml_content.decode('utf-8'))
        
        raise ValueError("Could not find Document.xml in mmap archive")
    
    def extract_text_from_node(self, node: ET.Element, namespaces: Dict[str, str]) -> str:
        """Extract text content from a MindManager node element"""
        text = ""
        
        # Try various text extraction patterns
        # 1. Look for Text element and check its PlainText ATTRIBUTE
        text_elem = node.find('.//ap:Text', namespaces)
        if text_elem is None:
            text_elem = node.find('.//{http://schemas.mindjet.com/MindManager/Application/2003}Text')
        
        if text_elem is not None:
            # PlainText is an ATTRIBUTE, not a child element!
            plain_text_attr = text_elem.get('PlainText', '')
            if plain_text_attr:
                text = plain_text_attr.strip()
            
            # Also try as child element for older formats
            if not text:
                plain_text = text_elem.find('.//ap:PlainText', namespaces)
                if plain_text is None:
                    plain_text = text_elem.find('.//{http://schemas.mindjet.com/MindManager/Primitive/2003}PlainText')
                
                if plain_text is not None and plain_text.text:
                    text = plain_text.text.strip()
        
        # 2. Try TextLabels element
        if not text:
            text_labels = node.find('.//ap:TextLabels', namespaces)
            if text_labels is None:
                text_labels = node.find('.//{http://schemas.mindjet.com/MindManager/Application/2003}TextLabels')
            
            if text_labels is not None:
                # Get first label text
                for label in text_labels:
                    label_text = label.get('PlainTextLabel', '')
                    if label_text:
                        text = label_text.strip()
                        break
        
        # 3. Try Title element (some versions use this)
        if not text:
            title_elem = node.find('.//ap:Title', namespaces)
            if title_elem is None:
                title_elem = node.find('.//{http://schemas.mindjet.com/MindManager/Core/2003}Title')
            
            if title_elem is not None and title_elem.text:
                text = title_elem.text.strip()
        
        # 4. Try Label attribute
        if not text:
            text = node.get('Label', '')
        
        # 5. Try text attribute
        if not text:
            text = node.get('text', '')
        
        # Decode HTML entities if present
        if text:
            text = html.unescape(text)
        
        return text
    
    def process_topic_node(self, topic: ET.Element, namespaces: Dict[str, str], parent_id: Optional[str] = None, level: int = 0) -> Dict:
        """Process a topic node and extract all its information"""
        node_id = topic.get('ObjectId', f'node_{self.node_counter}')
        self.node_counter += 1
        
        # Extract text
        text = self.extract_text_from_node(topic, namespaces)
        
        # If still no text, generate descriptive text based on position
        if not text:
            if level == 0:
                text = "Root Node"
            else:
                text = f"Node {self.node_counter}"
        
        # Determine node type based on text content
        node_type = self.classify_node(text)
        
        # Create node data
        node_data = {
            'id': node_id,
            'text': text,
            'level': level,
            'type': node_type,
            'modality': self.detect_modality(text),
            'stage': self.extract_stage_number(text),
            'gate': self.extract_gate_number(text)
        }
        
        # Store node
        self.nodes[node_id] = node_data
        
        # Track special nodes
        if node_type in ['stage', 'gate', 'stage_gate']:
            self.stage_nodes.append(node_id)
            if node_data['modality'] == 'Protein':
                self.protein_nodes.append(node_id)
            elif node_data['modality'] == 'CGT':
                self.cgt_nodes.append(node_id)
        
        # Add parent relationship
        if parent_id:
            self.relationships.append({
                'parent': parent_id,
                'child': node_id,
                'type': 'hasChild'
            })
        
        # Process SubTopics (children)
        # Try multiple patterns to find subtopics
        subtopics = None
        
        # Pattern 1: Direct SubTopics child
        subtopics = topic.find('ap:SubTopics', namespaces)
        if subtopics is None:
            subtopics = topic.find('{http://schemas.mindjet.com/MindManager/Core/2003}SubTopics')
        
        # Pattern 2: Look for any SubTopics element anywhere
        if subtopics is None:
            for elem in topic:
                if 'SubTopics' in elem.tag:
                    subtopics = elem
                    print(f"Found SubTopics via iteration: {elem.tag}")
                    break
        
        if subtopics is not None:
            child_count = 0
            # Process each child topic
            for child_topic in subtopics:
                if 'Topic' in child_topic.tag or 'OneTopic' in child_topic.tag:
                    child_count += 1
                    self.process_topic_node(child_topic, namespaces, node_id, level + 1)
            
            if child_count > 0:
                print(f"  Level {level}: Processed {child_count} children for '{text[:50]}...'")
        else:
            # Also try to find direct Topic children
            child_count = 0
            for child in topic:
                if 'Topic' in child.tag and 'SubTopics' not in child.tag:
                    child_count += 1
                    self.process_topic_node(child, namespaces, node_id, level + 1)
            
            if child_count > 0:
                print(f"  Level {level}: Processed {child_count} direct Topic children for '{text[:50]}...'")
        
        return node_data
    
    def classify_node(self, text: str) -> str:
        """Classify node based on text content"""
        text_lower = text.lower()
        
        if 'stage' in text_lower and 'gate' in text_lower:
            return 'stage_gate'
        elif 'stage' in text_lower:
            return 'stage'
        elif 'gate' in text_lower:
            return 'gate'
        elif 'deliverable' in text_lower:
            return 'deliverable'
        elif 'milestone' in text_lower:
            return 'milestone'
        elif 'cqa' in text_lower or 'quality' in text_lower:
            return 'quality_attribute'
        elif 'process' in text_lower:
            return 'process'
        elif 'formulation' in text_lower:
            return 'formulation'
        elif 'clinical' in text_lower:
            return 'clinical'
        elif 'regulatory' in text_lower:
            return 'regulatory'
        else:
            return 'general'
    
    def detect_modality(self, text: str) -> Optional[str]:
        """Detect if node is specific to Protein or CGT modality"""
        text_lower = text.lower()
        
        # CGT indicators
        cgt_keywords = ['cgt', 'cell', 'gene', 'therapy', 'car-t', 'cart', 
                       'lentivirus', 'aav', 'vector', 'transduction']
        for keyword in cgt_keywords:
            if keyword in text_lower:
                return 'CGT'
        
        # Protein indicators  
        protein_keywords = ['protein', 'mab', 'antibody', 'biologic', 
                          'monoclonal', 'fusion', 'peptide']
        for keyword in protein_keywords:
            if keyword in text_lower:
                return 'Protein'
        
        return None
    
    def extract_stage_number(self, text: str) -> Optional[str]:
        """Extract stage number from text"""
        # Look for patterns like "Stage 0", "Stage 1", "S0", "S1"
        patterns = [
            r'[Ss]tage\s*(\d+)',
            r'S(\d+)',
            r'Phase\s*(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    def extract_gate_number(self, text: str) -> Optional[str]:
        """Extract gate number from text"""
        # Look for patterns like "Gate 0", "Gate 1", "G0", "G1"
        patterns = [
            r'[Gg]ate\s*(\d+)',
            r'G(\d+)',
            r'Review\s*(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    def extract_all(self) -> Dict:
        """Main extraction method"""
        try:
            # Extract mmap data
            base64_data = self.extract_mmap_data()
            
            # Decode and get XML root
            root = self.decode_and_extract_xml(base64_data)
            
            # Define namespaces
            namespaces = {
                'ap': 'http://schemas.mindjet.com/MindManager/Application/2003',
                'cor': 'http://schemas.mindjet.com/MindManager/Core/2003',
                'pri': 'http://schemas.mindjet.com/MindManager/Primitive/2003'
            }
            
            print(f"Root element: {root.tag}")
            
            # Find the main topic (root of the mindmap)
            main_topic = root.find('.//ap:OneTopic', namespaces)
            if main_topic is None:
                main_topic = root.find('.//{http://schemas.mindjet.com/MindManager/Core/2003}OneTopic')
            
            if main_topic is not None:
                print("Found main topic, processing hierarchy...")
                
                # Debug: show what's in the main topic
                print(f"Main topic tag: {main_topic.tag}")
                print(f"Main topic children: {[child.tag for child in main_topic][:10]}")
                
                self.process_topic_node(main_topic, namespaces, level=0)
                
                print(f"\nExtracted {len(self.nodes)} nodes")
                print(f"  - Stage/Gate nodes: {len(self.stage_nodes)}")
                print(f"  - Protein-specific: {len(self.protein_nodes)}")
                print(f"  - CGT-specific: {len(self.cgt_nodes)}")
            else:
                print("Could not find main topic in MindMap")
            
            return {
                'nodes': self.nodes,
                'relationships': self.relationships,
                'stage_nodes': self.stage_nodes,
                'protein_nodes': self.protein_nodes,
                'cgt_nodes': self.cgt_nodes
            }
            
        except Exception as e:
            print(f"Error during extraction: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_augmented_ttl(self, data: Dict, output_path: str):
        """Generate TTL that augments existing ontology"""
        print(f"Generating augmented TTL: {output_path}")
        
        ttl_lines = [
            '# MindMap Augmentation for CMC Stage-Gate Ontology',
            f'# Generated: {datetime.now().isoformat()}',
            f'# Source: {self.html_path.name}',
            '# This file AUGMENTS the existing ontology - it only adds new triples',
            '',
            '@prefix ex: <https://w3id.org/cmc-stagegate#> .',
            '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .',
            '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .',
            '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
            '',
            '# MindMap Structure Instance',
            'ex:mindmap_lm_2023q3 a ex:MindMapStructure ;',
            '    rdfs:label "LM Stage Gates MindMap Q3 2023" ;',
            '    rdfs:comment "Visual hierarchy extracted from MindManager document" .',
            ''
        ]
        
        # Generate nodes with proper text labels
        for node_id, node_data in data['nodes'].items():
            safe_id = node_id.replace(' ', '_').replace('-', '_')
            text = node_data['text'].replace('"', '\\"')
            
            # Determine class based on node classification
            node_class = 'ex:MindMapNode'
            if node_data['type'] == 'stage_gate':
                if node_data['modality'] == 'Protein':
                    node_class = 'ex:ProteinStageGate'
                elif node_data['modality'] == 'CGT':
                    node_class = 'ex:CGTStageGate'
                else:
                    node_class = 'ex:StageGate'
            elif node_data['type'] == 'stage':
                node_class = 'ex:Stage'
            elif node_data['type'] == 'gate':
                node_class = 'ex:StageGate'
            
            ttl_lines.append(f'# {text[:80]}...' if len(text) > 80 else f'# {text}')
            ttl_lines.append(f'ex:mm_{safe_id} a {node_class}, ex:MindMapNode ;')
            ttl_lines.append(f'    rdfs:label "{text}" ;')
            
            # Add modality if detected
            if node_data['modality']:
                ttl_lines.append(f'    ex:modality "{node_data["modality"]}" ;')
            
            # Add stage reference if detected
            if node_data['stage']:
                ttl_lines.append(f'    ex:hasStage ex:stage_{node_data["stage"]} ;')
            
            # Add gate reference if detected
            if node_data['gate']:
                ttl_lines.append(f'    ex:hasGate ex:gate_{node_data["gate"]} ;')
            
            # Add hierarchy level
            ttl_lines.append(f'    ex:hierarchyLevel {node_data["level"]} ;')
            
            # Add node type
            ttl_lines.append(f'    ex:nodeType "{node_data["type"]}" ;')
            
            # Add visual metadata
            metadata = {
                'originalId': node_id,
                'level': node_data['level'],
                'type': node_data['type']
            }
            ttl_lines.append(f'    ex:visualMetadata """{json.dumps(metadata)}""" .')
            ttl_lines.append('')
        
        # Add hierarchical relationships
        ttl_lines.append('# Hierarchical Relationships')
        for rel in data['relationships']:
            parent_id = rel['parent'].replace(' ', '_').replace('-', '_')
            child_id = rel['child'].replace(' ', '_').replace('-', '_')
            ttl_lines.append(f'ex:mm_{child_id} ex:hasParentNode ex:mm_{parent_id} .')
        ttl_lines.append('')
        
        # Add connections to existing ontology entities (if we can identify them)
        ttl_lines.append('# Links to existing CMC Stage-Gate entities')
        ttl_lines.append('# These connect MindMap nodes to existing stages and gates')
        
        # Write to file
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ttl_lines))
        
        print(f"Generated augmented ontology with {len(data['nodes'])} nodes")
        return len(data['nodes'])


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python extract_mindmap_augmented.py <html_file> [output_ttl]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_augment_mindmap/mindmap_augmented.ttl"
    
    extractor = EnhancedMindMapExtractor(html_file)
    data = extractor.extract_all()
    
    if data:
        node_count = extractor.generate_augmented_ttl(data, output_file)
        print(f"Successfully generated augmented ontology")
        sys.exit(0)
    else:
        print("Extraction failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
