import numpy as np 
from statistics import mean, stdev
from collections import Counter
import matplotlib.pyplot as plt
from dense_sparse_DB_handler import DenseSparseDBHandler  

class AlgorithmEfficiencyAnalyzer:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def calculate_avg_execution_time(self):
        """Calcola il tempo di esecuzione medio per ciascun algoritmo su istanze dense e sparse."""
        dense_times = {algo: [] for algo in ['Dynamic Programming', 'Meet-in-the-Middle', 'Backtracking']}
        sparse_times = {algo: [] for algo in dense_times}
       
        dense_instances = self.db_handler.get_instances_by_type('dense')
        sparse_instances = self.db_handler.get_instances_by_type('sparse')

        for instance in dense_instances:
            algo = instance.get('algorithm')
            if algo in dense_times:
                dense_times[algo].append(instance['execution_time'])

        for instance in sparse_instances:
            algo = instance.get('algorithm')
            if algo in sparse_times:
                sparse_times[algo].append(instance['execution_time'])

        avg_times_dense = {algo: mean(times) for algo, times in dense_times.items() if times}
        avg_times_sparse = {algo: mean(times) for algo, times in sparse_times.items() if times}

        return avg_times_dense, avg_times_sparse

    def calculate_variance_and_std_dev(self):
        """Calcola la varianza e la deviazione standard dei tempi di esecuzione per ciascun algoritmo."""
        dense_times = {algo: [] for algo in ['Dynamic Programming', 'Meet-in-the-Middle', 'Backtracking']}
        sparse_times = {algo: [] for algo in dense_times}

        dense_instances = self.db_handler.get_instances_by_type('dense')
        sparse_instances = self.db_handler.get_instances_by_type('sparse')

        for instance in dense_instances:
            dense_times[instance['algorithm']].append(instance['execution_time'])
        for instance in sparse_instances:
            sparse_times[instance['algorithm']].append(instance['execution_time'])

        variance_std_dense = {algo: (np.var(times), stdev(times)) for algo, times in dense_times.items()}
        variance_std_sparse = {algo: (np.var(times), stdev(times)) for algo, times in sparse_times.items()}

        return variance_std_dense, variance_std_sparse

    def count_fastest_algorithm(self):
        """Conta la frequenza con cui ciascun algoritmo è il più veloce per ciascuna istanza in base al tipo."""
        dense_instances = self.db_handler.get_instances_by_type('dense')
        sparse_instances = self.db_handler.get_instances_by_type('sparse')
    
        dense_fastest = []
        sparse_fastest = []

        for instance in dense_instances:
            algo_times = {
                'Dynamic Programming': instance['execution_time'],
                'Meet-in-the-Middle': instance['execution_time'],
                'Backtracking': instance['execution_time']
            }
            dense_fastest.append(min(algo_times, key=algo_times.get))

        for instance in sparse_instances:
            algo_times = {
                'Dynamic Programming': instance['execution_time'],
                'Meet-in-the-Middle': instance['execution_time'],
                'Backtracking': instance['execution_time']
            }
            sparse_fastest.append(min(algo_times, key=algo_times.get))

        dense_count = Counter(dense_fastest)
        sparse_count = Counter(sparse_fastest)

        return dense_count, sparse_count

    def plot_execution_time_distribution(self):
        """Genera grafici di distribuzione dei tempi di esecuzione per ciascun algoritmo e tipo di istanza."""
        dense_times = {algo: [] for algo in ['Dynamic Programming', 'Meet-in-the-Middle', 'Backtracking']}
        sparse_times = {algo: [] for algo in dense_times}

        dense_instances = self.db_handler.get_instances_by_type('dense')
        sparse_instances = self.db_handler.get_instances_by_type('sparse')

        for instance in dense_instances:
            dense_times[instance['algorithm']].append(instance['execution_time'])
        for instance in sparse_instances:
            sparse_times[instance['algorithm']].append(instance['execution_time'])

        graphs = []
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle("Distribuzione dei Tempi di Esecuzione per Algoritmo e Tipo di Istanze")

        for i, (algo, times) in enumerate(dense_times.items()):
            axs[0, i].hist(times, bins=20, color='teal', alpha=0.7)
            axs[0, i].set_title(f'{algo} - Denso')
            axs[0, i].set_xlabel('Tempo di Esecuzione')
            axs[0, i].set_ylabel('Frequenza')
            axs[0, i].grid(axis='y', linestyle='--', alpha=0.7)
   
        
        for i, (algo, times) in enumerate(sparse_times.items()):
            axs[1, i].hist(times, bins=20, color='orange', alpha=0.7)
            axs[1, i].set_title(f'{algo} - Sparso')
            axs[1, i].set_xlabel('Tempo di Esecuzione')
            axs[1, i].set_ylabel('Frequenza')
            axs[1, i].grid(axis='y', linestyle='--', alpha=0.7)
            
        plt.subplots_adjust(hspace=0.20, wspace=0.20)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        graphs.append(fig)
        return graphs

    def evaluate_best_algorithm(self):
        """Determina la classifica degli algoritmi in base al execution_time per istanze dense e sparse."""
        dense_instances = self.db_handler.get_instances_by_type('dense')
        sparse_instances = self.db_handler.get_instances_by_type('sparse')

        dense_complexities = {algo: [] for algo in ['Dynamic Programming', 'Meet-in-the-Middle', 'Backtracking']}
        sparse_complexities = {algo: [] for algo in dense_complexities}

        for instance in dense_instances:
            total_complexity = instance['execution_time']
            dense_complexities[instance['algorithm']].append(total_complexity)
        for instance in sparse_instances:
            total_complexity = instance['execution_time']
            sparse_complexities[instance['algorithm']].append(total_complexity)

        avg_complexities_dense = {algo: mean(complexities) for algo, complexities in dense_complexities.items() if complexities}
        avg_complexities_sparse = {algo: mean(complexities) for algo, complexities in sparse_complexities.items() if complexities}

        sorted_dense = sorted(avg_complexities_dense.items(), key=lambda x: x[1])
        sorted_sparse = sorted(avg_complexities_sparse.items(), key=lambda x: x[1])

        return sorted_dense, sorted_sparse

    def run_analysis(self):
        """Esegui l'analisi completa e visualizza i risultati."""
        sorted_dense, sorted_sparse = self.evaluate_best_algorithm()
        avg_times_dense, avg_times_sparse = self.calculate_avg_execution_time()
        variance_std_dense, variance_std_sparse = self.calculate_variance_and_std_dev()

        return (avg_times_dense, avg_times_sparse,
                variance_std_dense, variance_std_sparse,
                self.count_fastest_algorithm()[0],  
                self.count_fastest_algorithm()[1], 
                sorted_dense, sorted_sparse)
