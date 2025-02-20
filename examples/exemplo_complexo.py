from src.pyzapzure import WhatsAppBot
from src.pyzapmoduloscmp import GerenciadorMensagens
import time
from datetime import datetime
import json
import logging
from typing import List, Dict

def exemplo_complexo():
    # Exemplo de lista de contatos
    contatos_exemplo = [
        {
            "nome": "João",
            "numero": "+5511999999991",
            "mensagem": "Olá João! Mensagem personalizada para você.",
            "horario": "2024-03-20 14:30:00"
        },
        {
            "nome": "Maria",
            "numero": "+5511999999992",
            "mensagem": "Oi Maria! Aqui está sua mensagem especial.",
            "horario": "2024-03-20 15:00:00"
        }
    ]
    
    # Salva contatos em arquivo JSON para exemplo
    with open('contatos.json', 'w', encoding='utf-8') as f:
        json.dump(contatos_exemplo, f, indent=4, ensure_ascii=False)
    
    try:
        # Inicializa o gerenciador
        gerenciador = GerenciadorMensagens()
        gerenciador.iniciar_bot(headless=False)  # Modo visual para demonstração
        
        # Carrega contatos
        contatos = gerenciador.carregar_contatos('contatos.json')
        
        # Envia mensagens agendadas
        for contato in contatos:
            horario_envio = datetime.strptime(contato['horario'], '%Y-%m-%d %H:%M:%S')
            gerenciador.enviar_mensagem_agendada(
                contato['numero'],
                contato['mensagem'],
                horario_envio
            )
        
        # Envia mensagens em lote
        resultados = gerenciador.enviar_mensagens_em_lote(contatos)
        logging.info(f"Resultados do envio em lote: {resultados}")
        
    except Exception as e:
        logging.error(f"Erro durante execução: {str(e)}")
    finally:
        gerenciador.finalizar()

if __name__ == "__main__":
    exemplo_complexo() 