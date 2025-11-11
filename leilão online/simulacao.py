
import time
import json


from functions.config import ARQUIVO_FILA, ARQUIVO_DATABASE
from functions.lambda_1 import lambda_1_registrar_lance
from functions.lambda_2 import lambda_2_processar_lance

def rodar_simulacao():
    print("========= INICIANDO SIMULAÇÃO DE LEILÃO =========\n")
  
    print("--- Usuários estão dando lances (Chamando Lambda 1)... ---")
    
    lance1 = {"itemId": "item123", "valor": 2600, "userId": "ana_silva"}
    lambda_1_registrar_lance(lance1)
    time.sleep(0.1) 
    
    lance2 = {"itemId": "item123", "valor": 2550, "userId": "bruno_costa"}
    lambda_1_registrar_lance(lance2)
    time.sleep(0.1)
    
    lance3 = {"itemId": "item456", "valor": 900, "userId": "carla_dias"}
    lambda_1_registrar_lance(lance3)
    time.sleep(0.1)

    lance4 = {"itemId": "item123", "valor": 5700, "userId": "david_rocha"}
    lambda_1_registrar_lance(lance4)
    
    print("\n--- Fim dos lances. Verifique o 'filas/fila_simulada.json'. Ele deve estar CHEIO! ---\n")
    print("Pressione ENTER para começar o processamento da fila (Lambda 2)...")
    input()

  
    print("--- Processando a fila (Chamando Lambda 2 em loop)... ---")
    
    while True:
        try:
            with open(ARQUIVO_FILA, 'r') as f:
                fila = json.load(f)
                if not fila:
                    print("\n--- Fila esvaziada! ---")
                    break
        except Exception:
            print("\n--- Fila esvaziada! ---")
            break
            
        lambda_2_processar_lance()
        time.sleep(0.5) 

    print("\n========= SIMULAÇÃO FINALIZADA =========\n")
    print("Verifique o 'database/database_simulado.json' para ver o resultado final.")
    print("Verifique o 'filas/fila_simulada.json'. Ele deve estar VAZIO ([]) agora.")


if __name__ == "__main__":
 
    db_inicial = {
        "item123": {"nomeItem": "Notebook Gamer", "maiorLance": 2500, "maiorLanceUser": "usuario_inicial"},
        "item456": {"nomeItem": "Monitor Ultrawide", "maiorLance": 800, "maiorLanceUser": "usuario_inicial"}
    }
    with open(ARQUIVO_DATABASE, 'w') as f:
        json.dump(db_inicial, f, indent=2)

    with open(ARQUIVO_FILA, 'w') as f:
        json.dump([], f)


    rodar_simulacao()