from time import perf_counter
from bisect import bisect_left

class SubsetSumSolver:
    """
    Questa classe implementa tre metodi diversi per risolvere il problema del subset sum: Programmazione Dinamica, 
    Meet-in-the-Middle e Backtracking. Ciascun algoritmo è ottimizzato per situazioni diverse in termini di memoria e tempo.
    """

    def __init__(self, S, T):
        """
        Inizializza la classe con il set S e il target T.
        
        :param S: Lista di numeri interi che rappresentano il set.
        :param T: Somma target da raggiungere.
        """
        self.S = S
        self.T = T
    
    def calculate_dynamic_programming(self):
        """
        Risoluzione con Programmazione Dinamica utilizzando un approccio con set per ottimizzare memoria e tempo.
        La logica è quella di utilizzare un set per memorizzare tutte le somme raggiungibili durante l'iterazione attraverso gli elementi del set.
        Se viene trovata una somma uguale al target, la funzione termina restituendo la soluzione.
        
        :return: Lista degli elementi che sommano al target e il tempo di esecuzione.
        """
        reachable_sums = set()
        reachable_sums.add(0)
        prev = {0: []}

        start_time = perf_counter()
        for num in self.S:
            new_sums = set()
            new_prev = {}
            for s in reachable_sums:
                new_sum = s + num
                if new_sum <= self.T and new_sum not in reachable_sums:
                    new_sums.add(new_sum)
                    new_prev[new_sum] = prev[s] + [num]
            reachable_sums.update(new_sums)
            prev.update(new_prev)
            if self.T in reachable_sums:
                execution_time = perf_counter() - start_time
                return prev[self.T], execution_time
        
        execution_time = perf_counter() - start_time
        return [], execution_time   
    
    def calculate_meet_in_the_middle(self):
        """
        Risoluzione con Meet-in-the-Middle, un algoritmo adatto per set di grandi dimensioni dividendo il problema in due metà più piccole.
        La logica prevede di suddividere il set iniziale in due metà, calcolare tutte le possibili somme di sottoinsiemi per ciascuna metà, 
        e cercare se combinando somme dalle due metà è possibile raggiungere il target.
        
        :return: Lista degli elementi che sommano al target e il tempo di esecuzione.
        """
        n = len(self.S)
        mid = n // 2
        first_half = self.S[:mid]
        second_half = self.S[mid:]

        def get_subset_sums(arr):
            subset_sums = {}
            n = len(arr)
            for i in range(1 << n):
                s = 0
                subset = []
                for j in range(n):
                    if i & (1 << j):
                        s += arr[j]
                        subset.append(j)
                if s <= self.T:
                    subset_sums[s] = subset
            return subset_sums

        start_time = perf_counter()
        sum_first_half = get_subset_sums(first_half)
        sum_second_half = get_subset_sums(second_half)
        sum_second_half_keys = sorted(sum_second_half.keys())
        execution_time = perf_counter() - start_time

        for s in sum_first_half:
            target = self.T - s
            idx = bisect_left(sum_second_half_keys, target)
            if idx < len(sum_second_half_keys) and sum_second_half_keys[idx] == target:
                first_indices = sum_first_half[s]
                second_indices = sum_second_half[target]
                solution = self.reconstruct_solution_from_indices(first_half, first_indices, second_half, second_indices)
                return solution, execution_time

        return [], execution_time

    def reconstruct_solution_from_indices(self, first_half, first_indices, second_half, second_indices):
        """
        Ricostruisce la soluzione utilizzando gli indici memorizzati.
        
        :return: Lista degli elementi che sommano al target.
        """
        first_combination = [first_half[i] for i in first_indices]
        second_combination = [second_half[i] for i in second_indices]
        return first_combination + second_combination

    def calculate_backtracking(self):
        """
        Risoluzione con Backtracking iterativo per evitare il rischio di overflow della pila di chiamate ricorsive.
        La logica dell'algoritmo consiste nel provare ogni combinazione possibile degli elementi del set in modo iterativo, 
        ma applicando tecniche di potatura come l'ordinamento decrescente e il calcolo delle somme cumulative per ridurre 
        il numero di esplorazioni non necessarie.
        
        :return: Lista degli elementi che sommano al target e il tempo di esecuzione.
        """
        S_sorted = sorted(self.S, reverse=True)
        start_time = perf_counter()
        memo = {}
        stack = [(0, 0, [])]  # (indice, somma corrente, soluzione parziale)
        found_solution = None
        cumulative_sums = [0] * (len(S_sorted) + 1)
        for i in range(len(S_sorted) - 1, -1, -1):
            cumulative_sums[i] = cumulative_sums[i + 1] + S_sorted[i]

        while stack:
            i, current_sum, partial_solution = stack.pop()

            if current_sum == self.T:
                found_solution = partial_solution
                break

            if current_sum > self.T or i >= len(S_sorted):
                continue

            key = (i, current_sum)
            if key in memo:
                continue
            memo[key] = True

            if current_sum + cumulative_sums[i] < self.T:
                continue

            stack.append((i + 1, current_sum, partial_solution.copy()))
            stack.append((i + 1, current_sum + S_sorted[i], partial_solution + [S_sorted[i]]))

        execution_time = perf_counter() - start_time
        return found_solution if found_solution is not None else [], execution_time
