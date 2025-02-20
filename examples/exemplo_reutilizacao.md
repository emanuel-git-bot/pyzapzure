from src.pyzapzure import WhatsAppBot
import time

def exemplo_reutilizacao():
    """
    Demonstra como reutilizar uma sessão do WhatsApp entre diferentes instâncias do bot,
    evitando a necessidade de escanear o QR Code novamente.
    """
    
    print("=== Iniciando primeira sessão ===")
    # Primeira instância do bot
    bot1 = WhatsAppBot(headless=False)  # Modo visual para demonstração
    bot1.abrir_whatsapp()
    
    # Primeira sequência de mensagens
    print("\nEnviando primeira sequência de mensagens...")
    bot1.enviar_mensagem("+5511999999991", "Mensagem 1 da primeira sessão")
    bot1.enviar_mensagem("+5511999999991", "Mensagem 2 da primeira sessão")
    time.sleep(2)
    
    print("\n=== Criando segunda sessão reaproveitando o navegador ===")
    # Segunda instância reaproveitando o driver da primeira
    bot2 = WhatsAppBot(driver=bot1.driver)
    
    # Segunda sequência de mensagens (sem precisar escanear QR Code)
    print("\nEnviando mensagens da segunda sessão...")
    bot2.enviar_mensagem("+5511999999991", "Mensagem 1 da segunda sessão")
    bot2.enviar_mensagem("+5511999999991", "Mensagem 2 da segunda sessão")
    time.sleep(2)
    
    print("\n=== Criando terceira sessão reaproveitando o mesmo navegador ===")
    # Terceira instância também reaproveitando o mesmo driver
    bot3 = WhatsAppBot(driver=bot1.driver)
    
    # Terceira sequência de mensagens (ainda usando a mesma sessão)
    print("\nEnviando mensagens da terceira sessão...")
    bot3.enviar_mensagem("+5511999999991", "Mensagem 1 da terceira sessão")
    bot3.enviar_mensagem("+5511999999991", "Mensagem 2 da terceira sessão")
    
    # Importante: só fechar o navegador na última instância
    print("\n=== Finalizando todas as sessões ===")
    bot3.fechar()
    print("Navegador fechado e sessões encerradas!")

if __name__ == "__main__":
    exemplo_reutilizacao() 