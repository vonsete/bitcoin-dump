# Changelog - Bitcoin Analyzer

## Versión 2.0 - Nueva Versión con Exportación y Visualización (2026-02-20)

### 🎉 Nuevas Funcionalidades Principales

#### 1. **Exportación a CSV** 📊
- ✅ Exportación completa de transacciones (inputs, outputs, resumen)
- ✅ Exportación de información de direcciones (balance, historial)
- ✅ Formato CSV compatible con Excel, LibreOffice, pandas
- ✅ Opción `--csv` o `-c` en línea de comandos
- ✅ Activación/desactivación en modo interactivo con `:csv ON/OFF`

**Archivos generados:**
- Para transacciones: 3 archivos CSV (inputs, outputs, summary)
- Para direcciones: 2 archivos CSV (summary, transactions)

#### 2. **Visualización Gráfica de Flujos** 🎨
- ✅ Gráficos de flujo de transacciones con NetworkX
- ✅ Visualización de inputs → transacción → outputs
- ✅ Código de colores:
  - 🔴 Rojo: Inputs (origen)
  - 🟡 Dorado: Transacción central
  - 🟢 Verde: Outputs no gastados (UTXO)
  - 🔵 Azul: Outputs gastados
- ✅ Tamaño de nodos proporcional al valor en BTC
- ✅ Opción `--visualize` o `-v` en línea de comandos
- ✅ Activación/desactivación en modo interactivo con `:viz ON/OFF`
- ✅ Genera archivos PNG de alta resolución (300 DPI)

#### 3. **Sistema Multi-API con Fallback** 🔄
- ✅ 4 APIs integradas:
  1. Blockchain.info (principal)
  2. Blockstream.info (backup 1)
  3. Mempool.space (backup 2)
  4. BlockCypher (backup 3)
- ✅ Cambio automático si una API falla o tiene rate limit
- ✅ Normalización automática de formatos entre APIs
- ✅ Detección inteligente de errores (timeout, rate limit, conexión)
- ✅ Mensajes informativos sobre qué API se está usando

#### 4. **Mejoras en la Interfaz** 💻
- ✅ Argumentos de línea de comandos con argparse
- ✅ Opción `--help` con ejemplos de uso
- ✅ Comandos especiales en modo interactivo
- ✅ Mensajes más claros y descriptivos
- ✅ Indicadores visuales de progreso

### 📦 Nuevos Archivos

- **install.sh** - Script de instalación automática
- **EXAMPLES.md** - Guía completa de ejemplos avanzados
- **CHANGELOG.md** - Este archivo
- **test_apis.py** - Mejorado para probar todas las APIs

### 🔧 Mejoras Técnicas

- ✅ Manejo robusto de errores HTTP
- ✅ Timeouts configurables (15 segundos)
- ✅ Pausas entre intentos de API para evitar rate limits
- ✅ Código modular y extensible
- ✅ Documentación completa en README y EXAMPLES
- ✅ Compatibilidad con Python 3.8+

### 📚 Documentación

- ✅ README.md actualizado con todas las nuevas funciones
- ✅ EXAMPLES.md con casos de uso reales
- ✅ Ejemplos de análisis en lote
- ✅ Guías de instalación para diferentes sistemas
- ✅ Consejos para evitar rate limits

---

## Versión 1.0 - Versión Inicial (2026-02-20)

### Funcionalidades Básicas

- ✅ Análisis de direcciones Bitcoin
- ✅ Análisis de transacciones
- ✅ Información detallada de inputs/outputs
- ✅ Balance y historial de direcciones
- ✅ Modo interactivo
- ✅ Detección automática de tipo (dirección vs transacción)
- ✅ Integración con Blockchain.info API

---

## Roadmap Futuro (Posibles Mejoras)

### Versión 2.1 (Planificada)
- [ ] Soporte para direcciones SegWit (bc1...)
- [ ] Caché local de consultas para reducir llamadas a API
- [ ] Exportación a JSON además de CSV
- [ ] Análisis de fee estimation
- [ ] Comparación entre múltiples transacciones

### Versión 2.2 (Ideas)
- [ ] Visualización de cadenas de transacciones (taint analysis)
- [ ] Gráficos de evolución de balance en el tiempo
- [ ] Detección de patrones sospechosos
- [ ] Integración con Lightning Network
- [ ] Dashboard web interactivo
- [ ] Soporte para otras criptomonedas (ETH, LTC, etc.)

### Versión 3.0 (Futuro)
- [ ] Base de datos local para análisis offline
- [ ] Machine Learning para detección de fraudes
- [ ] API REST propia
- [ ] GUI con Qt o Electron
- [ ] Modo servidor multi-usuario

---

## Contribuciones

Este proyecto es de código abierto. Las contribuciones son bienvenidas:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

---

## Agradecimientos

- Blockchain.info por su API pública
- Blockstream.info por su excelente infraestructura
- Mempool.space por su API rápida y confiable
- BlockCypher por su documentación detallada
- La comunidad de Bitcoin por hacer esto posible

---

## Licencia

MIT License - Uso libre para fines educativos y comerciales

---

## Contacto y Soporte

- Reporta bugs o sugiere mejoras creando un Issue
- Documenta problemas con ejemplos reproducibles
- Comparte tus casos de uso interesantes

**Happy Bitcoin Analysis! 🪙🚀**
