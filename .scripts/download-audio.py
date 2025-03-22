import yt_dlp
from pydub import AudioSegment, effects
import json, os, tempfile

def download_audio(url):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{temp_path}.%(ext)s',
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            actual_file = f"{temp_path}.{info['ext']}"
        except yt_dlp.utils.PostProcessingError as e:
            print(f"Error in post-processing: {e}")
            return None
    
    return actual_file

def normalize_audio(input, output):
    try:
        audio = AudioSegment.from_file(input)
        normalized_audio = effects.normalize(audio)
        normalized_audio[:120000].export(output, format="mp3")
    except Exception as e:
        print(f"Error processing audio file: {e}")
    
    return path

path = os.environ.get('DECK_PATH', os.path.pardir)
if not os.path.isabs(path):
    path = os.path.join(os.path.dirname(__file__), path)

with open(os.path.join(path, 'deck.json'), "r") as file:
    meta = json.load(file)

print(f"Loaded {meta['name']}\n")

for m in meta["cards"]:
    out = os.path.join(path, 'Sounds', m["audio"])
    if "audio_url" in m: 
        print(f"Downloading {m['title']} ({m['anime']} - {m['numbering']})")

        temp_path = download_audio(m["audio_url"], )
        if not temp_path:
            print(f"Error while downloading {m['title']} ({m['anime']} - {m['numbering']})")
        
        normalize_audio(temp_path, out)
        os.remove(temp_path)
    else:
        if os.path.isfile(out):
            print(f"No download link provided, using exising file for {m['title']} ({m['anime']} - {m['numbering']})")
            normalize_audio(out, out)
        else:
            print(f"ERROR: No download link provided and file does not exist for {m['title']} ({m['anime']} - {m['numbering']})")
