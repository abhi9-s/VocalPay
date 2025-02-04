from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
import fleep
from gtts import gTTS
from googletrans import Translator
import speech_recognition as sr
import os

from data import langList, dic, units, tens, scales
from utils import text2int
from models import LanguageRequest, TranslateSpeechRequest, TranslateTextRequest

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


translator = Translator()
lang = "en"


@app.post("/setLang")
async def set_lang(req: LanguageRequest):
    global lang
    lang = langList[langList.index(req.language.lower()) + 1]
    return {"message": f"Language successfully set to {lang}"}


@app.post("/transText/headings")
async def trans_headings(req: TranslateTextRequest):
    text_dict = req.text
    for key in text_dict:
        txt = translator.translate(text_dict[key], src="en", dest=lang)
        text_dict[key] = txt.text
    return text_dict


@app.get("/transText/details")
async def trans_details(name: str):
    if name in dic:
        new_dic = {
            "name": translator.translate(dic[name]["name"], src="en", dest=lang).text,
            "contact_no": translator.translate(dic[name]["contact_no"], src="en", dest=lang).text,
            "UPI_ID": dic[name]["UPI_ID"],
            "bank_name": translator.translate(dic[name]["bank_name"], src="en", dest=lang).text,
        }
        return new_dic
    return JSONResponse(content={"error": "Name not found"}, status_code=404)


@app.get("/transText/details/all")
async def trans_details_all():
    new_dic = {}
    for name in dic:
        new_dic[name] = {
            "name": translator.translate(dic[name]["name"], src="en", dest=lang).text,
            "contact_no": translator.translate(dic[name]["contact_no"], src="en", dest=lang).text,
            "UPI_ID": dic[name]["UPI_ID"],
            "bank_name": translator.translate(dic[name]["bank_name"], src="en", dest=lang).text,
        }
    return new_dic


@app.post("/transAudio")
async def trans_audio(req: TranslateSpeechRequest):
    translated = translator.translate(req.speak["text"], src="en", dest=lang)
    text_1 = translated.text

    output_path = "output/trans_voice.mp3"
    audio = gTTS(text=text_1, lang=lang, slow=False)
    audio.save(output_path)

    wav_filename = "output/trans_voice.wav"
    track = AudioSegment.from_file(output_path, format="mp3")
    track.export(wav_filename, format="wav")

    return {"message": "Audio translation completed"}


@app.get("/getAudio")
async def get_audio():
    wav_filename = "output/trans_voice.wav"
    if os.path.exists(wav_filename):
        return FileResponse(wav_filename, media_type="audio/wav", filename="trans_voice.wav")
    return JSONResponse(content={"error": "File not found"}, status_code=404)


@app.post("/audio")
async def upload_audio(file: UploadFile = File(...)):
    r = sr.Recognizer()

    file_path = f"output/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    with open(file_path, "rb") as f:
        info = fleep.get(f.read(128))
    
    print("File extension:", info.extension)

    wav_filename = "output/audio.wav"
    track = AudioSegment.from_file(file_path, format="m4a")
    track.export(wav_filename, format="wav")

    with sr.AudioFile(wav_filename) as source:
        audio_data = r.record(source)
    
    try:
        text_output = r.recognize_google(audio_data, language=lang)
        response = translator.translate(text_output)
        text = response.text.lower()

        input_words = text.split()
        words = input_words.copy()
        rem = ["to", "rupees", "make", "of", "were", "rs", *scales, *tens, *units]
        
        amount = -1
        action = 0

        for x in input_words:
            if x.isnumeric():
                amount = int(x)
                words.remove(x)
            if x.startswith("₹"):
                amount = int(x[1:])
                words.remove(x)
            if x in ["pay", "payment", "send", "transfer", "give", "sent"]:
                action = 1
                words.remove(x)
            if x == "balance":
                action = 2
                words.remove(x)
            if x in ["transaction", "history"]:
                action = 3
                words.remove(x)
            if x in rem:
                words.remove(x)
        
        name = words[0] if words else "--"

        if action == 1:
            if amount == -1:
                amount = text2int(" ".join(input_words[input_words.index("rupees") - 2: input_words.index("rupees")]))
            acc_details = dic.get(name, {"name": "not found", "contact_no": "not found", "UPI_ID": "--", "bank_name": "--"})
            response = {"action": action, "amount": amount, "name": acc_details}
        else:
            response = {"action": action, "amount": 0, "name": "--"}

        return response
    except Exception as e:
        return {"error": str(e), "message": "Sorry, couldn't process the audio."}
