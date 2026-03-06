// Knowledge Graph Creation Script for Neo4j
// Generated from research paper data

// ========================================
// STEP 1: Create Constraints and Indexes
// ========================================

CREATE CONSTRAINT paper_id IF NOT EXISTS FOR (p:Paper) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT author_name IF NOT EXISTS FOR (a:Author) REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT journal_name IF NOT EXISTS FOR (j:Journal) REQUIRE j.name IS UNIQUE;

CREATE CONSTRAINT keyword_name IF NOT EXISTS FOR (k:Keyword) REQUIRE k.name IS UNIQUE;

CREATE CONSTRAINT domain_name IF NOT EXISTS FOR (d:Domain) REQUIRE d.name IS UNIQUE;

CREATE CONSTRAINT institution_name IF NOT EXISTS FOR (i:Institution) REQUIRE i.name IS UNIQUE;

CREATE CONSTRAINT reference_id IF NOT EXISTS FOR (r:Reference) REQUIRE r.id IS UNIQUE;

CREATE INDEX paper_year IF NOT EXISTS FOR (p:Paper) ON (p.year);

CREATE INDEX paper_title IF NOT EXISTS FOR (p:Paper) ON (p.title);

CREATE INDEX author_name_idx IF NOT EXISTS FOR (a:Author) ON (a.name);

// ========================================
// STEP 2: Create Nodes
// ========================================

MERGE (p:Paper {id: 'P01'})
SET p.title = "Revolutionizing Research Writing and Publishing by using AI-Powered Tools and Technique",
    p.year = 2024,
    p.doi = "10.1109/ACCESS.2025.3536205";

MERGE (p:Paper {id: 'P02'})
SET p.title = "SmartNews: AI-Powered News Summarize",
    p.year = 2025,
    p.doi = "ISSN: 2319-2526";

MERGE (p:Paper {id: 'P03'})
SET p.title = "Automatic Text Summarization Methods: A Comprehensive Review",
    p.year = 2024,
    p.doi = "10.1109/TCC.2025.3612322";

MERGE (p:Paper {id: 'P04'})
SET p.title = "Automatic text summarization of scientific articles using transformers",
    p.year = 2024,
    p.doi = "10.32629/jai.v7i5.1331";

MERGE (p:Paper {id: 'P05'})
SET p.title = "Text Summarization Using Natural Language Processing",
    p.year = 2024,
    p.doi = "ISSN: 2320-2882";

MERGE (p:Paper {id: 'P06'})
SET p.title = "TEXT SUMMARIZATION USING NATURAL LANGUAGE PROCESSING AND GOOGLE TEXT TO SPEECH API",
    p.year = 2020,
    p.doi = "e-ISSN: 2395-0056";

MERGE (p:Paper {id: 'P07'})
SET p.title = "A Survey of Text Summarization Using NLP",
    p.year = 2025,
    p.doi = "ISSN:2455-1058";

MERGE (p:Paper {id: 'P08'})
SET p.title = "A Survey of Automatic Text Summarization",
    p.year = 2014,
    p.doi = "ISSN: 2278-0181";

MERGE (p:Paper {id: 'P09'})
SET p.title = "Research Paper Summarizer Using AI",
    p.year = 2024,
    p.doi = "e ISSN: 2584-2854";

MERGE (a:Author {name: "Mandira Bairagi"});

MERGE (a:Author {name: "Dr. Shalini R. Lihitkar"});

MERGE (a:Author {name: "Mrs. Abha Pathak"});

MERGE (a:Author {name: "Trupti Pawar"});

MERGE (a:Author {name: "Yogeshwari Pawar"});

MERGE (a:Author {name: "Shreya pawar"});

MERGE (a:Author {name: "Divakar Yadav"});

MERGE (a:Author {name: "Jalpa Desai"});

MERGE (a:Author {name: "Arun Kumar Yadav"});

MERGE (a:Author {name: "Seema Aswani"});

MERGE (a:Author {name: "Kabita Choudhary"});

MERGE (a:Author {name: "Sujala Shetty"});

MERGE (a:Author {name: "Nasheen Nur"});

MERGE (a:Author {name: "Sanjivani Chandrashekhar Kachare"});

