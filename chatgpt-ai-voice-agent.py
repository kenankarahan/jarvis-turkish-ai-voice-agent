import time
import io
import os
import openai
from google.cloud import texttospeech
import pygame
from PIL import ImageGrab, Image
import pyperclip
import speech_recognition as sr
import cv2
import google.generativeai as genai
import webbrowser




# API Key Configuration
# -----------------------
# OpenAI
openai.api_key = "openai-api-key"
# Generative AI 
genai.configure(api_key="generativeai-api-key")
# Google Cloud Text To Speech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-cloud-text-to-speech-api-key-file.json"

# Gemini Model Configuration
config= {
    'temperature' : 0.7,
    'top_p' : 1,
    'top_k' : 1,
    'max_output_tokens': 2048
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT",
     "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",
     "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
     "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
     "threshold": "BLOCK_NONE"}
]


# Gemini Model Creation
model = genai.GenerativeModel("gemini-1.5-flash-latest", generation_config=config, safety_settings=safety_settings)

# Text to Speech Definition
client = texttospeech.TextToSpeechClient()
# Speech to Text Definition
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Text To Speech Func & Configuration
def speak(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="tr-TR",
        name="tr-TR-Wavenet-E",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    audio_content = response.audio_content
    audio_stream = io.BytesIO(audio_content)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# ChatGPT Prompt Func & Configuration
def chatgpt_prompt(prompt, img_context=None):
    
    
    messages = [{"role": "system", "content": "Sen çok modlu bir yapay zeka sesli asistansın. Herhangi bir fotoğraf, metin açıklamalarına dönüştürülmüş olacaktır. Yanıtlarını anlamlı ve öz tut. Sanki fotoğrafı sen inceliyorsun gibi konuş."}]

    if img_context:
        prompt = f"KULLANICI GİRİŞİ: {prompt}\n\n RESİM İÇERİĞİ: {img_context}"

    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=512,
        temperature=0.7
    )

    return response['choices'][0]['message']['content']

# Function Call Func & Configuration
def function_call(prompt):
    system_msg = (
    "Sen bir yapay zeka fonksiyon çağırma modelisin. Kullanıcıdan gelen metne dayanarak, "
    "en uygun fonksiyon çağrısını belirlemen gerekmektedir. Kullanıcı, bir ekran görüntüsü almak, "
    "panodaki içeriği çıkarmak, web kamerası görüntüsünü almak, bir programı açmak, bir web sitesini açmak, uygulamadan çıkmak veya hiçbir işlem yapmamak isteyebilir. "
    "Aşağıdaki işlevlerden sadece birini seçip yanıt olarak döndürmelisin:\n "
    '["extract_clipboard", "take_screenshot", "capture_webcam", "open_any_program", "open_any_website", "exit", "None"]\n'
    "Fonksiyon çağrısının doğru olmasını sağlamak için, kullanıcının ihtiyacını ve komutunun amacını "
    "anlayarak yalnızca bir seçenek döndürmelisin. Yanıt olarak, yukarıdaki listedeki seçeneklerden birini tam olarak kullanmalısın."
    "Lütfen verilen seçenekler dışında başka bir şey kullanma ve her zaman bu seçeneklerden en uygun olanını seç.\n\n"
    "EĞER KULLANICI BİR PROGRAM AÇMANI İSTERSE:\n"
    "1. KULLANICI ÖZELLİKLE 'program_adı', AÇ DİYE BELİRTMELİDİR!\n"
    "2. LİSTEDEN 'open_any_program' SEÇENEĞİNİ SEÇ.\n"
    "3. SADECE PROGRAMIN TAM ADINI DEĞER OLARAK DÖNDÜR.\n"
    "4. DÖNDÜRECEĞİN DEĞER {'open_any_program': 'program_adı'} FORMATINDA OLMALI.\n"
    "5. EĞER PROGRAMIN TAM ADINI BİLİYORSAN 'program_adı' KISMINA PROGRAMIN TAM ADINI GİR!\n"
    "6. PROGRAMIN ADI NE KADAR UZUN OLURSA OLSUN SAKIN YUKARIDA ÖZELLİKLE BELİRTTİĞİM DÖNDÜRÜLECEK DEĞER FORMATI'NIN DIŞINA ÇIKMA!\n"
    "7. ASLA YUKARIDA SANA VERİLEN YÖNERGELERİN DIŞINA ÇIKMA!\n\n"
    "EĞER KULLANICI SENDEN BİR WEB SİTESİNİ AÇMANI İSTERSE:\n"
    "1. KULLANICI ÖZELLİKLE 'web_url', AÇ DİYE BELİRTMELİDİR!"
    "2. BU DURUMDA SADECE SENDEN İSTENEN ŞEY AÇILMASI İSTENEN WEB SİTESİNİN URL'SİDİR. URL DIŞINDA HERHANGİ BİR DEĞER DÖNDÜRME VEYA BİR ŞEY SÖYLEME!\n"
    "3. LİSTEDEN 'open_any_website' SEÇENEĞİNİ SEÇ.\n"
    "4. SEDECE SİTENİN URL'SİNİ DEĞER OLARAK DÖNDÜR.\n"
    "5. DÖNDÜRECEĞİN DEĞER {'open_any_website': 'web_site_url' FORMATINDA OLMALI.\n}"
    "6. 'web_site_url' KISMINA SADECE URL DEĞERİ ALABİLİR!\n"
    "7. URL NE KADAR UZUN OLURSA OLSUN TAM URL DEĞERİ GİRİLMEK ZORUNLUDUR!\n"
    "8. ASLA YUKARIDA SANA VERİLEN YÖNERGELERİN DIŞINA ÇIKMA!"

    )

    
    function_convo = [{'role': 'system', 'content': system_msg},
                      {'role': 'user', 'content': prompt}]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=function_convo,
        max_tokens=150
    )
    
    return response['choices'][0]['message']['content']

