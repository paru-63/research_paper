# Research Paper Knowledge Graph

A comprehensive knowledge graph extraction and visualization system for research papers on text summarization and NLP.

## 📊 Overview

This project extracts entities, relationships, and creates triples from research paper metadata to build a knowledge graph that can be visualized in Neo4j.

### Key Statistics

- **Papers**: 9
- **Authors**: 34
- **Institutions**: 10
- **Journals**: 8
- **Keywords**: 34
- **Research Domains**: 12
- **References**: 9
- **Total Relationships**: 207
- **Total Triples**: 801

## 🏗️ Architecture

```
Input Data (JSON/Excel)
        ↓
Entity Extraction
        ↓
Relationship Extraction
        ↓
Triple Creation (RDF)
        ↓
Neo4j Knowledge Graph
```

## 📁 Project Structure

### Scripts

1. **entity_extraction.py** - Extracts entities from research paper data
   - Papers, Authors, Institutions, Journals, Keywords, Domains, References

2. **relationship_extraction.py** - Identifies relationships between entities
   - AUTHORED, PUBLISHED_IN, HAS_KEYWORD, BELONGS_TO_DOMAIN
   - AFFILIATED_WITH, CITES, SHARES_TOPIC, SHARES_DOMAIN
   - COLLABORATED_WITH

3. **triple_creation.py** - Creates RDF-style triples (subject-predicate-object)
   - Outputs: JSON, N-Triples, Turtle, CSV formats

4. **neo4j_integration.py** - Generates Neo4j Cypher queries
   - Creates constraints, nodes, and relationships
   - Provides example queries

5. **neo4j_connector.py** - Python connector for direct Neo4j population
   - Requires: `pip install neo4j --break-system-packages`

6. **main_pipeline.py** - Orchestrates the complete pipeline

### Output Files

#### Entity and Relationship Data
- `extracted_entities.json` - All extracted entities
- `extracted_relationships.json` - All extracted relationships

#### Triples
- `triples.json` - Triples in JSON format
- `triples.nt` - Triples in N-Triples (RDF) format
- `triples.ttl` - Triples in Turtle (RDF) format
- `triples.csv` - Triples in CSV format

#### Neo4j
- `neo4j_knowledge_graph.cypher` - Complete Cypher script
- `neo4j_example_queries.cypher` - Example queries to explore the graph

## 🚀 Quick Start

### Option 1: Run the Complete Pipeline

```bash
python3 main_pipeline.py
```

### Option 2: Run Individual Components

```bash
# Extract entities
python3 entity_extraction.py

# Extract relationships
python3 relationship_extraction.py

# Create triples
python3 triple_creation.py

# Generate Neo4j script
python3 neo4j_integration.py
```

## 🗄️ Neo4j Setup

### Installation

1. **Download Neo4j Desktop**
   - Visit: https://neo4j.com/download/
   - Create a new database

2. **Or use Neo4j Aura (Cloud)**
   - Visit: https://neo4j.com/cloud/aura/

### Populate Database

#### Method 1: Using Cypher Script (Manual)

1. Open Neo4j Browser
2. Copy contents of `neo4j_knowledge_graph.cypher`
3. Paste and execute in Neo4j Browser

#### Method 2: Using Command Line

```bash
cat neo4j_knowledge_graph.cypher | cypher-shell -u neo4j -p your_password
```

#### Method 3: Using Python Connector

```bash
# Install Neo4j driver
pip install neo4j --break-system-packages

# Edit neo4j_connector.py with your credentials
# Then run:
python3 neo4j_connector.py
```

## 📊 Knowledge Graph Schema

### Entity Types (Nodes)

1. **Paper**
   - Properties: id, title, year, doi

2. **Author**
   - Properties: name

3. **Institution**
   - Properties: name

4. **Journal**
   - Properties: name

5. **Keyword**
   - Properties: name

6. **Domain**
   - Properties: name

7. **Reference**
   - Properties: id, title, year, citation_count, link

### Relationship Types (Edges)

1. **AUTHORED**: Author → Paper
   - Properties: year

2. **PUBLISHED_IN**: Paper → Journal
   - Properties: year

3. **HAS_KEYWORD**: Paper → Keyword

