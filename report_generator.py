import os 
import io
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import TableStyle
from mongo_DB_handler import MongoDBHandler
from statistical_analysis import StatisticalAnalysis 
from variance_distribution_calculator import VarianceDistributionCalculator
from dense_sparse_DB_handler import DenseSparseDBHandler
from algorithm_efficiency_analyzer import AlgorithmEfficiencyAnalyzer

class ReportGenerator:
    def __init__(self, db_name='subset_sum_db', filename="report.pdf"):
        self.db_handler = MongoDBHandler(db_name)
        self.dense_sparse_handler = DenseSparseDBHandler()
        self.analysis = StatisticalAnalysis(self.db_handler)
        self.variance_calculator = VarianceDistributionCalculator(self.db_handler)
        self.efficiency_analyzer = AlgorithmEfficiencyAnalyzer(self.dense_sparse_handler)
        self.filename = filename

    def generate_report(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        full_path = os.path.join(desktop_path, self.filename)

        doc = SimpleDocTemplate(full_path, pagesize=A4)
        styles = getSampleStyleSheet()

        # Stili personalizzati
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor("#003366"),
            spaceAfter=12,
            alignment=1
        )

        heading_style = ParagraphStyle(
            'HeadingStyle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor("#00509E"),
            spaceAfter=6
        )

        normal_style = styles['Normal']
        normal_style.fontSize = 12

        elements = []

        # Titolo del progetto
        title = Paragraph("Progetto Algoritmi Avanzati", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Autore
        author = Paragraph("Ideato da Carmine Citro", normal_style)
        elements.append(author)
        elements.append(Spacer(1, 24))

        # Sottotitolo
        subtitle = Paragraph("Studio Empirico del Problema del Subset Sum", heading_style)
        elements.append(subtitle)
        elements.append(Spacer(1, 12))

        # Statistiche
        statistics = self.analysis.collect_statistics()
        for algorithm, stats in statistics.items():
            elements.append(Paragraph(f"<b>Algoritmo: {algorithm}</b>", heading_style))
            for key, value in stats.items():
                translated_key = {
                    "total_instances": "Totale delle istanze",
                    "num_subsets_found": "Numero di sottoinsiemi trovati",
                    "avg_size": "Media dimensione",
                    "avg_target": "Media target",
                    "avg_complexity": "Media complessità (Tempo di esecuzione)",
                }.get(key, key)
                
                elements.append(Paragraph(f"{translated_key}: {value}", normal_style))
            elements.append(Spacer(1, 12))

        # Grafico delle statistiche
        plt.switch_backend('Agg')
        plt.figure(figsize=(10, 5))
        self.analysis.plot_statistics(statistics)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        elements.append(Spacer(1, 24))
        elements.append(Paragraph("Grafico delle Statistiche", heading_style))
        elements.append(Spacer(1, 12))
        elements.append(Image(buffer, width=500, height=250))

        # Calcola varianza e distribuzione
        variance_results = self.variance_calculator.calculate_variance_and_distribution()
        for algorithm, results in variance_results.items():
            elements.append(Paragraph(f"<b>Algoritmo: {algorithm}</b>", heading_style))
            elements.append(Paragraph(f"Varianza: {results['variance']:.12f}", normal_style))
            elements.append(Paragraph(f"Deviazione standard: {results['standard_deviation']:.12f}", normal_style))
            elements.append(Spacer(1, 12))

            # Grafico della distribuzione della varianza
            plt.switch_backend('Agg')
            plt.figure(figsize=(10, 5))
            plt.hist(results['complexities'], bins=10, alpha=0.7, color='blue', label=algorithm)
            plt.title(f"Distribuzione della Varianza per {algorithm}", fontsize=14)
            plt.xlabel("Complessità (T.E.)", fontsize=12)
            plt.ylabel("Frequenza", fontsize=12)
            plt.legend()
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            plt.close()

            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Grafico della Distribuzione della Varianza", heading_style))
            elements.append(Spacer(1, 12))
            elements.append(Image(buffer, width=500, height=250))

        # Analisi dell'efficienza
        avg_times_dense, avg_times_sparse, variance_std_dense, variance_std_sparse, dense_fastest, sparse_fastest, sorted_dense, sorted_sparse = self.efficiency_analyzer.run_analysis()
        # Descrizione analisi
        subtitle = Paragraph("Analisi delle prestazioni algoritmiche tramite istanze numeriche dense e sparse", heading_style)
        elements.append(subtitle)
        elements.append(Spacer(1, 12))
        # Descrizione analisi
    

        # Classifiche
        elements.append(Paragraph("<b>Classifica Algoritmi per Istanze Dense</b>", heading_style))
        for rank, (algo, avg_complexity) in enumerate(sorted_dense, start=1):
            elements.append(Paragraph(f"{rank}. {algo} - Complessità Media: {avg_complexity:.12f}", normal_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("<b>Classifica Algoritmi per Istanze Sparse</b>", heading_style))
        for rank, (algo, avg_complexity) in enumerate(sorted_sparse, start=1):
            elements.append(Paragraph(f"{rank}. {algo} - Complessità Media: {avg_complexity:.12f}", normal_style))
        elements.append(Spacer(1, 12))

        # Grafici di distribuzione dei tempi di esecuzione
        graphs = self.efficiency_analyzer.plot_execution_time_distribution()
        for fig in graphs:
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            elements.append(Image(buffer, width=400, height=300))

        # Creazione PDF
        doc.build(elements)

        # Salvataggio dei risultati in PDF
        self.save_results_to_pdf(full_path)

    def save_results_to_pdf(self, filename):
        """Salva i risultati dell'analisi in un file PDF."""
        sorted_dense, sorted_sparse = self.efficiency_analyzer.evaluate_best_algorithm()
        avg_times_dense, avg_times_sparse = self.efficiency_analyzer.calculate_avg_execution_time()
        variance_std_dense, variance_std_sparse = self.efficiency_analyzer.calculate_variance_and_std_dev()
        fastest_dense, fastest_sparse = self.efficiency_analyzer.count_fastest_algorithm()

        pdf = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        results_style = ParagraphStyle(
            'ResultsStyle',
            parent=styles['Normal'],
            fontSize=18,
            spaceAfter=12,
            alignment=1
        )

        # Titolo
        elements.append(Paragraph("=== Risultati dell'Analisi ===", results_style))

        # Tempi di esecuzione medi
        elements.append(Paragraph("=== Tempi di Esecuzione Medi ===", styles['Heading2']))

        # Tabella per istanze dense
        dense_table_data = [["Algoritmo", "Tempo Medio"]]
        for algo, time in avg_times_dense.items():
            dense_table_data.append([algo, f"{time:.12f}"])
        
        dense_table = Table(dense_table_data)
        dense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0E0E0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('SIZE', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(dense_table)
        elements.append(Spacer(1, 12))

        # Tabella per istanze sparse
        sparse_table_data = [["Algoritmo", "Tempo Medio"]]
        for algo, time in avg_times_sparse.items():
            sparse_table_data.append([algo, f"{time:.12f}"])
        
        sparse_table = Table(sparse_table_data)
        sparse_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0E0E0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('SIZE', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(sparse_table)

        # Statistiche di varianza
        elements.append(Paragraph("=== Statistiche di Varianza ===", styles['Heading2']))
        elements.append(Paragraph(f"Varianza Media per Istanze Dense: {variance_std_dense:.12f}", styles['Normal']))
        elements.append(Paragraph(f"Varianza Media per Istanze Sparse: {variance_std_sparse:.12f}", styles['Normal']))
        elements.append(Paragraph(f"Algoritmo più veloce per istanze dense: {fastest_dense}", styles['Normal']))
        elements.append(Paragraph(f"Algoritmo più veloce per istanze sparse: {fastest_sparse}", styles['Normal']))

        pdf.build(elements)
