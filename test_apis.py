#!/usr/bin/env python3
"""
Script de prueba para verificar el estado de todas las APIs
"""

from bitcoin_analyzer import BitcoinAnalyzer
import sys


def test_all_apis():
    """Prueba todas las APIs disponibles"""
    analyzer = BitcoinAnalyzer()

    # Transacción de prueba (primera tx de Bitcoin)
    test_tx = "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16"

    # Dirección de prueba (Satoshi)
    test_addr = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

    print("="*80)
    print("🧪 PRUEBA DE APIS - Bitcoin Analyzer")
    print("="*80)

    # Probar APIs de transacciones
    print("\n📝 PROBANDO APIs DE TRANSACCIONES")
    print("-"*80)

    apis_tx = [
        ('Blockchain.info', analyzer.get_transaction_blockchain),
        ('Blockstream.info', analyzer.get_transaction_blockstream),
        ('Mempool.space', analyzer.get_transaction_mempool),
        ('BlockCypher', analyzer.get_transaction_blockcypher)
    ]

    tx_results = {}
    for name, method in apis_tx:
        print(f"\n🔍 Probando {name}...")
        try:
            result = method(test_tx)
            if result:
                tx_results[name] = "✅ OK"
                print(f"   Hash: {result.get('hash', 'N/A')[:16]}...")
            else:
                tx_results[name] = "❌ FALLO"
        except Exception as e:
            tx_results[name] = f"❌ ERROR: {str(e)[:30]}"
            print(f"   Error: {e}")

    # Probar APIs de direcciones
    print("\n\n👛 PROBANDO APIs DE DIRECCIONES")
    print("-"*80)

    apis_addr = [
        ('Blockchain.info', analyzer.get_address_blockchain),
        ('Blockstream.info', analyzer.get_address_blockstream),
        ('Mempool.space', analyzer.get_address_mempool),
        ('BlockCypher', analyzer.get_address_blockcypher)
    ]

    addr_results = {}
    for name, method in apis_addr:
        print(f"\n🔍 Probando {name}...")
        try:
            result = method(test_addr)
            if result:
                addr_results[name] = "✅ OK"
                balance = analyzer.format_btc(result.get('final_balance', 0))
                print(f"   Balance: {balance}")
            else:
                addr_results[name] = "❌ FALLO"
        except Exception as e:
            addr_results[name] = f"❌ ERROR: {str(e)[:30]}"
            print(f"   Error: {e}")

    # Resumen
    print("\n\n" + "="*80)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*80)

    print("\n📝 APIs de Transacciones:")
    for name, status in tx_results.items():
        print(f"   {name:20} {status}")

    print("\n👛 APIs de Direcciones:")
    for name, status in addr_results.items():
        print(f"   {name:20} {status}")

    # Contar éxitos
    tx_success = sum(1 for v in tx_results.values() if "✅" in v)
    addr_success = sum(1 for v in addr_results.values() if "✅" in v)

    print("\n" + "="*80)
    print(f"✅ APIs funcionando para transacciones: {tx_success}/{len(tx_results)}")
    print(f"✅ APIs funcionando para direcciones: {addr_success}/{len(addr_results)}")
    print("="*80 + "\n")

    if tx_success > 0 and addr_success > 0:
        print("🎉 Al menos una API está funcionando correctamente!")
        print("   El script debería funcionar sin problemas.\n")
        return 0
    else:
        print("⚠️  ADVERTENCIA: Ninguna API está respondiendo correctamente.")
        print("   Verifica tu conexión a internet.\n")
        return 1


if __name__ == "__main__":
    sys.exit(test_all_apis())
