#!/usr/bin/python3

from time import sleep
from datetime import datetime
from deezspot.deezloader.__utils__ import artist_sort
from requests import get as req_get
from deezspot.libutils.utils import convert_to_date
from deezspot.libutils.others_settings import header
from deezspot.exceptions import (
    NoDataApi,
    QuotaExceeded,
    TrackNotFound,
)

class API:

	@classmethod
	def __init__(cls):
		cls.__api_link = "https://api.deezer.com/"
		cls.__cover = "https://e-cdns-images.dzcdn.net/images/cover/%s/{}-000000-80-0-0.jpg"

	@classmethod
	def __get_api(cls, url, quota_exceeded = False):
		json = req_get(url, headers = header).json()

		if "error" in json:
			if json['error']['message'] == "no data":
				raise NoDataApi("No data avalaible :(")

			elif json['error']['message'] == "Quota limit exceeded":
				if not quota_exceeded:
					sleep(0.8)
					json = cls.__get_api(url, True)
				else:
					raise QuotaExceeded

		return json

	@classmethod
	def get_chart(cls, index = 0):
		url = f"{cls.__api_link}chart/{index}"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def get_track(cls, ids):
		url = f"{cls.__api_link}track/{ids}"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def get_album(cls, ids):
		url = f"{cls.__api_link}album/{ids}"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def get_playlist(cls, ids):
		url = f"{cls.__api_link}playlist/{ids}"
		infos = cls.__get_api(url)

		return infos
	
	@classmethod
	def get_episode(cls, episode_id):
		url = f"{cls.__api_link}episode/{episode_id}"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def get_artist(cls, ids):
		url = f"{cls.__api_link}artist/{ids}"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def get_artist_top_tracks(cls, ids, limit = 25):
		url = f"{cls.__api_link}artist/{ids}/top?limit={limit}"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def get_artist_top_albums(cls, ids, limit = 25):
		url = f"{cls.__api_link}artist/{ids}/albums?limit={limit}"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def get_artist_related(cls, ids):
		url = f"{cls.__api_link}artist/{ids}/related"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def get_artist_radio(cls, ids):
		url = f"{cls.__api_link}artist/{ids}/radio"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def get_artist_top_playlists(cls, ids, limit = 25):
		url = f"{cls.__api_link}artist/{ids}/playlists?limit={limit}"
		infos = cls.__get_api(url)

		return infos

	@classmethod
	def search(cls, query):
		url = f"{cls.__api_link}search/?q={query}"
		infos = cls.__get_api(url)

		if infos['total'] == 0:
			raise NoDataApi(query)

		return infos

	@classmethod
	def search_track(cls, query):
		url = f"{cls.__api_link}search/track/?q={query}"
		infos = cls.__get_api(url)

		if infos['total'] == 0:
			raise NoDataApi(query)

		return infos

	@classmethod
	def search_album(cls, query):
		url = f"{cls.__api_link}search/album/?q={query}"
		infos = cls.__get_api(url)

		if infos['total'] == 0:
			raise NoDataApi(query)

		return infos

	@classmethod
	def search_playlist(cls, query):
		url = f"{cls.__api_link}search/playlist/?q={query}"
		infos = cls.__get_api(url)

		if infos['total'] == 0:
			raise NoDataApi(query)

		return infos

	@classmethod
	def search_artist(cls, query):
		url = f"{cls.__api_link}search/artist/?q={query}"
		infos = cls.__get_api(url)

		if infos['total'] == 0:
			raise NoDataApi(query)

		return infos

	@classmethod
	def not_found(cls, song, title):
		try:
			data = cls.search_track(song)['data']
		except NoDataApi:
			raise TrackNotFound(song)

		ids = None

		for track in data:
			if (
				track['title'] == title
			) or (
				title in track['title_short']
			):
				ids = track['id']
				break

		if not ids:
			raise TrackNotFound(song)

		return str(ids)

	@classmethod
	def get_img_url(cls, md5_image, size = "1200x1200"):
		cover = cls.__cover.format(size)
		image_url = cover % md5_image

		return image_url

	@classmethod
	def choose_img(cls, md5_image, size = "1200x1200"):
		image_url = cls.get_img_url(md5_image, size)
		image = req_get(image_url).content

		if len(image) == 13:
			image_url = cls.get_img_url("", size)
			image = req_get(image_url).content

		return image

	@classmethod
	def tracking(cls, ids, album = False, tags_separator = None):
			song_metadata = {}
			json_track = cls.get_track(ids)

			if not album:
				album_ids = json_track['album']['id']
				album_json = cls.get_album(album_ids)
				genres = []

				if "genres" in album_json:
					for genre in album_json['genres']['data']:
						genres.append(genre['name'])

				song_metadata['genre'] = " & ".join(genres)
				ar_album = []

				for contributor in album_json['contributors']:
					if contributor['role'] == "Main":
						ar_album.append(contributor['name'])

				song_metadata['ar_album'] = artist_sort(ar_album, separator=tags_separator)  
				song_metadata['album'] = album_json['title']
				song_metadata['label'] = album_json['label']
				song_metadata['upc'] = album_json['upc']
				song_metadata['nb_tracks'] = album_json['nb_tracks']

			song_metadata['music'] = json_track['title']
			song_metadata['explicit'] = json_track['explicit_lyrics']

			array = []

			for contributor in json_track['contributors']:
				if contributor['name'] != "":
					array.append(contributor['name'])

			array.append(json_track['artist']['name'])

			song_metadata['artist'] = artist_sort(array, separator=tags_separator)  
			song_metadata['tracknum'] = json_track['track_position']
			song_metadata['discnum'] = json_track['disk_number']
			song_metadata['year'] = convert_to_date(json_track['release_date'])
			song_metadata['bpm'] = json_track['bpm']
			song_metadata['duration'] = json_track['duration']
			song_metadata['isrc'] = json_track['isrc']
			song_metadata['gain'] = json_track['gain']

			return song_metadata

	@classmethod
	def tracking_album(cls, ids, tags_separator = None):
			album_json = cls.get_album(ids)
			song_metadata = {
				"music": [],
				"artist": [],
				"tracknum": [],
				"discnum": [],
				"bpm": [],
				"duration": [],
				"isrc": [],
				"gain": [],
				"album": album_json['title'],
				"label": album_json['label'],
				"year": convert_to_date(album_json['release_date']),
				"upc": album_json['upc'],
				"nb_tracks": album_json['nb_tracks']
			}

			genres = []

			if "genres" in album_json:
				for a in album_json['genres']['data']:
					genres.append(a['name'])

			song_metadata['genre'] = " & ".join(genres)
			ar_album = []

			for a in album_json['contributors']:
				if a['role'] == "Main":
					ar_album.append(a['name'])

			song_metadata['ar_album'] = artist_sort(ar_album, separator=tags_separator)  # Use custom separator
			sm_items = song_metadata.items()

			for track in album_json['tracks']['data']:
				c_ids = track['id']
				detas = cls.tracking(c_ids, album=True, tags_separator=tags_separator)  # Pass separator

				for key, item in sm_items:
					if type(item) is list:
						song_metadata[key].append(detas[key])

			return song_metadata