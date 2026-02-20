#!/usr/bin/env python3
"""
Bitcoin Wallet and Transaction Analyzer
Analiza wallets y transacciones de Bitcoin mostrando información detallada
Usa múltiples APIs con sistema de fallback automático
"""

import requests
import sys
from datetime import datetime
from typing import Dict, List, Optional
import time
import csv
import os
import argparse

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import networkx as nx
    import pandas as pd
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False


class BitcoinAnalyzer:
    def __init__(self):
        # Múltiples fuentes de datos
        self.apis = {
            'blockchain': 'https://blockchain.info',
            'blockcypher': 'https://api.blockcypher.com/v1/btc/main',
            'blockstream': 'https://blockstream.info/api',
            'mempool': 'https://mempool.space/api'
        }
        self.current_api = 'blockchain'
        self.timeout = 15

    def satoshi_to_btc(self, satoshi: int) -> float:
        """Convierte satoshis a BTC"""
        return satoshi / 100000000

    def format_timestamp(self, timestamp: int) -> str:
        """Formatea timestamp Unix a fecha legible"""
        if timestamp == 0:
            return "No confirmado"
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def format_btc(self, satoshi: int) -> str:
        """Formatea cantidad en BTC con símbolo"""
        btc = self.satoshi_to_btc(satoshi)
        return f"{btc:.8f} BTC"

    def make_request(self, url: str, api_name: str) -> Optional[Dict]:
        """Realiza una petición HTTP con manejo de errores"""
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"⏱️  Timeout en {api_name}")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"🚫 Rate limit alcanzado en {api_name}")
            else:
                print(f"❌ Error HTTP {e.response.status_code} en {api_name}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión en {api_name}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado en {api_name}: {e}")
            return None

    def get_transaction_blockchain(self, tx_hash: str) -> Optional[Dict]:
        """Obtiene transacción desde Blockchain.info"""
        url = f"{self.apis['blockchain']}/rawtx/{tx_hash}"
        print(f"🔍 Intentando con Blockchain.info...")
        data = self.make_request(url, 'Blockchain.info')
        if data:
            print(f"✅ Datos obtenidos desde Blockchain.info")
        return data

    def get_transaction_blockstream(self, tx_hash: str) -> Optional[Dict]:
        """Obtiene transacción desde Blockstream.info y la normaliza"""
        url = f"{self.apis['blockstream']}/tx/{tx_hash}"
        print(f"🔍 Intentando con Blockstream.info...")
        data = self.make_request(url, 'Blockstream.info')

        if not data:
            return None

        print(f"✅ Datos obtenidos desde Blockstream.info")

        # Normalizar formato a blockchain.info
        normalized = {
            'hash': data['txid'],
            'size': data['size'],
            'weight': data['weight'],
            'time': data.get('status', {}).get('block_time', 0),
            'block_height': data.get('status', {}).get('block_height'),
            'inputs': [],
            'out': []
        }

        # Normalizar inputs
        for inp in data.get('vin', []):
            prev_out = {
                'value': inp.get('prevout', {}).get('value', 0),
                'addr': inp.get('prevout', {}).get('scriptpubkey_address', 'N/A'),
                'type': inp.get('prevout', {}).get('scriptpubkey_type', 'N/A')
            }
            normalized['inputs'].append({'prev_out': prev_out})

        # Normalizar outputs
        for out in data.get('vout', []):
            output = {
                'value': out.get('value', 0),
                'addr': out.get('scriptpubkey_address', 'N/A'),
                'type': out.get('scriptpubkey_type', 'N/A'),
                'spent': out.get('status', {}).get('spent', False)
            }
            normalized['out'].append(output)

        return normalized

    def get_transaction_mempool(self, tx_hash: str) -> Optional[Dict]:
        """Obtiene transacción desde Mempool.space y la normaliza"""
        url = f"{self.apis['mempool']}/tx/{tx_hash}"
        print(f"🔍 Intentando con Mempool.space...")
        data = self.make_request(url, 'Mempool.space')

        if not data:
            return None

        print(f"✅ Datos obtenidos desde Mempool.space")

        # Normalizar formato
        normalized = {
            'hash': data['txid'],
            'size': data['size'],
            'weight': data['weight'],
            'time': data.get('status', {}).get('block_time', 0),
            'block_height': data.get('status', {}).get('block_height'),
            'inputs': [],
            'out': []
        }

        # Normalizar inputs
        for inp in data.get('vin', []):
            prev_out = {
                'value': inp.get('prevout', {}).get('value', 0),
                'addr': inp.get('prevout', {}).get('scriptpubkey_address', 'N/A'),
                'type': inp.get('prevout', {}).get('scriptpubkey_type', 'N/A')
            }
            normalized['inputs'].append({'prev_out': prev_out})

        # Normalizar outputs
        for out in data.get('vout', []):
            output = {
                'value': out.get('value', 0),
                'addr': out.get('scriptpubkey_address', 'N/A'),
                'type': out.get('scriptpubkey_type', 'N/A'),
                'spent': out.get('status', {}).get('spent', False)
            }
            normalized['out'].append(output)

        return normalized

    def get_transaction_blockcypher(self, tx_hash: str) -> Optional[Dict]:
        """Obtiene transacción desde BlockCypher y la normaliza"""
        url = f"{self.apis['blockcypher']}/txs/{tx_hash}"
        print(f"🔍 Intentando con BlockCypher...")
        data = self.make_request(url, 'BlockCypher')

        if not data:
            return None

        print(f"✅ Datos obtenidos desde BlockCypher")

        # Normalizar formato
        block_time = 0
        if 'confirmed' in data:
            block_time = int(datetime.fromisoformat(data['confirmed'].replace('Z', '+00:00')).timestamp())

        normalized = {
            'hash': data['hash'],
            'size': data.get('size', 0),
            'time': block_time,
            'block_height': data.get('block_height'),
            'inputs': [],
            'out': []
        }

        # Normalizar inputs
        for inp in data.get('inputs', []):
            prev_out = {
                'value': inp.get('output_value', 0),
                'addr': inp.get('addresses', ['N/A'])[0] if inp.get('addresses') else 'N/A',
                'type': inp.get('script_type', 'N/A')
            }
            normalized['inputs'].append({'prev_out': prev_out})

        # Normalizar outputs
        for out in data.get('outputs', []):
            output = {
                'value': out.get('value', 0),
                'addr': out.get('addresses', ['N/A'])[0] if out.get('addresses') else 'N/A',
                'type': out.get('script_type', 'N/A'),
                'spent': out.get('spent_by') is not None
            }
            normalized['out'].append(output)

        return normalized

    def get_transaction(self, tx_hash: str) -> Optional[Dict]:
        """Obtiene información de una transacción con fallback entre APIs"""
        # Intentar con cada API en orden
        methods = [
            self.get_transaction_blockchain,
            self.get_transaction_blockstream,
            self.get_transaction_mempool,
            self.get_transaction_blockcypher
        ]

        for method in methods:
            try:
                result = method(tx_hash)
                if result:
                    return result
                time.sleep(1)  # Pequeña pausa entre intentos
            except Exception as e:
                print(f"⚠️  Error en {method.__name__}: {e}")
                continue

        print("❌ No se pudo obtener la transacción de ninguna fuente")
        return None

    def get_address_blockchain(self, address: str) -> Optional[Dict]:
        """Obtiene información de dirección desde Blockchain.info"""
        url = f"{self.apis['blockchain']}/rawaddr/{address}"
        print(f"🔍 Intentando con Blockchain.info...")
        data = self.make_request(url, 'Blockchain.info')
        if data:
            print(f"✅ Datos obtenidos desde Blockchain.info")
        return data

    def get_address_blockstream(self, address: str) -> Optional[Dict]:
        """Obtiene información de dirección desde Blockstream.info y la normaliza"""
        # Obtener info básica
        url = f"{self.apis['blockstream']}/address/{address}"
        print(f"🔍 Intentando con Blockstream.info...")
        data = self.make_request(url, 'Blockstream.info')

        if not data:
            return None

        # Obtener transacciones
        txs_url = f"{self.apis['blockstream']}/address/{address}/txs"
        txs_data = self.make_request(txs_url, 'Blockstream.info')

        print(f"✅ Datos obtenidos desde Blockstream.info")

        # Normalizar formato
        normalized = {
            'address': address,
            'final_balance': data.get('chain_stats', {}).get('funded_txo_sum', 0) -
                           data.get('chain_stats', {}).get('spent_txo_sum', 0),
            'total_received': data.get('chain_stats', {}).get('funded_txo_sum', 0),
            'total_sent': data.get('chain_stats', {}).get('spent_txo_sum', 0),
            'n_tx': data.get('chain_stats', {}).get('tx_count', 0),
            'txs': []
        }

        # Normalizar transacciones
        if txs_data:
            for tx in txs_data[:25]:  # Limitar a 25 transacciones
                normalized_tx = {
                    'hash': tx['txid'],
                    'time': tx.get('status', {}).get('block_time', 0),
                    'block_height': tx.get('status', {}).get('block_height'),
                    'inputs': [],
                    'out': []
                }

                # Inputs
                for inp in tx.get('vin', []):
                    prev_out = {
                        'value': inp.get('prevout', {}).get('value', 0),
                        'addr': inp.get('prevout', {}).get('scriptpubkey_address', 'N/A')
                    }
                    normalized_tx['inputs'].append({'prev_out': prev_out})

                # Outputs
                for out in tx.get('vout', []):
                    output = {
                        'value': out.get('value', 0),
                        'addr': out.get('scriptpubkey_address', 'N/A')
                    }
                    normalized_tx['out'].append(output)

                normalized['txs'].append(normalized_tx)

        return normalized

    def get_address_mempool(self, address: str) -> Optional[Dict]:
        """Obtiene información de dirección desde Mempool.space y la normaliza"""
        url = f"{self.apis['mempool']}/address/{address}"
        print(f"🔍 Intentando con Mempool.space...")
        data = self.make_request(url, 'Mempool.space')

        if not data:
            return None

        # Obtener transacciones
        txs_url = f"{self.apis['mempool']}/address/{address}/txs"
        txs_data = self.make_request(txs_url, 'Mempool.space')

        print(f"✅ Datos obtenidos desde Mempool.space")

        # Normalizar formato (igual que blockstream)
        normalized = {
            'address': address,
            'final_balance': data.get('chain_stats', {}).get('funded_txo_sum', 0) -
                           data.get('chain_stats', {}).get('spent_txo_sum', 0),
            'total_received': data.get('chain_stats', {}).get('funded_txo_sum', 0),
            'total_sent': data.get('chain_stats', {}).get('spent_txo_sum', 0),
            'n_tx': data.get('chain_stats', {}).get('tx_count', 0),
            'txs': []
        }

        # Normalizar transacciones
        if txs_data:
            for tx in txs_data[:25]:
                normalized_tx = {
                    'hash': tx['txid'],
                    'time': tx.get('status', {}).get('block_time', 0),
                    'block_height': tx.get('status', {}).get('block_height'),
                    'inputs': [],
                    'out': []
                }

                for inp in tx.get('vin', []):
                    prev_out = {
                        'value': inp.get('prevout', {}).get('value', 0),
                        'addr': inp.get('prevout', {}).get('scriptpubkey_address', 'N/A')
                    }
                    normalized_tx['inputs'].append({'prev_out': prev_out})

                for out in tx.get('vout', []):
                    output = {
                        'value': out.get('value', 0),
                        'addr': out.get('scriptpubkey_address', 'N/A')
                    }
                    normalized_tx['out'].append(output)

                normalized['txs'].append(normalized_tx)

        return normalized

    def get_address_blockcypher(self, address: str) -> Optional[Dict]:
        """Obtiene información de dirección desde BlockCypher y la normaliza"""
        url = f"{self.apis['blockcypher']}/addrs/{address}"
        print(f"🔍 Intentando con BlockCypher...")
        data = self.make_request(url, 'BlockCypher')

        if not data:
            return None

        print(f"✅ Datos obtenidos desde BlockCypher")

        # Normalizar formato
        normalized = {
            'address': address,
            'final_balance': data.get('final_balance', 0),
            'total_received': data.get('total_received', 0),
            'total_sent': data.get('total_sent', 0),
            'n_tx': data.get('n_tx', 0),
            'txs': []
        }

        # BlockCypher incluye refs de transacciones, obtener detalles si es necesario
        # Por simplicidad, dejamos txs vacío o procesamos las txrefs

        return normalized

    def get_address_info(self, address: str) -> Optional[Dict]:
        """Obtiene información de una dirección/wallet con fallback entre APIs"""
        methods = [
            self.get_address_blockchain,
            self.get_address_blockstream,
            self.get_address_mempool,
            self.get_address_blockcypher
        ]

        for method in methods:
            try:
                result = method(address)
                if result:
                    return result
                time.sleep(1)
            except Exception as e:
                print(f"⚠️  Error en {method.__name__}: {e}")
                continue

        print("❌ No se pudo obtener información de la dirección de ninguna fuente")
        return None

    def export_transaction_to_csv(self, tx_data: Dict, filename: str = None):
        """Exporta información de transacción a CSV"""
        if not filename:
            filename = f"tx_{tx_data['hash'][:16]}.csv"

        # CSV para inputs
        inputs_file = filename.replace('.csv', '_inputs.csv')
        with open(inputs_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Input_Index', 'Address', 'Value_BTC', 'Value_Satoshi', 'Type'])

            for i, inp in enumerate(tx_data['inputs'], 1):
                prev_out = inp.get('prev_out', {})
                value = prev_out.get('value', 0)
                writer.writerow([
                    i,
                    prev_out.get('addr', 'N/A'),
                    self.satoshi_to_btc(value),
                    value,
                    prev_out.get('type', 'N/A')
                ])

        # CSV para outputs
        outputs_file = filename.replace('.csv', '_outputs.csv')
        with open(outputs_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Output_Index', 'Address', 'Value_BTC', 'Value_Satoshi', 'Spent', 'Type'])

            for i, out in enumerate(tx_data['out'], 1):
                value = out.get('value', 0)
                writer.writerow([
                    i,
                    out.get('addr', 'N/A'),
                    self.satoshi_to_btc(value),
                    value,
                    out.get('spent', False),
                    out.get('type', 'N/A')
                ])

        # CSV resumen
        summary_file = filename.replace('.csv', '_summary.csv')
        with open(summary_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Field', 'Value'])
            writer.writerow(['Hash', tx_data['hash']])
            writer.writerow(['Block_Height', tx_data.get('block_height', 'Unconfirmed')])
            if 'time' in tx_data:
                writer.writerow(['Date', self.format_timestamp(tx_data['time'])])
            writer.writerow(['Size_Bytes', tx_data['size']])
            if 'weight' in tx_data:
                writer.writerow(['Weight_WU', tx_data['weight']])

            total_input = sum(inp.get('prev_out', {}).get('value', 0) for inp in tx_data['inputs'])
            total_output = sum(out.get('value', 0) for out in tx_data['out'])
            fee = total_input - total_output

            writer.writerow(['Total_Input_BTC', self.satoshi_to_btc(total_input)])
            writer.writerow(['Total_Output_BTC', self.satoshi_to_btc(total_output)])
            writer.writerow(['Fee_BTC', self.satoshi_to_btc(fee)])
            if tx_data['size'] > 0:
                writer.writerow(['Fee_Per_Byte', fee / tx_data['size']])

        print(f"\n💾 CSV exportados:")
        print(f"   📥 Inputs: {inputs_file}")
        print(f"   📤 Outputs: {outputs_file}")
        print(f"   📊 Resumen: {summary_file}")

    def export_address_to_csv(self, addr_data: Dict, address: str, filename: str = None):
        """Exporta información de dirección a CSV"""
        if not filename:
            filename = f"addr_{address[:16]}.csv"

        # CSV resumen de dirección
        summary_file = filename.replace('.csv', '_summary.csv')
        with open(summary_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Field', 'Value'])
            writer.writerow(['Address', address])
            writer.writerow(['Final_Balance_BTC', self.satoshi_to_btc(addr_data['final_balance'])])
            writer.writerow(['Total_Received_BTC', self.satoshi_to_btc(addr_data['total_received'])])
            writer.writerow(['Total_Sent_BTC', self.satoshi_to_btc(addr_data['total_sent'])])
            writer.writerow(['Transaction_Count', addr_data['n_tx']])

        # CSV de transacciones
        txs_file = filename.replace('.csv', '_transactions.csv')
        txs = addr_data.get('txs', [])

        if txs:
            with open(txs_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['TxID', 'Block_Height', 'Date', 'Net_BTC', 'Direction'])

                for tx in txs:
                    # Calcular si es entrada o salida para esta dirección
                    received = 0
                    sent = 0

                    for inp in tx.get('inputs', []):
                        prev_out = inp.get('prev_out', {})
                        if prev_out.get('addr') == address:
                            sent += prev_out.get('value', 0)

                    for out in tx.get('out', []):
                        if out.get('addr') == address:
                            received += out.get('value', 0)

                    net = received - sent
                    direction = 'Received' if net > 0 else ('Sent' if net < 0 else 'Internal')

                    writer.writerow([
                        tx['hash'],
                        tx.get('block_height', 'Unconfirmed'),
                        self.format_timestamp(tx.get('time', 0)),
                        self.satoshi_to_btc(abs(net)),
                        direction
                    ])

        print(f"\n💾 CSV exportados:")
        print(f"   📊 Resumen: {summary_file}")
        if txs:
            print(f"   📜 Transacciones: {txs_file}")

    def visualize_transaction(self, tx_data: Dict, filename: str = None):
        """Crea visualización gráfica del flujo de la transacción"""
        if not VISUALIZATION_AVAILABLE:
            print("❌ Bibliotecas de visualización no disponibles.")
            print("   Instala con: pip install matplotlib networkx pandas")
            return

        if not filename:
            filename = f"tx_{tx_data['hash'][:16]}_flow.png"

        # Crear grafo dirigido
        G = nx.DiGraph()

        # Nodo central de la transacción
        tx_node = f"TX\n{tx_data['hash'][:8]}..."
        G.add_node(tx_node, node_type='tx')

        # Agregar inputs
        input_nodes = []
        for i, inp in enumerate(tx_data['inputs'][:20], 1):  # Limitar a 20 para claridad
            prev_out = inp.get('prev_out', {})
            addr = prev_out.get('addr', 'N/A')
            value = prev_out.get('value', 0)

            # Crear nodo abreviado
            if addr != 'N/A':
                node_label = f"{addr[:8]}...\n{self.format_btc(value)}"
            else:
                node_label = f"Input {i}\n{self.format_btc(value)}"

            G.add_node(node_label, node_type='input', value=value)
            G.add_edge(node_label, tx_node, weight=value)
            input_nodes.append(node_label)

        # Agregar outputs
        output_nodes = []
        for i, out in enumerate(tx_data['out'][:20], 1):  # Limitar a 20
            addr = out.get('addr', 'N/A')
            value = out.get('value', 0)
            spent = out.get('spent', False)

            if addr != 'N/A':
                node_label = f"{addr[:8]}...\n{self.format_btc(value)}"
            else:
                node_label = f"Output {i}\n{self.format_btc(value)}"

            status = '✓' if spent else '○'
            node_label = f"{status} {node_label}"

            G.add_node(node_label, node_type='output', value=value, spent=spent)
            G.add_edge(tx_node, node_label, weight=value)
            output_nodes.append(node_label)

        # Crear layout
        pos = {}

        # Posicionar el nodo de transacción en el centro
        pos[tx_node] = (0, 0)

        # Posicionar inputs a la izquierda
        input_count = len(input_nodes)
        for i, node in enumerate(input_nodes):
            y = (i - input_count / 2) * 0.5
            pos[node] = (-2, y)

        # Posicionar outputs a la derecha
        output_count = len(output_nodes)
        for i, node in enumerate(output_nodes):
            y = (i - output_count / 2) * 0.5
            pos[node] = (2, y)

        # Crear figura
        plt.figure(figsize=(16, max(10, max(input_count, output_count) * 0.5)))

        # Dibujar nodos
        node_colors = []
        node_sizes = []

        for node in G.nodes():
            node_type = G.nodes[node].get('node_type')
            if node_type == 'tx':
                node_colors.append('#FFD700')  # Dorado
                node_sizes.append(3000)
            elif node_type == 'input':
                node_colors.append('#FF6B6B')  # Rojo
                value = G.nodes[node].get('value', 0)
                node_sizes.append(min(2000 + value / 10000000, 5000))
            else:  # output
                spent = G.nodes[node].get('spent', False)
                node_colors.append('#90EE90' if not spent else '#87CEEB')  # Verde/Azul
                value = G.nodes[node].get('value', 0)
                node_sizes.append(min(2000 + value / 10000000, 5000))

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)

        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True,
                               arrowsize=20, arrowstyle='->', width=2,
                               connectionstyle='arc3,rad=0.1')

        # Dibujar etiquetas
        nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold')

        # Título y leyenda
        total_input = sum(inp.get('prev_out', {}).get('value', 0) for inp in tx_data['inputs'])
        total_output = sum(out.get('value', 0) for out in tx_data['out'])
        fee = total_input - total_output

        plt.title(f"Flujo de Transacción Bitcoin\n{tx_data['hash']}\n"
                 f"Inputs: {self.format_btc(total_input)} | Outputs: {self.format_btc(total_output)} | "
                 f"Fee: {self.format_btc(fee)}", fontsize=12, fontweight='bold')

        # Leyenda
        legend_elements = [
            mpatches.Patch(color='#FF6B6B', label='Inputs (Origen)'),
            mpatches.Patch(color='#FFD700', label='Transacción'),
            mpatches.Patch(color='#90EE90', label='Outputs No Gastados (UTXO)'),
            mpatches.Patch(color='#87CEEB', label='Outputs Gastados')
        ]
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"\n📊 Gráfico de flujo guardado: {filename}")
        plt.close()

    def display_transaction(self, tx_data: Dict):
        """Muestra información detallada de una transacción"""
        print("\n" + "="*80)
        print("📝 INFORMACIÓN DE TRANSACCIÓN")
        print("="*80)

        print(f"\n🔗 Hash: {tx_data['hash']}")
        print(f"📦 Bloque: {tx_data.get('block_height', 'No confirmado')}")

        if 'time' in tx_data:
            print(f"🕐 Fecha: {self.format_timestamp(tx_data['time'])}")

        # Tamaño y fees
        print(f"📏 Tamaño: {tx_data['size']} bytes")
        if 'weight' in tx_data:
            print(f"⚖️  Peso: {tx_data['weight']} WU")

        # Inputs (Entradas)
        print(f"\n📥 ENTRADAS ({len(tx_data['inputs'])}):")
        print("-" * 80)
        total_input = 0
        for i, inp in enumerate(tx_data['inputs'], 1):
            prev_out = inp.get('prev_out', {})
            value = prev_out.get('value', 0)
            total_input += value
            addr = prev_out.get('addr', 'N/A')

            print(f"  [{i}] Dirección: {addr}")
            print(f"      Cantidad: {self.format_btc(value)}")
            if 'script' in prev_out:
                print(f"      Tipo: {prev_out.get('type', 'N/A')}")
            print()

        # Outputs (Salidas)
        print(f"📤 SALIDAS ({len(tx_data['out'])}):")
        print("-" * 80)
        total_output = 0
        for i, out in enumerate(tx_data['out'], 1):
            value = out.get('value', 0)
            total_output += value
            addr = out.get('addr', 'N/A')
            spent = out.get('spent', False)

            print(f"  [{i}] Dirección: {addr}")
            print(f"      Cantidad: {self.format_btc(value)}")
            print(f"      Estado: {'✅ Gastado' if spent else '💰 No gastado (UTXO)'}")
            if 'script' in out:
                print(f"      Tipo: {out.get('type', 'N/A')}")
            print()

        # Resumen
        print("💰 RESUMEN:")
        print("-" * 80)
        print(f"  Total Entradas:  {self.format_btc(total_input)}")
        print(f"  Total Salidas:   {self.format_btc(total_output)}")
        fee = total_input - total_output
        print(f"  Fee (Comisión):  {self.format_btc(fee)}")
        if tx_data['size'] > 0:
            fee_per_byte = fee / tx_data['size']
            print(f"  Fee/byte:        {fee_per_byte:.2f} sat/byte")

        print("="*80 + "\n")

    def display_address(self, addr_data: Dict, address: str):
        """Muestra información detallada de una dirección"""
        print("\n" + "="*80)
        print("👛 INFORMACIÓN DE WALLET/DIRECCIÓN")
        print("="*80)

        print(f"\n📍 Dirección: {address}")
        print(f"💰 Balance actual: {self.format_btc(addr_data['final_balance'])}")
        print(f"📊 Total recibido: {self.format_btc(addr_data['total_received'])}")
        print(f"📤 Total enviado: {self.format_btc(addr_data['total_sent'])}")
        print(f"🔢 Número de transacciones: {addr_data['n_tx']}")

        # Transacciones
        txs = addr_data.get('txs', [])
        if txs:
            print(f"\n📜 ÚLTIMAS TRANSACCIONES ({len(txs)} mostradas):")
            print("-" * 80)

            for i, tx in enumerate(txs[:10], 1):  # Mostrar máximo 10
                print(f"\n[{i}] TxID: {tx['hash']}")
                print(f"    Bloque: {tx.get('block_height', 'No confirmado')}")

                if 'time' in tx:
                    print(f"    Fecha: {self.format_timestamp(tx['time'])}")

                # Calcular si es entrada o salida para esta dirección
                received = 0
                sent = 0

                for inp in tx.get('inputs', []):
                    prev_out = inp.get('prev_out', {})
                    if prev_out.get('addr') == address:
                        sent += prev_out.get('value', 0)

                for out in tx.get('out', []):
                    if out.get('addr') == address:
                        received += out.get('value', 0)

                net = received - sent
                if net > 0:
                    print(f"    ✅ Recibido: +{self.format_btc(net)}")
                elif net < 0:
                    print(f"    ❌ Enviado: {self.format_btc(abs(net))}")
                else:
                    print(f"    🔄 Cambio interno")

        print("\n" + "="*80 + "\n")

    def analyze(self, input_str: str, export_csv: bool = False, visualize: bool = False):
        """Analiza un hash de transacción o dirección"""
        input_str = input_str.strip()

        # Detectar si es una transacción (64 caracteres hex) o dirección
        if len(input_str) == 64 and all(c in '0123456789abcdefABCDEF' for c in input_str):
            # Es un hash de transacción
            print("🔍 Detectado: Hash de transacción")
            tx_data = self.get_transaction(input_str)
            if tx_data:
                self.display_transaction(tx_data)

                if export_csv:
                    self.export_transaction_to_csv(tx_data)

                if visualize:
                    self.visualize_transaction(tx_data)

        else:
            # Asumir que es una dirección
            print("🔍 Detectado: Dirección de Bitcoin")
            addr_data = self.get_address_info(input_str)
            if addr_data:
                self.display_address(addr_data, input_str)

                if export_csv:
                    self.export_address_to_csv(addr_data, input_str)


def main():
    parser = argparse.ArgumentParser(
        description='🪙 Bitcoin Analyzer - Analizador de Wallets y Transacciones',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
  %(prog)s a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
  %(prog)s --csv --visualize a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d
  %(prog)s -cv 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
        """
    )

    parser.add_argument('input', nargs='?', help='Dirección Bitcoin o TxID hash')
    parser.add_argument('-c', '--csv', action='store_true',
                       help='Exportar datos a archivos CSV')
    parser.add_argument('-v', '--visualize', action='store_true',
                       help='Crear visualización gráfica del flujo (solo para transacciones)')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')

    args = parser.parse_args()

    print("="*80)
    print("🪙  BITCOIN ANALYZER - Analizador de Wallets y Transacciones")
    print("="*80)

    if not VISUALIZATION_AVAILABLE and args.visualize:
        print("\n⚠️  ADVERTENCIA: Bibliotecas de visualización no instaladas.")
        print("   Instala con: pip install -r requirements.txt")
        print()

    analyzer = BitcoinAnalyzer()

    if args.input:
        # Argumento pasado por línea de comandos
        analyzer.analyze(args.input, export_csv=args.csv, visualize=args.visualize)
    else:
        # Modo interactivo
        print("\nModo interactivo - Ingresa 'q' para salir")
        print("Comandos especiales:")
        print("  :csv ON/OFF  - Activar/desactivar exportación CSV")
        print("  :viz ON/OFF  - Activar/desactivar visualización")
        print("-" * 80)

        csv_mode = False
        viz_mode = False

        while True:
            try:
                user_input = input("\n📝 Ingresa dirección Bitcoin o TxID: ").strip()

                if user_input.lower() in ['q', 'quit', 'exit', 'salir']:
                    print("\n👋 ¡Hasta luego!")
                    break

                # Comandos especiales
                if user_input.lower().startswith(':csv'):
                    parts = user_input.split()
                    if len(parts) > 1:
                        csv_mode = parts[1].upper() == 'ON'
                    print(f"   💾 Exportación CSV: {'✅ Activada' if csv_mode else '❌ Desactivada'}")
                    continue

                if user_input.lower().startswith(':viz'):
                    parts = user_input.split()
                    if len(parts) > 1:
                        viz_mode = parts[1].upper() == 'ON'
                    print(f"   📊 Visualización: {'✅ Activada' if viz_mode else '❌ Desactivada'}")
                    continue

                if not user_input:
                    continue

                analyzer.analyze(user_input, export_csv=csv_mode, visualize=viz_mode)

            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
