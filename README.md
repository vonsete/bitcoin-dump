# Bitcoin Analyzer 🪙

Script en Python para analizar wallets y transacciones de Bitcoin con información detallada en formato humano.

## Características

✅ Analiza direcciones de Bitcoin (wallets)
✅ Analiza transacciones individuales (TxID)
✅ Muestra balance, historial y UTXOs
✅ Información detallada de inputs/outputs
✅ Formato legible con emojis y colores
✅ Modo interactivo y por línea de comandos
✅ **Exportación a CSV** (inputs, outputs, resumen, transacciones)
✅ **Visualización gráfica de flujos** de transacciones con grafos interactivos
✅ Sistema multi-API con fallback automático

## Quick Start (Inicio Rápido)

```bash
# 1. Instalación automática (recomendado)
./install.sh

# 2. O instalación manual
pip3 install requests  # Solo requests es obligatorio
# matplotlib, networkx y pandas son opcionales (para visualización)

# 3. Probar las APIs
python3 test_apis.py

# 4. Analizar una transacción famosa (Bitcoin Pizza)
python3 bitcoin_analyzer.py a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d

# 5. Con exportación CSV
python3 bitcoin_analyzer.py --csv 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

# 6. Con todo (CSV + visualización)
python3 bitcoin_analyzer.py -cv a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
```

## Instalación Detallada

### Opción 1: Script automático
```bash
chmod +x install.sh
./install.sh
```

### Opción 2: Manual con pip
```bash
pip3 install -r requirements.txt
```

### Opción 3: Paquetes del sistema (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3-requests python3-matplotlib python3-networkx python3-pandas
```

**Nota:** Solo `requests` es obligatorio. Las demás bibliotecas son opcionales para visualización.

## Uso

### Modo 1: Probar que las APIs funcionan

```bash
# Verificar el estado de todas las APIs
python test_apis.py
```

Este script probará todas las fuentes de datos y te mostrará cuáles están funcionando.

### Modo 2: Línea de comandos

```bash
# Analizar una dirección
python3 bitcoin_analyzer.py 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

# Analizar una transacción
python3 bitcoin_analyzer.py 4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b

# Analizar Y exportar a CSV
python3 bitcoin_analyzer.py --csv 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

# Analizar Y crear visualización gráfica (solo transacciones)
python3 bitcoin_analyzer.py --visualize a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d

# Analizar, exportar CSV Y crear gráfico (combinado)
python3 bitcoin_analyzer.py -cv a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d

# Ver ayuda completa
python3 bitcoin_analyzer.py --help
```

### Modo 3: Interactivo

```bash
python3 bitcoin_analyzer.py
```

Luego ingresa direcciones o TxIDs cuando se te solicite.

**Comandos especiales en modo interactivo:**
- `:csv ON` - Activar exportación automática a CSV
- `:csv OFF` - Desactivar exportación a CSV
- `:viz ON` - Activar visualización automática
- `:viz OFF` - Desactivar visualización
- `q` o `exit` - Salir

Ejemplo:
```
📝 Ingresa dirección Bitcoin o TxID: :csv ON
   💾 Exportación CSV: ✅ Activada

📝 Ingresa dirección Bitcoin o TxID: :viz ON
   📊 Visualización: ✅ Activada

📝 Ingresa dirección Bitcoin o TxID: a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
[Analiza, exporta CSV y crea gráfico automáticamente]
```

### Modo 4: Usar ejemplos predefinidos

El archivo `ejemplos.txt` contiene direcciones y transacciones famosas para probar:

```bash
# Ver ejemplos disponibles
cat ejemplos.txt

# Probar con la dirección de Satoshi
python bitcoin_analyzer.py 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

# Probar con la transacción de las pizzas
python bitcoin_analyzer.py a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
```

## Archivos Generados

### Exportación CSV para Transacciones:
Cuando usas `--csv` con una transacción, se generan 3 archivos:
- `tx_[hash]_inputs.csv` - Todos los inputs con direcciones y valores
- `tx_[hash]_outputs.csv` - Todos los outputs con direcciones, valores y estado (gastado/no gastado)
- `tx_[hash]_summary.csv` - Resumen con hash, fecha, tamaño, fees, etc.

### Exportación CSV para Direcciones:
Cuando usas `--csv` con una dirección, se generan 2 archivos:
- `addr_[address]_summary.csv` - Resumen con balance, total recibido/enviado, nº transacciones
- `addr_[address]_transactions.csv` - Listado completo de todas las transacciones

### Visualización Gráfica:
Cuando usas `--visualize` con una transacción, se genera:
- `tx_[hash]_flow.png` - Diagrama visual del flujo de la transacción
  - **Rojo**: Inputs (origen de fondos)
  - **Dorado**: Nodo central de transacción
  - **Verde**: Outputs no gastados (UTXOs disponibles)
  - **Azul**: Outputs ya gastados
  - Tamaño de nodos proporcional al valor en BTC

## Ejemplo de Salida

### Para una Dirección:
```
👛 INFORMACIÓN DE WALLET/DIRECCIÓN
================================================================================

