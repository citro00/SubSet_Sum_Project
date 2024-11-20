import random
import logging
import gc
from subset_sum_calculator_for_analysis import SubsetSumSolver
from mongo_DB_handler import MongoDBHandler

class SubsetInstanceGeneratorWithS:
    def __init__(self, num_instances, target, s, seed=None):
        self.num_instances = num_instances
        self.target = target
        self.s = s
        self.seed = seed

        if self.seed is not None:
            random.seed(self.seed)

        self.db_handler = MongoDBHandler()  

        # Configura il logger
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_instance(self):
        """Genera un'istanza con s elementi casuali e un target dato."""
        S = [random.randint(1, 10000) for _ in range(self.s)]
        return S, self.target

    def run_subset_sum_algorithms(self):
        """Esegue gli algoritmi e salva i risultati nel database."""
        try:
            for i in range(self.num_instances):
                S, target = self.generate_instance()  # Genera l'istanza
                solver = SubsetSumSolver(S, target)

                algorithms = [
                    ("Dynamic Programming", solver.calculate_dynamic_programming),
                    ("Backtracking", solver.calculate_backtracking),
                    ("Meet In The Middle", solver.calculate_meet_in_the_middle),
                ]

                for algorithm_name, algorithm_method in algorithms:
                    try:
                        optimal_solution, execution_time = algorithm_method()

                        self.db_handler.save_instance(
                            S=S,
                            T=target,
                            execution_time=execution_time,
                            optimal_solution=optimal_solution,
                            algorithm=algorithm_name
                        )
                    except Exception as e:
                        self.logger.error(f"Errore durante l'esecuzione di {algorithm_name}: {e}")
                        continue  # Passa all'algoritmo successivo

  
                del S, target, solver
                gc.collect()  # Chiama il Garbage Collector per liberare la memoria non più usata

        finally:
            self.db_handler.close()  # Chiudi la connessione al database
