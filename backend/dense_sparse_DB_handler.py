from pymongo import MongoClient, errors 

class DenseSparseDBHandler:
    """
    Questa classe gestisce l'interazione con un database MongoDB per salvare, recuperare, eliminare e contare le istanze di set densi e sparsi.
    """
    
    def __init__(self, db_name='subset_sum_db', collection_name='dense_sparse_instances'):
        """
        Inizializza una connessione al database MongoDB specificando il nome del database e della collezione.
        """
        try:
            self.client = MongoClient('localhost', 27017)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]  
        except errors.ConnectionFailure as e:
            print(f"Errore di connessione al database: {e}")

    def save_instance(self, S, T, instance_type, execution_time, optimal_solution, algorithm):
        """
        Salva un'istanza nel database con le informazioni fornite (set, target, tipo di istanza, tempo di esecuzione, soluzione ottimale, algoritmo).
        """
        document = {
            'set': S,
            'target_sum': T,
            'instance_type': instance_type,  
            'execution_time': execution_time,
            'optimal_solution': optimal_solution,
            'algorithm': algorithm
        }
        try:
            self.collection.insert_one(document)
        except errors.PyMongoError as e:
            print(f"Errore durante il salvataggio dell'istanza: {e}")
            
    def get_instances_by_type(self, instance_type):
        """
        Recupera tutte le istanze di un determinato tipo ('dense' o 'sparse') dal database.
        """
        return list(self.collection.find({"instance_type": instance_type}))
    
    def get_all_entries(self):
        """
        Recupera tutte le istanze dal database senza filtri.
        """
        return list(self.collection.find({}))

    def get_instance_count(self):
        """
        Restituisce il conteggio di tutte le istanze presenti nella collezione.
        """
        return self.collection.count_documents({})

    def delete_all(self):
        """
        Elimina tutte le istanze presenti nella collezione.
        """
        try:
            self.collection.delete_many({})
            print("Tutte le istanze sono state eliminate con successo.")
        except errors.PyMongoError as e:
            print(f"Errore durante l'eliminazione delle istanze: {e}")

    def close(self):
        """
        Chiude la connessione al database.
        """
        self.client.close()
