# **Subset Sum Problem Analyzer **

## **Descrizione del Progetto**

Il progetto **Subset Sum Problem Analyzer** è uno strumento avanzato e completo per l'analisi, la risoluzione e la visualizzazione del problema del Subset Sum, un classico problema NP-completo. Questo strumento è progettato per:

- Generare e analizzare istanze del problema in configurazioni dense e sparse.
- Applicare e confrontare diverse tecniche di risoluzione, inclusi:
  - **Dynamic Programming**
  - **Meet-in-the-Middle**
  - **Backtracking**
- Calcolare statistiche dettagliate, come medie, varianze e distribuzioni dei risultati.
- Fornire visualizzazioni interattive e grafiche per un'analisi immediata.
- Generare report PDF esaustivi per documentare i risultati e le prestazioni.

## **Funzionalità Principali**

1. **Generazione di Istanze**:
   - Supporto alla generazione di istanze personalizzabili (dense e sparse).
   - Salvataggio delle istanze in un database MongoDB per consentire una gestione organizzata e duratura.

2. **Risoluzione del Problema**:
   - Implementazione di algoritmi efficienti, ottimizzati per diverse tipologie di istanze.
   - Calcolo delle soluzioni ottimali con metriche di performance dettagliate.

3. **Analisi Statistica**:
   - Calcolo di parametri statistici fondamentali come medie, varianze e deviazioni standard.
   - Confronto diretto delle prestazioni dei diversi algoritmi.

4. **Visualizzazione**:
   - Interfaccia grafica interattiva per la generazione e l'analisi delle istanze.
   - Grafici rappresentativi dei tempi di esecuzione e delle complessità per fornire una visione chiara delle performance.

5. **Generazione Report**:
   - Generazione di report PDF dettagliati contenenti tutti i dati, grafici e analisi, per una facile condivisione e documentazione.

---

## **Struttura del Progetto**

### **1. Risoluzione del Problema**
- **`SubsetSumSolver`**: 
  Implementazione dei seguenti algoritmi:
  - **Dynamic Programming**: Approccio tabulare per una gestione efficace della risoluzione del problema.
  - **Meet-in-the-Middle**: Tecnica di suddivisione per migliorare l'efficienza computazionale.
  - **Backtracking**: Approccio iterativo per evitare il limite della profondità di ricorsione.

### **2. Gestione del Database**
- **`MongoDBHandler`**:
  - Gestione del salvataggio e recupero delle istanze nel database MongoDB.
  - Supporta operazioni su istanze dense, sparse e generiche.

- **`DenseSparseDBHandler`**:
  - Estensione specifica per la gestione separata delle istanze dense e sparse.

### **3. Generazione di Istanze**
- **`SubsetInstanceGenerator`**:
  - Generazione automatizzata di insiemi numerici con caratteristiche configurabili.
  - Supporto a vari tipi di istanze, tra cui dense, sparse e partizionate.

### **4. Analisi Statistica**
- **`StatisticalAnalysis`**:
  - Calcolo di statistiche come media, deviazione standard e complessità degli algoritmi.
  - Generazione di grafici per visualizzare le differenze tra i vari algoritmi.

- **`VarianceDistributionCalculator`**:
  - Calcolo di varianza e distribuzione dei tempi di esecuzione per fornire una misura della dispersione delle prestazioni.

### **5. Analisi dell'Efficienza**
- **`AlgorithmEfficiencyAnalyzer`**:
  - Analisi comparativa delle prestazioni degli algoritmi.
  - Calcolo di metriche fondamentali come il tempo medio, la varianza e la classifica dell'algoritmo più efficiente per ciascun tipo di istanza.

### **6. Generazione Report**
- **`ReportGenerator`**:
  - Creazione di report PDF contenenti dati dettagliati, grafici e analisi descrittive.
  - Report professionali per una facile consultazione e condivisione.

### **7. Interfacce Grafiche**
- **`SubsetSumGUI`**:
  - Interfaccia intuitiva per risolvere il problema del Subset Sum con input personalizzati.
  - Visualizzazione di soluzioni, tempi di esecuzione e matrici di calcolo per una maggiore comprensione dei risultati.

- **`StatisticalAnalysisGUI`**:
  - Interfaccia per esplorare in modo approfondito le statistiche e generare grafici di analisi.

---

## **Installazione**

### **Prerequisiti**
- **Python**: Versione 3.8 o superiore.
- **MongoDB**: Installato e configurato correttamente sul sistema.

### **Librerie necessarie**
Per installare le librerie Python richieste, utilizza il seguente comando:

```sh
pip install numpy matplotlib reportlab pymongo tkinter
```

### **Esecuzione**

1. Avvia il server MongoDB.
2. Esegui l'interfaccia principale con il seguente comando:

```sh
python main.py
```

---

## **Utilizzo**

### **Interfaccia Grafica**

#### **Calcolo Subset Sum**
- Seleziona uno degli algoritmi disponibili: Programmazione Dinamica, Meet-in-the-Middle o Backtracking.
- Inserisci l'insieme di numeri e la somma target.
- Avvia il calcolo per visualizzare le soluzioni trovate e il tempo di esecuzione.

#### **Analisi Statistica**
- Genera nuove istanze con parametri personalizzati per analisi più dettagliate.
- Confronta le prestazioni degli algoritmi attraverso grafici esplicativi e statistiche dettagliate.

### **Generazione Report**
- Accedi all'opzione "Genera Report" direttamente dall'interfaccia grafica.
- Il PDF generato sarà automaticamente salvato sul desktop, pronto per essere consultato.

---

## **Architettura del Database**

### **Collezione**
- **Nome**: `instances`
- **Nome**: `dense_sparse_instances`
### **Campi**
- `set`: L'insieme di numeri considerato.
- `target_sum`: Il valore della somma target.
- `solutions`: Le soluzioni trovate per l'istanza.
- `algorithm`: Algoritmo utilizzato per risolvere l'istanza.
- `execution_time`: Tempo impiegato per risolvere l'istanza.

---

## **Contributi**
Contributi e suggerimenti sono benvenuti per migliorare il progetto. Sentiti libero di fare una pull request o aprire un'issue per condividere le tue idee.
  }
  ]
}
