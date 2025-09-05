import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Carrega variáveis do .env
load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-private user-read-email user-top-read playlist-read-private"
))

# Dados do usuário
user = sp.current_user()
print(f"\n👤 Usuário: {user['display_name']}")
print(f"📧 Email: {user['email']}")
print(f"🌎 País: {user['country']}")
print("-" * 40)

# Artistas mais ouvidos
print("🎧 Top artistas mais ouvidos:")
top_artistas = sp.current_user_top_artists(limit=5, time_range='medium_term')
for idx, artista in enumerate(top_artistas['items'], 1):
    print(f"{idx}. {artista['name']} ({', '.join(artista['genres'])})")

print("-" * 40)

print("🎧 Top músicas mais ouvidas nos últimos 6 meses:")
top_tracks = sp.current_user_top_tracks(limit=10, time_range='medium_term')
for idx, track in enumerate(top_tracks['items'], 1):
    print(f"{idx}. {track['name']} - {track['artists'][0]['name']}")

print("-" * 40)

print("📁 Suas playlists:")

limit = 50
offset = 0
all_playlists = []

while True:
    playlists = sp.current_user_playlists(limit=limit, offset=offset)
    all_playlists.extend(playlists['items'])
    if playlists['next']:
        offset += limit
    else:
        break

# Filtra duplicados usando o id único da playlist
unique_playlists = []
seen_ids = set()

for playlist in all_playlists:
    if playlist['id'] not in seen_ids:
        unique_playlists.append(playlist)
        seen_ids.add(playlist['id'])

# Agora printa só as playlists únicas, com numeração correta
for idx, playlist in enumerate(unique_playlists, 1):
    print(f"{idx}. {playlist['name']} ({playlist['tracks']['total']} músicas)")
