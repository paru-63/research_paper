# Research Graph Database Project

This project aims to build a graph database using Neo4j for research papers, focusing on entity extraction, relationship extraction, and triple creation. The extracted data will be organized into a graph structure to facilitate advanced querying and analysis.

## Project Structure

```
research-graph-db
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── entity_extraction.py
│   ├── relationship_extraction.py
│   ├── triple_creation.py
│   ├── neo4j_handler.py
│   ├── data_loader.py
│   └── utils.py
├── data
│   ├── metadata.json
│   ├── reference.json
│   ├── abstracts.json
│   └── extracted_content.json
├── logs
│   └── .gitkeep
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd research-graph-db
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

- Copy the `.env.example` file to `.env` and fill in the necessary environment variables, including your Neo4j database credentials.

## Usage

1. Run the main application:
   ```
   python src/main.py
   ```

2. The application will perform the following tasks:
   - Extract entities from the research papers.
   - Identify relationships between the extracted entities.
   - Create triples (subject, predicate, object) for insertion into the Neo4j database.
   - Load the data into the Neo4j graph database.

## Files Overview

- **src/__init__.py**: Marks the directory as a Python package.
- **src/main.py**: Entry point for the application.
- **src/config.py**: Configuration settings for the application.
- **src/entity_extraction.py**: Functions for extracting entities from data.
- **src/relationship_extraction.py**: Functions for extracting relationships between entities.
- **src/triple_creation.py**: Responsible for creating triples for Neo4j.
- **src/neo4j_handler.py**: Manages the connection to the Neo4j database.
- **src/data_loader.py**: Loads data from JSON files.
- **src/utils.py**: Utility functions for various tasks.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.