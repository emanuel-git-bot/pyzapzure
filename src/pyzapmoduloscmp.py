from src.pyzapzure import WhatsAppBot
import time
from datetime import datetime
import json
import logging
from typing import List, Dict

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='whatsapp_bot.log'
)

class GerenciadorMensagens:
    def __init__(self):
        self.bot = None
        self.mensagens_enviadas = []
        self.tentativas_maximas = 3
        
    def iniciar_bot(self, headless: bool = True) -> None:
        """Inicializa o bot com tratamento de erros"""
        try:
            self.bot = WhatsAppBot(headless=headless)
            self.bot.abrir_whatsapp()
            logging.info("Bot iniciado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao iniciar bot: {str(e)}")
            raise
    
    def carregar_contatos(self, arquivo: str) -> List[Dict]:
        """Carrega contatos de um arquivo JSON"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Arquivo {arquivo} não encontrado")
            return []
            
    def enviar_mensagem_agendada(self, numero: str, mensagem: str, horario: datetime) -> bool:
        """Envia mensagem em um horário específico"""
        while datetime.now() < horario:
            time.sleep(60)  # Verifica a cada minuto
            
        return self.enviar_com_retry(numero, mensagem)
    
    def enviar_com_retry(self, numero: str, mensagem: str) -> bool:
        """Tenta enviar mensagem com várias tentativas"""
        for tentativa in range(self.tentativas_maximas):
            try:
                self.bot.enviar_mensagem(numero, mensagem)
                self.mensagens_enviadas.append({
                    'numero': numero,
                    'mensagem': mensagem,
                    'data': datetime.now().isoformat(),
                    'status': 'sucesso'
                })
                return True
            except Exception as e:
                logging.warning(f"Tentativa {tentativa + 1} falhou: {str(e)}")
                time.sleep(5)  # Espera antes de tentar novamente
                
        logging.error(f"Todas as tentativas falharam para o número {numero}")
        return False
    
    def enviar_mensagens_em_lote(self, contatos: List[Dict]) -> Dict:
        """Envia mensagens para múltiplos contatos com relatório"""
        resultados = {
            'sucesso': 0,
            'falha': 0,
            'total': len(contatos)
        }
        
        for contato in contatos:
            sucesso = self.enviar_com_retry(
                contato['numero'],
                contato['mensagem']
            )
            if sucesso:
                resultados['sucesso'] += 1
            else:
                resultados['falha'] += 1
            
            time.sleep(10)  # Intervalo entre mensagens
            
        return resultados
    
    def gerar_relatorio(self) -> None:
        """Gera relatório de mensagens enviadas"""
        with open('relatorio_mensagens.json', 'w', encoding='utf-8') as f:
            json.dump(self.mensagens_enviadas, f, indent=4, ensure_ascii=False)
    
    def finalizar(self) -> None:
        """Finaliza o bot e gera relatório"""
        if self.bot:
            self.bot.fechar()
        self.gerar_relatorio()
        logging.info("Bot finalizado e relatório gerado")