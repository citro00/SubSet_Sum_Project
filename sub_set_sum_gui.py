import tkinter as tk
from tkinter import ttk, messagebox
from subset_sum_calculator import SubsetSumSolver
from mongo_DB_handler import MongoDBHandler
from statistical_analysis import StatisticalAnalysis 
from statistical_analysis_gui import StatisticalAnalysisGUI
from subset_instance_generator import SubsetInstanceGeneratorWithS
class SubsetSumGUI:
    def __init__(self, master):
        self.master = master
        master.title("Subset Sum Solver")
        master.configure(bg="#f0f0f5")  
        master.state("zoomed")
        self.frame = tk.Frame(master, bg="#f0f0f5", relief=tk.RAISED, borderwidth=2)
        self.frame.pack(padx=20, pady=20)
        
       # Frame per input generazione istanze
        self.input_frame = tk.Frame(self.frame, bg="#f0f0f5")
        self.input_frame.grid(row=8, columnspan=2, pady=10, sticky="se")  

        # Label e Entry per il numero di istanze
        tk.Label(self.input_frame, text="Quante istanze vuoi generare?", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.num_instances_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=5)
        self.num_instances_entry.pack(side=tk.LEFT, padx=5)
        
         # Label e Entry per il target
        tk.Label(self.input_frame, text="Grandezza insieme T:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.target_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=10)
        self.target_entry.pack(side=tk.LEFT, padx=5)

        # Label e Entry per l'insieme S
        tk.Label(self.input_frame, text="Grandezza insieme S :", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.insieme_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=30)
        self.insieme_entry.pack(side=tk.LEFT, padx=5)

        # Pulsante per generare le istanze
        self.generate_button = tk.Button(self.input_frame, text="Genera", command=self.generate_instances_from_input, bg="#1A5276", fg="white", font=("Arial", 14, "bold") )
        self.generate_button.pack(side=tk.LEFT, padx=10)


        self.label_set = tk.Label(self.frame, text="Inserisci l'insieme di numeri (separati da virgola):", bg="#f0f0f5", font=("Arial", 14))
        self.label_set.grid(row=0, column=0, sticky="w")

        self.entry_set = tk.Entry(self.frame, width=80, font=("Arial", 14))
        self.entry_set.grid(row=0, column=1, padx=5, pady=5)

        self.label_target = tk.Label(self.frame, text="Inserisci la somma target:", bg="#f0f0f5", font=("Arial", 14))
        self.label_target.grid(row=1, column=0, sticky="w")

        self.entry_target = tk.Entry(self.frame, width=80, font=("Arial", 14))
        self.entry_target.grid(row=1, column=1, padx=5, pady=5)

        self.label_algorithm = tk.Label(self.frame, text="Seleziona l'algoritmo:", bg="#f0f0f5", font=("Arial", 14))
        self.label_algorithm.grid(row=2, column=0, sticky="w")

        self.algorithm_options = ["Dynamic Programming", "Meet-in-the-Middle", "Backtracking"]
        self.selected_algorithm = tk.StringVar(value=self.algorithm_options[0])
        self.menu = ttk.Combobox(self.frame, textvariable=self.selected_algorithm, values=self.algorithm_options, font=("Arial", 14))
        self.menu.grid(row=2, column=1, padx=5, pady=5)

        self.button_solve = tk.Button(self.frame, text="Esegui", command=self.solve, bg="#1A5276", fg="white", font=("Arial", 14, "bold"))
        self.button_solve.grid(row=3, columnspan=2, pady=10)

        self.disable_graph_var = tk.BooleanVar(value=False)
        self.checkbox_disable_graph = tk.Checkbutton(self.frame, text="Disabilita Generazione Grafico", variable=self.disable_graph_var, bg="#f0f0f5", font=("Arial", 14, "bold"))
        self.checkbox_disable_graph.grid(row=4, columnspan=2, pady=5)

        self.button_frame = tk.Frame(self.frame, bg="#f0f0f5")
        self.button_frame.grid(row=5, columnspan=2, pady=10)

        self.button_delete_all = tk.Button(self.button_frame, text="Elimina Tutti gli Elementi dal DB", command=self.delete_all_entries, bg="#FF4C4C", fg="white", font=("Arial", 14, "bold"))
        self.button_delete_all.pack(side=tk.LEFT, padx=10)
        
        self.db_handler = MongoDBHandler()
        self.statistical_analysis = StatisticalAnalysis(self.db_handler)  
        
        self.button_statistical_analysis = tk.Button(self.button_frame, text="Analisi Statistiche", command=self.open_statistical_analysis, bg="#1A5276", fg="white", font=("Arial", 14, "bold"))
        self.button_statistical_analysis.pack(side=tk.LEFT, padx=10)
        
        self.output_frame = tk.Frame(self.frame, bg="#f0f0f5")
        self.output_frame.grid(row=6, columnspan=2, pady=10)

        self.output_text = tk.Text(self.output_frame, width=40, height=17, font=("Arial", 12), bg="#ffffff")
        self.output_text.pack(side=tk.LEFT, padx=5)

        self.calculation_box = tk.Text(self.output_frame, width=40, height=17, font=("Arial", 12), bg="#e7f1ff")
        self.calculation_box.pack(side=tk.LEFT, padx=5)

        self.separator = ttk.Separator(self.output_frame, orient="vertical")
        self.separator.pack(side=tk.LEFT, padx=10, fill=tk.Y)

        self.solution_frame = tk.Frame(self.frame, bg="#f0f0f5")
        self.solution_frame.grid(row=7, columnspan=2, pady=10)

        self.solution_label = tk.Label(self.solution_frame, text="Soluzioni Grafiche:", bg="#f0f0f5", font=("Arial", 14))
        self.solution_label.pack()

        self.matrix_frame = tk.Frame(self.solution_frame, bg="#f0f0f5")
        self.matrix_frame.pack(padx=5)

        self.update_statistical_analysis_button()

    def update_statistical_analysis_button(self):
        """Controlla il numero di istanze nel database e abilita/disabilita il pulsante per l'analisi statistica."""
        instance_count = self.db_handler.get_instance_count()  
        if instance_count >= 10:
            self.button_statistical_analysis.config(state=tk.NORMAL)
        else:
            self.button_statistical_analysis.config(state=tk.DISABLED)

    def solve(self):
        try:
            S = list(map(int, self.entry_set.get().split(',')))
            T = int(self.entry_target.get())
        except ValueError:
            messagebox.showerror("Errore di input", "Assicurati di inserire numeri validi.")
            return

        solver = SubsetSumSolver(S, T)
     
        if self.selected_algorithm.get() == "Dynamic Programming":
            result, calculations, operations, execution_time, matrix = solver.calculate_dynamic_programming()
        elif self.selected_algorithm.get() == "Meet-in-the-Middle":
            result, calculations, operations, execution_time, matrix = solver.calculate_meet_in_the_middle()
        elif self.selected_algorithm.get() == "Backtracking":
            result, calculations, operations, execution_time, matrix = solver.calculate_backtracking()

        
        optimal_solution_message = f"Algoritmo: {self.selected_algorithm.get()}\n" \
                                    f"Insieme S: {S}\n" \
                                    f"Somma Target T: {T}\n" \
                                    f"Soluzione Ottimale: {result if result else 'Nessuna soluzione'}\n" \
                                    f"Tempo di esecuzione: {execution_time:.10f} secondi\n"\

        messagebox.showinfo("Risultato Ottimale", optimal_solution_message)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Tempo di esecuzione: {execution_time:.10f} secondi\n")
        self.output_text.insert(tk.END, f"Operazioni: {operations}\n")

        self.calculation_box.delete(1.0, tk.END)
        self.calculation_box.insert(tk.END, "Calcoli:\n" + "\n".join(calculations) + "\n")

        self.db_handler.save_instance(S, T, execution_time, result, self.selected_algorithm.get())
        
        self.update_statistical_analysis_button()  # Verifica e aggiorna lo stato del pulsante

        if not self.disable_graph_var.get():
            self.display_matrix(matrix, S, T)

    def open_statistical_analysis(self):
        # Creazione di una nuova finestra per l'analisi statistica
        new_window = tk.Toplevel(self.master)
        StatisticalAnalysisGUI(new_window, self.statistical_analysis, self.db_handler) 

    def display_matrix(self, dp, S, T):
        # Rimuovi i widget esistenti nella matrice
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Intestazione per S e T
        header_label_S = tk.Label(self.matrix_frame, text="S \\ T", borderwidth=2, relief="solid", bg="#007bff", fg="white", font=("Arial", 12, "bold"), width=4)
        header_label_S.grid(row=0, column=0, padx=2, pady=2)

        # Intestazione per la somma target T
        for j in range(T + 1):
            header_label = tk.Label(self.matrix_frame, text=str(j), borderwidth=2, relief="solid", bg="#007bff", fg="white", font=("Arial", 12, "bold"), width=4)
            header_label.grid(row=0, column=j + 1, padx=2, pady=2)

        # Popolamento della matrice
        for i in range(1, len(S) + 1):
            header_label = tk.Label(self.matrix_frame, text=str(S[i - 1]), borderwidth=2, relief="solid", bg="#007bff", fg="white", font=("Arial", 12, "bold"), width=4)
            header_label.grid(row=i, column=0, padx=2, pady=2)

            for j in range(T + 1):
                value = dp[i][j]
                # Colorazione delle celle in base al valore
                if  value == 1:  # Supponiamo che 1 rappresenti parte della soluzione ottimale
                    value_label = tk.Label(self.matrix_frame, text=str(value), borderwidth=2, relief="solid", bg="lightgreen", width=4, font=("Arial", 12))
                else:
                    value_label = tk.Label(self.matrix_frame, text=str(value), borderwidth=2, relief="solid", bg="salmon", width=4, font=("Arial", 12))

                value_label.grid(row=i, column=j + 1, padx=2, pady=2)

        self.matrix_frame.config(borderwidth=2, relief="groove")

    def delete_all_entries(self):
        """Funzione per eliminare tutti gli elementi dal database."""
        if messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare tutti gli elementi dal database?"):
            self.db_handler.delete_all()
            messagebox.showinfo("Successo", "Tutti gli elementi sono stati eliminati dal database.")
            self.update_statistical_analysis_button()  # Aggiorna lo stato del pulsante per l'analisi statistica
            
    def generate_instances_from_input(self):
        try:
            # Recupera i valori dagli input
            num_instances = int(self.num_instances_entry.get())
            target = int(self.target_entry.get())
            s = int(self.insieme_entry.get())
            
            generator = SubsetInstanceGeneratorWithS(num_instances, target, s)
            generator.run_subset_sum_algorithms()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Successo {3* num_instances} soluzioni salvate nel database.\n")
        
        except ValueError:
            messagebox.showerror("Errore di input", "Assicurati di inserire valori numerici validi.")
