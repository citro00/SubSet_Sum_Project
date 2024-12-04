from pymongo import MongoClient

class MongoDBHandler:
    """
    Questa classe gestisce le operazioni di base su un database MongoDB per la gestione delle istanze del problema subset sum, 
    come salvare, recuperare, contare e cancellare le istanze.
    """

    def __init__(self, db_name='subset_sum_db'):
        """
        Inizializza una connessione al server MongoDB e seleziona il database e la collezione specificata.
        
        :param db_name: Nome del database da utilizzare.
        """
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[db_name]
        self.collection = self.db['instances']

    def save_instance(self, S, T, execution_time, optimal_solution, algorithm):
        """
        Salva un'istanza nel database con le informazioni fornite (set, target, tempo di esecuzione, soluzione ottimale, algoritmo).
        
        :param S: Set di input.
        :param T: Target sum.
        :param execution_time: Tempo di esecuzione dell'algoritmo.
        :param optimal_solution: Soluzione ottimale trovata.
        :param algorithm: Nome dell'algoritmo utilizzato.
        """
        document = {
            'set': S,
            'target_sum': T,
            'execution_time': execution_time,
            'optimal_solution': optimal_solution,
            'algorithm': algorithm
        }
        self.collection.insert_one(document)
        
    def count_entries(self):
        """
        Restituisce il numero totale di documenti presenti nella collezione.
        """
        return self.collection.count_documents({})  

    def delete_all(self):
        """
        Elimina tutti i documenti dalla collezione.
        """
        self.collection.delete_many({})

    def get_all_entries(self):
        """
        Recupera tutte le istanze presenti nella collezione e le restituisce come lista di documenti.
        """
        return list(self.collection.find({}))

    def get_instance_count(self):
        """
        Restituisce il conteggio totale delle istanze presenti nella collezione.
        """
        return self.count_entries()

    def close(self):
        """
        Chiude la connessione al server MongoDB.
        """
        self.client.close()
