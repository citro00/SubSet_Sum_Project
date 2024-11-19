import tkinter as tk 
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from variance_distribution_calculator import VarianceDistributionCalculator
from istance_generator_dense_sparse import SubsetInstanceGenerator
from algorithm_efficiency_analyzer import AlgorithmEfficiencyAnalyzer
from dense_sparse_DB_handler import DenseSparseDBHandler 
from report_generator import ReportGenerator

class StatisticalAnalysisGUI:
    
    def __init__(self, master, statistical_analysis, db_handler):
        self.master = master
        self.statistical_analysis = statistical_analysis
        self.db_handler = db_handler
        master.title("Analisi Statistiche")
        master.configure(bg="#F4F6F7")  
        master.geometry("700x500")
        self.current_algorithm = 0
        self.algorithms = ['Dynamic Programming', 'Meet In The Middle', 'Backtracking']
        
        # Frame con bordo e padding
        self.frame = tk.Frame(master, bg="#FFFFFF", relief=tk.GROOVE, borderwidth=3)
        self.frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        button_style = {
            "font": ("Arial", 14, "bold"),
            "bg": "#1A5276",
            "fg": "white",
            "bd": 0,
            "activebackground": "#154360",
            "activeforeground": "white"
        }
        
        self.button1 = tk.Button(self.frame, text="Visualizza Statistiche Media", **button_style, command=self.display_statistics)
        self.button1.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=5, sticky="ew")

        self.button2 = tk.Button(self.frame, text="Calcola Varianza e Distribuzione", **button_style, command=self.calculate_variance_distribution)
        self.button2.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=5, sticky="ew")

        self.button3 = tk.Button(self.frame, text="Comparazione Algoritmi", **button_style, command=self.show_comparison_buttons)
        self.button3.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=5, sticky="ew")

        self.button4 = tk.Button(self.frame, text="Genera Report", **button_style, command=self.generate_report)  
        self.button4.grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=5, sticky="ew")

        self.statistic_text = tk.Text(self.frame, width=80, height=15, bg="#E8F8F5", 
                               font=("Arial", 12), wrap=tk.WORD, relief=tk.FLAT, 
                               padx=10, pady=10)
        self.statistic_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Grafico
        self.figure = Figure(figsize=(10, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.canvas.draw()
        
        # Pulsante "Grafico Successivo" nascosto inizialmente
        self.next_button = tk.Button(self.frame, text="Grafico Successivo", **button_style, command=self.next_algorithm)
        self.next_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)  
        self.next_button.grid_remove()  # Nasconde il pulsante inizialmente

        self.input_frame = tk.Frame(self.frame, bg="#F8F9FA", bd=2, relief=tk.RAISED)
        
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def show_comparison_buttons(self):
        """Mostra i pulsanti 'Genera Istanze' e 'Compara'."""        
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#2874A6",
            "fg": "white",
            "bd": 0,
            "activebackground": "#1B4F72",
            "activeforeground": "white"
        }
        
        # Crea pulsante 'Genera Istanze'
        self.generate_button = tk.Button(self.frame, text="Genera Istanze", **button_style, command=self.show_input_form)
        self.generate_button.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=5, sticky="ew")

        # Crea pulsante 'Compara'
        self.compare_button = tk.Button(self.frame, text="Compara Algoritmi", **button_style, command=self.compare_algorithms)
        self.compare_button.grid(row=2, column=1, padx=10, pady=10, ipadx=10, ipady=5, sticky="ew")
    def clear_input_frame(self):
        """Rimuove tutti i widget dall'input frame."""
        for widget in self.input_frame.winfo_children():
            widget.destroy()
    def show_input_form(self):
        """Mostra il form di input per il numero di istanze, dimensione del set, e altri parametri."""
        self.canvas.get_tk_widget().grid_remove()  # Nasconde il grafico
        self.next_button.grid_remove()  # Nasconde il pulsante "Grafico Successivo"
        self.clear_input_frame()  # Rimuove eventuali widget esistenti nel frame di input

        # Crea i vari campi di input necessari
        inputs = [
            ("Numero di Istanze:", "num_instances_entry", 5),
            ("Dimensione Minima del Set:", "min_size_entry", 10),
            ("Dimensione Massima del Set:", "max_size_entry", 10),
            ("Valore Massimo per un Elemento del Set:", "max_value_entry", 10),
            ("Target come metà della somma del set? (True/False):", "is_partition_entry", 5)
        ]

        # Aggiungi ogni campo di input al frame di input
        for text, attr, width in inputs:
            tk.Label(self.input_frame, text=text, font=("Arial", 12)).pack(side=tk.TOP, anchor="w", padx=5, pady=5)
            entry = tk.Entry(self.input_frame, font=("Arial", 12), width=width)
            entry.pack(side=tk.TOP, anchor="w", padx=5, pady=2)
            setattr(self, attr, entry)

        # Pulsante per generare le istanze
        generate_input_button = tk.Button(self.input_frame, text="Genera", bg="#1A5276", fg="white", font=("Arial", 14, "bold"), command=self.generate_instances)
        generate_input_button.pack(side=tk.TOP, anchor="w", padx=5, pady=10)

        # Posiziona il frame di input sotto la casella di testo
        self.input_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


    def display_statistics(self):
        # Nasconde il pulsante "Grafico Successivo" e pulisce l'area grafica
        self.next_button.grid_remove()
        self.figure.clear()
        self.canvas.draw()
        statistics = self.statistical_analysis.collect_statistics()
        self.statistic_text.delete(1.0, tk.END)
        
        for algorithm, stats in statistics.items():
            if isinstance(stats, str):
                self.statistic_text.insert(tk.END, f"{algorithm}: {stats}\n")
            else:
                self.statistic_text.insert(tk.END, f"--- {algorithm} ---\n")
                self.statistic_text.insert(tk.END, f"Totale Istanze: {stats['total_instances']}\n")
                self.statistic_text.insert(tk.END, f"Sottoinsiemi Trovati: {stats['num_subsets_found']}\n")
                self.statistic_text.insert(tk.END, f"Dimensione Media: {stats['avg_size']:.2f}\n")
                self.statistic_text.insert(tk.END, f"Target Medio: {stats['avg_target']:.2f}\n")
                self.statistic_text.insert(tk.END, f"Tempo di esecuzione Medio: {stats['avg_complexity']:.10f}\n")
                self.statistic_text.insert(tk.END, "\n")
        
        self.plot_statistics(statistics)

    def next_algorithm(self):
        self.current_algorithm = (self.current_algorithm + 1) % len(self.algorithms)
        self.calculate_variance_distribution()

    def calculate_variance_distribution(self):
        algorithm = self.algorithms[self.current_algorithm]
        variance_calculator = VarianceDistributionCalculator(self.db_handler)
        results = variance_calculator.calculate_variance_and_distribution()
    
        # Nascondi i pulsanti di comparazione
        self.hide_comparison_buttons()
        
        if algorithm in results:
            complexities = results[algorithm]['complexities']
            self.plot_variance_distribution(complexities, algorithm)
        
            self.statistic_text.delete(1.0, tk.END)
            stats = results[algorithm]
            self.statistic_text.insert(tk.END, f"--- {algorithm} ---\n")
            self.statistic_text.insert(tk.END, f"Varianza: {stats['variance']}\n")
            self.statistic_text.insert(tk.END, f"Deviazione Standard: {stats['standard_deviation']}\n")
            self.statistic_text.insert(tk.END, f"Sottoinsiemi S: {stats['subsets']}\n")
            self.statistic_text.insert(tk.END, f"Targets: {stats['targets']}\n\n")
        
            # Rendi visibile il pulsante "Grafico Successivo" solo dopo il calcolo
            self.next_button.grid()  
        else:
            messagebox.showerror("Errore", "Nessun risultato trovato per questo algoritmo.")    
    
    def hide_comparison_buttons(self):
        """Nasconde i pulsanti di comparazione e il form di input."""
        if hasattr(self, 'generate_button'):
            self.generate_button.grid_remove()
        if hasattr(self, 'compare_button'):
            self.compare_button.grid_remove()
        self.input_frame.grid_remove()
    
    
    def plot_variance_distribution(self, complexities, algorithm):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.hist(complexities, bins=15, color='#2980B9', edgecolor='black', alpha=0.85)
        ax.set_title(f"Distribuzione Varianza - {algorithm}", fontsize=16, fontweight='bold', color="#34495E")
        ax.set_xlabel("Complessità")
        ax.set_ylabel("Frequenza")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        self.canvas.draw()     

    def plot_statistics(self, statistics):
        self.figure.clear()
        algorithms = list(statistics.keys())
        avg_sizes = [stats['avg_size'] for stats in statistics.values() if isinstance(stats, dict)]
        avg_targets = [stats['avg_target'] for stats in statistics.values() if isinstance(stats, dict)]
        avg_complexities = [stats['avg_complexity'] for stats in statistics.values() if isinstance(stats, dict)]

        # Configura i tre sottografici
        ax1 = self.figure.add_subplot(131)
        ax1.bar(algorithms, avg_sizes, color='teal')
        ax1.set_title('Dimensione Media', fontsize=12)
        ax1.set_ylabel('Dimensione', fontsize=10)
        ax1.set_xticks(range(len(algorithms)))
        ax1.set_xticklabels(algorithms, rotation=15, ha='right', fontsize=6)
        ax1.tick_params(axis='x', pad=5)

        ax2 = self.figure.add_subplot(132)
        ax2.bar(algorithms, avg_targets, color='salmon')
        ax2.set_title('Target Medio', fontsize=12)
        ax2.set_ylabel('Target', fontsize=10)
        ax2.set_xticks(range(len(algorithms)))
        ax2.set_xticklabels(algorithms, rotation=15, ha='right', fontsize=6)
        ax2.tick_params(axis='x', pad=5)

        ax3 = self.figure.add_subplot(133)
        ax3.bar(algorithms, avg_complexities, color='orange')
        ax3.set_title('Tempo di esecuzione Medio', fontsize=12)
        ax3.set_ylabel('Complessità', fontsize=10)
        ax3.set_xticks(range(len(algorithms)))
        ax3.set_xticklabels(algorithms, rotation=15, ha='right', fontsize=6)
        ax3.tick_params(axis='x', pad=5)

        self.canvas.draw()

    def generate_instances(self):
        # Ottieni il numero di istanze dall'entry
        try:
            num_instances = int(self.num_instances_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un numero valido di istanze.")
            return

        # Ottieni la dimensione minima del set
        try:
            min_size = int(self.min_size_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un valore valido per la dimensione minima del set.")
            return

        # Ottieni la dimensione massima del set
        try:
            max_size = int(self.max_size_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un valore valido per la dimensione massima del set.")
            return

        # Ottieni il valore massimo per un elemento del set
        try:
            max_value = int(self.max_value_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un valore valido per il valore massimo del set.")
            return

        # Ottieni il valore di is_partition
        is_partition_str = self.is_partition_entry.get().strip().lower()
        if is_partition_str not in ['true', 'false']:
            messagebox.showerror("Errore", "Inserisci 'True' o 'False' per is_partition.")
            return
        is_partition = is_partition_str == 'true'

        # Crea un'istanza del generatore e genera le istanze
        generator = SubsetInstanceGenerator(num_instances, min_size, max_size, max_value, is_partition)
        generator.run_subset_sum_algorithms()  # Esegui e salva i risultati nel DB

        # Ottieni il conteggio di istanze e soluzioni salvate
        dense_count = num_instances
        sparse_count = num_instances

        # Mostra un messaggio con il conteggio dei risultati
        self.statistic_text.delete(1.0, tk.END)
        self.statistic_text.insert(tk.END, f"Istanze dense generate: {dense_count}\n")
        self.statistic_text.insert(tk.END, f"Istanze sparse generate: {sparse_count}\n")
        self.statistic_text.insert(tk.END, f"Soluzioni salvate nel DB: {6 * num_instances}\n")

        print(f"Generando {num_instances} istanze con dimensione minima {min_size}, dimensione massima {max_size}, valore massimo {max_value}, e is_partition={is_partition}.")

        
    def compare_algorithms(self):
        """Confronta le prestazioni degli algoritmi."""
        db_handler = DenseSparseDBHandler()  # Crea un'istanza della tua classe di gestione del DB
        self.analyzer = AlgorithmEfficiencyAnalyzer(db_handler)
        results = self.analyzer.run_analysis()

        # Estrai i risultati
        avg_times_dense, avg_times_sparse, variance_std_dense, variance_std_sparse, dense_fastest, sparse_fastest, sorted_dense, sorted_sparse = results

        # Cancella il contenuto precedente della casella di testo
        self.statistic_text.delete(1.0, tk.END)

        # Visualizza i tempi medi di esecuzione
        self.statistic_text.insert(tk.END, "Tempo di Esecuzione Medio - Istanze Dense:\n")
        for algo, time in avg_times_dense.items():
            self.statistic_text.insert(tk.END, f"{algo}: {time:.10f}\n")

        self.statistic_text.insert(tk.END, "\nTempo di Esecuzione Medio - Istanze Sparse:\n")
        for algo, time in avg_times_sparse.items():
            self.statistic_text.insert(tk.END, f"{algo}: {time:.10f}\n")

        # Visualizza varianza e deviazione standard
        self.statistic_text.insert(tk.END, "\nVarianza e Deviazione Standard - Istanze Dense:\n")
        for algo, (var, std) in variance_std_dense.items():
            self.statistic_text.insert(tk.END, f"{algo}: Varianza: {var:.10f}, Deviazione Standard: {std:.10f}\n")

        self.statistic_text.insert(tk.END, "\nVarianza e Deviazione Standard - Istanze Sparse:\n")
        for algo, (var, std) in variance_std_sparse.items():
            self.statistic_text.insert(tk.END, f"{algo}: Varianza: {var:.10f}, Deviazione Standard: {std:.10f}\n")

        # Visualizza il conteggio degli algoritmi più veloci
        self.statistic_text.insert(tk.END, "\nConteggio degli Algoritmi Più Veloci - Istanze Dense:\n")
        for algo, count in dense_fastest.items():
            self.statistic_text.insert(tk.END, f"{algo}: {count}\n")

        self.statistic_text.insert(tk.END, "\nConteggio degli Algoritmi Più Veloci - Istanze Sparse:\n")
        for algo, count in sparse_fastest.items():
            self.statistic_text.insert(tk.END, f"{algo}: {count}\n")

        # Visualizza le classifiche opzionali degli algoritmi
        self.statistic_text.insert(tk.END, "\nClassifica degli Algoritmi per le Istanze Dense:\n")
        for rank, (algo, avg) in enumerate(sorted_dense, start=1):
            self.statistic_text.insert(tk.END, f"{rank}. {algo} con Tempo di esecuzione medio: {avg:.10f}\n")

        self.statistic_text.insert(tk.END, "\nClassifica degli Algoritmi per le Istanze Sparse:\n")
        for rank, (algo, avg) in enumerate(sorted_sparse, start=1):
            self.statistic_text.insert(tk.END, f"{rank}. {algo} con Tempo di esecuzione medio: {avg:.10f}\n")

        # Inizializza la lista dei grafici
        self.graphs = [] 

        # Aggiungi il pulsante per generare i grafici all'interno del frame
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#2874A6",
            "fg": "white",
            "bd": 0,
            "activebackground": "#1B4F72",
            "activeforeground": "white"
            }
    
        self.graph_frame = tk.Frame(self.frame)
        self.graph_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")  

        self.generate_graphs_button = tk.Button(self.frame, text="Genera Grafici", **button_style, command=self.show_graphs)
        self.generate_graphs_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        

    def show_graphs(self):
        """Visualizza i grafici di distribuzione dei tempi di esecuzione."""
        self.graphs = self.analyzer.plot_execution_time_distribution()  

        # Pulisci il frame dei grafici
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        for fig in self.graphs:
    
            fig.set_size_inches(15, 8) 
        
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
        
            
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False)  
        self.generate_graphs_button.grid_forget()  # Nasconde il pulsante dopo la generazione dei grafici
        
        
    def generate_report(self):
        """Genera un report e mostra un messaggio di conferma nel box della grafica."""
        # Aggiorna il messaggio iniziale nel box della grafica
        self.statistic_text.config(state='normal')  # Abilita il widget per la modifica
        self.statistic_text.delete(1.0, "end")  # Cancella il contenuto precedente
        self.statistic_text.insert("end", "Il report è stato generato sul desktop.")  # Inserisci il messaggio iniziale
        report_generator = ReportGenerator()
        report_generator.generate_report()  # Genera il report

        
     

   
    