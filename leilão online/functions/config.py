
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


ROOT_DIR = os.path.dirname(BASE_DIR)

ARQUIVO_FILA = os.path.join(ROOT_DIR, 'filas', 'fila_simulada.json')
ARQUIVO_DATABASE = os.path.join(ROOT_DIR, 'database', 'database_simulado.json')