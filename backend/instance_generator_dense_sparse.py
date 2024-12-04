import random
import gc
from backend.subset_sum_calculator_for_analysis import SubsetSumSolver
from backend.dense_sparse_DB_handler import DenseSparseDBHandler

class SubsetInstanceGenerator:
    """
    Questa classe genera istanze di problemi del subset sum, le esegue con diversi algoritmi e salva i risultati in un database.
    """
    
    def __init__(self, num_instances, min_size, max_size, max_value, is_partition=False):
        """
        Inizializza i parametri per la generazione delle istanze.
        
        :param num_instances: Numero di istanze da generare.
        :param min_size: Dimensione minima del set.
        :param max_size: Dimensione massima del set.
        :param max_value: Valore massimo per un elemento del set.
        :param is_partition: Se True, imposta il target come metà della somma del set.
        """
        self.num_instances = num_instances
        self.min_size = min_size
        self.max_size = max_size
        self.max_value = max_value
        self.is_partition = is_partition
        self.db_handler = DenseSparseDBHandler()

    def generate_instance(self, size, density):
        """
        Genera un'istanza densa o sparsa in base alla densità specificata.
        
        :param size: Dimensione del set.
        :param density: Tipo di densità ('dense' o 'sparse').
        :return: Un tuple contenente il set S e il target T.
        """
        max_element = self.max_value // 10 if density == 'dense' else self.max_value
        S = [random.randint(1, max_element) for _ in range(size)]
        total_sum = sum(S)
        target = total_sum // 2 if self.is_partition else int(random.uniform(0.4, 0.6) * total_sum)
        return S, target

    def run_subset_sum_algorithms(self):
        """
        Esegue diversi algoritmi di subset sum su tutte le istanze generate e salva i risultati nel database.
        """
        try:
            for density in ['dense', 'sparse']:
                for _ in range(self.num_instances):
                    size = random.randint(self.min_size, self.max_size)
                    S, target = self.generate_instance(size, density)
                    solver = SubsetSumSolver(S, target)

                    for algorithm_method in [
                        solver.calculate_dynamic_programming,
                        solver.calculate_meet_in_the_middle,
                        solver.calculate_backtracking
                    ]:
                        try:
                            solution, exec_time = algorithm_method()
                            algorithm_name = algorithm_method.__name__.replace('calculate_', '').replace('_', ' ').title()
                            self.db_handler.save_instance(
                                S=S,
                                T=target,
                                instance_type=density,
                                execution_time=exec_time,
                                optimal_solution=solution,
                                algorithm=algorithm_name
                            )
                        except Exception as e:
                            print(f"Errore durante l'esecuzione di {algorithm_method.__name__}: {e}")
                    
                    del S, target, solver
                    gc.collect()
        finally:
            self.db_handler.close()
