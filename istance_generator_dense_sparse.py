import random
import gc
from subset_sum_calculator_for_analysis import SubsetSumSolver
from dense_sparse_DB_handler import DenseSparseDBHandler

class SubsetInstanceGenerator:
    def __init__(self, num_instances, min_size, max_size, max_value, is_partition=False):
        """
        Inizializza il generatore di istanze.

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
        """Genera un'istanza densa o sparsa in base alla densità specificata."""
        if density == 'dense':
            max_element = self.max_value // 10
        else:
            max_element = self.max_value

        # Genera l'insieme S utilizzando un generatore per ridurre il consumo di memoria
        S = [random.randint(1, max_element) for _ in range(size)]
        total_sum = sum(S)
        if self.is_partition:
            target = total_sum // 2 
            #se il parametro is_partition è impostato su True, il valore di target viene
            # impostato come metà della somma degli elementi del set S.
        else:
            target = int(random.uniform(0.4, 0.6) * total_sum) 
           #Se is_partition è False, il valore di target viene impostato in modo casuale,
        # scegliendo un valore tra il 40% e il 60% della somma totale degli elementi del set S:
        return S, target

    def run_subset_sum_algorithms(self):
        """Esegue gli algoritmi su tutte le istanze generate e salva i risultati nel database."""
        try:
            for density in ['dense', 'sparse']:
                for _ in range(self.num_instances):
                    size = random.randint(self.min_size, self.max_size)
                    S, target = self.generate_instance(size, density)
                    solver = SubsetSumSolver(S, target)

                    # Esegui e salva i risultati per ciascun algoritmo
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
                            # Gestisci errori specifici dell'algoritmo senza interrompere il processo
                            print(f"Errore durante l'esecuzione di {algorithm_method.__name__}: {e}")
                    
                    # Libera esplicitamente la memoria utilizzata
                    del S, target, solver
                    gc.collect()  # Chiama il Garbage Collector per liberare la memoria non più usata

        finally:
            # Chiude la connessione al database al termine o in caso di errore
            self.db_handler.close()
