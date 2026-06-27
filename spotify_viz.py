import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import sys

# Fix Windows CMD emoji crash
sys.stdout.reconfigure(encoding='utf-8')

# --- Authentication ---
# Replace these with your credentials from the Spotify Developer Dashboard!
CLIENT_ID = "PASTE_YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = "PASTE_YOUR_CLIENT_SECRET_HERE"

if "PASTE_YOUR_" in CLIENT_ID or "PASTE_YOUR_" in CLIENT_SECRET:
    print("❌ Error: Missing Spotify credentials. Please paste them into the code.")
    sys.exit(1)

# We use ClientCredentials because we are searching public data, not personal data.
# This bypasses the Premium requirement!
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

print("✅ Successfully connected to Spotify!")

# --- Search for an Artist's Top Tracks ---
# Change "Daft Punk" to your favorite artist!
artist_name = "Daft Punk"
print(f"🎵 Fetching top tracks for {artist_name}...")

try:
    # Search for the artist
    result = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    if not result["artists"]["items"]:
        print(f"❌ Could not find artist: {artist_name}")
        sys.exit(1)
        
    artist_id = result["artists"]["items"][0]["id"]
    
    # Get their top 10 tracks
    tracks_data = sp.artist_top_tracks(artist_id, country="US")["tracks"][:10]
except Exception as e:
    print(f"❌ Spotify API error: {e}")
    sys.exit(1)

track_names = []
popularity = []
duration_min = []

for track in tracks_data:
    track_names.append(track["name"])
    # Get popularity (0-100) and duration (convert from milliseconds to minutes)
    popularity.append(track["popularity"])
    duration_min.append(track["duration_ms"] / 60000)
    print(f"  • {track['name']}")

print(f"\n✅ Found {len(track_names)} tracks!")

# --- Create the Visualization ---
plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(12, 7))

ax.scatter(
    duration_min,
    popularity,
    color="#1DB954",     # Spotify Green
    s=120,
    edgecolors="white",
    linewidths=0.5,
    alpha=0.9,
    zorder=5
)

for i, name in enumerate(track_names):
    ax.annotate(
        name,
        (duration_min[i], popularity[i]),
        textcoords="offset points",
        xytext=(8, 8),
        fontsize=9,
        color="white",
        alpha=0.85
    )

ax.set_title(
    f"🎵 {artist_name} Top Tracks: Duration vs. Popularity",
    fontsize=18,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("← Shorter · · · Duration (Minutes) · · · Longer →", fontsize=12)
ax.set_ylabel("← Underground · · · Popularity · · · Mainstream →", fontsize=12)

ax.grid(color="#535353", linestyle="--", linewidth=0.5, alpha=0.5)

plt.tight_layout()
plt.savefig("my_spotify_vibes.png", dpi=150, bbox_inches="tight")
plt.show()

print("✅ Visualization saved as 'my_spotify_vibes.png'!")