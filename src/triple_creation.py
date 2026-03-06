import json
from typing import List, Tuple, Dict

class TripleCreator:
    """Create RDF-style triples (subject, predicate, object) from extracted data"""
    
    def __init__(self, entities_file: str, relationships_file: str):
        """Initialize with entities and relationships files"""
        with open(entities_file, 'r', encoding='utf-8') as f:
            self.entities_data = json.load(f)
            self.entities = self.entities_data.get('entities', {})
        
        with open(relationships_file, 'r', encoding='utf-8') as f:
            self.relationships_data = json.load(f)
            self.relationships = self.relationships_data.get('relationships', {})
    
    def create_entity_triples(self) -> List[Tuple]:
        """Create triples for entity properties"""
        triples = []
        
        # Paper triples
        for paper in self.entities.get('papers', []):
            paper_id = paper['id']
            triples.append((paper_id, 'rdf:type', 'Paper'))
            triples.append((paper_id, 'has_title', paper.get('title', '')))
            if paper.get('year'):
                triples.append((paper_id, 'published_year', str(paper['year'])))
            if paper.get('doi'):
                triples.append((paper_id, 'has_doi', paper['doi']))
        
        # Author triples
        for author in self.entities.get('authors', []):
            author_name = author['name']
            triples.append((author_name, 'rdf:type', 'Author'))
            triples.append((author_name, 'has_name', author_name))
        
        # Institution triples
        for institution in self.entities.get('institutions', []):
            inst_name = institution['name']
            triples.append((inst_name, 'rdf:type', 'Institution'))
            triples.append((inst_name, 'has_name', inst_name))
        
        # Journal triples
        for journal in self.entities.get('journals', []):
            journal_name = journal['name']
            triples.append((journal_name, 'rdf:type', 'Journal'))
            triples.append((journal_name, 'has_name', journal_name))
        
        # Keyword triples
        for keyword in self.entities.get('keywords', []):
            keyword_name = keyword['name']
            triples.append((keyword_name, 'rdf:type', 'Keyword'))
            triples.append((keyword_name, 'has_name', keyword_name))
        
        # Domain triples
        for domain in self.entities.get('domains', []):
            domain_name = domain['name']
            triples.append((domain_name, 'rdf:type', 'Domain'))
            triples.append((domain_name, 'has_name', domain_name))
        
        # Reference triples
        for reference in self.entities.get('references', []):
            ref_id = reference['id']
            triples.append((ref_id, 'rdf:type', 'Reference'))
            triples.append((ref_id, 'has_title', reference.get('title', '')))
            if reference.get('year'):
                triples.append((ref_id, 'cited_year', str(reference['year'])))
            if reference.get('citation_count'):
                triples.append((ref_id, 'citation_count', str(reference['citation_count'])))
            if reference.get('link'):
                triples.append((ref_id, 'has_link', reference['link']))
        
        return triples
    
    def create_relationship_triples(self) -> List[Tuple]:
        """Create triples from relationships"""
        triples = []
        
        for rel_type, rel_list in self.relationships.items():
            for rel in rel_list:
                # Basic triple
                triples.append((
                    rel['source'],
                    rel['relation'],
                    rel['target']
                ))
                
                # Add property triples if they exist
                if rel.get('properties'):
                    # Create a unique relationship identifier
                    rel_id = f"{rel['source']}_{rel['relation']}_{rel['target']}"
                    for prop_key, prop_value in rel['properties'].items():
                        if prop_value is not None:
                            triples.append((
                                rel_id,
                                f"has_{prop_key}",
                                str(prop_value)
                            ))
        
        return triples
    
    def create_all_triples(self) -> List[Tuple]:
        """Create all triples"""
        entity_triples = self.create_entity_triples()
        relationship_triples = self.create_relationship_triples()
        
        all_triples = entity_triples + relationship_triples
        return all_triples
    
    def save_triples(self, output_file: str, format: str = 'json'):
        """Save triples in specified format"""
        all_triples = self.create_all_triples()
        
        if format == 'json':
            # Save as JSON
            triples_list = []
            for triple in all_triples:
                triples_list.append({
                    'subject': triple[0],
                    'predicate': triple[1],
                    'object': triple[2]
                })
            
            output = {
                'statistics': {
                    'total_triples': len(triples_list),
                    'entity_triples': len(self.create_entity_triples()),
                    'relationship_triples': len(self.create_relationship_triples())
                },
                'triples': triples_list
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
        
        elif format == 'ntriples':
            # Save as N-Triples format (RDF)
            with open(output_file, 'w', encoding='utf-8') as f:
                for triple in all_triples:
                    # Format: <subject> <predicate> "object" .
                    subject = self._format_uri(triple[0])
                    predicate = self._format_uri(triple[1])
                    obj = self._format_literal(triple[2])
                    f.write(f"{subject} {predicate} {obj} .\n")
        
        elif format == 'turtle':
            # Save as Turtle format (RDF)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
                f.write("@prefix ex: <http://example.org/> .\n\n")
                
                for triple in all_triples:
                    subject = self._format_uri_turtle(triple[0])
                    predicate = self._format_uri_turtle(triple[1])
                    obj = self._format_literal_turtle(triple[2])
                    f.write(f"{subject} {predicate} {obj} .\n")
        
        print(f"✅ Triples created successfully!")
        print(f"📊 Statistics:")
        print(f"   Total triples: {len(all_triples)}")
        print(f"   Entity triples: {len(self.create_entity_triples())}")
        print(f"   Relationship triples: {len(self.create_relationship_triples())}")
        print(f"\n💾 Saved to: {output_file} (format: {format})")
        
        return all_triples
    
    def _format_uri(self, text: str) -> str:
        """Format text as URI for N-Triples"""
        # Simple URI formatting
        clean_text = str(text).replace(' ', '_').replace('"', '')
        return f'<http://example.org/{clean_text}>'
    
    def _format_literal(self, text: str) -> str:
        """Format text as literal for N-Triples"""
        # Escape quotes
        clean_text = str(text).replace('\\', '\\\\').replace('"', '\\"')
        return f'"{clean_text}"'
    
    def _format_uri_turtle(self, text: str) -> str:
        """Format text as URI for Turtle"""
        clean_text = str(text).replace(' ', '_').replace('"', '')
        return f'ex:{clean_text}'
    
    def _format_literal_turtle(self, text: str) -> str:
        """Format text as literal for Turtle"""
        clean_text = str(text).replace('\\', '\\\\').replace('"', '\\"')
        return f'"{clean_text}"'
    
    def export_to_csv(self, output_file: str):
        """Export triples to CSV format"""
        import csv
        
        all_triples = self.create_all_triples()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Subject', 'Predicate', 'Object'])
            
            for triple in all_triples:
                writer.writerow([triple[0], triple[1], triple[2]])
        
        print(f"✅ Triples exported to CSV: {output_file}")
        print(f"   Total rows: {len(all_triples)}")


if __name__ == "__main__":
    # Initialize triple creator
    creator = TripleCreator(
        entities_file='/home/claude/extracted_entities.json',
        relationships_file='/home/claude/extracted_relationships.json'
    )
    
    # Save triples in different formats
    creator.save_triples('/home/claude/triples.json', format='json')
    creator.save_triples('/home/claude/triples.nt', format='ntriples')
    creator.save_triples('/home/claude/triples.ttl', format='turtle')
    creator.export_to_csv('/home/claude/triples.csv')
