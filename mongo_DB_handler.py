from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, db_name='subset_sum_db'):
        # Connessione al server MongoDB
        self.client = MongoClient('localhost', 27017)  # Cambia l'host e la porta se necessario
        self.db = self.client[db_name]
        self.collection = self.db['instances']  # Nome della collection

    def save_instance(self, S, T, execution_time, optimal_solution, algorithm):
        # Crea un documento da inserire
        document = {
            'set': S,
            'target_sum': T,
            'execution_time': execution_time,
            'optimal_solution': optimal_solution,
            'algorithm': algorithm
        }
        # Inserisci il documento nella collection
        self.collection.insert_one(document)
        
    def count_entries(self):
        # Restituisce il numero totale di documenti nella collezione
        return self.collection.count_documents({})  # Ritorna il conteggio dei documenti

    def delete_all(self):
        # Elimina tutti i documenti dalla collezione
        self.collection.delete_many({})

    def get_all_entries(self):
        """Recupera tutte le istanze dalla collezione."""
        return list(self.collection.find({}))  # Restituisce una lista di documenti

    def get_instance_count(self):
        # Restituisce il conteggio delle istanze
        return self.count_entries()

    def close(self):
        self.client.close()