📍 Dirección: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
💰 Balance actual: 0.00000000 BTC
📊 Total recibido: 68.90000000 BTC
📤 Total enviado: 68.90000000 BTC
🔢 Número de transacciones: 1234

📜 ÚLTIMAS TRANSACCIONES:
...
```

### Para una Transacción:
```
📝 INFORMACIÓN DE TRANSACCIÓN
================================================================================

🔗 Hash: 4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b
📦 Bloque: 125552
🕐 Fecha: 2011-05-22 18:16:31

📥 ENTRADAS:
...

📤 SALIDAS:
...

💰 RESUMEN:
  Total Entradas:  10.00000000 BTC
  Total Salidas:    9.99900000 BTC
  Fee (Comisión):   0.00100000 BTC
```

## APIs Utilizadas (Sistema de Fallback Multi-Fuente)

El script utiliza **múltiples APIs** con sistema de fallback automático:

### APIs Soportadas:
1. **Blockchain.info** (Principal)
   - `https://blockchain.info/rawtx/{tx_hash}`
   - `https://blockchain.info/rawaddr/{address}`

2. **Blockstream.info** (Backup 1)
   - `https://blockstream.info/api/tx/{tx_hash}`
   - `https://blockstream.info/api/address/{address}`

3. **Mempool.space** (Backup 2)
   - `https://mempool.space/api/tx/{tx_hash}`
   - `https://mempool.space/api/address/{address}`

4. **BlockCypher** (Backup 3)
   - `https://api.blockcypher.com/v1/btc/main/txs/{tx_hash}`
   - `https://api.blockcypher.com/v1/btc/main/addrs/{address}`

### Ventajas del Sistema Multi-Fuente:
✅ **Alta disponibilidad**: Si una API falla, automáticamente usa otra
✅ **Evita rate limits**: Distribuye las peticiones entre diferentes servicios
✅ **Normalización automática**: Unifica los formatos de diferentes APIs
✅ **Sin API keys**: Todas las fuentes son gratuitas y públicas

## Manejo de Errores y Rate Limits

El script detecta y maneja automáticamente varios tipos de errores:

### 🚫 Rate Limit Detectado
Cuando una API alcanza su límite de peticiones:
```
🚫 Rate limit alcanzado en Blockchain.info
🔍 Intentando con Blockstream.info...
✅ Datos obtenidos desde Blockstream.info
```

### ⏱️ Timeout
Si una API tarda mucho en responder:
```
⏱️  Timeout en Mempool.space
🔍 Intentando con BlockCypher...
```

### ❌ Error de Conexión
Si una API no está disponible:
```
❌ Error de conexión en Blockchain.info: Connection refused
🔍 Intentando con Blockstream.info...
```

### 🔄 Fallback Automático
El script siempre intentará con todas las fuentes disponibles hasta encontrar una que funcione.

## Archivos del Proyecto

```
bitcoin-dump/
├── bitcoin_analyzer.py (34 KB)  - ⭐ Script principal del analizador
├── test_apis.py (3.5 KB)        - 🧪 Verificador de estado de APIs
├── install.sh (1.6 KB)          - 📦 Script de instalación automática
├── requirements.txt             - 📋 Dependencias Python
├── README.md (7.2 KB)           - 📖 Documentación principal
├── EXAMPLES.md (6.0 KB)         - 📚 Guía de ejemplos avanzados
└── ejemplos.txt (1 KB)          - 💡 Direcciones/TXs famosas para testing
```

### Archivos generados durante el uso:
```
├── tx_[hash]_inputs.csv         - Inputs de transacción
├── tx_[hash]_outputs.csv        - Outputs de transacción
├── tx_[hash]_summary.csv        - Resumen de transacción
├── tx_[hash]_flow.png           - Gráfico visual de flujo
├── addr_[address]_summary.csv   - Resumen de dirección
└── addr_[address]_transactions.csv - Historial de transacciones
```

## Notas

- ✅ No requiere API keys (todas las APIs son gratuitas)
- ✅ El script intenta automáticamente con cada fuente si una falla
- ✅ Timeout de 15 segundos por petición
- ✅ Pausa de 1 segundo entre intentos de diferentes APIs
- ✅ Normalización automática de datos entre diferentes formatos de API
- ⚠️  Para uso muy intensivo, considera configurar API keys en BlockCypher
- ⚠️  Algunas APIs pueden tener límites de peticiones por hora/día
