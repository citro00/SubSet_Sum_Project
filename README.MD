# **Subset Sum Problem**

## **Descrizione del Progetto**

Il progetto **Subset Sum Problem Analyzer** è uno strumento completo per l'analisi, la risoluzione e la visualizzazione di risultati relativi al problema del Subset Sum, un classico problema NP-completo. Questo progetto permette di:

- Generare e analizzare istanze dense e sparse del problema.
- Applicare e confrontare diversi algoritmi di risoluzione:
  - **Dynamic Programming**
  - **Meet-in-the-Middle**
  - **Backtracking**
- Calcolare statistiche dettagliate come medie, varianze e distribuzioni.
- Visualizzare i risultati con grafici e interfacce interattive.
- Generare report PDF per documentare i risultati.

## **Funzionalità Principali**

1. **Generazione di Istanze**:
   - Supporta la generazione di istanze dense e sparse personalizzabili.
   - Salva le istanze in un database MongoDB.

2. **Risoluzione del Problema**:
   - Implementazioni degli algoritmi con diverse tecniche di ottimizzazione.
   - Calcolo di soluzioni ottimali, tempi di esecuzione e altre metriche.

3. **Analisi Statistica**:
   - Calcolo di medie, varianze, deviazioni standard e distribuzioni dei risultati.
   - Confronto delle prestazioni degli algoritmi.

4. **Visualizzazione**:
   - Interfaccia grafica interattiva per la generazione e analisi delle istanze.
   - Grafici della distribuzione dei tempi di esecuzione e delle complessità.

5. **Generazione Report**:
   - Report PDF dettagliati che includono dati, analisi e grafici.

---

## **Struttura del Progetto**

### **1. Risoluzione del Problema**
- **`SubsetSumSolver`**:
  Implementazione degli algoritmi:
  - **Dynamic Programming**: Approccio tabulare per il calcolo delle soluzioni.
  - **Meet-in-the-Middle**: Dividi e combina per migliorare l'efficienza.
  - **Backtracking**: Approccio iterativo per evitare il limite di ricorsione.

### **2. Gestione del Database**
- **`MongoDBHandler`**:
  - Salvataggio e gestione delle istanze del problema in un database MongoDB.
  - Supporta il recupero di istanze dense, sparse e generiche.

- **`DenseSparseDBHandler`**:
  - Estensione per gestire istanze dense e sparse.

### **3. Generazione di Istanze**
- **`SubsetInstanceGenerator`**:
  - Generazione automatica di insiemi con caratteristiche personalizzabili.
  - Supporta istanze dense, sparse e partizionate.

### **4. Analisi Statistica**
- **`StatisticalAnalysis`**:
  - Calcolo di statistiche come medie, deviazioni standard e complessità.
  - Generazione di grafici riassuntivi.

- **`VarianceDistributionCalculator`**:
  - Calcolo di varianze, deviazioni standard e distribuzioni dei tempi di esecuzione.

### **5. Analisi dell'Efficienza**
- **`AlgorithmEfficiencyAnalyzer`**:
  - Analisi comparativa delle prestazioni degli algoritmi.
  - Calcolo del tempo medio, della varianza e del miglior algoritmo per ciascuna istanza.

### **6. Generazione Report**
- **`ReportGenerator`**:
  - Creazione di report PDF dettagliati con analisi, dati e grafici.

### **7. Interfacce Grafiche**
- **`SubsetSumGUI`**:
  - Interfaccia per risolvere il problema del Subset Sum con input personalizzati.
  - Mostra soluzioni, tempi di esecuzione e matrici di calcolo.

- **`StatisticalAnalysisGUI`**:
  - Interfaccia per analizzare statistiche e generare grafici.

---

## **Installazione**

### **Prerequisiti**
- **Python 3.8+**
- **MongoDB** (installato e configurato)
- Librerie Python necessarie:

  pip install numpy matplotlib reportlab pymongo tkinter

Esecuzione
Avvia il server MongoDB.
Esegui l'interfaccia principale con:
python main.py
Utilizzo
1. Interfaccia Grafica
Seleziona un algoritmo, inserisci un insieme e una somma target.
Avvia il calcolo per visualizzare risultati e tempi di esecuzione.
Analisi Statistica:
Genera istanze con parametri personalizzati.
Analizza le prestazioni degli algoritmi.
2. Generazione Report
Accedi all'opzione "Genera Report" nell'interfaccia.
Troverai il PDF generato sul desktop.
Architettura del Database
Collezione: instances
Campi:
set: L'insieme di numeri.
target_sum: Somma target.
execution_time: Tempo di esecuzione.
algorithm: Nome dell'algoritmo utilizzato.
optimal_solution: Soluzione ottimale trovata.