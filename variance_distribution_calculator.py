from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

class VarianceDistributionCalculator:
    
    def __init__(self, db_handler, master=None):
        self.db_handler = db_handler 
        self.master = master  # Riferimento alla finestra principale

    def calculate_variance_and_distribution(self):
        """Calcola varianza, distribuzione e deviazione standard delle complessità per ciascun algoritmo."""
        entries = self.db_handler.get_all_entries()  # Recupera tutte le istanze
        algorithm_data = {'Dynamic Programming': [], 'Meet-in-the-Middle': [], 'Backtracking': []}

        for entry in entries:
            algorithm = entry.get('algorithm')
            execution_time = entry.get('execution_time')
            if algorithm in algorithm_data and execution_time is not None:
                algorithm_data[algorithm].append(execution_time)

        results = {}
        for algorithm, complexities in algorithm_data.items():
            if complexities:
                # Calcola varianza e deviazione standard
                variance = np.var(complexities)
                std_dev = np.std(complexities)

                # Calcola distribuzione degli insiemi S e T
                subsets = [entry.get('set') for entry in entries if entry.get('algorithm') == algorithm]
                targets = [entry.get('target_sum') for entry in entries if entry.get('algorithm') == algorithm]

                results[algorithm] = {
                    'variance': variance,
                    'standard_deviation': std_dev,
                    'subsets': subsets,
                    'targets': targets,
                    'complexities': complexities 
                }

            else:
                results[algorithm] = {
                    'variance': None,
                    'standard_deviation': None,
                    'subsets': [],
                    'targets': [],
                    'complexities': []
                }

        return results

    def plot_variance_distribution(self, canvas, algorithm, complexities):
        """Disegna la distribuzione della varianza nel canvas fornito."""
        # Crea un nuovo grafico per ogni algoritmo
        ax = canvas.figure.add_subplot(111)
        ax.clear()  # Cancella il grafico precedente
        ax.hist(complexities, bins=10, alpha=0.7, color='blue', label=algorithm)
        ax.set_title(f"Distribuzione della Varianza per {algorithm}")
        ax.set_xlabel("Tempo di esecuzione")
        ax.set_ylabel("Frequenza")
        ax.legend()

        canvas.draw()
