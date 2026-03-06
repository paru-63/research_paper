import json
import re
from typing import List, Dict, Tuple

class RelationshipExtractor:
    """Extract relationships between entities from research paper data"""
    
    def __init__(self, metadata_file: str, abstracts_file: str, references_file: str):
        """Initialize with data files"""
        with open(metadata_file, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        with open(abstracts_file, 'r', encoding='utf-8') as f:
            self.abstracts = json.load(f)
            
        with open(references_file, 'r', encoding='utf-8') as f:
            self.references = json.load(f)
    
    def extract_authorship_relations(self) -> List[Tuple]:
        """Extract AUTHORED relationships between Authors and Papers"""
        relationships = []
        
        for paper in self.metadata:
            paper_id = paper.get('Paper ID')
            if paper.get('Authors') and paper_id:
                # Split authors
                author_list = [a.strip() for a in paper['Authors'].split(',')]
                
                for author in author_list:
                    # Clean author name
                    author_clean = re.sub(r'^\d+\s*', '', author).strip()
                    
                    if author_clean:
                        relationships.append((
                            author_clean,
                            'AUTHORED',
                            paper_id,
                            {
                                'year': paper.get('Publication year'),
                                'paper_title': paper.get('Paper title', '')
                            }
                        ))
        
        return relationships
    
    def extract_publication_relations(self) -> List[Tuple]:
        """Extract PUBLISHED_IN relationships between Papers and Journals"""
        relationships = []
        
        for paper in self.metadata:
            paper_id = paper.get('Paper ID')
            journal = paper.get('Journal / conference name', '').strip()
            
            if paper_id and journal:
                relationships.append((
                    paper_id,
                    'PUBLISHED_IN',
                    journal,
                    {
                        'year': paper.get('Publication year'),
                        'doi': paper.get('DOI / arXiv ID / PubMed ID', '')
                    }
                ))
        
        return relationships
    
    def extract_keyword_relations(self) -> List[Tuple]:
        """Extract HAS_KEYWORD relationships between Papers and Keywords"""
        relationships = []
        
        for paper in self.metadata:
            paper_id = paper.get('Paper ID')
            if paper.get('Keywords') and paper_id:
                # Split keywords
                keyword_list = [k.strip() for k in paper['Keywords'].split(',')]
                
                for keyword in keyword_list:
                    if keyword:
                        relationships.append((
                            paper_id,
                            'HAS_KEYWORD',
                            keyword,
                            {}
                        ))
        
        return relationships
    
    def extract_domain_relations(self) -> List[Tuple]:
        """Extract BELONGS_TO_DOMAIN relationships between Papers and Domains"""
        relationships = []
        
        for paper in self.metadata:
            paper_id = paper.get('Paper ID')
            if paper.get('Domain / research area') and paper_id:
                # Split domains
                domain_list = [d.strip() for d in paper['Domain / research area'].split(',')]
                
                for domain in domain_list:
                    if domain:
                        relationships.append((
                            paper_id,
                            'BELONGS_TO_DOMAIN',
                            domain,
                            {}
                        ))
        
        return relationships
    
    def extract_affiliation_relations(self) -> List[Tuple]:
        """Extract AFFILIATED_WITH relationships between Authors and Institutions"""
        relationships = []
        
        for paper in self.metadata:
            if paper.get('Authors') and paper.get('Author affiliations / institutions'):
                affiliation = paper['Author affiliations / institutions']
                
                # Extract institution names
                patterns = [
                    r'([\w\s]+University[\w\s]*)',
                    r'([\w\s]+College[\w\s]*)',
                    r'([\w\s]+Institute[\w\s]*)',
                ]
                
                institutions = []
                for pattern in patterns:
                    matches = re.findall(pattern, affiliation, re.IGNORECASE)
                    institutions.extend([m.strip().rstrip(',') for m in matches])
                
                # Get authors
                author_list = [a.strip() for a in paper['Authors'].split(',')]
                
                # Create relationships (simplified: all authors to all institutions in paper)
                for author in author_list:
                    author_clean = re.sub(r'^\d+\s*', '', author).strip()
                    for institution in institutions:
                        if author_clean and institution:
                            relationships.append((
                                author_clean,
                                'AFFILIATED_WITH',
                                institution,
                                {'paper_id': paper.get('Paper ID')}
                            ))
        
        return relationships
    
    def extract_citation_relations(self) -> List[Tuple]:
        """Extract CITES relationships between Papers and References"""
        relationships = []
        
        for ref in self.references:
            paper_id = ref.get('Paper_ID')
            ref_id = ref.get('Ref_ID')
            
            if paper_id and ref_id:
                relationships.append((
                    paper_id,
                    'CITES',
                    ref_id,
                    {
                        'citation_count': ref.get('Citation Count', 0),
                        'cited_year': ref.get('Cited Year')
                    }
                ))
        
        return relationships
    
    def extract_topic_similarity_relations(self) -> List[Tuple]:
        """Extract SHARES_TOPIC relationships between Papers based on common keywords"""
        relationships = []
        
        # Build keyword map: keyword -> list of paper_ids
        keyword_map = {}
        for paper in self.metadata:
            paper_id = paper.get('Paper ID')
            if paper.get('Keywords') and paper_id:
                keyword_list = [k.strip() for k in paper['Keywords'].split(',')]
                for keyword in keyword_list:
                    if keyword:
                        if keyword not in keyword_map:
                            keyword_map[keyword] = []
                        keyword_map[keyword].append(paper_id)
        
        # Create relationships for papers sharing keywords
        seen_pairs = set()
        for keyword, papers in keyword_map.items():
            if len(papers) > 1:
                # Create relationships between all pairs
                for i, paper1 in enumerate(papers):
                    for paper2 in papers[i+1:]:
                        pair = tuple(sorted([paper1, paper2]))
                        if pair not in seen_pairs:
                            relationships.append((
                                paper1,
                                'SHARES_TOPIC',
                                paper2,
                                {'shared_keyword': keyword}
                            ))
                            seen_pairs.add(pair)
        
        return relationships
    
    def extract_domain_similarity_relations(self) -> List[Tuple]:
        """Extract SHARES_DOMAIN relationships between Papers based on common domains"""
        relationships = []
        
        # Build domain map: domain -> list of paper_ids
        domain_map = {}
        for paper in self.metadata:
            paper_id = paper.get('Paper ID')
            if paper.get('Domain / research area') and paper_id:
                domain_list = [d.strip() for d in paper['Domain / research area'].split(',')]
                for domain in domain_list:
                    if domain:
                        if domain not in domain_map:
                            domain_map[domain] = []
                        domain_map[domain].append(paper_id)
        
        # Create relationships for papers sharing domains
        seen_pairs = set()
        for domain, papers in domain_map.items():
            if len(papers) > 1:
                for i, paper1 in enumerate(papers):
                    for paper2 in papers[i+1:]:
                        pair = tuple(sorted([paper1, paper2]))
                        if pair not in seen_pairs:
                            relationships.append((
                                paper1,
                                'SHARES_DOMAIN',
                                paper2,
                                {'shared_domain': domain}
                            ))
                            seen_pairs.add(pair)
        
        return relationships
    
    def extract_collaboration_relations(self) -> List[Tuple]:
        """Extract COLLABORATED_WITH relationships between Authors who co-authored papers"""
        relationships = []
        seen_pairs = set()
        
        for paper in self.metadata:
            if paper.get('Authors'):
                author_list = [re.sub(r'^\d+\s*', '', a.strip()).strip() 
                              for a in paper['Authors'].split(',')]
                author_list = [a for a in author_list if a]
                
                # Create collaboration relationships
                if len(author_list) > 1:
                    for i, author1 in enumerate(author_list):
                        for author2 in author_list[i+1:]:
                            pair = tuple(sorted([author1, author2]))
                            if pair not in seen_pairs:
                                relationships.append((
                                    author1,
                                    'COLLABORATED_WITH',
                                    author2,
                                    {
                                        'paper_id': paper.get('Paper ID'),
                                        'paper_title': paper.get('Paper title', ''),
                                        'year': paper.get('Publication year')
                                    }
                                ))
                                seen_pairs.add(pair)
        
        return relationships
    
    def extract_all_relationships(self) -> Dict[str, List[Tuple]]:
        """Extract all relationships"""
        relationships = {
            'AUTHORED': self.extract_authorship_relations(),
            'PUBLISHED_IN': self.extract_publication_relations(),
            'HAS_KEYWORD': self.extract_keyword_relations(),
            'BELONGS_TO_DOMAIN': self.extract_domain_relations(),
            'AFFILIATED_WITH': self.extract_affiliation_relations(),
            'CITES': self.extract_citation_relations(),
            'SHARES_TOPIC': self.extract_topic_similarity_relations(),
            'SHARES_DOMAIN': self.extract_domain_similarity_relations(),
            'COLLABORATED_WITH': self.extract_collaboration_relations()
        }
        
        return relationships
    
    def save_relationships(self, output_file: str):
        """Save extracted relationships to JSON file"""
        relationships = self.extract_all_relationships()
        
        # Convert tuples to dictionaries for JSON serialization
        output = {}
        stats = {}
        
        for rel_type, rel_list in relationships.items():
            output[rel_type] = []
            for rel in rel_list:
                output[rel_type].append({
                    'source': rel[0],
                    'relation': rel[1],
                    'target': rel[2],
                    'properties': rel[3] if len(rel) > 3 else {}
                })
            stats[rel_type] = len(rel_list)
        
        result = {
            'statistics': stats,
            'total_relationships': sum(stats.values()),
            'relationships': output
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Relationships extracted successfully!")
        print(f"📊 Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        print(f"   TOTAL: {sum(stats.values())}")
        print(f"\n💾 Saved to: {output_file}")
        
        return relationships


if __name__ == "__main__":
    # Initialize extractor
    extractor = RelationshipExtractor(
        metadata_file='/mnt/user-data/uploads/metadata.json',
        abstracts_file='/mnt/user-data/uploads/abstracts.json',
        references_file='/mnt/user-data/uploads/reference.json'
    )
    
    # Extract and save relationships
    extractor.save_relationships('/home/claude/extracted_relationships.json')
