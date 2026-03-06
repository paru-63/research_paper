"""
Knowledge Graph Visualization and Analysis
Generates visualizations and statistics without requiring Neo4j
"""

import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from collections import Counter
import networkx as nx

class KnowledgeGraphVisualizer:
    """Visualize knowledge graph statistics and relationships"""
    
    def __init__(self, entities_file: str, relationships_file: str):
        """Initialize with data files"""
        with open(entities_file, 'r', encoding='utf-8') as f:
            self.entities_data = json.load(f)
            self.entities = self.entities_data.get('entities', {})
        
        with open(relationships_file, 'r', encoding='utf-8') as f:
            self.relationships_data = json.load(f)
            self.relationships = self.relationships_data.get('relationships', {})
    
    def plot_entity_distribution(self, output_file: str):
        """Plot distribution of entities"""
        entity_counts = {
            'Papers': len(self.entities.get('papers', [])),
            'Authors': len(self.entities.get('authors', [])),
            'Institutions': len(self.entities.get('institutions', [])),
            'Journals': len(self.entities.get('journals', [])),
            'Keywords': len(self.entities.get('keywords', [])),
            'Domains': len(self.entities.get('domains', [])),
            'References': len(self.entities.get('references', []))
        }
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(entity_counts.keys(), entity_counts.values(), color='steelblue')
        plt.title('Knowledge Graph - Entity Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Entity Type', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Entity distribution chart saved: {output_file}")
    
    def plot_relationship_distribution(self, output_file: str):
        """Plot distribution of relationships"""
        rel_counts = {}
        for rel_type, rels in self.relationships.items():
            rel_counts[rel_type] = len(rels)
        
        # Sort by count
        sorted_rels = dict(sorted(rel_counts.items(), key=lambda x: x[1], reverse=True))
        
        plt.figure(figsize=(14, 7))
        bars = plt.barh(list(sorted_rels.keys()), list(sorted_rels.values()), color='coral')
        plt.title('Knowledge Graph - Relationship Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Count', fontsize=12)
        plt.ylabel('Relationship Type', fontsize=12)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{int(width)}',
                    ha='left', va='center', fontsize=10, style='italic')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Relationship distribution chart saved: {output_file}")
    
    def plot_papers_by_year(self, output_file: str):
        """Plot papers by publication year"""
        years = []
        for paper in self.entities.get('papers', []):
            if paper.get('year'):
                years.append(paper['year'])
        
        year_counts = Counter(years)
        sorted_years = sorted(year_counts.items())
        
        plt.figure(figsize=(12, 6))
        plt.plot([y[0] for y in sorted_years], 
                [y[1] for y in sorted_years], 
                marker='o', linewidth=2, markersize=8, color='green')
        plt.title('Research Papers by Publication Year', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Number of Papers', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Papers by year chart saved: {output_file}")
    
    def plot_keyword_frequency(self, output_file: str, top_n: int = 15):
        """Plot top keywords by frequency"""
        keyword_papers = {}
        
        for rel in self.relationships.get('HAS_KEYWORD', []):
            keyword = rel['target']
            if keyword not in keyword_papers:
                keyword_papers[keyword] = 0
            keyword_papers[keyword] += 1
        
        # Get top N keywords
        top_keywords = dict(sorted(keyword_papers.items(), 
                                   key=lambda x: x[1], 
                                   reverse=True)[:top_n])
        
        plt.figure(figsize=(14, 8))
        bars = plt.barh(list(top_keywords.keys()), list(top_keywords.values()), 
                       color='purple', alpha=0.7)
        plt.title(f'Top {top_n} Keywords by Frequency', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Papers', fontsize=12)
        plt.ylabel('Keyword', fontsize=12)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{int(width)}',
                    ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Keyword frequency chart saved: {output_file}")
    
    def plot_domain_distribution(self, output_file: str):
        """Plot research domain distribution"""
        domain_papers = {}
        
        for rel in self.relationships.get('BELONGS_TO_DOMAIN', []):
            domain = rel['target']
            if domain not in domain_papers:
                domain_papers[domain] = 0
            domain_papers[domain] += 1
        
        sorted_domains = dict(sorted(domain_papers.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True))
        
        plt.figure(figsize=(12, 8))
        colors = plt.cm.Set3(range(len(sorted_domains)))
        bars = plt.barh(list(sorted_domains.keys()), list(sorted_domains.values()), 
                       color=colors)
        plt.title('Research Domain Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Papers', fontsize=12)
        plt.ylabel('Domain', fontsize=12)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{int(width)}',
                    ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Domain distribution chart saved: {output_file}")
    
    def plot_collaboration_network(self, output_file: str):
        """Plot author collaboration network"""
        G = nx.Graph()
        
        # Add nodes (authors)
        for author in self.entities.get('authors', []):
            G.add_node(author['name'])
        
        # Add edges (collaborations)
        for rel in self.relationships.get('COLLABORATED_WITH', []):
            G.add_edge(rel['source'], rel['target'])
        
        # Create visualization
        plt.figure(figsize=(16, 12))
        
        # Use spring layout
        pos = nx.spring_layout(G, k=1, iterations=50, seed=42)
        
        # Calculate node sizes based on degree
        node_sizes = [G.degree(node) * 200 + 300 for node in G.nodes()]
        
        # Draw network
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                              node_color='lightblue', alpha=0.7)
        nx.draw_networkx_edges(G, pos, alpha=0.3, width=2)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        
        plt.title('Author Collaboration Network', fontsize=18, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Collaboration network chart saved: {output_file}")
    
    def plot_citation_analysis(self, output_file: str):
        """Plot citation analysis"""
        citations = []
        titles = []
        
        for ref in self.entities.get('references', []):
            if ref.get('citation_count', 0) > 0:
                citations.append(ref['citation_count'])
                # Truncate long titles
                title = ref.get('title', 'Unknown')[:40] + '...'
                titles.append(title)
        
        if not citations:
            print("⚠️  No citation data available")
            return
        
        # Sort by citation count
        sorted_data = sorted(zip(citations, titles), reverse=True)
        citations_sorted = [x[0] for x in sorted_data]
        titles_sorted = [x[1] for x in sorted_data]
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(titles_sorted, citations_sorted, color='orange', alpha=0.7)
        plt.title('Citation Analysis', fontsize=16, fontweight='bold')
        plt.xlabel('Citation Count', fontsize=12)
        plt.ylabel('Reference', fontsize=12)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{int(width)}',
                    ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Citation analysis chart saved: {output_file}")
    
    def generate_all_visualizations(self, output_dir: str = '/home/claude'):
        """Generate all visualizations"""
        print("\n📊 Generating visualizations...\n")
        
        self.plot_entity_distribution(f'{output_dir}/viz_entity_distribution.png')
        self.plot_relationship_distribution(f'{output_dir}/viz_relationship_distribution.png')
        self.plot_papers_by_year(f'{output_dir}/viz_papers_by_year.png')
        self.plot_keyword_frequency(f'{output_dir}/viz_keyword_frequency.png')
        self.plot_domain_distribution(f'{output_dir}/viz_domain_distribution.png')
        self.plot_collaboration_network(f'{output_dir}/viz_collaboration_network.png')
        self.plot_citation_analysis(f'{output_dir}/viz_citation_analysis.png')
        
        print("\n✅ All visualizations generated successfully!")
    
    def generate_statistics_report(self, output_file: str):
        """Generate a text statistics report"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("KNOWLEDGE GRAPH STATISTICS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            # Entity statistics
            f.write("ENTITY STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Papers:       {len(self.entities.get('papers', []))}\n")
            f.write(f"Authors:      {len(self.entities.get('authors', []))}\n")
            f.write(f"Institutions: {len(self.entities.get('institutions', []))}\n")
            f.write(f"Journals:     {len(self.entities.get('journals', []))}\n")
            f.write(f"Keywords:     {len(self.entities.get('keywords', []))}\n")
            f.write(f"Domains:      {len(self.entities.get('domains', []))}\n")
            f.write(f"References:   {len(self.entities.get('references', []))}\n\n")
            
            # Relationship statistics
            f.write("RELATIONSHIP STATISTICS\n")
            f.write("-" * 80 + "\n")
            total_rels = 0
            for rel_type, rels in self.relationships.items():
                count = len(rels)
                total_rels += count
                f.write(f"{rel_type:25} {count:5}\n")
            f.write(f"{'TOTAL':25} {total_rels:5}\n\n")
            
            # Top keywords
            f.write("TOP 10 KEYWORDS\n")
            f.write("-" * 80 + "\n")
            keyword_counts = {}
            for rel in self.relationships.get('HAS_KEYWORD', []):
                keyword = rel['target']
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
            
            for i, (keyword, count) in enumerate(sorted(keyword_counts.items(), 
                                                       key=lambda x: x[1], 
                                                       reverse=True)[:10], 1):
                f.write(f"{i:2}. {keyword:40} ({count})\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"✅ Statistics report saved: {output_file}")


if __name__ == "__main__":
    # Initialize visualizer
    viz = KnowledgeGraphVisualizer(
        entities_file='/home/claude/extracted_entities.json',
        relationships_file='/home/claude/extracted_relationships.json'
    )
    
    # Generate all visualizations
    viz.generate_all_visualizations()
    
    # Generate statistics report
    viz.generate_statistics_report('/home/claude/statistics_report.txt')
