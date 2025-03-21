from pytubefix import YouTube
from pydub import AudioSegment, effects
import io, json, os, sys

def progress_function(chunk, file_handle, bytes_remaining):
    current = ((chunk.filesize - bytes_remaining) / chunk.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()

def download_and_normalize_audio(url, path):
    yt = YouTube(url, on_progress_callback=progress_function)
    audio_stream = yt.streams.filter(only_audio=True).first()

    audio_data = io.BytesIO()
    audio_stream.stream_to_buffer(audio_data)
    audio_data.seek(0)

    audio = AudioSegment.from_file(audio_data, format="m4a")
    normalized_audio = effects.normalize(audio)
    file_path = path
    normalized_audio[:120000].export(file_path, format="mp3")
    
    print()
    return file_path

path = os.environ.get('DECK_PATH', os.path.pardir)
if not os.path.isabs(path):
    path = os.path.join(os.path.dirname(__file__), path)

with open(os.path.join(path, 'deck.json'), "r") as file:
    meta = json.load(file)

print(f"Loaded {meta['name']}\n")

for m in meta["cards"]:
    print(f"Downloading {m['title']} ({m['anime']} - {m['numbering']})")
    download_and_normalize_audio(m["audio_url"], os.path.join(path, 'Sounds', m["audio"]))
