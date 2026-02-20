# Ejemplos de Uso Avanzado - Bitcoin Analyzer

## Tabla de Contenidos
1. [Análisis Básico](#análisis-básico)
2. [Exportación CSV](#exportación-csv)
3. [Visualización Gráfica](#visualización-gráfica)
4. [Modo Interactivo](#modo-interactivo)
5. [Análisis en Lote](#análisis-en-lote)

---

## Análisis Básico

### Analizar la dirección de Satoshi Nakamoto
```bash
python3 bitcoin_analyzer.py 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
```

**Resultado:**
- Balance actual: 57+ BTC
- Más de 56,000 transacciones
- Nunca se ha gastado nada

### Analizar la transacción de las Bitcoin Pizzas
```bash
python3 bitcoin_analyzer.py a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
```

**Resultado:**
- 10,000 BTC pagados por 2 pizzas
- 131 inputs consolidados
- Fee de 0.99 BTC

---

## Exportación CSV

### Exportar transacción a CSV
```bash
python3 bitcoin_analyzer.py --csv a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
```

**Archivos generados:**
- `tx_a1075db55d416d3c_inputs.csv` - Todos los 131 inputs con direcciones y valores
- `tx_a1075db55d416d3c_outputs.csv` - Output de 10,000 BTC
- `tx_a1075db55d416d3c_summary.csv` - Resumen completo

### Exportar dirección a CSV
```bash
python3 bitcoin_analyzer.py --csv 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
```

**Archivos generados:**
- `addr_1A1zP1eP5QGefi2D_summary.csv` - Balance y estadísticas
- `addr_1A1zP1eP5QGefi2D_transactions.csv` - Historial de transacciones

### Análisis posterior con pandas

```python
import pandas as pd

# Leer CSV de inputs
inputs = pd.read_csv('tx_a1075db55d416d3c_inputs.csv')

# Calcular total de inputs
total = inputs['Value_BTC'].sum()
print(f"Total inputs: {total} BTC")

# Agrupar por dirección única
by_address = inputs.groupby('Address')['Value_BTC'].sum()
print(by_address)
```

---

## Visualización Gráfica

### Crear gráfico de flujo de transacción
```bash
python3 bitcoin_analyzer.py --visualize a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
```

**Resultado:**
- Genera: `tx_a1075db55d416d3c_flow.png`
- Muestra inputs (rojo) → transacción (dorado) → outputs (verde/azul)
- Tamaño de nodos proporcional al valor

### Combinar análisis, CSV y visualización
```bash
python3 bitcoin_analyzer.py -cv a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
```

**Resultado:**
- Muestra información en pantalla
- Exporta 3 archivos CSV
- Genera gráfico PNG

---

## Modo Interactivo

### Iniciar modo interactivo
```bash
python3 bitcoin_analyzer.py
```

### Activar funciones automáticamente
```
📝 Ingresa dirección Bitcoin o TxID: :csv ON
   💾 Exportación CSV: ✅ Activada

📝 Ingresa dirección Bitcoin o TxID: :viz ON
   📊 Visualización: ✅ Activada

📝 Ingresa dirección Bitcoin o TxID: a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
[Analiza, exporta CSV y crea gráfico automáticamente]

📝 Ingresa dirección Bitcoin o TxID: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
[Analiza y exporta CSV automáticamente]

📝 Ingresa dirección Bitcoin o TxID: :csv OFF
   💾 Exportación CSV: ❌ Desactivada

📝 Ingresa dirección Bitcoin o TxID: q
👋 ¡Hasta luego!
```

---

## Análisis en Lote

### Crear script para analizar múltiples transacciones

```bash
#!/bin/bash
# analyze_batch.sh

# Lista de transacciones históricas
txs=(
    "a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d"  # Pizza
    "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16"  # Primera tx
    "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"  # Otra famosa
)

for tx in "${txs[@]}"; do
    echo "Analizando: $tx"
    python3 bitcoin_analyzer.py --csv --visualize "$tx"
    sleep 2  # Pausa para evitar rate limits
done

echo "✅ Análisis completado para ${#txs[@]} transacciones"
```

### Ejecutar análisis en lote
```bash
chmod +x analyze_batch.sh
./analyze_batch.sh
```

---

## Consejos y Trucos

### 1. Evitar Rate Limits
```bash
# Espera entre consultas
for addr in $(cat addresses.txt); do
    python3 bitcoin_analyzer.py "$addr"
    sleep 5  # Pausa de 5 segundos
done
```

### 2. Organizar archivos CSV
```bash
# Crear directorio para exports
mkdir -p exports
mv tx_*.csv addr_*.csv exports/
```

### 3. Ver ayuda completa
```bash
python3 bitcoin_analyzer.py --help
```

### 4. Verificar APIs disponibles
```bash
python3 test_apis.py
```

---

## Casos de Uso Reales

### Investigar transacción sospechosa
```bash
# 1. Analizar transacción
python3 bitcoin_analyzer.py --csv [TX_HASH]

# 2. Revisar CSV de outputs
cat tx_*_outputs.csv

# 3. Analizar direcciones receptoras
python3 bitcoin_analyzer.py --csv [DIRECCION_OUTPUT]
```

### Auditoría de dirección corporativa
```bash
# Exportar todo a CSV para análisis detallado
python3 bitcoin_analyzer.py --csv [DIRECCION_EMPRESA]

# Importar en Excel/LibreOffice para reportes
```

### Investigación forense
```bash
# Analizar y visualizar
python3 bitcoin_analyzer.py -cv [TX_SOSPECHOSA]

# El gráfico muestra visualmente el flujo de fondos
```

---

## Limitaciones y Consideraciones

⚠️ **Rate Limits**: Las APIs públicas tienen límites
- Usa pausas entre consultas masivas
- El script rota automáticamente entre 4 APIs diferentes

⚠️ **Direcciones con muchas transacciones**:
- Blockchain.info puede limitar a primeras 50-100 transacciones
- Para análisis completo, considera APIs premium

⚠️ **Visualización**:
- Solo para transacciones (no direcciones)
- Limitada a primeros 20 inputs/outputs para claridad
- Requiere matplotlib y networkx instalados

---

## Recursos Adicionales

- **Blockchain Explorers**:
  - https://blockchain.info
  - https://blockstream.info
  - https://mempool.space

- **Documentación de APIs**:
  - Blockchain.info API: https://www.blockchain.com/api
  - BlockCypher API: https://www.blockcypher.com/dev/bitcoin/
  - Mempool.space API: https://mempool.space/docs/api

- **Herramientas complementarias**:
  - Bitcoin Core RPC para node local
  - Electrum para gestión de wallets
  - BTCPay Server para análisis de pagos
