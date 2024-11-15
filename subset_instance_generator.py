import random
from subset_sum_calculator import SubsetSumSolver
from mongo_DB_handler import MongoDBHandler 

class SubsetInstanceGeneratorWithS:
    def __init__(self, num_instances, target, s):
        self.num_instances = num_instances
        self.target = target
        self.s = s

        self.db_handler = MongoDBHandler()  # Connessione al database MongoDB


    def generate_instance(self):
        """Genera un'istanza con s elementi casuali e un target dato."""
        S = [random.randint(1, 10) for _ in range(self.s)]
        return S, self.target

    def run_subset_sum_algorithms(self):
        """Esegue i tre algoritmi su tutte le istanze generate e salva i risultati nel database."""
        for i in range(self.num_instances):
            S, target = self.generate_instance()  # Genera l'istanza
            
            solver = SubsetSumSolver(S, target)
            
            # Esegui e salva i risultati per ciascun algoritmo
            for algorithm, result in [
                ("Dynamic Programming", solver.calculate_dynamic_programming()),
                ("Meet-in-the-Middle", solver.calculate_meet_in_the_middle()),
                ("Backtracking", solver.calculate_backtracking())
            ]:
   
                optimal_solution = result[0] 
                execution_time = result[3]  
               
            
                self.db_handler.save_instance(
                    S=S,
                    T=target,
                    execution_time=execution_time,
                    optimal_solution=optimal_solution,
                    algorithm=algorithm
                )
        
        self.db_handler.close()  # Chiudi la connessione al database
