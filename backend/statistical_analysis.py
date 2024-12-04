import matplotlib.pyplot as plt

class StatisticalAnalysis:
    """
    Questa classe si occupa di raccogliere e visualizzare statistiche sulle istanze del problema del subset sum, 
    categorizzando le istanze in base all'algoritmo utilizzato.
    """

    def __init__(self, db_handler):
        """
        Inizializza la classe con un gestore di database e carica tutte le istanze per analizzarle.
        
        :param db_handler: Gestore del database da cui recuperare le istanze.
        """
        self.db_handler = db_handler
        self.instances = self.db_handler.get_all_entries()
        self.dynamic_programming_instances = []
        self.meet_in_the_middle_instances = []
        self.backtracking_instances = []
        self.categorize_instances()

    def categorize_instances(self):
        """
        Categorizza le istanze in base all'algoritmo utilizzato (Dynamic Programming, Meet In The Middle, Backtracking).
        """
        for instance in self.instances:
            algorithm = instance['algorithm']
            if algorithm == "Dynamic Programming":
                self.dynamic_programming_instances.append(instance)
            elif algorithm == "Meet In The Middle":
                self.meet_in_the_middle_instances.append(instance)
            elif algorithm == "Backtracking":
                self.backtracking_instances.append(instance)

    def collect_statistics(self):
        """
        Raccoglie statistiche per ogni categoria di algoritmo e restituisce un dizionario contenente i risultati.
        
        :return: Dizionario con le statistiche di ogni algoritmo.
        """
        statistics = {}
        for algorithm, instances in zip(
            ["Dynamic Programming", "Meet In The Middle", "Backtracking"],
            [self.dynamic_programming_instances, self.meet_in_the_middle_instances, self.backtracking_instances]
        ):
            instance_count = len(instances)
            total_size = total_target = total_complexity = num_subsets_found = 0

            for instance in instances:
                S = instance['set']
                T = instance['target_sum']
                solution = instance['optimal_solution']
                execution_time = float(instance.get('execution_time', 0))

                num_subsets_found += len(solution) if solution else 0
                total_size += len(S)
                total_target += T
                total_complexity += execution_time

            if instance_count > 0:
                avg_size = total_size / instance_count
                avg_target = total_target / instance_count
                avg_complexity = total_complexity / instance_count
                
                statistics[algorithm] = {
                    "total_instances": instance_count,
                    "num_subsets_found": num_subsets_found,
                    "avg_size": avg_size,
                    "avg_target": avg_target,
                    "avg_complexity": avg_complexity,
                }
            else:
                statistics[algorithm] = {
                    "total_instances": 0,
                    "num_subsets_found": 0,
                    "avg_size": 0,
                    "avg_target": 0,
                    "avg_complexity": 0,
                }

        return statistics

    def plot_statistics(self, statistics):
        """
        Visualizza le statistiche raccolte in un grafico a barre per ciascun algoritmo.
        
        :param statistics: Dizionario contenente le statistiche da visualizzare.
        """
        algorithms = list(statistics.keys())
        avg_sizes = [statistics[alg]["avg_size"] for alg in algorithms]
        avg_targets = [statistics[alg]["avg_target"] for alg in algorithms]
        avg_complexities = [statistics[alg]["avg_complexity"] for alg in algorithms]

        x = range(len(algorithms))

        plt.figure(figsize=(12, 6))
        plt.bar(x, avg_sizes, width=0.2, label='Avg Size', align='center', color='skyblue')
        plt.bar([p + 0.2 for p in x], avg_targets, width=0.2, label='Avg Target', align='center', color='orange')
        plt.bar([p + 0.4 for p in x], avg_complexities, width=0.2, label='Avg Complexity', align='center', color='lightgreen')

        plt.xlabel('Algorithms')
        plt.ylabel('Values')
        plt.title('Statistics of Subset Sum Algorithms')
        plt.xticks([p + 0.2 for p in x], algorithms)
        plt.legend()
        plt.grid(axis='y')

        plt.show()
