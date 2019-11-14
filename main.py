from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
import smtplib, ssl
import gmail_credentials

# Parameters related to trip
ORIGEN = "MADRID (TODAS)"
DESTINO = "ALICANTE/ALACANT"
FECHA_IDA = "25/12/2019"

# We need to make it headless, to run in the back without opening the browser
chrome_options = Options()  
chrome_options.add_argument("--headless") 

# Step 1) Open Chrome 
# The chrome driver must be in the folder
#browser = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'), options=chrome_options)
browser = webdriver.Chrome('/Users/gr/Ironhack/renfe/chromedriver', options=chrome_options)


# Step 2) Navigate to Renfe
browser.get("http://www.renfe.com/")
# We don't need next if we run it headless
# browser.maximize_window()

# Step 3) Search & Enter the Email or Phone field & Enter Password
# Find the elements
origen = browser.find_element_by_id("IdOrigen")
destino = browser.find_element_by_id("IdDestino")
fecha_ida = browser.find_element_by_id("__fechaIdaVisual")
submit = browser.find_element_by_class_name("btn_home")

# Clear and fill in the form
origen.clear()
origen.send_keys(ORIGEN)
origen.send_keys(Keys.ARROW_DOWN) # Select the first option from the drop-down list (renfe style)
origen.send_keys(Keys.ENTER)

destino.clear()
destino.send_keys(DESTINO)
destino.send_keys(Keys.ARROW_DOWN)
destino.send_keys(Keys.ENTER)

fecha_ida.clear()
fecha_ida.send_keys(FECHA_IDA)

# Step 4) Click button
submit.click()

# Create wait object with a timeout of 5 sec
wait = WebDriverWait(browser, 5)

# Find the element with the tickets information. If there are no tickets, message is "El trayecto consultado no se encuentra disponible..."
message = browser.find_element_by_id("tab-mensaje_contenido").text

# Close the browser
browser.close()

# Send a message by email if the tickets are posted.
if message != "El trayecto consultado no se encuentra disponible para la venta en estos momentos o bien no existe conexión directa, por favor inténtelo más adelante y disculpe las molestias.":
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = gmail_credentials.SENDER_EMAIL  # Enter your address
    receiver_email = gmail_credentials.RECEIVER_EMAIL  # Enter receiver address
    password = gmail_credentials.PASSWORD
    msg = "Los trenes de " + ORIGEN + " a " + DESTINO + " para el día " + FECHA_IDA + " ya están disponibles. ¡Corre que vuelan!"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.encode('utf-8')) # Whihout .encode, there would be an ascii encoding error