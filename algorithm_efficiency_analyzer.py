import numpy as np
from statistics import mean
from collections import Counter
import matplotlib.pyplot as plt
import hashlib

class AlgorithmEfficiencyAnalyzer:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.algorithm_names = ['Dynamic Programming', 'Meet In The Middle', 'Backtracking']

    def calculate_avg_execution_time(self):
        """Calcola il tempo di esecuzione medio per ciascun algoritmo su istanze dense e sparse."""
        dense_times = {algo: [] for algo in self.algorithm_names}
        sparse_times = {algo: [] for algo in self.algorithm_names}

        dense_instances = self.db_handler.get_instances_by_type('dense')
        sparse_instances = self.db_handler.get_instances_by_type('sparse')

        for instance in dense_instances:
            algo = instance.get('algorithm')
            exec_time = instance.get('execution_time')
            if algo in dense_times and exec_time is not None:
                dense_times[algo].append(exec_time)

        for instance in sparse_instances:
            algo = instance.get('algorithm')
            exec_time = instance.get('execution_time')
            if algo in sparse_times and exec_time is not None:
                sparse_times[algo].append(exec_time)

        avg_times_dense = {algo: mean(times) for algo, times in dense_times.items() if times}
        avg_times_sparse = {algo: mean(times) for algo, times in sparse_times.items() if times}

        return avg_times_dense, avg_times_sparse

    def calculate_variance_and_std_dev(self):
        """Calcola la varianza e la deviazione standard dei tempi di esecuzione per ciascun algoritmo."""
        dense_times = {algo: [] for algo in self.algorithm_names}
        sparse_times = {algo: [] for algo in self.algorithm_names}

        dense_instances = self.db_handler.get_instances_by_type('dense')
        sparse_instances = self.db_handler.get_instances_by_type('sparse')

        for instance in dense_instances:
            algo = instance.get('algorithm')
            exec_time = instance.get('execution_time')
            if algo in dense_times and exec_time is not None:
                dense_times[algo].append(exec_time)

        for instance in sparse_instances:
            algo = instance.get('algorithm')
            exec_time = instance.get('execution_time')
            if algo in sparse_times and exec_time is not None:
                sparse_times[algo].append(exec_time)

        variance_std_dense = {}
        for algo, times in dense_times.items():
            if len(times) > 1:
                var = np.var(times, ddof=1)
                std = np.std(times, ddof=1)
                variance_std_dense[algo] = (var, std)
            elif len(times) == 1:
                variance_std_dense[algo] = (0.0, 0.0)
            else:
                variance_std_dense[algo] = (None, None)

        variance_std_sparse = {}
        for algo, times in sparse_times.items():
            if len(times) > 1:
                var = np.var(times, ddof=1)
                std = np.std(times, ddof=1)
                variance_std_sparse[algo] = (var, std)
            elif len(times) == 1:
                variance_std_sparse[algo] = (0.0, 0.0)
            else:
                variance_std_sparse[algo] = (None, None)

        return variance_std_dense, variance_std_sparse

    def count_fastest_algorithm(self):
        """Conta la frequenza con cui ciascun algoritmo è il più veloce per ciascuna istanza in base al tipo."""
        dense_instances = self.db_handler.get_instances_by_type('dense')
        sparse_instances = self.db_handler.get_instances_by_type('sparse')

        dense_times_per_instance = {}
        sparse_times_per_instance = {}

        def get_instance_id(instance):
            S = instance['set']
            T = instance['target_sum']
            S_tuple = tuple(sorted(S))
            unique_str = str(S_tuple) + '_' + str(T)
            return hashlib.md5(unique_str.encode()).hexdigest()

        # Organizza i tempi per istanza e algoritmo
        for instance in dense_instances:
            instance_id = get_instance_id(instance)
            algo = instance.get('algorithm')
            exec_time = instance.get('execution_time')
            if algo in self.algorithm_names and exec_time is not None:
                if instance_id not in dense_times_per_instance:
                    dense_times_per_instance[instance_id] = {}
                dense_times_per_instance[instance_id][algo] = exec_time

        for instance in sparse_instances:
            instance_id = get_instance_id(instance)
            algo = instance.get('algorithm')
            exec_time = instance.get('execution_time')
            if algo in self.algorithm_names and exec_time is not None:
                if instance_id not in sparse_times_per_instance:
                    sparse_times_per_instance[instance_id] = {}
                sparse_times_per_instance[instance_id][algo] = exec_time

        dense_fastest = []
        sparse_fastest = []

        # Trova l'algoritmo più veloce per ogni istanza
        for times in dense_times_per_instance.values():
            if times and len(times) == len(self.algorithm_names):
                fastest_algo = min(times, key=times.get)
                dense_fastest.append(fastest_algo)

        for times in sparse_times_per_instance.values():
            if times and len(times) == len(self.algorithm_names):
                fastest_algo = min(times, key=times.get)
                sparse_fastest.append(fastest_algo)

        dense_count = Counter(dense_fastest)
        sparse_count = Counter(sparse_fastest)

        return dense_count, sparse_count

    def plot_execution_time_distribution(self):
        """Genera grafici di distribuzione dei tempi di esecuzione per ciascun algoritmo e tipo di istanza."""
        dense_times = {algo: [] for algo in self.algorithm_names}
        sparse_times = {algo: [] for algo in self.algorithm_names}

        dense_instances = self.db_handler.get_instances_by_type('dense')
        sparse_instances = self.db_handler.get_instances_by_type('sparse')

        for instance in dense_instances:
            algo = instance.get('algorithm')
            exec_time = instance.get('execution_time')
            if algo in dense_times and exec_time is not None:
                dense_times[algo].append(exec_time)

        for instance in sparse_instances:
            algo = instance.get('algorithm')
            exec_time = instance.get('execution_time')
            if algo in sparse_times and exec_time is not None:
                sparse_times[algo].append(exec_time)

        # Crea i grafici solo se ci sono dati
        graphs = []
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle("Distribuzione dei Tempi di Esecuzione per Algoritmo e Tipo di Istanze")

        for i, (algo, times) in enumerate(dense_times.items()):
            if times:
                axs[0, i].hist(times, bins=20, color='teal', alpha=0.7)
            axs[0, i].set_title(f'{algo} - Denso')
            axs[0, i].set_xlabel('Tempo di Esecuzione')
            axs[0, i].set_ylabel('Frequenza')
            axs[0, i].grid(axis='y', linestyle='--', alpha=0.7)

        for i, (algo, times) in enumerate(sparse_times.items()):
            if times:
                axs[1, i].hist(times, bins=20, color='orange', alpha=0.7)
            axs[1, i].set_title(f'{algo} - Sparso')
            axs[1, i].set_xlabel('Tempo di Esecuzione')
            axs[1, i].set_ylabel('Frequenza')
            axs[1, i].grid(axis='y', linestyle='--', alpha=0.7)

        plt.subplots_adjust(hspace=0.20, wspace=0.20)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        graphs.append(fig)
        return graphs

    def evaluate_best_algorithm(self, avg_times_dense, avg_times_sparse):
        """Determina la classifica degli algoritmi in base al tempo medio di esecuzione per istanze dense e sparse."""
        sorted_dense = sorted(avg_times_dense.items(), key=lambda x: x[1]) if avg_times_dense else []
        sorted_sparse = sorted(avg_times_sparse.items(), key=lambda x: x[1]) if avg_times_sparse else []

        return sorted_dense, sorted_sparse

    def run_analysis(self):
        """Esegui l'analisi completa e restituisci i risultati."""
        avg_times_dense, avg_times_sparse = self.calculate_avg_execution_time()

        sorted_dense, sorted_sparse = self.evaluate_best_algorithm(avg_times_dense, avg_times_sparse)

        variance_std_dense, variance_std_sparse = self.calculate_variance_and_std_dev()
        dense_count, sparse_count = self.count_fastest_algorithm()

        return (avg_times_dense, avg_times_sparse,
                variance_std_dense, variance_std_sparse,
                dense_count,
                sparse_count,
                sorted_dense, sorted_sparse)
