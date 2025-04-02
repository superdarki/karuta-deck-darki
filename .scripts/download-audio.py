import yt_dlp
from pydub import AudioSegment, effects
import json, os, tempfile, argparse

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

def valid_directory(path):
    if os.path.isdir(path): return path
    else: raise argparse.ArgumentTypeError(f"'{path}' is not a valid directory.")
parser = argparse.ArgumentParser(description="Download and normalize the audio files for the deck")
parser.add_argument("--deck-path", type=valid_directory, help="Path to the deck directory", default=os.path.pardir)
parser.add_argument("-f", "--force", action="store_true", help="Force re-download if file already exists")
args = parser.parse_args()

path = args.deck_path
if not os.path.isabs(path): path = os.path.join(os.path.dirname(__file__), path)

with open(os.path.join(path, 'deck.json'), "r") as file:
    meta = json.load(file)

print(f"Loaded {meta['name']}\n")

for m in meta["cards"]:
    fout = os.path.join(path, 'Sounds', m["audio"])
    fin = fout
    if (os.path.isfile(fout) and args.force) or not os.path.isfile(fout):
        if "audio_url" in m: 
            print(f"Downloading {m['title']} ({m['anime']} - {m['numbering']})")

            fin = download_audio(m["audio_url"])
            if not fin:
                print(f"Error while downloading {m['title']} ({m['anime']} - {m['numbering']})")

    if os.path.isfile(fin):  
        print(f"Normalizing {m['title']} ({m['anime']} - {m['numbering']})")   
        normalize_audio(fin, fout)
        if fin != fout:
            os.remove(fin)
    else:
        print(f"ERROR: No download link provided and file does not exist for {m['title']} ({m['anime']} - {m['numbering']})")
    
