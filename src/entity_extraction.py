import json
import re
from typing import Dict, List, Set

class EntityExtractor:
    """Extract entities from research paper data"""
    
    def __init__(self, metadata_file: str, abstracts_file: str, references_file: str):
        """Initialize with data files"""
        with open(metadata_file, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        with open(abstracts_file, 'r', encoding='utf-8') as f:
            self.abstracts = json.load(f)
            
        with open(references_file, 'r', encoding='utf-8') as f:
            self.references = json.load(f)
    
    def extract_papers(self) -> List[Dict]:
        """Extract paper entities"""
        papers = []
        for paper in self.metadata:
            if paper.get('Paper ID'):
                entity = {
                    'id': paper['Paper ID'],
                    'title': paper.get('Paper title', '').strip(),
                    'year': paper.get('Publication year'),
                    'doi': paper.get('DOI / arXiv ID / PubMed ID', '').strip(),
                    'entity_type': 'Paper'
                }
                papers.append(entity)
        return papers
    
    def extract_authors(self) -> List[Dict]:
        """Extract author entities"""
        authors = []
        seen_authors = set()
        
        for paper in self.metadata:
            if paper.get('Authors'):
                # Split authors by comma
                author_list = [a.strip() for a in paper['Authors'].split(',')]
                
                for author in author_list:
                    if author and author not in seen_authors:
                        # Clean author name
                        author_clean = re.sub(r'^\d+\s*', '', author)  # Remove leading numbers
                        author_clean = author_clean.strip()
                        
                        if author_clean:
                            authors.append({
                                'name': author_clean,
                                'entity_type': 'Author'
                            })
                            seen_authors.add(author)
        
        return authors
    
    def extract_institutions(self) -> List[Dict]:
        """Extract institution entities"""
        institutions = []
        seen_institutions = set()
        
        for paper in self.metadata:
            if paper.get('Author affiliations / institutions'):
                affiliation = paper['Author affiliations / institutions']
                
                # Extract institution names (simplified)
                # Look for University, College, Institute, Department patterns
                patterns = [
                    r'([\w\s]+University[\w\s]*)',
                    r'([\w\s]+College[\w\s]*)',
                    r'([\w\s]+Institute[\w\s]*)',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, affiliation, re.IGNORECASE)
                    for match in matches:
                        inst_clean = match.strip().rstrip(',')
                        if inst_clean and inst_clean not in seen_institutions:
                            institutions.append({
                                'name': inst_clean,
                                'entity_type': 'Institution'
                            })
                            seen_institutions.add(inst_clean)
        
        return institutions
    
    def extract_journals(self) -> List[Dict]:
        """Extract journal/conference entities"""
        journals = []
        seen_journals = set()
        
        for paper in self.metadata:
            journal_name = paper.get('Journal / conference name', '').strip()
            if journal_name and journal_name not in seen_journals:
                journals.append({
                    'name': journal_name,
                    'entity_type': 'Journal'
                })
                seen_journals.add(journal_name)
        
        return journals
    
    def extract_keywords(self) -> List[Dict]:
        """Extract keyword entities"""
        keywords = []
        seen_keywords = set()
        
        for paper in self.metadata:
            if paper.get('Keywords'):
                # Split keywords by comma
                keyword_list = [k.strip() for k in paper['Keywords'].split(',')]
                
                for keyword in keyword_list:
                    if keyword and keyword not in seen_keywords:
                        keywords.append({
                            'name': keyword,
                            'entity_type': 'Keyword'
                        })
                        seen_keywords.add(keyword)
        
        return keywords
    
    def extract_domains(self) -> List[Dict]:
        """Extract domain/research area entities"""
        domains = []
        seen_domains = set()
        
        for paper in self.metadata:
            if paper.get('Domain / research area'):
                # Split domains by comma
                domain_list = [d.strip() for d in paper['Domain / research area'].split(',')]
                
                for domain in domain_list:
                    if domain and domain not in seen_domains:
                        domains.append({
                            'name': domain,
                            'entity_type': 'Domain'
                        })
                        seen_domains.add(domain)
        
        return domains
    
    def extract_references(self) -> List[Dict]:
        """Extract reference entities"""
        refs = []
        for ref in self.references:
            entity = {
                'id': ref.get('Ref_ID'),
                'title': ref.get('Reference Title', '').strip(),
                'year': ref.get('Cited Year'),
                'citation_count': ref.get('Citation Count', 0),
                'link': ref.get('Reference link', '').strip(),
                'entity_type': 'Reference'
            }
            refs.append(entity)
        return refs
    
    def extract_all_entities(self) -> Dict[str, List[Dict]]:
        """Extract all entities and return organized dictionary"""
        entities = {
            'papers': self.extract_papers(),
            'authors': self.extract_authors(),
            'institutions': self.extract_institutions(),
            'journals': self.extract_journals(),
            'keywords': self.extract_keywords(),
            'domains': self.extract_domains(),
            'references': self.extract_references()
        }
        
        return entities
    
    def save_entities(self, output_file: str):
        """Save extracted entities to JSON file"""
        entities = self.extract_all_entities()
        
        # Add statistics
        stats = {
            'total_papers': len(entities['papers']),
            'total_authors': len(entities['authors']),
            'total_institutions': len(entities['institutions']),
            'total_journals': len(entities['journals']),
            'total_keywords': len(entities['keywords']),
            'total_domains': len(entities['domains']),
            'total_references': len(entities['references'])
        }
        
        output = {
            'statistics': stats,
            'entities': entities
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Entities extracted successfully!")
        print(f"📊 Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        print(f"\n💾 Saved to: {output_file}")
        
        return entities


if __name__ == "__main__":
    # Initialize extractor
    extractor = EntityExtractor(
        metadata_file='/mnt/user-data/uploads/metadata.json',
        abstracts_file='/mnt/user-data/uploads/abstracts.json',
        references_file='/mnt/user-data/uploads/reference.json'
    )
    
    # Extract and save entities
    extractor.save_entities('/home/claude/extracted_entities.json')
