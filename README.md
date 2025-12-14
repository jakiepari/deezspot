# DeezSpot 🎵

A powerful Python and Lightweight library for downloading music from Deezer and Spotify. Clone of the original deezloader with additional features and improvements.

### ⚠️ IMPORTANT NOTES !!!!! ⚠️
```
USE AS YOUR OWN RISK I'M NOT RESPONSIBLE TO ANY YOUR PROBLEM AT SPOTIFY OR DEEZER ACCOUNT !
```
## ✨ Features

- Download songs, albums, playlists from Deezer
- Download songs, albums, playlists, episode from Spotify
- Support for multiple audio qualities (MP3, FLAC) and OGG for spotify
- Download podcast episodes
- Batch downloading
- Progress bar support
- ID3 tags and artwork

## 🚀 Installation

```bash
pip install deezspot
```
But will be better use this one
```bash
pip install git+https://github.com/jakiepari/deezspot
```

Also you need to install this package:
```bash
pip install git+https://github.com/kokarare1212/librespot-python
```

## 🔑 Authentication Setup

### Deezer Authentication
1. Get your Deezer ARL token from browser cookies after logging in to Deezer
2. Use the token in your code:
```python
from deezspot.deezloader import DeeLogin

dl = DeeLogin(arl='your_arl_token', email='your_Deezer_email', password='your_Deezer_password', tags_separator=" / ")
```

### Spotify Authentication
1. Clone the librespot-auth repository:
```bash
git clone https://github.com/dspearson/librespot-auth
cd librespot-auth
cargo build --release
```

2. Generate credentials:
```bash
./target/release/librespot-auth
```

3. Adjust your credentials.json with the format:
```json
{
    "username": "your_spotify_username",
    "credentials": "your_credentials_string",
    "type": "AUTHENTICATION_STORED_SPOTIFY_CREDENTIALS"
}
```

# Or also you can use this code
```python
from librespot.zeroconf import ZeroconfServer
import time
import logging
import pathlib

zs = ZeroconfServer.Builder().create()
logging.warning("Transfer playback from desktop client to librespot-python via Spotify Connect in order to store session")

while True:
    time.sleep(1)
    if zs._ZeroconfServer__session:
        logging.warning(f"Grabbed {zs._ZeroconfServer__session} for {zs._ZeroconfServer__session.username()}")
        
        if pathlib.Path("credentials.json").exists():
            logging.warning("Session stored in credentials.json. Now you can Ctrl+C")
            break
```
Steps:
Its same like using the code from librespot-auth. but you need a premium plan to use this code!
Just play 1 song and then click connect to a device and select librespot-python then your credentials.json will be appear

## 📚 Usage Examples

### Downloading with Deezer 
```python
import sys
import os
import traceback

# Add the local deezspot directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from deezspot.deezloader import DeeLogin
from deezspot.spotloader import SpoLogin

try:
    # Deezer Example
    print("Initializing Deezer client...")
    deezer = DeeLogin(arl='your_arl_token', email='', password='', tags_separator=" / ")

    # Download a single track from Deezer
    deezer.download_trackdee(
        link_track='https://www.deezer.com/track/123456789',
        output_dir='./downloads/deezer/tracks',
        quality_download='MP3_320',
        recursive_quality=False,
        recursive_download=False
    )

    # Download an album from Deezer
    deezer.download_albumdee(
        link_album='https://www.deezer.com/album/123456789',
        output_dir='./downloads/deezer/albums',
        quality_download='FLAC',
        recursive_quality=True,
        recursive_download=False
    )

    # Download a playlist from Deezer
    deezer.download_playlistdee(
        link_playlist='https://www.deezer.com/playlist/123456789',
        output_dir='./downloads/deezer/playlists',
        quality_download='MP3_320',
        recursive_quality=True,
        recursive_download=False
    )

    # Download an artist's top tracks from Deezer
    deezer.download_artisttopdee(
        link_artist='https://www.deezer.com/artist/123456789',
        output_dir='./downloads/deezer/artists',
        quality_download='MP3_320',
        recursive_quality=True,
        recursive_download=False
    )

    # Download an episode from Deezer
    deezer.download_episode(
        link_episode='https://www.deezer.com/episode/123456789',
        output_dir='./downloads/deezer/episodes',
        quality_download='MP3_320',
        recursive_quality=True,
        recursive_download=False
    )

    # Spotify Example
    print("Initializing Spotify client...")
    credentials_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'credentials.json'))
    spotify = SpoLogin(credentials_path=credentials_path, client_id='your_client_id', client_secret='your_client_secret')

    # Download a single track from Spotify
    spotify.download_track(
        link_track="https://open.spotify.com/track/4tCtwWceOPWzenK2HAIJSb",
        output_dir="./downloads/spotify/tracks",
        quality_download="NORMAL",
        recursive_quality=False,
        recursive_download=False,
        not_interface=False,
        method_save=1
    )

    # Download an album from Spotify
    spotify.download_album(
        link_album="https://open.spotify.com/album/6n4YU8iRm07O7lR1zQZypN",
        output_dir="./downloads/spotify/albums",
        quality_download="NORMAL",
        recursive_quality=True,
        recursive_download=False,
        not_interface=False,
        method_save=1,
        make_zip=True
    )

    # Download a playlist from Spotify
    spotify.download_playlist(
        link_playlist="https://open.spotify.com/playlist/1ZyEi4bBTYGTIlY23U1kwG",
        output_dir="./downloads/spotify/playlists",
        quality_download="NORMAL",
        recursive_quality=True,
        recursive_download=False,
        not_interface=False,
        method_save=1,
        make_zip=True
    )

    # Download an episode from Spotify
    spotify.download_episode(
        link_episode="https://open.spotify.com/episode/1hgO8Y3CCymyxn934lNtDq",
        output_dir="./downloads/spotify/episodes",
        quality_download="NORMAL",
        recursive_quality=False,
        recursive_download=False,
        not_interface=False,
        method_save=1
    )

except Exception as e:
    traceback.print_exc()
```

## 📋 Supported Formats
# Deezer
- MP3_128
- MP3_320 (SOMETIMES NEED PAID DEEZER)
- FLAC (PAID DEEZER ONLY)
# Spotify
- NORMAL
- HIGH
- VERY_HIGH
## NOTE !
Sometimes when you using spotloader after downloading 20+ tracks, Will be giving an error about audio key. its because you're using free spotify!

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚖️ License

This project is licensed under the GNU Affero General Public License v3 - see the 

LICENSE

 file for details.

## 🙏 Acknowledgments

- Original deezloader project
- Deezer API
- Spotify API
- Spotify Anon
- librespot-python
- librespot-auth

## ⭐️ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=jakiepari/deezspot&type=Date)](https://star-history.com/#jakiepari/deezspot&Date)
