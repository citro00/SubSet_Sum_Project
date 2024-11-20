from itertools import combinations
from time import perf_counter
from collections import defaultdict

class SubsetSumSolver:
    def __init__(self, S, T):
        self.S = S
        self.T = T
        self.calculations = []
        self.operations = 0

    def calculate_dynamic_programming(self):
        """Risoluzione con Programmazione Dinamica."""
        start_time = perf_counter()
        n = len(self.S)
        dp = [[False] * (self.T + 1) for _ in range(n + 1)]
        
        for i in range(n + 1):
            dp[i][0] = True
            self.calculations.append(f"dp[{i}][0] = True (somma 0 sempre possibile)")
            self.operations += 1

        for i in range(1, n + 1):
            for t in range(1, self.T + 1):
                if self.S[i - 1] > t:
                    dp[i][t] = dp[i - 1][t]
                    self.calculations.append(f"dp[{i}][{t}] = dp[{i-1}][{t}] (Escludo {self.S[i-1]})")
                else:
                    dp[i][t] = dp[i - 1][t] or dp[i - 1][t - self.S[i - 1]]
                    action = f"Includo {self.S[i-1]}" if dp[i - 1][t - self.S[i - 1]] else f"Escludo {self.S[i-1]}"
                    self.calculations.append(f"dp[{i}][{t}] = {dp[i][t]} ({action})")
                self.operations += 1

        execution_time = perf_counter() - start_time
        optimal_solution = self.find_solution(dp, self.S, self.T)
        return optimal_solution, self.calculations, self.operations, execution_time, dp

    def calculate_meet_in_the_middle(self):
        """Risoluzione con Meet-in-the-Middle."""
        start_time = perf_counter()

        def get_subset_sums(arr):
            subset_sums = defaultdict(list)
            for r in range(len(arr) + 1):
                for subset in combinations(arr, r):
                    subset_sum = sum(subset)
                    subset_sums[subset_sum].append(subset)
            return subset_sums

        mid = len(self.S) // 2
        first_half = self.S[:mid]
        second_half = self.S[mid:]
        sum_first_half = get_subset_sums(first_half)
        sum_second_half = get_subset_sums(second_half)
        second_half_sums = set(sum_second_half.keys())

        self.operations = 0
        self.calculations.append(f"Somme sottoinsieme della prima metà: {list(sum_first_half.keys())}")
        self.calculations.append(f"Somme sottoinsieme della seconda metà: {list(second_half_sums)}")

        for x in sum_first_half.keys():
            self.operations += 1
            y = self.T - x
            if y in second_half_sums:
                execution_time = perf_counter() - start_time
                self.calculations.append(f"Trova sottoinsieme con somma {y} in seconda metà")
                solution = list(sum_first_half[x][0]) + list(sum_second_half[y][0])  # Prendi il primo sottoinsieme valido
                return solution, self.calculations, self.operations, execution_time, []

            self.calculations.append(f"Controllo se esiste {y} per la somma {x}")

        execution_time = perf_counter() - start_time
        return [], self.calculations, self.operations, execution_time, []

    def calculate_backtracking(self):
        """Risoluzione con Backtracking."""
        start_time = perf_counter()
        S_sorted = sorted(self.S, reverse=True)  # Ordina in ordine decrescente per potatura efficace
        memo = {}

        def backtrack(i, current_sum, current_numbers):
            if current_sum == self.T:
                return True, current_numbers
            if i == len(S_sorted) or current_sum > self.T:
                return False, current_numbers
            
            # Usa memoization per evitare calcoli ripetuti
            key = (i, current_sum)
            if key in memo:
                return False, current_numbers
            memo[key] = True
            
            self.operations += 1

            # Prova a includere l'elemento corrente
            include = backtrack(i + 1, current_sum + S_sorted[i], current_numbers + [S_sorted[i]])
            if include[0]:
                self.calculations.append(f"Includo {S_sorted[i]}: {include[1]}")
                return include

            # Prova a escludere l'elemento corrente
            exclude = backtrack(i + 1, current_sum, current_numbers)
            self.calculations.append(f"Escludo {S_sorted[i]}")
            return exclude

        result = backtrack(0, 0, [])
        execution_time = perf_counter() - start_time
        return result[1], self.calculations, self.operations, execution_time, []

    @staticmethod
    def binary_search(arr, x):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == x:
                return True
            elif arr[mid] < x:
                left = mid + 1
            else:
                right = mid - 1
        return False

    @staticmethod
    def find_solution(dp, S, T):
        solution = []
        n = len(S)
        
        if not dp[n][T]:
            return solution
        
        for i in range(n, 0, -1):
            if dp[i][T] and not dp[i - 1][T]:
                solution.append(S[i - 1])
                T -= S[i - 1]

        return solution
