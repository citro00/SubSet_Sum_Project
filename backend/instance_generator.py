import random
import logging
import gc
from backend.subset_sum_calculator_for_analysis import SubsetSumSolver
from backend.mongo_DB_handler import MongoDBHandler

class SubsetInstanceGeneratorWithS:
    """
    Questa classe genera istanze del problema del subset sum utilizzando un numero fisso di elementi e un target, 
    esegue vari algoritmi per risolvere il problema e salva i risultati in un database.
    """

    def __init__(self, num_instances, target, s, seed=None):
        """
        Inizializza i parametri per la generazione delle istanze e configura il gestore del database.
        
        :param num_instances: Numero di istanze da generare.
        :param target: Valore target per il problema del subset sum.
        :param s: Numero di elementi nel set S.
        :param seed: Seed per la generazione casuale.
        """
        self.num_instances = num_instances
        self.target = target
        self.s = s
        self.seed = seed

        if self.seed is not None:
            random.seed(self.seed)

        self.db_handler = MongoDBHandler()  

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_instance(self):
        """
        Genera un'istanza del problema con un set di s elementi casuali e un target prestabilito.
        
        :return: Una tupla contenente il set S e il target T.
        """
        S = [random.randint(1, 10000) for _ in range(self.s)]
        return S, self.target

    def run_subset_sum_algorithms(self):
        """
        Esegue i vari algoritmi per risolvere il problema del subset sum sulle istanze generate e salva i risultati nel database.
        """
        try:
            for i in range(self.num_instances):
                S, target = self.generate_instance()
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
                        continue

                del S, target, solver
                gc.collect()
        finally:
            self.db_handler.close()
