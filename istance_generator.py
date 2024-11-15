import random
from subset_sum_calculator import SubsetSumSolver
from dense_sparse_DB_handler import DenseSparseDBHandler

class SubsetInstanceGenerator:
    def __init__(self, num_instances,target, s):
        self.size = s
        self.target = target
        self.num_instances = num_instances
        self.db_handler = DenseSparseDBHandler()

    def generate_instance(self, density):
        """Genera un'istanza basata sulla densità specificata ('dense' o 'sparse')."""
        if density == 'dense':
            base_value = random.randint(1, 10)
            S = [max(1, base_value + random.randint(-2, 2)) for _ in range(self.size)]
        elif density == 'sparse':
            S = sorted(random.randint(1, 100) for _ in range(self.size))
        else:
            raise ValueError("La densità deve essere 'dense' o 'sparse'.")
        return S, self.target

    def generate_instances(self):
        """Genera una lista di istanze dense e una lista di istanze sparse."""
        return (
            [self.generate_instance('dense') for _ in range(self.num_instances)],
            [self.generate_instance('sparse') for _ in range(self.num_instances)]
        )

    def run_subset_sum_algorithms(self):
        """Esegue i tre algoritmi su tutte le istanze generate e salva i risultati nel database."""
        dense_instances, sparse_instances = self.generate_instances()

        for density, instances in zip(['dense', 'sparse'], [dense_instances, sparse_instances]):
            for S, target in instances:
                solver = SubsetSumSolver(S, target)
            
                # Esegui e salva i risultati per ciascun algoritmo
                for algorithm, result in [
                    ("Dynamic Programming", solver.calculate_dynamic_programming()),
                    ("Meet-in-the-Middle", solver.calculate_meet_in_the_middle()),
                    ("Backtracking", solver.calculate_backtracking())
                ]:
                    
                    self.db_handler.save_instance(
                        S=S,
                        T=target,
                        instance_type=density,
                        execution_time=result[3],
                        optimal_solution=result[0],
                        algorithm=algorithm
                    )

        # Chiude la connessione al database al termine
        self.db_handler.close()
