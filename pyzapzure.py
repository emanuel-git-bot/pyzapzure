from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from PIL import Image, ImageTk
import tkinter as tk
import io
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class WhatsAppBot:
    def __init__(self, driver=None, headless=True):
        """Inicializa o WebDriver, ou reutiliza uma sessão existente."""
        self.driver = driver
        if not self.driver:
            self.options = Options()
            if headless:
                self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-dev-shm-usage")
            
            # Inicializa o WebDriver se não foi passado um driver existente
            self.service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def abrir_whatsapp(self):
        """Abre o WhatsApp Web e aguarda o login se necessário."""
        self.driver.get("https://web.whatsapp.com/")
        time.sleep(5)  # Aguarda a página carregar

        try:
            # Verifica se o botão de "novo chat" está visível (indicando que o WhatsApp já está logado)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-testid='menu-chat']"))
            )
            print("WhatsApp já está logado! Continuando...")
        except:
            # Caso não encontre o botão, significa que o QR Code precisa ser escaneado
            print("Aguardando login no WhatsApp...")
            self.aguardar_qrcode()

    def aguardar_qrcode(self):
        """Exibe o QR Code para login no WhatsApp."""
        qr_element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )

        qr_screenshot = qr_element.screenshot_as_png
        qr_img = Image.open(io.BytesIO(qr_screenshot))

        # Exibe o QR Code em uma janela
        self.exibir_qrcode(qr_img)

        print("Aguardando login no WhatsApp...")
        time.sleep(15)

    def exibir_qrcode(self, qr_img):
        """Exibe o QR Code em uma janela Tkinter."""
        root = tk.Tk()
        root.title("Escaneie o QR Code do WhatsApp")

        img_tk = ImageTk.PhotoImage(qr_img)
        label = tk.Label(root, image=img_tk)
        label.image = img_tk
        label.pack()

        tk.Button(root, text="OK, já escaneei!", command=root.destroy).pack()

        root.mainloop()
   
    def enviar_mensagem(self, numero, mensagem):
        """Envia uma mensagem para um número no WhatsApp."""
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}"
        self.driver.get(url)

        try:
            
            print("Procurando campo de texto...")
            campo_texto = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//span[@class='selectable-text copyable-text false'][contains(text(), '{mensagem}')]"))
            )
            print("Campo de texto encontrado com sucesso!")
            time.sleep(3)
            campo_texto.send_keys(Keys.ENTER)
            time.sleep(3)
            print(f"✅ Mensagem enviada para {numero}")
        except Exception as e:
            print(f"⚠️ Erro ao enviar mensagem para {numero}: {str(e)}")

    def fechar(self):
        """Fecha o navegador após o envio."""
        time.sleep(5)
        self.driver.quit()


# Inicializa o bot pela primeira vez
bot1 = WhatsAppBot(headless=True)

# Abre o WhatsApp Web (se necessário)
bot1.abrir_whatsapp()

# Envia mensagens
bot1.enviar_mensagem("+5517992760490", "Olá! Mensagem automática via Selenium!")
bot1.enviar_mensagem("+5517992760490", "Olá! aqui está outra mensagem!")

# Fecha a sessão depois caso não for continuar a segunda
#bot1.fechar()

# Se você for usar o código novamente sem fechar o navegador:
bot2 = WhatsAppBot(driver=bot1.driver)  # Reutiliza a sessão
bot2.enviar_mensagem("+5517992760490", "Olá! Outra mensagem sem escanear QR Code!")
bot2.fechar()