4. **BELONGS_TO_DOMAIN**: Paper → Domain

5. **AFFILIATED_WITH**: Author → Institution

6. **CITES**: Paper → Reference
   - Properties: citation_count

7. **SHARES_TOPIC**: Paper ↔ Paper
   - Properties: shared_keyword

8. **SHARES_DOMAIN**: Paper ↔ Paper
   - Properties: shared_domain

9. **COLLABORATED_WITH**: Author ↔ Author
   - Properties: paper_id, year

## 🔍 Example Queries

### Find all papers and their authors

```cypher
MATCH (a:Author)-[:AUTHORED]->(p:Paper)
RETURN a.name, p.title, p.year
ORDER BY p.year DESC;
```

### Find papers on NLP

```cypher
MATCH (p:Paper)-[:HAS_KEYWORD]->(k:Keyword)
WHERE k.name CONTAINS "NLP"
RETURN p.title, p.year;
```

### Find author collaboration network

```cypher
MATCH (a1:Author)-[:COLLABORATED_WITH]-(a2:Author)
RETURN a1.name, a2.name, count(*) as collaborations
ORDER BY collaborations DESC;
```

### Find papers sharing topics

```cypher
MATCH (p1:Paper)-[r:SHARES_TOPIC]-(p2:Paper)
RETURN p1.title, p2.title, r.shared_keyword
LIMIT 10;
```

### Find most cited references

```cypher
MATCH (r:Reference)
RETURN r.title, r.citation_count
ORDER BY r.citation_count DESC
LIMIT 5;
```

### Get graph statistics

```cypher
MATCH (n)
WITH labels(n) as nodeType, count(*) as count
RETURN nodeType, count
ORDER BY count DESC;
```

## 📈 Visualization

The knowledge graph can be visualized using:

1. **Neo4j Browser** (Built-in)
   - Automatically displays graph relationships
   - Interactive exploration

2. **Neo4j Bloom** (Advanced)
   - Natural language search
   - Custom perspectives

3. **Python Libraries**
   - NetworkX + Matplotlib
   - Pyvis
   - Plotly

## 🔧 Advanced Features

### Export Formats

The system supports multiple export formats:
- **JSON**: Standard data interchange
- **N-Triples**: RDF standard format
- **Turtle**: Human-readable RDF
- **CSV**: Spreadsheet compatible

### Custom Queries

Add your own queries to `neo4j_example_queries.cypher`:

```cypher
// Your custom query
MATCH (n:NodeType)
WHERE condition
RETURN n
```

## 📚 Research Domains Covered

- Natural Language Processing (NLP)
- Artificial Intelligence Tools
- Machine Learning
- Text Summarization
- Long Short-Term Memory (LSTM)
- Google Text-to-Speech API
- Automatic Text Summarization

## 🎯 Use Cases

1. **Research Discovery**: Find related papers and authors
2. **Collaboration Analysis**: Identify research networks
3. **Topic Trends**: Track keyword evolution over time
4. **Citation Analysis**: Understand paper impact
5. **Domain Mapping**: Visualize research landscape

## 🛠️ Requirements

### Python Packages

```bash
pip install pandas openpyxl neo4j --break-system-packages
```

### Neo4j

- Neo4j Desktop 5.x or higher
- Or Neo4j Aura (Cloud)

## 📝 Data Sources

The knowledge graph is built from:
- `metadata.json` - Paper metadata
- `abstracts.json` - Paper abstracts
- `reference.json` - Citation data

## 🤝 Contributing

To add more papers:
1. Update metadata.json with new paper information
2. Update abstracts.json with abstracts
3. Update reference.json with citations
4. Run `python3 main_pipeline.py`

## 📄 License

This project is for academic and research purposes.

## 🆘 Support

For issues or questions:
1. Check the example queries in `neo4j_example_queries.cypher`
2. Review Neo4j documentation: https://neo4j.com/docs/
3. Verify your Neo4j connection settings in `neo4j_connector.py`

## 🎓 Citation

If you use this knowledge graph in your research, please cite:
```
Research Paper Knowledge Graph System
https://github.com/your-repo/research-kg
```

---

**Last Updated**: February 2026
**Version**: 1.0
