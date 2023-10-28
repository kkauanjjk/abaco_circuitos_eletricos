import pyfirmata
import time
from gtts import gTTS
import os
import threading
import uuid

# Configuração das portas e resistores
vin = 5.0
r1 = 1000.0
r2 = 0.0

# Função para calcular Vout e R2
def calculate_vout_and_r2(pin):
    raw = pin.read()
    raw *= 1024.0
    if raw:
        vout = (raw * vin) / 1024.0
        buffer = (vin / vout) - 1.0
        r2 = round((r1 * buffer) / 1000)
        return vout, r2
    else:
        return None, None

# Função para ler os valores analógicos e criar um arquivo de áudio com nome exclusivo
def read_analog_values_and_create_audio():
    unique_filename = str(uuid.uuid4()) + ".mp3"
    
    max_attempts = 3
    for _ in range(max_attempts):
        values = []  
        for pin in pins:
            analog_value = pin.read()
            if analog_value is not None:
                vout, r2 = calculate_vout_and_r2(pin)
                if vout is not None and r2 is not None:
                    values.append(str(int(r2)))  
                else:
                    print("Leitura analógica é inválida. Verifique suas conexões.")
            else:
                print("Leitura analógica é None. Verifique suas conexões.")

        if len(values) == 3:
            print("Valores armazenados!")            
            valor = int("".join(values))  
            valor = str(valor)
            print(valor)
            tts = gTTS(text=valor, lang='pt-br')
            tts.save(unique_filename)  
            play_audio(unique_filename)  
            return  
        else:
            print(f"Tentativa {_ + 1} falhou. Tentando novamente...")
            time.sleep(1)  

    print("Número máximo de tentativas atingido. Verifique suas conexões ou problema no Arduino.")

# Função para reproduzir áudio
def play_audio(filename):
    os.system("mpg123 " + filename)
    time.sleep(5)
    os.remove(filename)  # Exclua o arquivo de áudio após a reprodução


# Portas analógicas A0, A1 e A2
port = '/dev/ttyUSB0'
board = pyfirmata.Arduino(port)
pins = [board.get_pin('a:0:i'), board.get_pin('a:1:i'), board.get_pin('a:2:i')]

it = pyfirmata.util.Iterator(board)
it.start()

button = board.get_pin('d:8:i')
previous_button_state = 0
button.mode = pyfirmata.INPUT

while True:
    button_state = button.read()
    if button_state == True and previous_button_state == False:
        print("Botão pressionado!")
        audio_thread = threading.Thread(target=read_analog_values_and_create_audio)
        audio_thread.start()
    previous_button_state = button_state
    time.sleep(0.1)

# sudo usermod -a -G dialout seu_nome_de_usuário
# sudo chmod a+rw /dev/ttyUSB0
# sudo apt-get update
# sudo apt-get install mpg123
# sudo dnf install mpg123

