from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

class VarianceDistributionCalculator:
    """
    Questa classe si occupa di calcolare la varianza, la deviazione standard e la distribuzione delle complessità degli algoritmi
    di subset sum, utilizzando dati memorizzati in un database. Permette anche la visualizzazione della distribuzione.
    """
    
    def __init__(self, db_handler, master=None):
        """
        Inizializza il gestore del database e, opzionalmente, un riferimento alla finestra principale per la visualizzazione.
        
        :param db_handler: Gestore del database MongoDB.
        :param master: Finestra principale per la visualizzazione (opzionale).
        """
        self.db_handler = db_handler
        self.master = master

    def calculate_variance_and_distribution(self):
        """
        Calcola la varianza, la deviazione standard e la distribuzione delle complessità per ciascun algoritmo.
        La logica utilizzata prevede il recupero dei tempi di esecuzione dal database, il calcolo delle statistiche e la raccolta
        degli insiemi di input per ciascun algoritmo.
        
        :return: Dizionario contenente la varianza, la deviazione standard, i sottoinsiemi e i target per ciascun algoritmo.
        """
        entries = self.db_handler.get_all_entries()
        algorithm_data = {'Dynamic Programming': [], 'Meet In The Middle': [], 'Backtracking': []}

        for entry in entries:
            algorithm = entry.get('algorithm')
            execution_time = entry.get('execution_time')
            if algorithm in algorithm_data and execution_time is not None:
                algorithm_data[algorithm].append(execution_time)

        results = {}
        for algorithm, complexities in algorithm_data.items():
            if complexities:
                variance = np.var(complexities)
                std_dev = np.std(complexities)
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
        """
        Disegna la distribuzione della varianza nel canvas fornito per un particolare algoritmo.
        La logica utilizzata prevede la creazione di un istogramma dei tempi di esecuzione per visualizzare la frequenza di ciascuna complessità.
        
        :param canvas: Oggetto di tipo Canvas per disegnare il grafico.
        :param algorithm: Nome dell'algoritmo per cui disegnare la distribuzione.
        :param complexities: Lista dei tempi di esecuzione per l'algoritmo specificato.
        """
        ax = canvas.figure.add_subplot(111)
        ax.clear()
        ax.hist(complexities, bins=10, alpha=0.7, color='blue', label=algorithm)
        ax.set_title(f"Distribuzione della Varianza per {algorithm}")
        ax.set_xlabel("Tempo di esecuzione")
        ax.set_ylabel("Frequenza")
        ax.legend()

        canvas.draw()
