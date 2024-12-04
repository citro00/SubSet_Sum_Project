import os
import io
import datetime
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from backend.mongo_DB_handler import MongoDBHandler
from backend.statistical_analysis import StatisticalAnalysis
from backend.variance_distribution_calculator import VarianceDistributionCalculator
from backend.dense_sparse_DB_handler import DenseSparseDBHandler
from backend.algorithm_efficiency_analyzer import AlgorithmEfficiencyAnalyzer

class ReportGenerator:
    def __init__(self, db_name='subset_sum_db', filename="report.pdf"):
        self.db_handler = MongoDBHandler(db_name)
        self.dense_sparse_handler = DenseSparseDBHandler()
        self.analysis = StatisticalAnalysis(self.db_handler)
        self.variance_calculator = VarianceDistributionCalculator(self.db_handler)
        self.efficiency_analyzer = AlgorithmEfficiencyAnalyzer(self.dense_sparse_handler)
        self.filename = filename

        self.styles = self.get_styles()

    def get_styles(self):
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=26,
            leading=30,
            textColor=colors.HexColor("#002E5D"),  
            alignment=1,
            spaceAfter=30,
            ))

        styles.add(ParagraphStyle(
            name='CustomAuthor',
            parent=styles['Normal'],
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#555555"), 
            alignment=1,
            spaceAfter=10,
            ))

        styles.add(ParagraphStyle(
            name='CustomDate',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#777777"),  
            alignment=1,
            spaceAfter=20,
            ))

        styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=styles['Heading1'],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#003366"), 
            spaceAfter=15,
             ))

        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#004080"), 
            spaceAfter=10,
            ))

        styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=styles['Normal'],
            fontSize=12,
            leading=18,
            textColor=colors.HexColor("#333333"),  
            spaceAfter=12,
            ))  

        styles.add(ParagraphStyle(
            name='CustomCaption',
            parent=styles['Italic'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#666666"),  
            spaceAfter=8,
            alignment=1,
            ))

        return styles

       
    def generate_report(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        full_path = os.path.join(desktop_path, self.filename)

        doc = SimpleDocTemplate(
            full_path,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )

        elements = []

        # Creazione delle sezioni del report
        self.create_cover_page(elements)
        self.add_table_of_contents(elements)
        self.add_introduction(elements)
        self.add_statistical_analysis(elements)
        self.add_variance_analysis(elements)
        self.add_algorithm_efficiency_analysis(elements)
        self.add_conclusion(elements)

        # Costruzione del PDF con numeri di pagina
        doc.build(
            elements,
            onFirstPage=self.add_page_numbers,
            onLaterPages=self.add_page_numbers
        )

        print(f"Il report è stato generato con successo: {full_path}")

    def create_cover_page(self, elements):
        """Crea la copertina del report."""
        elements.append(Paragraph("Progetto di Analisi Avanzata degli Algoritmi", self.styles['CustomTitle']))
        elements.append(Paragraph("Studio Empirico sul Problema del Subset Sum", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 100))
        elements.append(Paragraph("Autore: Carmine Citro", self.styles['CustomAuthor']))
        elements.append(Paragraph(f"Data di Generazione: {datetime.datetime.now().strftime('%d/%m/%Y')}", self.styles['CustomDate']))
        elements.append(PageBreak())
        
    def add_table_of_contents(self, elements):
        """Aggiunge l'indice al report."""
        elements.append(Paragraph("Indice", self.styles['CustomHeading1']))

        # Crea una tabella per l'indice manuale
        data = [
            ["Sezione", "Pagina"],
            ["Introduzione", "1"],
            ["Analisi Statistica", "3"],
            ["Analisi della Varianza e Distribuzione", "5"],
            ["Analisi dell'Efficienza degli Algoritmi", "7"],
            ["Conclusione", "10"]
        ]

        toc_table = Table(data, colWidths=[350, 50])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0E0E0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(toc_table)
        elements.append(PageBreak())


    def add_introduction(self, elements):
        """Aggiunge l'introduzione al report."""
        elements.append(Paragraph("Introduzione", self.styles['CustomHeading1']))
        intro_text = """
        Questo report presenta uno studio empirico sul problema del Subset Sum, con un'analisi dettagliata delle prestazioni
        di vari algoritmi su istanze numeriche dense e sparse. Il Subset Sum rappresenta un problema centrale nella teoria
        della complessità computazionale, con applicazioni rilevanti in numerosi contesti pratici, tra cui crittografia,
        pianificazione e ottimizzazione.
        """
        elements.append(Paragraph(intro_text.strip(), self.styles['CustomBodyText']))
        elements.append(PageBreak())


    def add_statistical_analysis(self, elements):
        """Aggiunge la sezione di analisi statistica."""
        elements.append(Paragraph("Analisi Statistica", self.styles['CustomHeading1']))
        statistics = self.analysis.collect_statistics()

        for algorithm, stats in statistics.items():
            elements.append(Paragraph(f"Algoritmo: {algorithm}", self.styles['CustomHeading2']))

            data = []
            for key, value in stats.items():
                translated_key = {
                    "total_instances": "Totale delle Istanze",
                    "num_subsets_found": "Numero di Sottoinsiemi Trovati",
                    "avg_size": "Dimensione Media dell'Insieme",
                    "avg_target": "Valore Medio del Target",
                    "avg_complexity": "Tempo Medio di Esecuzione (s)",
                }.get(key, key)
                data.append([translated_key, str(value)])

            table = Table(data, colWidths=[250, 200])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F7F7F7")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))

        # Grafico delle statistiche
        plt.switch_backend('Agg')
        plt.figure(figsize=(6, 4))
        self.analysis.plot_statistics(statistics)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        elements.append(Image(buffer, width=400, height=300))
        elements.append(Paragraph("Figura 1: Visualizzazione Grafica delle Statistiche Rilevate", self.styles['CustomCaption']))
        elements.append(PageBreak())


    def add_variance_analysis(self, elements):
        """Aggiunge la sezione di analisi della varianza e distribuzione."""
        elements.append(Paragraph("Analisi della Varianza e Distribuzione", self.styles['Heading1']))
        variance_results = self.variance_calculator.calculate_variance_and_distribution()

        for algorithm, results in variance_results.items():
            elements.append(Paragraph(f"Algoritmo: {algorithm}", self.styles['Heading2']))
            elements.append(Paragraph(f"Varianza: {results['variance']:.12f}", self.styles['BodyText']))
            elements.append(Paragraph(f"Deviazione standard: {results['standard_deviation']:.12f}", self.styles['BodyText']))
            elements.append(Spacer(1, 12))

            # Grafico della distribuzione della varianza
            plt.switch_backend('Agg')
            plt.figure(figsize=(6, 4))
            plt.hist(results['complexities'], bins=10, alpha=0.7, color='blue', label=algorithm)
            plt.title(f"Distribuzione della Varianza per {algorithm}")
            plt.xlabel("Complessità (T.E.)")
            plt.ylabel("Frequenza")
            plt.legend()
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            plt.close()

            elements.append(Image(buffer, width=400, height=300))
            elements.append(Paragraph(f"Figura: Distribuzione della Varianza per {algorithm}", self.styles['CustomCaption']))
            elements.append(PageBreak())

    def add_algorithm_efficiency_analysis(self, elements):
        """Aggiunge la sezione di analisi dell'efficienza degli algoritmi."""
        elements.append(Paragraph("Analisi dell'Efficienza degli Algoritmi", self.styles['Heading1']))
        elements.append(Paragraph(
            "In questa sezione analizziamo le prestazioni degli algoritmi tramite istanze numeriche dense e sparse.",
            self.styles['BodyText']
        ))
        elements.append(Spacer(1, 12))

        # Ottenimento dei dati di analisi
        (
            avg_times_dense, avg_times_sparse,
            variance_std_dense, variance_std_sparse,
            dense_fastest, sparse_fastest,
            sorted_dense, sorted_sparse
        ) = self.efficiency_analyzer.run_analysis()

        # Classifica per istanze dense
        elements.append(Paragraph("Classifica Algoritmi per Istanze Dense", self.styles['Heading2']))
        data = [["Posizione", "Algoritmo", "Tempo Medio (s)"]]
        for rank, (algo, avg_complexity) in enumerate(sorted_dense, start=1):
            data.append([str(rank), algo, f"{avg_complexity:.12f}"])
        table = Table(data, colWidths=[80, 220, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        # Classifica per istanze sparse
        elements.append(Paragraph("Classifica Algoritmi per Istanze Sparse", self.styles['Heading2']))
        data = [["Posizione", "Algoritmo", "Tempo Medio (s)"]]
        for rank, (algo, avg_complexity) in enumerate(sorted_sparse, start=1):
            data.append([str(rank), algo, f"{avg_complexity:.12f}"])
        table = Table(data, colWidths=[80, 220, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        # Grafici di distribuzione dei tempi di esecuzione
        graphs = self.efficiency_analyzer.plot_execution_time_distribution()
        for idx, fig in enumerate(graphs):
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            plt.close(fig)
            elements.append(Image(buffer, width=400, height=300))
            elements.append(Paragraph(
                f"Figura {idx+1}: Distribuzione dei Tempi di Esecuzione",
                self.styles['CustomCaption']
            ))
            elements.append(Spacer(1, 12))

    def add_conclusion(self, elements):
        """Aggiunge la conclusione al report."""
        elements.append(Paragraph("Conclusione", self.styles['CustomHeading1']))
        conclusion_text = """
        In conclusione, lo studio ha evidenziato come l'efficacia degli algoritmi per il problema del Subset Sum vari
        significativamente a seconda della tipologia dell'istanza analizzata. Le istanze numeriche dense e sparse hanno
        dimostrato comportamenti diversi in termini di tempi di esecuzione e complessità computazionale. Questi risultati
        sottolineano l'importanza di una scelta accurata dell'algoritmo in base alle caratteristiche specifiche del problema
        affrontato, al fine di ottimizzare le risorse computazionali e migliorare l'efficienza.
        """
        elements.append(Paragraph(conclusion_text.strip(), self.styles['CustomBodyText']))


    def add_page_numbers(self, canvas, doc):
        """Aggiunge i numeri di pagina al PDF."""
        page_num = canvas.getPageNumber()
        text = f"Pagina {page_num}"
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(A4[0] - 50, 20, text)

        # Aggiunge il titolo come intestazione
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(50, A4[1] - 50, "Progetto Algoritmi Avanzati")

        # Aggiunge una linea orizzontale
        canvas.line(50, A4[1] - 55, A4[0] - 50, A4[1] - 55)

        # Aggiunge una linea orizzontale in basso
        canvas.line(50, 30, A4[0] - 50, 30)

