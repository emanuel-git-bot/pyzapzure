from src.pyzapzure import WhatsAppBot

def exemplo_simples():
    # Inicializa o bot
    bot = WhatsAppBot(headless=True)
    
    # Abre o WhatsApp Web
    bot.abrir_whatsapp()
    
    # Envia mensagem
    bot.enviar_mensagem("+5511999999999", "Olá! Mensagem de teste!")
    
    # Fecha a sessão
    bot.fechar()

if __name__ == "__main__":
    exemplo_simples() 