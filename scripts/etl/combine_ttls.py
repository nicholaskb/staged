#!/usr/bin/env python3
"""
Combine multiple TTL files into a single comprehensive file.
Consolidates base ontology, extensions, instances, and alignments.
"""

from pathlib import Path

# Default files to combine - now in organized location
DEFAULT_FILES = [
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_base.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_drug_products.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_modalities.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_temporal.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_lexicon.ttl",
    "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_instances.ttl",
    "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_sme_instances.ttl",
    "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_lexicon_instances.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/example_drug_instances.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/example_temporal_tracking.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_gist_align.ttl",
]
# Combined output goes to output/current/
DEFAULT_OUTPUT = "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_all.ttl"

def combine_ttl_files(input_files=DEFAULT_FILES, output_file=DEFAULT_OUTPUT):
    """
    Combine multiple TTL files into one.
    
    Args:
        input_files: List of TTL file paths to combine
        output_file: Output file path for combined TTL
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Track prefixes and triples
    all_prefixes = {}
    all_triples = []
    
    for file_path in input_files:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping...")
            continue
            
        print(f"Processing: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Split into prefixes and triples
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('@prefix'):
                    # Extract prefix
                    parts = line.split()
                    if len(parts) >= 3:
                        prefix_name = parts[1]
                        prefix_uri = ' '.join(parts[2:])
                        all_prefixes[prefix_name] = prefix_uri
                elif line and not line.startswith('#'):
                    # It's a triple (not a comment or empty)
                    all_triples.append(line)
    
    # Write combined file
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write prefixes first
        for prefix_name, prefix_uri in sorted(all_prefixes.items()):
            f.write(f"@prefix {prefix_name} {prefix_uri}\n")
        
        f.write("\n")
        
        # Write all triples
        f.write('\n'.join(all_triples))
    
    print(f"\n✅ Combined {len(input_files)} files into {output_path}")
    print(f"   Total prefixes: {len(all_prefixes)}")
    print(f"   Total lines: {len(all_triples)}")

if __name__ == "__main__":
    combine_ttl_files()