# Taking Screenshot Func
def take_screenshot():
    path = "screenshot.jpg"
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=15)

# Extracting Clipboard Func
def extract_clipboard():
    clipboard_content = pyperclip.paste()
    if isinstance(clipboard_content, str):
        print(clipboard_content)
        return clipboard_content
    else:
        print("Hiçbir şey kopyalanmamış")
        return None

# Capturing Webcam Func
def capture_webcam():
    camera_port = 0 
    ramp_frames = 30 
    camera = cv2.VideoCapture(camera_port)
    if not camera.isOpened():
        print("Kamera bulunamadı...")
        exit()

    def get_image():
        retval, im = camera.read()
        return im

    for i in range(ramp_frames):
        temp = camera.read()

    camera_capture = get_image()
    filename = "image.jpg"
    cv2.imwrite(filename, camera_capture)
    del(camera)

# Opening Programs (PATH CONFIGURE)
def open_any_program(prog):
    prog = prog.replace("{'open_any_program': ","")
    prog = prog.replace("}","")
    prog = prog.replace("'","")
    prog = prog.replace('"', "")
    prog = prog.replace(" ","")
    prog = prog.lower()
    match prog:
        case "game":
            os.system(r'start #your game path')
        case "browser":
            os.system(r'start #your browser path')
        case "spotify":
            os.system("start #your spotify path")
    speak(f"{prog}, açılıyor...")
            
# Opening Websites
def open_any_website(url):
    url = url.replace('{"open_any_website": ',"")
    url = url.replace("{'open_any_website': ", "")
    url = url.replace('}', "")
    url = url.replace('"', "")
    url = url.replace("'", "")
    webbrowser.open(url, new=0)
    url = url.replace("https://www.", "")
    speak(f"{url}, açılıyor...")

# Vision Analization Func
def vision_prompt(prompt, photo_path):
    img = Image.open(photo_path)
    prompt = (
        f"Sen, görüntülerden anlamsal çıkarımlar yaparak bağlam sağlayan bir görsel analiz yapay zekasısın. "
        "Kullanıcıya doğrudan yanıt veren bir yapay zeka asistanı gibi davranma. Bunun yerine, kullanıcıdan gelen komut girdisini al ve görüntüden, kullanıcı komutuyla ilgili olan tüm anlamları çıkarmaya çalış. "
        "Daha sonra, görüntüyle ilgili mümkün olduğunca fazla nesnel veri oluştur ve bunu kullanıcıya yanıt verecek yapay zeka asistanına ilet. \n KULLANICI GİRİŞİ: {prompt}"
    )
    
    response = model.generate_content([prompt, img])
    return response.text

# Wakeword Listening Function
def listen_for_wake_word():
    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Dinleniyor...\nLütfen wake word'ü söyleyin.")
            try:
                audio_data = recognizer.listen(source)
                print("Ses alındı!")
                text = recognizer.recognize_google(audio_data, language="tr-TR").lower()
                print(f"Algılanan metin: {text}")

                if "jarvis" in text:  # Wake Word Configuration. Default value is "jarvis"
                    print("Wake word 'Jarvis' algılandı.\nAsistan aktif!")
                    return True
            except sr.UnknownValueError:
                print("Anlaşılmayan ses.")
            except sr.RequestError as e:
                print(f"Servise bağlanılamadı; hata: {e}")


# Running Program
while True:
    
    if listen_for_wake_word(): # Waiting for Wake Word
        speak("Efendim.")
        print("Asistan başlıyor...\n")
    
        with sr.Microphone() as mic:
            print("Dinleniyor...\n")
            recognizer.adjust_for_ambient_noise(mic, duration=0)
            try:
                stt_data = recognizer.listen(mic)
                prompt = recognizer.recognize_google(stt_data, language="tr-TR")
                print(f"Kullanıcı: {prompt}")
            
                call = function_call(prompt)
            except sr.UnknownValueError:
                speak("Dediklerinizi anlayamadım. Lütfen tekrar ediniz.")
                continue
            except sr.RequestError:
                speak(f"Servise bağlanılamadı. Hata Kodu: {sr.RequestError}")
                continue
            
        if "take_screenshot" in call:
            speak("Ekran görüntüsü alındı! Ekran görüntüsünün analizi için lütfen bekleyin. Detaylı bir inceleme biraz uzun sürebilir.")
            take_screenshot()
            visual_context = vision_prompt(prompt=prompt, photo_path="screenshot.jpg")
        elif "extract_clipboard" in call:
            paste = extract_clipboard()
            prompt = f"{prompt}\n\n KOPYALANMIŞ İÇERİK: {paste}"
            visual_context = None
        elif "capture_webcam" in call:
            speak("Kamera görüntüsü alındı! Kamera görüntüsünün analizi için lütfen bekleyin. Detaylı bir inceleme biraz uzun sürebilir.")
            capture_webcam()
            visual_context = vision_prompt(prompt=prompt, photo_path="image.jpg")
        elif "exit" in call:
            speak("Çıkış yapılıyor...")
            exit()
        elif "open_any_program" in call:
            print(call)
            open_any_program(call)
            visual_context = None
            continue
            
        elif "open_any_website" in call:
            print(call)
            open_any_website(call)
            visual_context = None
            continue
        else:
            visual_context = None
            
        response = chatgpt_prompt(prompt=prompt, img_context=visual_context)
        print(response)
        speak(response)
        time.sleep(1)
    else:
        continue