MERGE (a:Author {name: "Manali Udaykumar Sawant"});

MERGE (a:Author {name: "Manasi Suresh Yadav"});

MERGE (a:Author {name: "Ms. Priyanka Rajendra Jadhav"});

MERGE (a:Author {name: "SUBASH VOLETI"});

MERGE (a:Author {name: "CHAITAN RAJU"});

MERGE (a:Author {name: "TEJA RANI"});

MERGE (a:Author {name: "MUGADA SWETHA"});

MERGE (a:Author {name: "Bhuvan Shingade"});

MERGE (a:Author {name: "Yash Matha"});

MERGE (a:Author {name: "Ved Kolambkar"});

MERGE (a:Author {name: "Suyash Kasar"});

MERGE (a:Author {name: "Prof. Rohini Palve"});

MERGE (a:Author {name: "Niharika Verma"});

MERGE (a:Author {name: "Prof. Ashish Tiwari"});

MERGE (a:Author {name: "G. Santhoshi"});

MERGE (a:Author {name: "M Jyothi"});

MERGE (a:Author {name: "Kovvuri Ramya Sri"});

MERGE (a:Author {name: "G. Hasika"});

MERGE (a:Author {name: "G. Varsha"});

MERGE (a:Author {name: "R. Snigdha"});

MERGE (i:Institution {name: "Rashtrasant Tukadoji Maharaj Nagpur University"});

MERGE (i:Institution {name: "Patil College of Engineering and Innovation"});

MERGE (i:Institution {name: "Birla Institute of Technology and Science"});

MERGE (i:Institution {name: "Florida Institute of Technology"});

MERGE (i:Institution {name: "LENDI INSTITUTE OF ENGINEERING AND TECHNOLOGY"});

MERGE (i:Institution {name: "Terna Engineering College"});

MERGE (i:Institution {name: "Rajiv Gandhi Technical University Airport Road"});

MERGE (i:Institution {name: "2 Vindhya Institute of Technology and Science Umrikheda"});

MERGE (i:Institution {name: "Narayanamma Institute of Technology and  Science for Women"});

