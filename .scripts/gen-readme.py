import json, os

path = os.environ.get('DECK_PATH', os.path.pardir)
if not os.path.isabs(path):
    path = os.path.join(os.path.dirname(__file__), path)

with open(os.path.join(path, 'deck.json'), "r") as file:
    meta = json.load(file)

with open(os.path.join(path, 'README.md'), "w") as file:
    file.write(f"# {meta['name']}\n")
    file.write(f"**Auteur :** {meta['author']}  \n")
    file.write(f"**Categorie :** {meta['category']}  \n")
    file.write(f"**Type :** {meta['type']}  \n\n")

    file.write(f"{meta['description']}  \n\n")

    file.write(f"**Couverture :**  \n")
    file.write(f'<img src="cover.png" alt="Image de couverture" width="250"/>  \n\n')

    file.write(f"## Liste des cartes :\n")

    for c in meta['cards']:
        if 'audio_url' in c:
            file.write(f"### [{c['id']:02d} - {c['title']}]({c['audio_url']})\n")
        else:
            file.write(f"### {c['id']:02d} - {c['title']}\n")
        file.write(f"&emsp;**Anime :** [{c['anime']}](https://anilist.co/anime/{c['anilist_id']}) - {c['numbering']}  \n")
        file.write(f"&emsp;**Artiste(s) :** {c['authors']}  \n\n")
        file.write(f'<img src="Visuals/{c['image'].replace(" ", "%20")}" alt="{" ".join([c['anime'], c['numbering'], c['title']])}" width="250"/>  \n\n')