from time import perf_counter
from bisect import bisect_left
class SubsetSumSolver:
    def __init__(self, S, T):
        self.S = S 
        self.T = T  
    
    def calculate_dynamic_programming(self):
        """Risoluzione con Programmazione Dinamica utilizzando set per ottimizzare memoria e tempo."""
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
        """Risoluzione con Meet-in-the-Middle ottimizzato per memoria e tempo."""
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
                    subset_sums[s] = subset  # Memorizza gli indici degli elementi
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
                # Soluzione trovata
                first_indices = sum_first_half[s]
                second_indices = sum_second_half[target]
                solution = self.reconstruct_solution_from_indices(first_half, first_indices, second_half, second_indices)
                return solution, execution_time

        return [], execution_time

    def reconstruct_solution_from_indices(self, first_half, first_indices, second_half, second_indices):
        """Ricostruisce la soluzione utilizzando gli indici memorizzati."""
        first_combination = [first_half[i] for i in first_indices]
        second_combination = [second_half[i] for i in second_indices]
        return first_combination + second_combination


    

    def calculate_backtracking(self):
        """Risoluzione con Backtracking iterativo per evitare l'overflow della ricorsione."""
        S_sorted = sorted(self.S, reverse=True)  # Ordina in ordine decrescente per potatura efficace

        start_time = perf_counter()
        memo = {}
        stack = []
        stack.append((0, 0, []))  # (indice, somma corrente, soluzione parziale)

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

            # Potatura: se la somma attuale più la somma massima possibile è inferiore al target, salta
            if current_sum + cumulative_sums[i] < self.T:
                continue

            # Prova a escludere l'elemento corrente
            stack.append((i + 1, current_sum, partial_solution.copy()))

            # Prova a includere l'elemento corrente
            stack.append((i + 1, current_sum + S_sorted[i], partial_solution + [S_sorted[i]]))

        execution_time = perf_counter() - start_time
        return found_solution if found_solution is not None else [], execution_time
