
import json
import os
from .config import ARQUIVO_FILA 

def lambda_1_registrar_lance(novo_lance):
    """
    Simula a Lambda 1.
    Responsabilidade: Receber um lance, validar superficialmente
    e colocá-lo na 'fila_simulada.json'.
    """
    print(f"[Lambda 1] Recebido: {novo_lance['valor']} para {novo_lance['itemId']} por {novo_lance['userId']}")

    # Validação 
    if not novo_lance.get('itemId') or not novo_lance.get('valor') or not novo_lance.get('userId'):
        print("[Lambda 1] ERRO: Lance inválido (faltando dados).")
        return False 

    try:
        
        fila_atual = []
        if os.path.exists(ARQUIVO_FILA) and os.path.getsize(ARQUIVO_FILA) > 0:
            with open(ARQUIVO_FILA, 'r', encoding='utf-8') as f:
                fila_atual = json.load(f)
        
     
        fila_atual.append(novo_lance)
        
        
        with open(ARQUIVO_FILA, 'w', encoding='utf-8') as f:
            json.dump(fila_atual, f, indent=2)
            
        print(f"[Lambda 1] Sucesso: Lance de {novo_lance['userId']} enfileirado.")
        return True 

    except Exception as e:
        print(f"[Lambda 1] ERRO ao escrever na fila: {e}")
        return False