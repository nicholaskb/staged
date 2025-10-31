#!/usr/bin/env python3
"""
Comprehensive TTL/OWL file verification
Validates syntax, counts triples, and checks consistency
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import re


def check_rapper_available():
    """Check if rapper (RDF parser) is available."""
    try:
        result = subprocess.run(['which', 'rapper'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def validate_ttl_syntax_basic(file_path: Path) -> Tuple[bool, str, Dict]:
    """Basic TTL syntax validation without external tools."""
    stats = {
        'lines': 0,
        'prefixes': 0,
        'classes': 0,
        'properties': 0,
        'instances': 0,
        'comments': 0,
        'triples': 0
    }
    errors = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        stats['lines'] = len(lines)
        
        # Check for basic TTL structure
        prefix_pattern = r'@prefix\s+(\w+):\s*<([^>]+)>\s*\.'
        class_pattern = r'(\w+:\w+)\s+a\s+(owl:Class|rdfs:Class)'
        property_pattern = r'(\w+:\w+)\s+a\s+(owl:ObjectProperty|owl:DatatypeProperty|rdf:Property)'
        subclass_pattern = r'(\w+:\w+)\s+rdfs:subClassOf'
        instance_pattern = r'(\w+:\w+)\s+a\s+(\w+:\w+)'
        
        bracket_depth = 0
        in_multiline = False
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Count comments
            if stripped.startswith('#'):
                stats['comments'] += 1
                continue
            
            # Count prefixes
            if re.match(prefix_pattern, stripped):
                stats['prefixes'] += 1
            
            # Count classes
            if re.search(class_pattern, stripped) or re.search(subclass_pattern, stripped):
                stats['classes'] += 1
            
            # Count properties
            if re.search(property_pattern, stripped):
                stats['properties'] += 1
            
            # Count instances (rough estimate)
            if ' a ' in stripped and not 'owl:' in stripped and not 'rdfs:Class' in stripped:
                stats['instances'] += 1
            
            # Check bracket balance
            bracket_depth += stripped.count('[') - stripped.count(']')
            bracket_depth += stripped.count('(') - stripped.count(')')
            
            # Count triple endings
            stats['triples'] += stripped.count('.') + stripped.count(';')
        
        # Check final bracket balance
        if bracket_depth != 0:
            errors.append(f"Unbalanced brackets: depth = {bracket_depth}")
        
        # Basic validation checks
        if stats['prefixes'] == 0:
            errors.append("No @prefix declarations found")
        
        # Check for required prefixes
        required_prefixes = ['ex:', 'rdfs:', 'owl:']
        for prefix in required_prefixes:
            if prefix not in content:
                errors.append(f"Missing expected prefix: {prefix}")
        
        # Check for common TTL syntax errors
        if ';;' in content:
            errors.append("Double semicolon found (possible syntax error)")
        
        if re.search(r'\.\s*[,;]', content):
            errors.append("Comma or semicolon after period (possible syntax error)")
        
        # Check for proper TTL ending
        if not content.rstrip().endswith(('.', ']', ')')):
            errors.append("File doesn't end with proper TTL terminator")
        
    except Exception as e:
        return False, f"Error reading file: {e}", stats
    
    if errors:
        return False, "; ".join(errors), stats
    return True, "Valid", stats


def validate_ttl_with_rapper(file_path: Path) -> Tuple[bool, str, int]:
    """Validate TTL using rapper if available."""
    try:
        # Try to parse and count triples
        result = subprocess.run(
            ['rapper', '-i', 'turtle', '-c', str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Extract triple count from stderr (rapper outputs stats to stderr)
            triple_count = 0
            for line in result.stderr.split('\n'):
                if 'returned' in line and 'triples' in line:
                    # Extract number from line like "rapper: Parsing returned 118 triples"
                    import re
                    match = re.search(r'returned (\d+) triples', line)
                    if match:
                        triple_count = int(match.group(1))
                        break
            return True, "Valid (rapper)", triple_count
        else:
            # Extract error message
            error_msg = result.stderr.strip()
            if 'Error' in error_msg:
                error_lines = [line for line in error_msg.split('\n') if 'Error' in line]
                return False, error_lines[0] if error_lines else "Validation failed", 0
            return False, "Validation failed", 0
            
    except subprocess.TimeoutExpired:
        return False, "Validation timeout", 0
    except Exception as e:
        return False, f"Rapper error: {e}", 0


def check_imports_and_dependencies(file_path: Path) -> List[str]:
    """Check for import statements and dependencies."""
    dependencies = []
    content = file_path.read_text(encoding='utf-8')
    
    # Check for owl:imports
    import_pattern = r'owl:imports\s+<([^>]+)>'
    for match in re.finditer(import_pattern, content):
        dependencies.append(match.group(1))
    
    # Check for references to other local files
    if 'cmc_stagegate_base' in content and 'base.ttl' not in str(file_path):
        dependencies.append("References base ontology")
    if 'gist:' in content:
        dependencies.append("Uses GIST ontology")
    if 'prov:' in content:
        dependencies.append("Uses PROV-O")
    if 'qudt:' in content:
        dependencies.append("Uses QUDT")
    
    return dependencies


def analyze_ttl_content(file_path: Path) -> Dict:
    """Analyze TTL content for key patterns."""
    content = file_path.read_text(encoding='utf-8')
    
    analysis = {
        'uses_gist': 'gist:' in content,
        'uses_prov': 'prov:' in content,
        'uses_qudt': 'qudt:' in content,
        'uses_owl': 'owl:' in content,
        'has_classes': 'rdfs:subClassOf' in content or 'a owl:Class' in content,
        'has_properties': 'owl:ObjectProperty' in content or 'owl:DatatypeProperty' in content,
        'has_instances': bool(re.search(r'\w+:\w+\s+a\s+ex:\w+', content)),
        'has_comments': '#' in content,
        'has_labels': 'rdfs:label' in content,
        'has_descriptions': 'rdfs:comment' in content
    }
    
    # Count specific elements
    analysis['prefix_count'] = len(re.findall(r'@prefix', content))
    analysis['class_count'] = len(re.findall(r'rdfs:subClassOf', content))
    analysis['gist_refs'] = len(re.findall(r'gist:\w+', content))
    
    return analysis


def main():
    """Main validation function."""
    print("=" * 70)
    print("TTL/OWL FILE VERIFICATION REPORT")
    print("=" * 70)
    
    # Find all TTL files
    ttl_files = sorted(Path('/Users/nicholasbaro/Python/staged').glob('*.ttl'))
    
    if not ttl_files:
        print("❌ No TTL files found!")
        return 1
    
    print(f"\nFound {len(ttl_files)} TTL files to verify\n")
    
    # Check if rapper is available
    has_rapper = check_rapper_available()
    if has_rapper:
        print("✅ Rapper RDF validator available\n")
    else:
        print("ℹ️  Rapper not available, using basic validation\n")
    
    all_valid = True
    results = []
    
    for file_path in ttl_files:
        print("-" * 70)
        print(f"📄 {file_path.name}")
        print("-" * 70)
        
        # Get file size
        size_kb = file_path.stat().st_size / 1024
        print(f"   Size: {size_kb:.1f} KB")
        
        # Basic validation
        valid, message, stats = validate_ttl_syntax_basic(file_path)
        
        # Advanced validation with rapper if available
        triple_count = 0
        if has_rapper:
            rapper_valid, rapper_msg, triple_count = validate_ttl_with_rapper(file_path)
            if rapper_valid:
                print(f"   ✅ Syntax: Valid (rapper validated)")
                print(f"   📊 Triples: {triple_count:,}")
                valid = True  # Ensure valid is True if rapper validates successfully
            else:
                print(f"   ❌ Rapper: {rapper_msg}")
                valid = False
                all_valid = False
        else:
            if valid:
                print(f"   ✅ Syntax: {message} (basic check)")
            else:
                print(f"   ❌ Syntax: {message}")
                all_valid = False
        
        # Print statistics
        print(f"   📈 Stats:")
        print(f"      Lines: {stats['lines']}")
        print(f"      Prefixes: {stats['prefixes']}")
        print(f"      Classes: {stats['classes']}")
        print(f"      Properties: {stats['properties']}")
        print(f"      Instances: ~{stats['instances']}")
        print(f"      Comments: {stats['comments']}")
        
        # Analyze content
        analysis = analyze_ttl_content(file_path)
        
        # Print analysis
        print(f"   🔍 Analysis:")
        if analysis['uses_gist']:
            print(f"      GIST: ✓ ({analysis['gist_refs']} references)")
        if analysis['uses_prov']:
            print(f"      PROV-O: ✓")
        if analysis['uses_qudt']:
            print(f"      QUDT: ✓")
        if analysis['has_labels']:
            print(f"      Labels: ✓")
        if analysis['has_descriptions']:
            print(f"      Descriptions: ✓")
        
        # Check dependencies
        deps = check_imports_and_dependencies(file_path)
        if deps:
            print(f"   🔗 Dependencies:")
            for dep in deps:
                print(f"      - {dep}")
        
        results.append({
            'file': file_path.name,
            'valid': valid,
            'size_kb': size_kb,
            'stats': stats,
            'triple_count': triple_count
        })
        
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    total_size = sum(r['size_kb'] for r in results)
    total_triples = sum(r['triple_count'] for r in results)
    valid_count = sum(1 for r in results if r['valid'])
    
    print(f"\n📊 Overall Statistics:")
    print(f"   Total files: {len(results)}")
    print(f"   Valid files: {valid_count}/{len(results)}")
    print(f"   Total size: {total_size:.1f} KB")
    if has_rapper and total_triples > 0:
        print(f"   Total triples: {total_triples:,}")
    
    print(f"\n📁 File Summary:")
    for r in results:
        status = "✅" if r['valid'] else "❌"
        print(f"   {status} {r['file']:<40} {r['size_kb']:>8.1f} KB")
        if has_rapper and r['triple_count'] > 0:
            print(f"      └─ {r['triple_count']:,} triples")
    
    # Check specific alignments
    print(f"\n🔍 GIST Alignment Check:")
    gist_align = Path('/Users/nicholasbaro/Python/staged/cmc_stagegate_gist_align.ttl')
    if gist_align.exists():
        content = gist_align.read_text(encoding='utf-8')
        alignments = [
            ('Stage → PlannedEvent', 'ex:Stage.*rdfs:subClassOf.*gist:PlannedEvent'),
            ('StageGate → Event', 'ex:StageGate.*rdfs:subClassOf.*gist:Event'),
            ('Material → PhysicalSubstance ∪ PhysicalIdentifiableItem', 'owl:unionOf.*gist:PhysicalSubstance'),
            ('QualityAttribute → Aspect', 'ex:QualityAttribute.*rdfs:subClassOf.*gist:Aspect'),
            ('AnalyticalResult → Magnitude', 'ex:AnalyticalResult.*rdfs:subClassOf.*gist:Magnitude'),
            ('QUDT bridge', 'qudt:numericValue.*owl:equivalentProperty.*gist:numericValue'),
        ]
        
        for name, pattern in alignments:
            if re.search(pattern, content, re.DOTALL):
                print(f"   ✅ {name}")
            else:
                print(f"   ❌ {name}")
    
    if all_valid:
        print("\n✅ All TTL files are valid!")
    else:
        print("\n⚠️  Some files have validation issues")
    
    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