MERGE (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"});

MERGE (j:Journal {name: "IEEE Access"});

MERGE (j:Journal {name: "International Journal on Advanced Computer Theory and Engineering"});

MERGE (j:Journal {name: "Journal of Autonomous Intelligence"});

MERGE (j:Journal {name: "IJCRT"});

MERGE (j:Journal {name: "International Research Journal of Engineering and Technology (IRJET)"});

MERGE (j:Journal {name: "SIRJANA JOURNAL"});

MERGE (j:Journal {name: "International Journal of Engineering Research & Technology (IJERT)"});

MERGE (j:Journal {name: "International Research Journal on Advanced Engineering and Management"});

MERGE (k:Keyword {name: "Artificial intelligence"});

MERGE (k:Keyword {name: "Artificial Intelligence Tools"});

MERGE (k:Keyword {name: "Research communication"});

MERGE (k:Keyword {name: "Scholarly publication"});

MERGE (k:Keyword {name: "NLP"});

MERGE (k:Keyword {name: "evaluate summarization models using Python"});

MERGE (k:Keyword {name: "Automatic text summarization"});

MERGE (k:Keyword {name: "Natural Language Processing"});

MERGE (k:Keyword {name: "Categorization of text summarization  system"});

MERGE (k:Keyword {name: "natural language processing; long document summarization; transformers; multi-headed attention; scientific article summarization"});

MERGE (k:Keyword {name: "Text Summarization"});

MERGE (k:Keyword {name: "Text Rank"});

MERGE (k:Keyword {name: "OCR"});

MERGE (k:Keyword {name: "Open AI"});

MERGE (k:Keyword {name: "Text Rank Algorithm"});

MERGE (k:Keyword {name: "NLTK"});

MERGE (k:Keyword {name: "GTTS(Google Text To Speech) API"});

MERGE (k:Keyword {name: "Extractive Text Summarization"});

MERGE (k:Keyword {name: "Machine Learning"});

MERGE (k:Keyword {name: "Natural Language Processing(NLP)"});

MERGE (k:Keyword {name: "Long term short memory(LSTM)"});

MERGE (k:Keyword {name: "Abstractive Summarization"});

MERGE (k:Keyword {name: "Extractive Summarization."});

MERGE (k:Keyword {name: "abstraction-predicated summary"});

MERGE (k:Keyword {name: "automatic text summarization"});

MERGE (k:Keyword {name: "extraction summary"});

MERGE (k:Keyword {name: "feature extraction"});

MERGE (k:Keyword {name: "text reduction."});

MERGE (k:Keyword {name: "Natural Language Processing (NLP)"});

MERGE (k:Keyword {name: "Highlighting Keywords"});

MERGE (k:Keyword {name: "Read Aloud"});

MERGE (k:Keyword {name: "Plagiarism"});

MERGE (k:Keyword {name: "Images"});

MERGE (k:Keyword {name: "Research."});

MERGE (d:Domain {name: "Artificial Intelligence Tools"});

MERGE (d:Domain {name: "Natural Language Processing (NLP)"});

MERGE (d:Domain {name: "NLP"});

MERGE (d:Domain {name: "Natural Language Processing"});

MERGE (d:Domain {name: "CNN"});

MERGE (d:Domain {name: "Open AI"});

MERGE (d:Domain {name: "GTTS(Google Text To Speech) API"});

MERGE (d:Domain {name: "Machine Learning"});

MERGE (d:Domain {name: "Long term short memory(LSTM)"});

MERGE (d:Domain {name: "Natural Language Processing(NLP)"});

MERGE (d:Domain {name: "Automatic Text Summarization"});

MERGE (d:Domain {name: "Natural Language Toolkit (NLTK)"});

MERGE (r:Reference {id: 'R001'})
SET r.title = "Revolutionizing Research Writing and Publishing by using AI-Powered Tools and Techniques",
    r.year = 2023,
    r.citation_count = 8,
    r.link = "https://doi.org/10.1108/ejim-02-2023-0156";

MERGE (r:Reference {id: 'R002'})
SET r.title = "SmartNews: AI-Powered News Summarizer",
    r.year = 2025,
    r.citation_count = 0,
    r.link = "https://journals.mriindia.com";

MERGE (r:Reference {id: 'R003'})
SET r.title = "Automatic Text Summarization Methods: A Comprehensive Review",
    r.year = 2023,
    r.citation_count = 25,
    r.link = "https://orcid.org/0000-0001-6051-479X";

MERGE (r:Reference {id: 'R004'})
SET r.title = "Automatic text summarization of scientific articles using transformers-A brief review",
    r.year = 2024,
    r.citation_count = 2,
    r.link = "https://doi.org/10.32629/jai.v7i5.1331";

MERGE (r:Reference {id: 'R005'})
SET r.title = "Text Summarization Using Natural Language Processing",
    r.year = 2024,
    r.citation_count = 3,
    r.link = "https://www.ijcrt.org";

MERGE (r:Reference {id: 'R006'})
SET r.title = "TEXT SUMMARIZATION USING NATURAL LANGUAGE PROCESSING AND GOOGLE TEXT TO SPEECH API",
    r.year = 2020,
    r.citation_count = 10,
    r.link = "https://www.irjet.net";

MERGE (r:Reference {id: 'R007'})
SET r.title = "A Survey of Text Summarization Using NLP",
    r.year = 2023,
    r.citation_count = 2,
    r.link = "https://sirjana.in";

MERGE (r:Reference {id: 'R008'})
SET r.title = "A Survey of Automatic Text Summarization",
    r.year = 2014,
    r.citation_count = 15,
    r.link = "https://www.irjet.net";

MERGE (r:Reference {id: 'R009'})
SET r.title = "Research Paper Summarizer Using AI",
    r.year = 2024,
    r.citation_count = 1,
    r.link = "https://doi.org/10.47392/IRJAEM.2024.0374";

// ========================================
// STEP 3: Create Relationships
// ========================================

MATCH (a:Author {name: "Mandira Bairagi"})
MATCH (p:Paper {id: 'P01'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Dr. Shalini R. Lihitkar"})
MATCH (p:Paper {id: 'P01'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Mrs. Abha Pathak"})
MATCH (p:Paper {id: 'P02'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2025;

MATCH (a:Author {name: "Trupti Pawar"})
MATCH (p:Paper {id: 'P02'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2025;

MATCH (a:Author {name: "Yogeshwari Pawar"})
MATCH (p:Paper {id: 'P02'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2025;

MATCH (a:Author {name: "Shreya pawar"})
MATCH (p:Paper {id: 'P02'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2025;

MATCH (a:Author {name: "Divakar Yadav"})
MATCH (p:Paper {id: 'P03'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Jalpa Desai"})
MATCH (p:Paper {id: 'P03'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Arun Kumar Yadav"})
MATCH (p:Paper {id: 'P03'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Seema Aswani"})
MATCH (p:Paper {id: 'P04'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Kabita Choudhary"})
MATCH (p:Paper {id: 'P04'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Sujala Shetty"})
MATCH (p:Paper {id: 'P04'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Nasheen Nur"})
MATCH (p:Paper {id: 'P04'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Sanjivani Chandrashekhar Kachare"})
MATCH (p:Paper {id: 'P05'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Manali Udaykumar Sawant"})
MATCH (p:Paper {id: 'P05'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Manasi Suresh Yadav"})
MATCH (p:Paper {id: 'P05'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Ms. Priyanka Rajendra Jadhav"})
MATCH (p:Paper {id: 'P05'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "SUBASH VOLETI"})
MATCH (p:Paper {id: 'P06'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2020;

MATCH (a:Author {name: "CHAITAN RAJU"})
MATCH (p:Paper {id: 'P06'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2020;

MATCH (a:Author {name: "TEJA RANI"})
MATCH (p:Paper {id: 'P06'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2020;

MATCH (a:Author {name: "MUGADA SWETHA"})
MATCH (p:Paper {id: 'P06'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2020;

MATCH (a:Author {name: "Bhuvan Shingade"})
MATCH (p:Paper {id: 'P07'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2025;

MATCH (a:Author {name: "Yash Matha"})
MATCH (p:Paper {id: 'P07'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2025;

MATCH (a:Author {name: "Ved Kolambkar"})
MATCH (p:Paper {id: 'P07'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2025;

MATCH (a:Author {name: "Suyash Kasar"})
MATCH (p:Paper {id: 'P07'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2025;

MATCH (a:Author {name: "Prof. Rohini Palve"})
MATCH (p:Paper {id: 'P07'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2025;

MATCH (a:Author {name: "Niharika Verma"})
MATCH (p:Paper {id: 'P08'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2014;

MATCH (a:Author {name: "Prof. Ashish Tiwari"})
MATCH (p:Paper {id: 'P08'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2014;

MATCH (a:Author {name: "G. Santhoshi"})
MATCH (p:Paper {id: 'P09'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "M Jyothi"})
MATCH (p:Paper {id: 'P09'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "Kovvuri Ramya Sri"})
MATCH (p:Paper {id: 'P09'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "G. Hasika"})
MATCH (p:Paper {id: 'P09'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "G. Varsha"})
MATCH (p:Paper {id: 'P09'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (a:Author {name: "R. Snigdha"})
MATCH (p:Paper {id: 'P09'})
MERGE (a)-[r:AUTHORED]->(p)
SET r.year = 2024;

MATCH (p:Paper {id: 'P01'})
MATCH (j:Journal {name: "IEEE Access"})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = 2024;

MATCH (p:Paper {id: 'P02'})
MATCH (j:Journal {name: "International Journal on Advanced Computer Theory and Engineering"})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = 2025;

MATCH (p:Paper {id: 'P03'})
MATCH (j:Journal {name: "IEEE Access"})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = 2024;

MATCH (p:Paper {id: 'P04'})
MATCH (j:Journal {name: "Journal of Autonomous Intelligence"})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = 2024;

MATCH (p:Paper {id: 'P05'})
MATCH (j:Journal {name: "IJCRT"})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = 2024;

MATCH (p:Paper {id: 'P06'})
MATCH (j:Journal {name: "International Research Journal of Engineering and Technology (IRJET)"})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = 2020;

MATCH (p:Paper {id: 'P07'})
MATCH (j:Journal {name: "SIRJANA JOURNAL"})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = 2025;

MATCH (p:Paper {id: 'P08'})
MATCH (j:Journal {name: "International Journal of Engineering Research & Technology (IJERT)"})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = 2014;

MATCH (p:Paper {id: 'P09'})
MATCH (j:Journal {name: "International Research Journal on Advanced Engineering and Management"})
MERGE (p)-[r:PUBLISHED_IN]->(j)
SET r.year = 2024;

MATCH (p:Paper {id: 'P01'})
MATCH (k:Keyword {name: "Artificial intelligence"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P01'})
MATCH (k:Keyword {name: "Artificial Intelligence Tools"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P01'})
MATCH (k:Keyword {name: "Research communication"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P01'})
MATCH (k:Keyword {name: "Scholarly publication"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P02'})
MATCH (k:Keyword {name: "NLP"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P02'})
MATCH (k:Keyword {name: "evaluate summarization models using Python"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P03'})
MATCH (k:Keyword {name: "Automatic text summarization"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P03'})
MATCH (k:Keyword {name: "Natural Language Processing"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P03'})
MATCH (k:Keyword {name: "Categorization of text summarization  system"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P04'})
MATCH (k:Keyword {name: "natural language processing; long document summarization; transformers; multi-headed attention; scientific article summarization"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P05'})
MATCH (k:Keyword {name: "NLP"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P05'})
MATCH (k:Keyword {name: "Text Summarization"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P05'})
MATCH (k:Keyword {name: "Text Rank"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P05'})
MATCH (k:Keyword {name: "OCR"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P05'})
MATCH (k:Keyword {name: "Open AI"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P06'})
MATCH (k:Keyword {name: "Text Summarization"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P06'})
MATCH (k:Keyword {name: "Text Rank Algorithm"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P06'})
MATCH (k:Keyword {name: "NLTK"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P06'})
MATCH (k:Keyword {name: "GTTS(Google Text To Speech) API"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P06'})
MATCH (k:Keyword {name: "Extractive Text Summarization"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P07'})
MATCH (k:Keyword {name: "Machine Learning"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P07'})
MATCH (k:Keyword {name: "Natural Language Processing(NLP)"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P07'})
MATCH (k:Keyword {name: "Long term short memory(LSTM)"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P07'})
MATCH (k:Keyword {name: "Abstractive Summarization"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P07'})
MATCH (k:Keyword {name: "Extractive Summarization."})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P08'})
MATCH (k:Keyword {name: "abstraction-predicated summary"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P08'})
MATCH (k:Keyword {name: "automatic text summarization"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P08'})
MATCH (k:Keyword {name: "extraction summary"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P08'})
MATCH (k:Keyword {name: "feature extraction"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P08'})
MATCH (k:Keyword {name: "text reduction."})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P09'})
MATCH (k:Keyword {name: "Natural Language Processing (NLP)"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P09'})
MATCH (k:Keyword {name: "Highlighting Keywords"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P09'})
MATCH (k:Keyword {name: "Read Aloud"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P09'})
MATCH (k:Keyword {name: "Plagiarism"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P09'})
MATCH (k:Keyword {name: "Images"})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P09'})
MATCH (k:Keyword {name: "Research."})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (p:Paper {id: 'P01'})
MATCH (d:Domain {name: "Artificial Intelligence Tools"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P02'})
MATCH (d:Domain {name: "Natural Language Processing (NLP)"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P03'})
MATCH (d:Domain {name: "NLP"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P04'})
MATCH (d:Domain {name: "Natural Language Processing"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P04'})
MATCH (d:Domain {name: "CNN"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P05'})
MATCH (d:Domain {name: "NLP"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P05'})
MATCH (d:Domain {name: "Open AI"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P06'})
MATCH (d:Domain {name: "GTTS(Google Text To Speech) API"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P07'})
MATCH (d:Domain {name: "Machine Learning"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P07'})
MATCH (d:Domain {name: "Long term short memory(LSTM)"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P07'})
MATCH (d:Domain {name: "Natural Language Processing(NLP)"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P08'})
MATCH (d:Domain {name: "Automatic Text Summarization"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (p:Paper {id: 'P09'})
MATCH (d:Domain {name: "Natural Language Toolkit (NLTK)"})
MERGE (p)-[:BELONGS_TO_DOMAIN]->(d);

MATCH (a:Author {name: "Mandira Bairagi"})
MATCH (i:Institution {name: "Rashtrasant Tukadoji Maharaj Nagpur University"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Dr. Shalini R. Lihitkar"})
MATCH (i:Institution {name: "Rashtrasant Tukadoji Maharaj Nagpur University"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Mrs. Abha Pathak"})
MATCH (i:Institution {name: "Patil College of Engineering and Innovation"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Mrs. Abha Pathak"})
MATCH (i:Institution {name: "Patil College of Engineering and Innovation"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Trupti Pawar"})
MATCH (i:Institution {name: "Patil College of Engineering and Innovation"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Trupti Pawar"})
MATCH (i:Institution {name: "Patil College of Engineering and Innovation"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Yogeshwari Pawar"})
MATCH (i:Institution {name: "Patil College of Engineering and Innovation"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Yogeshwari Pawar"})
MATCH (i:Institution {name: "Patil College of Engineering and Innovation"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Shreya pawar"})
MATCH (i:Institution {name: "Patil College of Engineering and Innovation"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Shreya pawar"})
MATCH (i:Institution {name: "Patil College of Engineering and Innovation"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Seema Aswani"})
MATCH (i:Institution {name: "Birla Institute of Technology and Science"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Seema Aswani"})
MATCH (i:Institution {name: "Florida Institute of Technology"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Kabita Choudhary"})
MATCH (i:Institution {name: "Birla Institute of Technology and Science"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Kabita Choudhary"})
MATCH (i:Institution {name: "Florida Institute of Technology"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Sujala Shetty"})
MATCH (i:Institution {name: "Birla Institute of Technology and Science"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Sujala Shetty"})
MATCH (i:Institution {name: "Florida Institute of Technology"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Nasheen Nur"})
MATCH (i:Institution {name: "Birla Institute of Technology and Science"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Nasheen Nur"})
MATCH (i:Institution {name: "Florida Institute of Technology"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "SUBASH VOLETI"})
MATCH (i:Institution {name: "LENDI INSTITUTE OF ENGINEERING AND TECHNOLOGY"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "CHAITAN RAJU"})
MATCH (i:Institution {name: "LENDI INSTITUTE OF ENGINEERING AND TECHNOLOGY"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "TEJA RANI"})
MATCH (i:Institution {name: "LENDI INSTITUTE OF ENGINEERING AND TECHNOLOGY"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "MUGADA SWETHA"})
MATCH (i:Institution {name: "LENDI INSTITUTE OF ENGINEERING AND TECHNOLOGY"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Bhuvan Shingade"})
MATCH (i:Institution {name: "Terna Engineering College"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Yash Matha"})
MATCH (i:Institution {name: "Terna Engineering College"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Ved Kolambkar"})
MATCH (i:Institution {name: "Terna Engineering College"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Suyash Kasar"})
MATCH (i:Institution {name: "Terna Engineering College"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Prof. Rohini Palve"})
MATCH (i:Institution {name: "Terna Engineering College"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Niharika Verma"})
MATCH (i:Institution {name: "Rajiv Gandhi Technical University Airport Road"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Niharika Verma"})
MATCH (i:Institution {name: "2 Vindhya Institute of Technology and Science Umrikheda"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Prof. Ashish Tiwari"})
MATCH (i:Institution {name: "Rajiv Gandhi Technical University Airport Road"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Prof. Ashish Tiwari"})
MATCH (i:Institution {name: "2 Vindhya Institute of Technology and Science Umrikheda"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "G. Santhoshi"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and  Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "G. Santhoshi"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "G. Santhoshi"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "M Jyothi"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and  Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "M Jyothi"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "M Jyothi"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Kovvuri Ramya Sri"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and  Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Kovvuri Ramya Sri"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "Kovvuri Ramya Sri"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "G. Hasika"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and  Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "G. Hasika"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "G. Hasika"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "G. Varsha"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and  Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "G. Varsha"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "G. Varsha"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "R. Snigdha"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and  Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "R. Snigdha"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (a:Author {name: "R. Snigdha"})
MATCH (i:Institution {name: "Narayanamma Institute of Technology and Science for Women"})
MERGE (a)-[:AFFILIATED_WITH]->(i);

MATCH (p:Paper {id: 'P01'})
MATCH (r:Reference {id: 'R001'})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = 8;

MATCH (p:Paper {id: 'P02'})
MATCH (r:Reference {id: 'R002'})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = 0;

MATCH (p:Paper {id: 'P03'})
MATCH (r:Reference {id: 'R003'})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = 25;

MATCH (p:Paper {id: 'P04'})
MATCH (r:Reference {id: 'R004'})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = 2;

MATCH (p:Paper {id: 'P05'})
MATCH (r:Reference {id: 'R005'})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = 3;

MATCH (p:Paper {id: 'P06'})
MATCH (r:Reference {id: 'R006'})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = 10;

MATCH (p:Paper {id: 'P07'})
MATCH (r:Reference {id: 'R007'})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = 2;

MATCH (p:Paper {id: 'P08'})
MATCH (r:Reference {id: 'R008'})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = 15;

MATCH (p:Paper {id: 'P9'})
MATCH (r:Reference {id: 'R009'})
MERGE (p)-[c:CITES]->(r)
SET c.citation_count = 1;

MATCH (p1:Paper {id: 'P02'})
MATCH (p2:Paper {id: 'P05'})
MERGE (p1)-[r:SHARES_TOPIC]-(p2)
SET r.shared_keyword = "NLP";

MATCH (p1:Paper {id: 'P05'})
MATCH (p2:Paper {id: 'P06'})
MERGE (p1)-[r:SHARES_TOPIC]-(p2)
SET r.shared_keyword = "Text Summarization";

MATCH (p1:Paper {id: 'P03'})
MATCH (p2:Paper {id: 'P05'})
MERGE (p1)-[r:SHARES_DOMAIN]-(p2)
SET r.shared_domain = "NLP";

MATCH (a1:Author {name: "Mandira Bairagi"})
MATCH (a2:Author {name: "Dr. Shalini R. Lihitkar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P01";

MATCH (a1:Author {name: "Mrs. Abha Pathak"})
MATCH (a2:Author {name: "Trupti Pawar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P02";

MATCH (a1:Author {name: "Mrs. Abha Pathak"})
MATCH (a2:Author {name: "Yogeshwari Pawar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P02";

MATCH (a1:Author {name: "Mrs. Abha Pathak"})
MATCH (a2:Author {name: "Shreya pawar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P02";

MATCH (a1:Author {name: "Trupti Pawar"})
MATCH (a2:Author {name: "Yogeshwari Pawar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P02";

MATCH (a1:Author {name: "Trupti Pawar"})
MATCH (a2:Author {name: "Shreya pawar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P02";

MATCH (a1:Author {name: "Yogeshwari Pawar"})
MATCH (a2:Author {name: "Shreya pawar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P02";

MATCH (a1:Author {name: "Divakar Yadav"})
MATCH (a2:Author {name: "Jalpa Desai"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P03";

MATCH (a1:Author {name: "Divakar Yadav"})
MATCH (a2:Author {name: "Arun Kumar Yadav"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P03";

MATCH (a1:Author {name: "Jalpa Desai"})
MATCH (a2:Author {name: "Arun Kumar Yadav"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P03";

MATCH (a1:Author {name: "Seema Aswani"})
MATCH (a2:Author {name: "Kabita Choudhary"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P04";

MATCH (a1:Author {name: "Seema Aswani"})
MATCH (a2:Author {name: "Sujala Shetty"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P04";

MATCH (a1:Author {name: "Seema Aswani"})
MATCH (a2:Author {name: "Nasheen Nur"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P04";

MATCH (a1:Author {name: "Kabita Choudhary"})
MATCH (a2:Author {name: "Sujala Shetty"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P04";

MATCH (a1:Author {name: "Kabita Choudhary"})
MATCH (a2:Author {name: "Nasheen Nur"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P04";

MATCH (a1:Author {name: "Sujala Shetty"})
MATCH (a2:Author {name: "Nasheen Nur"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P04";

MATCH (a1:Author {name: "Sanjivani Chandrashekhar Kachare"})
MATCH (a2:Author {name: "Manali Udaykumar Sawant"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P05";

MATCH (a1:Author {name: "Sanjivani Chandrashekhar Kachare"})
MATCH (a2:Author {name: "Manasi Suresh Yadav"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P05";

MATCH (a1:Author {name: "Sanjivani Chandrashekhar Kachare"})
MATCH (a2:Author {name: "Ms. Priyanka Rajendra Jadhav"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P05";

MATCH (a1:Author {name: "Manali Udaykumar Sawant"})
MATCH (a2:Author {name: "Manasi Suresh Yadav"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P05";

MATCH (a1:Author {name: "Manali Udaykumar Sawant"})
MATCH (a2:Author {name: "Ms. Priyanka Rajendra Jadhav"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P05";

MATCH (a1:Author {name: "Manasi Suresh Yadav"})
MATCH (a2:Author {name: "Ms. Priyanka Rajendra Jadhav"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P05";

MATCH (a1:Author {name: "SUBASH VOLETI"})
MATCH (a2:Author {name: "CHAITAN RAJU"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P06";

MATCH (a1:Author {name: "SUBASH VOLETI"})
MATCH (a2:Author {name: "TEJA RANI"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P06";

MATCH (a1:Author {name: "SUBASH VOLETI"})
MATCH (a2:Author {name: "MUGADA SWETHA"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P06";

MATCH (a1:Author {name: "CHAITAN RAJU"})
MATCH (a2:Author {name: "TEJA RANI"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P06";

MATCH (a1:Author {name: "CHAITAN RAJU"})
MATCH (a2:Author {name: "MUGADA SWETHA"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P06";

MATCH (a1:Author {name: "TEJA RANI"})
MATCH (a2:Author {name: "MUGADA SWETHA"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P06";

MATCH (a1:Author {name: "Bhuvan Shingade"})
MATCH (a2:Author {name: "Yash Matha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Bhuvan Shingade"})
MATCH (a2:Author {name: "Ved Kolambkar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Bhuvan Shingade"})
MATCH (a2:Author {name: "Suyash Kasar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Bhuvan Shingade"})
MATCH (a2:Author {name: "Prof. Rohini Palve"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Yash Matha"})
MATCH (a2:Author {name: "Ved Kolambkar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Yash Matha"})
MATCH (a2:Author {name: "Suyash Kasar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Yash Matha"})
MATCH (a2:Author {name: "Prof. Rohini Palve"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Ved Kolambkar"})
MATCH (a2:Author {name: "Suyash Kasar"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Ved Kolambkar"})
MATCH (a2:Author {name: "Prof. Rohini Palve"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Suyash Kasar"})
MATCH (a2:Author {name: "Prof. Rohini Palve"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P07";

MATCH (a1:Author {name: "Niharika Verma"})
MATCH (a2:Author {name: "Prof. Ashish Tiwari"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P08";

MATCH (a1:Author {name: "G. Santhoshi"})
MATCH (a2:Author {name: "M Jyothi"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "G. Santhoshi"})
MATCH (a2:Author {name: "Kovvuri Ramya Sri"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "G. Santhoshi"})
MATCH (a2:Author {name: "G. Hasika"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "G. Santhoshi"})
MATCH (a2:Author {name: "G. Varsha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "G. Santhoshi"})
MATCH (a2:Author {name: "R. Snigdha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "M Jyothi"})
MATCH (a2:Author {name: "Kovvuri Ramya Sri"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "M Jyothi"})
MATCH (a2:Author {name: "G. Hasika"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "M Jyothi"})
MATCH (a2:Author {name: "G. Varsha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "M Jyothi"})
MATCH (a2:Author {name: "R. Snigdha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "Kovvuri Ramya Sri"})
MATCH (a2:Author {name: "G. Hasika"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "Kovvuri Ramya Sri"})
MATCH (a2:Author {name: "G. Varsha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "Kovvuri Ramya Sri"})
MATCH (a2:Author {name: "R. Snigdha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "G. Hasika"})
MATCH (a2:Author {name: "G. Varsha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "G. Hasika"})
MATCH (a2:Author {name: "R. Snigdha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

MATCH (a1:Author {name: "G. Varsha"})
MATCH (a2:Author {name: "R. Snigdha"})
MERGE (a1)-[r:COLLABORATED_WITH]-(a2)
SET r.paper_id = "P09";

