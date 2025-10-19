from setuptools import setup

README = open("README.md", "r")
readmed = README.read()
README.close()

setup(
	name = "deezspot",
	version = "1.6",
	description = "Downloads songs, albums or playlists from deezer and spotify (clone from https://pypi.org/project/deezloader/)",
	long_description = readmed,
	long_description_content_type = "text/markdown",
	license = "GNU Affero General Public License v3",
	python_requires = ">=3.10",
	author = "jakiepari",
	author_email = "farihmuhammad75@gmail.com",
	url = "https://github.com/jakiepari/deezspot",

	packages = [
		"deezspot",
		"deezspot/models", "deezspot/spotloader",
		"deezspot/deezloader", "deezspot/libutils"
	],

        install_requires = [
                "mutagen", "pycryptodome", "requests",
                "spotipy", "tqdm", "fastapi",
                "uvicorn[standard]",
                "spotipy-anon",
                "librespot"
         ],
)
