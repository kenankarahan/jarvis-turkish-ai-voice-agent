import time
import io
import os
from google.cloud import texttospeech
import pygame
from groq import Groq
from PIL import ImageGrab, Image
import google.generativeai as genai
import cv2
import pyperclip
import speech_recognition as sr
import io
import os
import pygame
from google.cloud import texttospeech

# API Key Configuration
# ----------------------
# Google Cloud Text to Speech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-cloud-texttospeech-api-key-file.json"
# Groq
groq_client = Groq(api_key="groq_api_key")
# Generative AI
genai.configure(api_key="generativeai-api-key")


# Text to Speech Definition
client = texttospeech.TextToSpeechClient()
# Speech to Text Definition
recognizer = sr.Recognizer()

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
model = genai.GenerativeModel("gemini-1.5-flash-latest", generation_config=config, safety_settings=safety_settings)



# Llama Configuration
sys_msg = (
    "Sen çok modlu bir yapay zeka sesli asistansın. "
    "Kullanıcı, bir fotoğraf (ekran görüntüsü veya web kamerası çekimi) eklemiş olabilir ya da olmayabilir. "
    "Herhangi bir fotoğraf, son derece ayrıntılı bir metin açıklamasına dönüştürülmüş ve kullanıcının sesli komutunun transkriptine eklenmiş olacaktır. "
    "Mümkün olan en yararlı ve doğru yanıtı üret, yanıtına yeni ifadeler eklemeden önce önceki tüm oluşturulmuş metni dikkatlice değerlendir. Görselleri bekleme veya talep etme; yalnızca eklendiğinde bağlamı kullan. "
    "Yanıtlarını bu konuşmanın tüm bağlamını göz önünde bulundurarak ver ve konuşmaya uygun olacak şekilde anlamlı yanıtlar oluştur. Cevapların net ve öz olsun, gereksiz ayrıntılardan kaçın."
)
convo = [{'role':'system', 'content':sys_msg}]
def groq_prompt(prompt, img_context):
    if img_context:
        prompt = f"KULLANICI GİRİŞİ: {prompt}\n\n   RESİM İÇERİĞİ: {img_context}"
    convo.append({"role":"user", "content": prompt})
    chat_completion = groq_client.chat.completions.create(messages=convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message
    convo.append(response)
    return response.content

# Function Call Configuration. If you add any func to the program, first you should add it in the paragraph and func call list below.
def function_call(prompt):
    sys_msg=(
        'Sen bir yapay zeka fonksiyon çağırma modelisin. Kullanıcının komutuna yanıt verirken, '
        'kullanıcının pano içeriğini çıkarmak, ekran görüntüsü almak, web kamerasını yakalamak veya hiçbir fonksiyon çağırmamak arasında en iyi olanı belirleyeceksin. '
        'Web kamerasının, kullanıcının karşısına yerleştirilmiş normal bir dizüstü bilgisayar kamerası olduğu varsılabilir. Yalnızca şu seçeneklerden birini yanıt olarak vereceksin: ["extract_clipboard", "take_screenshot", "capture_webcam", "exit", "None"] \n'
        'Fonksiyon çağırma adı tam olarak yukarıdaki listede verdiğim gibi olacak.'               
    )
    
    function_convo = [{'role':'system', 'content':sys_msg},
                      {'role':'user', 'content':prompt}]
    chat_completion = groq_client.chat.completions.create(messages=function_convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message
    
    return response.content

# Functions
def take_screenshot():
    path = "screenshot.jpg"
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=15)
def extract_clipboard():
    clipboard_content = pyperclip.paste()
    if isinstance(clipboard_content, str):
        print(clipboard_content)
        return clipboard_content
    else:
        print("Hiçbir şey kopyalanmamış")
        return None
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
    cv2.imwrite(filename,camera_capture)
    del(camera)
def vision_prompt(prompt, photo_path):
    img = Image.open(photo_path)
    prompt = (
        f"Sen, görüntülerden anlamsal çıkarımlar yaparak bağlam sağlayan bir görsel analiz yapay zekasısın. "
        "Kullanıcıya doğrudan yanıt veren bir yapay zeka asistanı gibi davranma. Bunun yerine, kullanıcıdan gelen komut girdisini al ve görüntüden, kullanıcı komutuyla ilgili olan tüm anlamları çıkarmaya çalış. "
        "Daha sonra, görüntüyle ilgili mümkün olduğunca fazla nesnel veri oluştur ve bunu kullanıcıya yanıt verecek yapay zeka asistanına ilet. \n KULLANICI GİRİŞİ: {prompt}"
    )
    
    response = model.generate_content([prompt, img])
    return response.text
def speak(text):

    synthesis_input = texttospeech.SynthesisInput(text=text)


    voice = texttospeech.VoiceSelectionParams(
        language_code="tr-TR",  
        name="tr-TR-Wavenet-C",  
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE  
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

# Starting the Service
speak("Jarvis aktif!")
while True:
    
    speak("Sizi Dinliyorum...")
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
    else:
        visual_context = None
        
    response = groq_prompt(prompt=prompt, img_context=visual_context)
    print(response)
    speak(response)
    time.sleep(1)