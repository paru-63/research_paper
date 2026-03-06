"""
Neo4j Aura Database Connector and Populator
This script connects to your Neo4j Aura database and populates it with the knowledge graph

SETUP INSTRUCTIONS:
==================
1. Install the Neo4j driver:
   pip install neo4j

2. Get your Aura password:
   - Go to your Neo4j Aura console (https://console.neo4j.io)
   - Find your instance: b83346a2 (Instance01)
   - Copy your password (if you forgot it, you can generate a new one)

3. Edit this file:
   - Replace "YOUR_AURA_PASSWORD_HERE" on line 378 with your actual password
   - Save the file

4. Run this script:
   python neo4j_connector_aura.py

IMPORTANT NOTES:
===============
- Connection URI: neo4j+s://b83346a2.databases.neo4j.io (already configured)
- Username: neo4j (already configured)
- Password: YOU NEED TO ADD THIS!

The script will:
✅ Connect to your Aura database
✅ Create constraints and indexes
✅ Load all 116 entities (papers, authors, institutions, etc.)
✅ Create 207 relationships
✅ Show statistics when complete
"""

import json
from typing import List, Dict

# Note: To use this script, install the Neo4j driver:
# pip install neo4j

class Neo4jConnector:
    """Connect to Neo4j database and populate with knowledge graph"""
    
    def __init__(self, uri: str = "bolt://localhost:7687", 
                 user: str = "neo4j", 
                 password: str = "password"):
        """
        Initialize Neo4j connection
        
        Args:
            uri: Neo4j connection URI (default: bolt://localhost:7687)
            user: Username (default: neo4j)
            password: Password (default: password)
        """
        try:
            from neo4j import GraphDatabase
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            print(f"✅ Connected to Neo4j at {uri}")
        except ImportError:
            print("❌ Neo4j driver not installed. Install with: pip install neo4j --break-system-packages")
            self.driver = None
        except Exception as e:
            print(f"❌ Failed to connect to Neo4j: {e}")
            print("   Make sure Neo4j is running and credentials are correct")
            self.driver = None
    
    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()
            print("✅ Neo4j connection closed")
    
    def clear_database(self):
        """Clear all nodes and relationships from the database"""
        if not self.driver:
            return
        
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("🗑️  Database cleared")
    
    def create_constraints(self):
        """Create constraints and indexes"""
        if not self.driver:
            return
        
        constraints = [
            "CREATE CONSTRAINT paper_id IF NOT EXISTS FOR (p:Paper) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT author_name IF NOT EXISTS FOR (a:Author) REQUIRE a.name IS UNIQUE",
            "CREATE CONSTRAINT journal_name IF NOT EXISTS FOR (j:Journal) REQUIRE j.name IS UNIQUE",
            "CREATE CONSTRAINT keyword_name IF NOT EXISTS FOR (k:Keyword) REQUIRE k.name IS UNIQUE",
            "CREATE CONSTRAINT domain_name IF NOT EXISTS FOR (d:Domain) REQUIRE d.name IS UNIQUE",
            "CREATE CONSTRAINT institution_name IF NOT EXISTS FOR (i:Institution) REQUIRE i.name IS UNIQUE",
            "CREATE CONSTRAINT reference_id IF NOT EXISTS FOR (r:Reference) REQUIRE r.id IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    # Constraint might already exist
                    pass
        
        print("✅ Constraints created")
    
    def load_entities(self, entities_file: str):
        """Load entities into Neo4j"""
        if not self.driver:
            return
        
        with open(entities_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            entities = data.get('entities', {})
        
        with self.driver.session() as session:
            # Load Papers
            for paper in entities.get('papers', []):
                session.run(
                    """
                    MERGE (p:Paper {id: $id})
                    SET p.title = $title,
                        p.year = $year,
                        p.doi = $doi
                    """,
                    id=paper['id'],
                    title=paper.get('title', ''),
                    year=paper.get('year'),
                    doi=paper.get('doi', '')
                )
            print(f"  ✅ Loaded {len(entities.get('papers', []))} papers")
            
            # Load Authors
            for author in entities.get('authors', []):
                session.run(
                    "MERGE (a:Author {name: $name})",
                    name=author['name']
                )
            print(f"  ✅ Loaded {len(entities.get('authors', []))} authors")
            
            # Load Institutions
            for institution in entities.get('institutions', []):
                session.run(
                    "MERGE (i:Institution {name: $name})",
                    name=institution['name']
                )
            print(f"  ✅ Loaded {len(entities.get('institutions', []))} institutions")
            
            # Load Journals
            for journal in entities.get('journals', []):
                session.run(
                    "MERGE (j:Journal {name: $name})",
                    name=journal['name']
                )
            print(f"  ✅ Loaded {len(entities.get('journals', []))} journals")
            
            # Load Keywords
            for keyword in entities.get('keywords', []):
                session.run(
                    "MERGE (k:Keyword {name: $name})",
                    name=keyword['name']
                )
            print(f"  ✅ Loaded {len(entities.get('keywords', []))} keywords")
            
            # Load Domains
            for domain in entities.get('domains', []):
                session.run(
                    "MERGE (d:Domain {name: $name})",
                    name=domain['name']
                )
            print(f"  ✅ Loaded {len(entities.get('domains', []))} domains")
            
            # Load References
            for reference in entities.get('references', []):
                session.run(
                    """
                    MERGE (r:Reference {id: $id})
                    SET r.title = $title,
                        r.year = $year,
                        r.citation_count = $citation_count,
                        r.link = $link
                    """,
                    id=reference['id'],
                    title=reference.get('title', ''),
                    year=reference.get('year'),
                    citation_count=reference.get('citation_count', 0),
                    link=reference.get('link', '')
                )
            print(f"  ✅ Loaded {len(entities.get('references', []))} references")
    
    def load_relationships(self, relationships_file: str):
        """Load relationships into Neo4j"""
        if not self.driver:
            return
        
        with open(relationships_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            relationships = data.get('relationships', {})
        
        with self.driver.session() as session:
            # AUTHORED relationships
            for rel in relationships.get('AUTHORED', []):
                session.run(
                    """
                    MATCH (a:Author {name: $author_name})
                    MATCH (p:Paper {id: $paper_id})
                    MERGE (a)-[r:AUTHORED]->(p)
                    SET r.year = $year
                    """,
                    author_name=rel['source'],
                    paper_id=rel['target'],
                    year=rel['properties'].get('year')
                )
            print(f"  ✅ Created {len(relationships.get('AUTHORED', []))} AUTHORED relationships")
            
            # PUBLISHED_IN relationships
            for rel in relationships.get('PUBLISHED_IN', []):
                session.run(
                    """
                    MATCH (p:Paper {id: $paper_id})
                    MATCH (j:Journal {name: $journal_name})
                    MERGE (p)-[r:PUBLISHED_IN]->(j)
                    SET r.year = $year
                    """,
                    paper_id=rel['source'],
                    journal_name=rel['target'],
                    year=rel['properties'].get('year')
                )
            print(f"  ✅ Created {len(relationships.get('PUBLISHED_IN', []))} PUBLISHED_IN relationships")
            
            # HAS_KEYWORD relationships
            for rel in relationships.get('HAS_KEYWORD', []):
                session.run(
                    """
                    MATCH (p:Paper {id: $paper_id})
                    MATCH (k:Keyword {name: $keyword_name})
                    MERGE (p)-[:HAS_KEYWORD]->(k)
                    """,
                    paper_id=rel['source'],
                    keyword_name=rel['target']
                )
            print(f"  ✅ Created {len(relationships.get('HAS_KEYWORD', []))} HAS_KEYWORD relationships")
            
            # BELONGS_TO_DOMAIN relationships
            for rel in relationships.get('BELONGS_TO_DOMAIN', []):
                session.run(
                    """
                    MATCH (p:Paper {id: $paper_id})
                    MATCH (d:Domain {name: $domain_name})
                    MERGE (p)-[:BELONGS_TO_DOMAIN]->(d)
                    """,
                    paper_id=rel['source'],
                    domain_name=rel['target']
                )
            print(f"  ✅ Created {len(relationships.get('BELONGS_TO_DOMAIN', []))} BELONGS_TO_DOMAIN relationships")
            
            # AFFILIATED_WITH relationships
            for rel in relationships.get('AFFILIATED_WITH', []):
                session.run(
                    """
                    MATCH (a:Author {name: $author_name})
                    MATCH (i:Institution {name: $institution_name})
                    MERGE (a)-[:AFFILIATED_WITH]->(i)
                    """,
                    author_name=rel['source'],
                    institution_name=rel['target']
                )
            print(f"  ✅ Created {len(relationships.get('AFFILIATED_WITH', []))} AFFILIATED_WITH relationships")
            
            # CITES relationships
            for rel in relationships.get('CITES', []):
                session.run(
                    """
                    MATCH (p:Paper {id: $paper_id})
                    MATCH (r:Reference {id: $ref_id})
                    MERGE (p)-[c:CITES]->(r)
                    SET c.citation_count = $citation_count
                    """,
                    paper_id=rel['source'],
                    ref_id=rel['target'],
                    citation_count=rel['properties'].get('citation_count', 0)
                )
            print(f"  ✅ Created {len(relationships.get('CITES', []))} CITES relationships")
            
            # SHARES_TOPIC relationships
            for rel in relationships.get('SHARES_TOPIC', []):
                session.run(
                    """
                    MATCH (p1:Paper {id: $paper1_id})
                    MATCH (p2:Paper {id: $paper2_id})
                    MERGE (p1)-[r:SHARES_TOPIC]-(p2)
                    SET r.shared_keyword = $shared_keyword
                    """,
                    paper1_id=rel['source'],
                    paper2_id=rel['target'],
                    shared_keyword=rel['properties'].get('shared_keyword', '')
                )
            print(f"  ✅ Created {len(relationships.get('SHARES_TOPIC', []))} SHARES_TOPIC relationships")
            
            # SHARES_DOMAIN relationships
            for rel in relationships.get('SHARES_DOMAIN', []):
                session.run(
                    """
                    MATCH (p1:Paper {id: $paper1_id})
                    MATCH (p2:Paper {id: $paper2_id})
                    MERGE (p1)-[r:SHARES_DOMAIN]-(p2)
                    SET r.shared_domain = $shared_domain
                    """,
                    paper1_id=rel['source'],
                    paper2_id=rel['target'],
                    shared_domain=rel['properties'].get('shared_domain', '')
                )
            print(f"  ✅ Created {len(relationships.get('SHARES_DOMAIN', []))} SHARES_DOMAIN relationships")
            
            # COLLABORATED_WITH relationships
            for rel in relationships.get('COLLABORATED_WITH', []):
                session.run(
                    """
                    MATCH (a1:Author {name: $author1_name})
                    MATCH (a2:Author {name: $author2_name})
                    MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
                    SET r.paper_id = $paper_id
                    """,
                    author1_name=rel['source'],
                    author2_name=rel['target'],
                    paper_id=rel['properties'].get('paper_id', '')
                )
            print(f"  ✅ Created {len(relationships.get('COLLABORATED_WITH', []))} COLLABORATED_WITH relationships")
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        if not self.driver:
            return {}
        
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n)
                WITH labels(n) as nodeType, count(*) as count
                RETURN nodeType, count
                ORDER BY count DESC
                """
            )
            
            stats = {}
            for record in result:
                label = record['nodeType'][0] if record['nodeType'] else 'Unknown'
                stats[label] = record['count']
            
            return stats
    
    def run_example_query(self, query_name: str):
        """Run an example query"""
        if not self.driver:
            return
        
        queries = {
            'papers_by_year': """
                MATCH (p:Paper)
                RETURN p.title, p.year
                ORDER BY p.year DESC
                LIMIT 10
            """,
            'author_collaborations': """
                MATCH (a1:Author)-[:COLLABORATED_WITH]-(a2:Author)
                RETURN a1.name, a2.name
                LIMIT 10
            """,
            'papers_by_domain': """
                MATCH (p:Paper)-[:BELONGS_TO_DOMAIN]->(d:Domain)
                RETURN d.name, count(p) as paper_count
                ORDER BY paper_count DESC
            """,
            'keyword_frequency': """
                MATCH (k:Keyword)<-[:HAS_KEYWORD]-(p:Paper)
                RETURN k.name, count(p) as frequency
                ORDER BY frequency DESC
                LIMIT 10
            """
        }
        
        if query_name not in queries:
            print(f"Query '{query_name}' not found")
            return
        
        with self.driver.session() as session:
            result = session.run(queries[query_name])
            
            print(f"\n📊 Results for '{query_name}':")
            for record in result:
                print(f"   {dict(record)}")


def populate_neo4j_database():
    """Main function to populate Neo4j database"""
    
    print("=" * 80)
    print("  NEO4J DATABASE POPULATION")
    print("=" * 80)
    
    # Connection parameters for Neo4j Aura
    # Your Neo4j Aura Instance: b83346a2 (Instance01)
    URI = "neo4j+s://b83346a2.databases.neo4j.io"
    USER = "neo4j"
    PASSWORD = "_EJDrmhpbF8FSfVZQtVTYa9HkVxZQxZg001bvFXSgJ4"  # ⚠️ IMPORTANT: Replace with your actual Aura password!
    
    # Initialize connector
    connector = Neo4jConnector(URI, USER, PASSWORD)
    
    if not connector.driver:
        print("\n❌ Could not connect to Neo4j. Exiting.")
        return
    
    # Files (using the generated output files)
    entities_file = 'C:\\Users\\nagar\\OneDrive\\Desktop\\Research_Pro\\src\\extracted_entities.json'
    relationships_file = 'C:\\Users\\nagar\\OneDrive\\Desktop\\Research_Pro\\src\\extracted_relationships.json'
    
    try:
        # Option to clear database
        response = input("\n⚠️  Clear existing database? (yes/no): ").lower()
        if response == 'yes':
            connector.clear_database()
        
        # Create constraints
        print("\n📋 Creating constraints...")
        connector.create_constraints()
        
        # Load entities
        print("\n📦 Loading entities...")
        connector.load_entities(entities_file)
        
        # Load relationships
        print("\n🔗 Loading relationships...")
        connector.load_relationships(relationships_file)
        
        # Get statistics
        print("\n📊 Database Statistics:")
        stats = connector.get_statistics()
        for label, count in stats.items():
            print(f"   {label}: {count}")
        
        print("\n✅ Database populated successfully!")
        
        # Run example query
        print("\n🔍 Running example query...")
        connector.run_example_query('papers_by_year')
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        connector.close()


if __name__ == "__main__":
    populate_neo4j_database()