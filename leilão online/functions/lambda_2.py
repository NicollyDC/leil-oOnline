# A Lambda 2 executa a lógica de negócios:

	#O leilão ainda está aberto?

	#O lance_recebido é maior que o maior_lance_atual no DynamoDB?
# functions/lambda_2.py
import json
import os
# A linha abaixo é a que foi corrigida (linha 4 ou 9, dependendo de como você conta)
from .config import ARQUIVO_FILA, ARQUIVO_DATABASE # <-- CORREÇÃO AQUI

def lambda_2_processar_lance():
   
    print("\n--- [Lambda 2] Acionada! Verificando fila... ---")
    
  
    
    fila_atual = []
    if not os.path.exists(ARQUIVO_FILA) or os.path.getsize(ARQUIVO_FILA) == 0:
        print("[Lambda 2] Fila está vazia. Nada a fazer.")
        return
        
    try:
        with open(ARQUIVO_FILA, 'r', encoding='utf-8') as f:
            fila_atual = json.load(f)
    except json.JSONDecodeError:
         print("[Lambda 2] Fila vazia ou corrompida. Nada a fazer.")
         return

    if not fila_atual:
        print("[Lambda 2] Fila está vazia. Nada a fazer.")
        return

    
    lance_para_processar = fila_atual.pop(0)
    

    with open(ARQUIVO_FILA, 'w', encoding='utf-8') as f:
        json.dump(fila_atual, f, indent=2)
        
    print(f"[Lambda 2] Processando lance: {lance_para_processar}")

    #  Logica de negocio

    try:
        # Lê o banco de dados
        with open(ARQUIVO_DATABASE, 'r', encoding='utf-8') as f:
            database = json.load(f)
            
        # Pega os dados do lance
        itemId = lance_para_processar['itemId']
        novoValor = lance_para_processar['valor']
        novoUser = lance_para_processar['userId']

        if itemId not in database:
            print(f"[Lambda 2] ERRO: Item {itemId} não existe no banco de dados.")
            return

        leilao_atual = database[itemId]
        maiorLanceAtual = leilao_atual['maiorLance']
        
        if novoValor > maiorLanceAtual:
            leilao_atual['maiorLance'] = novoValor
            leilao_atual['maiorLanceUser'] = novoUser
            
            with open(ARQUIVO_DATABASE, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2)
                
            print(f" [Lambda 2] SUCESSO: Novo lance alto para {itemId}! Valor: {novoValor} por {novoUser}")
        else:
            print(f"[Lambda 2] FALHA: Lance de {novoValor} por {novoUser} é menor ou igual ao lance atual de {maiorLanceAtual}.")
            
    except Exception as e:
        print(f"[Lambda 2] ERRO ao processar o banco de dados: {e}")