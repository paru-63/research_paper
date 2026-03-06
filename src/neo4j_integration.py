import json
from typing import List, Dict

class Neo4jKnowledgeGraph:
    """Generate Neo4j Cypher queries for knowledge graph creation"""
    
    def __init__(self, entities_file: str, relationships_file: str):
        """Initialize with entities and relationships files"""
        with open(entities_file, 'r', encoding='utf-8') as f:
            self.entities_data = json.load(f)
            self.entities = self.entities_data.get('entities', {})
        
        with open(relationships_file, 'r', encoding='utf-8') as f:
            self.relationships_data = json.load(f)
            self.relationships = self.relationships_data.get('relationships', {})
    
    def _escape_cypher_string(self, text: str) -> str:
        """Escape special characters for Cypher queries"""
        if text is None:
            return ''
        return str(text).replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
    
    def generate_constraint_queries(self) -> List[str]:
        """Generate Cypher queries for creating constraints and indexes"""
        queries = [
            # Constraints for uniqueness
            "CREATE CONSTRAINT paper_id IF NOT EXISTS FOR (p:Paper) REQUIRE p.id IS UNIQUE;",
            "CREATE CONSTRAINT author_name IF NOT EXISTS FOR (a:Author) REQUIRE a.name IS UNIQUE;",
            "CREATE CONSTRAINT journal_name IF NOT EXISTS FOR (j:Journal) REQUIRE j.name IS UNIQUE;",
            "CREATE CONSTRAINT keyword_name IF NOT EXISTS FOR (k:Keyword) REQUIRE k.name IS UNIQUE;",
            "CREATE CONSTRAINT domain_name IF NOT EXISTS FOR (d:Domain) REQUIRE d.name IS UNIQUE;",
            "CREATE CONSTRAINT institution_name IF NOT EXISTS FOR (i:Institution) REQUIRE i.name IS UNIQUE;",
            "CREATE CONSTRAINT reference_id IF NOT EXISTS FOR (r:Reference) REQUIRE r.id IS UNIQUE;",
            
            # Indexes for better performance
            "CREATE INDEX paper_year IF NOT EXISTS FOR (p:Paper) ON (p.year);",
            "CREATE INDEX paper_title IF NOT EXISTS FOR (p:Paper) ON (p.title);",
            "CREATE INDEX author_name_idx IF NOT EXISTS FOR (a:Author) ON (a.name);",
        ]
        return queries
    
    def generate_node_creation_queries(self) -> List[str]:
        """Generate Cypher queries for creating nodes"""
        queries = []
        
        # Create Paper nodes
        for paper in self.entities.get('papers', []):
            title = self._escape_cypher_string(paper.get('title', ''))
            doi = self._escape_cypher_string(paper.get('doi', ''))
            year = paper.get('year', 'null')
            
            query = f"""
MERGE (p:Paper {{id: '{paper['id']}'}})
SET p.title = "{title}",
    p.year = {year if year != 'null' else 'null'},
    p.doi = "{doi}";
"""
            queries.append(query.strip())
        
        # Create Author nodes
        for author in self.entities.get('authors', []):
            name = self._escape_cypher_string(author['name'])
            query = f"""
MERGE (a:Author {{name: "{name}"}});
"""
            queries.append(query.strip())
        
        # Create Institution nodes
        for institution in self.entities.get('institutions', []):
            name = self._escape_cypher_string(institution['name'])
            query = f"""
MERGE (i:Institution {{name: "{name}"}});
"""
            queries.append(query.strip())
        
        # Create Journal nodes
        for journal in self.entities.get('journals', []):
            name = self._escape_cypher_string(journal['name'])
            query = f"""
MERGE (j:Journal {{name: "{name}"}});
"""
            queries.append(query.strip())
        
        # Create Keyword nodes
        for keyword in self.entities.get('keywords', []):
            name = self._escape_cypher_string(keyword['name'])
            query = f"""
MERGE (k:Keyword {{name: "{name}"}});
"""
            queries.append(query.strip())
        
        # Create Domain nodes
        for domain in self.entities.get('domains', []):
            name = self._escape_cypher_string(domain['name'])
            query = f"""
MERGE (d:Domain {{name: "{name}"}});
"""
            queries.append(query.strip())
        
        # Create Reference nodes
        for reference in self.entities.get('references', []):
            title = self._escape_cypher_string(reference.get('title', ''))
            link = self._escape_cypher_string(reference.get('link', ''))
            year = reference.get('year', 'null')
            citation_count = reference.get('citation_count', 0)
            
            query = f"""
MERGE (r:Reference {{id: '{reference['id']}'}})
SET r.title = "{title}",
    r.year = {year if year != 'null' else 'null'},
    r.citation_count = {citation_count},
    r.link = "{link}";
"""
            queries.append(query.strip())
        
        return queries
    
    def generate_relationship_creation_queries(self) -> List[str]:
        """Generate Cypher queries for creating relationships"""
        queries = []
        
        # AUTHORED relationships
        for rel in self.relationships.get('AUTHORED', []):
            author_name = self._escape_cypher_string(rel['source'])
            paper_id = rel['target']
            year = rel['properties'].get('year', 'null')
            
            query = f"""
MATCH (a:Author {{name: "{author_name}"}})
MATCH (p:Paper {{id: '{paper_id}'}})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = {year if year != 'null' else 'null'};
"""
            queries.append(query.strip())
        
        # PUBLISHED_IN relationships
        for rel in self.relationships.get('PUBLISHED_IN', []):
            paper_id = rel['source']
            journal_name = self._escape_cypher_string(rel['target'])
            year = rel['properties'].get('year', 'null')
            
            query = f"""
MATCH (p:Paper {{id: '{paper_id}'}})
MATCH (j:Journal {{name: "{journal_name}"}})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = {year if year != 'null' else 'null'};
"""
            queries.append(query.strip())
        
        # HAS_KEYWORD relationships
        for rel in self.relationships.get('HAS_KEYWORD', []):
            paper_id = rel['source']
            keyword_name = self._escape_cypher_string(rel['target'])
            
            query = f"""
MATCH (p:Paper {{id: '{paper_id}'}})
MATCH (k:Keyword {{name: "{keyword_name}"}})
MERGE (p)-[:HAS_KEYWORD]->(k);
"""
            queries.append(query.strip())
        
        # BELONGS_TO_DOMAIN relationships
        for rel in self.relationships.get('BELONGS_TO_DOMAIN', []):
            paper_id = rel['source']
            domain_name = self._escape_cypher_string(rel['target'])
            
            query = f"""
MATCH (p:Paper {{id: '{paper_id}'}})
MATCH (d:Domain {{name: "{domain_name}"}})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);
"""
            queries.append(query.strip())
        
        # AFFILIATED_WITH relationships
        for rel in self.relationships.get('AFFILIATED_WITH', []):
            author_name = self._escape_cypher_string(rel['source'])
            institution_name = self._escape_cypher_string(rel['target'])
            
            query = f"""
MATCH (a:Author {{name: "{author_name}"}})
MATCH (i:Institution {{name: "{institution_name}"}})
MERGE (a)-[:AFFILIATED_WITH]->(i);
"""
            queries.append(query.strip())
        
        # CITES relationships
        for rel in self.relationships.get('CITES', []):
            paper_id = rel['source']
            ref_id = rel['target']
            citation_count = rel['properties'].get('citation_count', 0)
            
            query = f"""
MATCH (p:Paper {{id: '{paper_id}'}})
MATCH (r:Reference {{id: '{ref_id}'}})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = {citation_count};
"""
            queries.append(query.strip())
        
        # SHARES_TOPIC relationships
        for rel in self.relationships.get('SHARES_TOPIC', []):
            paper1_id = rel['source']
            paper2_id = rel['target']
            shared_keyword = self._escape_cypher_string(rel['properties'].get('shared_keyword', ''))
            
            query = f"""
MATCH (p1:Paper {{id: '{paper1_id}'}})
MATCH (p2:Paper {{id: '{paper2_id}'}})
MERGE (p1)-[r:SHARES_TOPIC]-(p2)
SET r.shared_keyword = "{shared_keyword}";
"""
            queries.append(query.strip())
        
        # SHARES_DOMAIN relationships
        for rel in self.relationships.get('SHARES_DOMAIN', []):
            paper1_id = rel['source']
            paper2_id = rel['target']
            shared_domain = self._escape_cypher_string(rel['properties'].get('shared_domain', ''))
            
            query = f"""
MATCH (p1:Paper {{id: '{paper1_id}'}})
MATCH (p2:Paper {{id: '{paper2_id}'}})
MERGE (p1)-[r:SHARES_DOMAIN]-(p2)
SET r.shared_domain = "{shared_domain}";
"""
            queries.append(query.strip())
        
        # COLLABORATED_WITH relationships
        for rel in self.relationships.get('COLLABORATED_WITH', []):
            author1_name = self._escape_cypher_string(rel['source'])
            author2_name = self._escape_cypher_string(rel['target'])
            paper_id = rel['properties'].get('paper_id', '')
            
            query = f"""
MATCH (a1:Author {{name: "{author1_name}"}})
MATCH (a2:Author {{name: "{author2_name}"}})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "{paper_id}";
"""
            queries.append(query.strip())
        
        return queries
    
    def generate_all_queries(self) -> Dict[str, List[str]]:
        """Generate all Cypher queries"""
        return {
            'constraints': self.generate_constraint_queries(),
            'nodes': self.generate_node_creation_queries(),
            'relationships': self.generate_relationship_creation_queries()
        }
    
    def save_cypher_script(self, output_file: str):
        """Save all queries to a Cypher script file"""
        all_queries = self.generate_all_queries()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write("// Knowledge Graph Creation Script for Neo4j\n")
            f.write("// Generated from research paper data\n\n")
            
            # Constraints
            f.write("// ========================================\n")
            f.write("// STEP 1: Create Constraints and Indexes\n")
            f.write("// ========================================\n\n")
            for query in all_queries['constraints']:
                f.write(query + "\n\n")
            
            # Nodes
            f.write("// ========================================\n")
            f.write("// STEP 2: Create Nodes\n")
            f.write("// ========================================\n\n")
            for query in all_queries['nodes']:
                f.write(query + "\n\n")
            
            # Relationships
            f.write("// ========================================\n")
            f.write("// STEP 3: Create Relationships\n")
            f.write("// ========================================\n\n")
            for query in all_queries['relationships']:
                f.write(query + "\n\n")
        
        print(f"✅ Cypher script created successfully!")
        print(f"📊 Statistics:")
        print(f"   Constraint queries: {len(all_queries['constraints'])}")
        print(f"   Node creation queries: {len(all_queries['nodes'])}")
        print(f"   Relationship creation queries: {len(all_queries['relationships'])}")
        print(f"   Total queries: {sum(len(v) for v in all_queries.values())}")
        print(f"\n💾 Saved to: {output_file}")
        print(f"\n🔧 To use this script:")
        print(f"   1. Install Neo4j Desktop or use Neo4j Aura")
        print(f"   2. Create a new database")
        print(f"   3. Open Neo4j Browser")
        print(f"   4. Copy and paste the queries from {output_file}")
        print(f"   5. Or use: cat {output_file} | cypher-shell -u neo4j -p your_password")
    
    def generate_query_examples(self) -> List[Dict[str, str]]:
        """Generate example queries for exploring the graph"""
        examples = [
            {
                'description': 'Find all papers and their authors',
                'query': 'MATCH (a:Author)-[:AUTHORED]->(p:Paper) RETURN a.name, p.title, p.year ORDER BY p.year DESC;'
            },
            {
                'description': 'Find papers on a specific topic (e.g., NLP)',
                'query': 'MATCH (p:Paper)-[:HAS_KEYWORD]->(k:Keyword) WHERE k.name CONTAINS "NLP" RETURN p.title, p.year;'
            },
            {
                'description': 'Find author collaborations',
                'query': 'MATCH (a1:Author)-[:COLLABORATED_WITH]-(a2:Author) RETURN a1.name, a2.name, count(*) as collaborations ORDER BY collaborations DESC;'
            },
            {
                'description': 'Find papers in the same domain',
                'query': 'MATCH (p1:Paper)-[:SHARES_DOMAIN]-(p2:Paper) RETURN p1.title, p2.title, p1.year, p2.year LIMIT 10;'
            },
            {
                'description': 'Find most cited references',
                'query': 'MATCH (r:Reference) RETURN r.title, r.citation_count ORDER BY r.citation_count DESC LIMIT 5;'
            },
            {
                'description': 'Find papers and their keywords',
                'query': 'MATCH (p:Paper)-[:HAS_KEYWORD]->(k:Keyword) RETURN p.title, collect(k.name) as keywords;'
            },
            {
                'description': 'Find authors and their institutions',
                'query': 'MATCH (a:Author)-[:AFFILIATED_WITH]->(i:Institution) RETURN a.name, i.name;'
            },
            {
                'description': 'Find papers published in a specific journal',
                'query': 'MATCH (p:Paper)-[:PUBLISHED_IN]->(j:Journal) WHERE j.name CONTAINS "IEEE" RETURN p.title, p.year;'
            },
            {
                'description': 'Find papers sharing topics',
                'query': 'MATCH (p1:Paper)-[r:SHARES_TOPIC]-(p2:Paper) RETURN p1.title, p2.title, r.shared_keyword LIMIT 10;'
            },
            {
                'description': 'Get graph statistics',
                'query': '''
MATCH (n) 
WITH labels(n) as nodeType, count(*) as count 
RETURN nodeType, count 
ORDER BY count DESC;
'''
            }
        ]
        return examples
    
    def save_query_examples(self, output_file: str):
        """Save example queries to a file"""
        examples = self.generate_query_examples()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("// Example Neo4j Cypher Queries for Knowledge Graph Exploration\n\n")
            
            for i, example in enumerate(examples, 1):
                f.write(f"// {i}. {example['description']}\n")
                f.write(f"{example['query']}\n\n")
        
        print(f"✅ Example queries saved to: {output_file}")


if __name__ == "__main__":
    # Initialize Neo4j knowledge graph generator
    kg = Neo4jKnowledgeGraph(
        entities_file='/home/claude/extracted_entities.json',
        relationships_file='/home/claude/extracted_relationships.json'
    )
    
    # Generate and save Cypher script
    kg.save_cypher_script('/home/claude/neo4j_knowledge_graph.cypher')
    
    # Save example queries
    kg.save_query_examples('/home/claude/neo4j_example_queries.cypher')
