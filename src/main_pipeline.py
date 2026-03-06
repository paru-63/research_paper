#!/usr/bin/env python3
"""
Knowledge Graph Builder - Main Pipeline
Orchestrates entity extraction, relationship extraction, triple creation, and Neo4j integration
"""

import os
import sys
from entity_extraction import EntityExtractor
from relationship_extraction import RelationshipExtractor
from triple_creation import TripleCreator
from neo4j_integration import Neo4jKnowledgeGraph

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")

def main():
    """Main pipeline execution"""
    
    print_header("KNOWLEDGE GRAPH BUILDER - PIPELINE")
    
    # File paths
    metadata_file = 'metadata.json'
    abstracts_file = 'abstracts.json'
    references_file = 'reference.json'
    
    # Output files
    entities_output = 'src/extracted_entities.json'
    relationships_output = 'src/extracted_relationships.json'
    triples_json = 'src/triples.json'
    triples_ntriples = 'src/triples.nt'
    triples_turtle = 'src/triples.ttl'
    triples_csv = 'src/triples.csv'
    neo4j_script = 'src/neo4j_knowledge_graph.cypher'
    neo4j_examples = 'src/neo4j_example_queries.cypher'
    
    # Verify input files exist
    print("📁 Verifying input files...")
    for file in [metadata_file, abstracts_file, references_file]:
        if not os.path.exists(file):
            print(f"❌ Error: File not found: {file}")
            sys.exit(1)
    print("✅ All input files found!\n")
    
    # Step 1: Entity Extraction
    print_header("STEP 1: ENTITY EXTRACTION")
    try:
        extractor = EntityExtractor(metadata_file, abstracts_file, references_file)
        entities = extractor.save_entities(entities_output)
        print("\n✅ Entity extraction completed!")
    except Exception as e:
        print(f"❌ Error in entity extraction: {e}")
        sys.exit(1)
    
    # Step 2: Relationship Extraction
    print_header("STEP 2: RELATIONSHIP EXTRACTION")
    try:
        rel_extractor = RelationshipExtractor(metadata_file, abstracts_file, references_file)
        relationships = rel_extractor.save_relationships(relationships_output)
        print("\n✅ Relationship extraction completed!")
    except Exception as e:
        print(f"❌ Error in relationship extraction: {e}")
        sys.exit(1)
    
    # Step 3: Triple Creation
    print_header("STEP 3: TRIPLE CREATION")
    try:
        triple_creator = TripleCreator(entities_output, relationships_output)
        
        # Save in multiple formats
        print("Creating triples in JSON format...")
        triple_creator.save_triples(triples_json, format='json')
        
        print("\nCreating triples in N-Triples format...")
        triple_creator.save_triples(triples_ntriples, format='ntriples')
        
        print("\nCreating triples in Turtle format...")
        triple_creator.save_triples(triples_turtle, format='turtle')
        
        print("\nExporting triples to CSV...")
        triple_creator.export_to_csv(triples_csv)
        
        print("\n✅ Triple creation completed!")
    except Exception as e:
        print(f"❌ Error in triple creation: {e}")
        sys.exit(1)
    
    # Step 4: Neo4j Integration
    print_header("STEP 4: NEO4J INTEGRATION")
    try:
        kg = Neo4jKnowledgeGraph(entities_output, relationships_output)
        
        print("Generating Neo4j Cypher script...")
        kg.save_cypher_script(neo4j_script)
        
        print("\nGenerating example queries...")
        kg.save_query_examples(neo4j_examples)
        
        print("\n✅ Neo4j integration completed!")
    except Exception as e:
        print(f"❌ Error in Neo4j integration: {e}")
        sys.exit(1)
    
    # Summary
    print_header("PIPELINE COMPLETED SUCCESSFULLY!")
    
    print("📊 Generated Files:")
    print(f"   1. Entities: {entities_output}")
    print(f"   2. Relationships: {relationships_output}")
    print(f"   3. Triples (JSON): {triples_json}")
    print(f"   4. Triples (N-Triples): {triples_ntriples}")
    print(f"   5. Triples (Turtle): {triples_turtle}")
    print(f"   6. Triples (CSV): {triples_csv}")
    print(f"   7. Neo4j Script: {neo4j_script}")
    print(f"   8. Neo4j Examples: {neo4j_examples}")
    
    print("\n🚀 Next Steps:")
    print("   1. Install Neo4j: https://neo4j.com/download/")
    print("   2. Create a new database")
    print("   3. Run the Cypher script:")
    print(f"      cat {neo4j_script} | cypher-shell -u neo4j -p your_password")
    print("   4. Explore with example queries:")
    print(f"      {neo4j_examples}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
