// Example Neo4j Cypher Queries for Knowledge Graph Exploration

// 1. Find all papers and their authors
MATCH (a:Author)-[:AUTHORED]->(p:Paper) RETURN a.name, p.title, p.year ORDER BY p.year DESC;

// 2. Find papers on a specific topic (e.g., NLP)
MATCH (p:Paper)-[:HAS_KEYWORD]->(k:Keyword) WHERE k.name CONTAINS "NLP" RETURN p.title, p.year;

// 3. Find author collaborations
MATCH (a1:Author)-[:COLLABORATED_WITH]-(a2:Author) RETURN a1.name, a2.name, count(*) as collaborations ORDER BY collaborations DESC;

// 4. Find papers in the same domain
MATCH (p1:Paper)-[:SHARES_DOMAIN]-(p2:Paper) RETURN p1.title, p2.title, p1.year, p2.year LIMIT 10;

// 5. Find most cited references
MATCH (r:Reference) RETURN r.title, r.citation_count ORDER BY r.citation_count DESC LIMIT 5;

// 6. Find papers and their keywords
MATCH (p:Paper)-[:HAS_KEYWORD]->(k:Keyword) RETURN p.title, collect(k.name) as keywords;

// 7. Find authors and their institutions
MATCH (a:Author)-[:AFFILIATED_WITH]->(i:Institution) RETURN a.name, i.name;

// 8. Find papers published in a specific journal
MATCH (p:Paper)-[:PUBLISHED_IN]->(j:Journal) WHERE j.name CONTAINS "IEEE" RETURN p.title, p.year;

// 9. Find papers sharing topics
MATCH (p1:Paper)-[r:SHARES_TOPIC]-(p2:Paper) RETURN p1.title, p2.title, r.shared_keyword LIMIT 10;

// 10. Get graph statistics

MATCH (n) 
WITH labels(n) as nodeType, count(*) as count 
RETURN nodeType, count 
ORDER BY count DESC;


