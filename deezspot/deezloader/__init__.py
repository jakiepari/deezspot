#!/usr/bin/python3
from deezspot.deezloader.dee_api import API
from deezspot.easy_spoty import Spo
from deezspot.deezloader.deegw_api import API_GW
from deezspot.deezloader.deezer_settings import stock_quality
from deezspot.models import (
    Track,
    Album,
    Playlist,
    Preferences,
    Smart,
	Episode,
)
from deezspot.deezloader.__download__ import (
    DW_TRACK,
    DW_ALBUM,
    DW_PLAYLIST,
    DW_EPISODE,
)
from deezspot.exceptions import (
    InvalidLink,
    TrackNotFound,
    NoDataApi,
    AlbumNotFound,
)
from deezspot.libutils.utils import (
    create_zip,
    get_ids,
    link_is_valid,
    what_kind,
)
from deezspot.libutils.others_settings import (
    stock_output,
    stock_recursive_quality,
    stock_recursive_download,
    stock_not_interface,
    stock_zip,
    method_save,
)

API()

class DeeLogin:
	def __init__(
			self,
			arl=None,
			email=None,
			password=None,
			ensure_premium=False,
			tags_separator=None  
		) -> None:
			if arl:
				self.__gw_api = API_GW(arl=arl)
			else:
				self.__gw_api = API_GW(
					email=email,
					password=password
				)

			self.ensure_premium = ensure_premium
			self.tags_separator = tags_separator  
			self.__check_premium_status()

	def __check_premium_status(self):
			account_info = self.__gw_api.get_account_info()
			if not account_info.get('is_premium', False):
				if self.ensure_premium:
					raise Exception("Premium account is required but not found.")
				else:
					print("Warning: You are not using a premium account. FLAC quality downloads will not be available.")

	def download_trackdee(
			self, link_track,
			output_dir=stock_output,
			quality_download=stock_quality,
			recursive_quality=stock_recursive_quality,
			recursive_download=stock_recursive_download,
			not_interface=stock_not_interface,
			method_save=method_save
		) -> Track:
			link_is_valid(link_track)
			ids = get_ids(link_track)

			try:
				song_metadata = API.tracking(ids, tags_separator=self.tags_separator)  # Pass the separator
			except NoDataApi:
				infos = self.__gw_api.get_song_data(ids)

				if not "FALLBACK" in infos:
					raise TrackNotFound(link_track)

				ids = infos['FALLBACK']['SNG_ID']
				song_metadata = API.tracking(ids, tags_separator=self.tags_separator)  # Pass the separator

			preferences = Preferences()

			preferences.link = link_track
			preferences.song_metadata = song_metadata
			preferences.quality_download = quality_download
			preferences.output_dir = output_dir
			preferences.ids = ids
			preferences.recursive_quality = recursive_quality
			preferences.recursive_download = recursive_download
			preferences.not_interface = not_interface
			preferences.method_save = method_save

			track = DW_TRACK(preferences).dw()

			return track

	def download_albumdee(
		self, link_album,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		make_zip = stock_zip,
		method_save = method_save
	) -> Album:

		link_is_valid(link_album)
		ids = get_ids(link_album)

		try:
			album_json = API.get_album(ids)
		except NoDataApi:
			raise AlbumNotFound(link_album)

		song_metadata = API.tracking_album(ids, tags_separator=self.tags_separator)

		preferences = Preferences()

		preferences.link = link_album
		preferences.song_metadata = song_metadata
		preferences.quality_download = quality_download
		preferences.output_dir = output_dir
		preferences.ids = ids
		preferences.json_data = album_json
		preferences.recursive_quality = recursive_quality
		preferences.recursive_download = recursive_download
		preferences.not_interface = not_interface
		preferences.method_save = method_save
		preferences.make_zip = make_zip

		album = DW_ALBUM(preferences).dw()

		return album

	def download_playlistdee(
		self, link_playlist,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		make_zip = stock_zip,
		method_save = method_save
	) -> Playlist:

		link_is_valid(link_playlist)
		ids = get_ids(link_playlist)

		song_metadata = []
		playlist_json = API.get_playlist(ids)

		for track in playlist_json['tracks']['data']:
			c_ids = track['id']

			try:
				c_song_metadata = API.tracking(c_ids)
			except NoDataApi:
				infos = self.__gw_api.get_song_data(c_ids)

				if not "FALLBACK" in infos:
					c_song_metadata = f"{track['title']} - {track['artist']['name']}"
				else:
					c_song_metadata = API.tracking(c_ids)

			song_metadata.append(c_song_metadata)

		preferences = Preferences()

		preferences.link = link_playlist
		preferences.song_metadata = song_metadata
		preferences.quality_download = quality_download
		preferences.output_dir = output_dir
		preferences.ids = ids
		preferences.json_data = playlist_json
		preferences.recursive_quality = recursive_quality
		preferences.recursive_download = recursive_download
		preferences.not_interface = not_interface
		preferences.method_save = method_save
		preferences.make_zip = make_zip

		playlist = DW_PLAYLIST(preferences).dw()

		return playlist

	def download_artisttopdee(
		self, link_artist,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface
	) -> list[Track]:

		link_is_valid(link_artist)
		ids = get_ids(link_artist)

		playlist_json = API.get_artist_top_tracks(ids)['data']

		names = [
			self.download_trackdee(
				track['link'], output_dir,
				quality_download, recursive_quality,
				recursive_download, not_interface
			)

			for track in playlist_json
		]

		return names

	def download_name(
		self, artist, song,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		method_save = method_save
	) -> Track:

		query = f"track:{song} artist:{artist}"
		search = self.__spo.search(query)
		items = search['tracks']['items']

		if len(items) == 0:
			msg = f"No result for {query} :("
			raise TrackNotFound(message = msg)

		link_track = items[0]['external_urls']['spotify']

		track = self.download_trackspo(
			link_track,
			output_dir = output_dir,
			quality_download = quality_download,
			recursive_quality = recursive_quality,
			recursive_download = recursive_download,
			not_interface = not_interface,
			method_save = method_save
		)

		return track

	def download_episode(
		self,
		link_episode,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		method_save = method_save
	) -> Episode:
		
		link_is_valid(link_episode)
		ids = get_ids(link_episode)
		
		try:
			episode_metadata = API.tracking(ids)
		except NoDataApi:
			infos = self.__gw_api.get_episode_data(ids)
			if not infos:
				raise TrackNotFound("Episode not found")
			episode_metadata = {
				'music': infos.get('EPISODE_TITLE', ''),
				'artist': infos.get('SHOW_NAME', ''),
				'album': infos.get('SHOW_NAME', ''),
				'date': infos.get('EPISODE_PUBLISHED_TIMESTAMP', '').split()[0],
				'genre': 'Podcast',
				'explicit': infos.get('SHOW_IS_EXPLICIT', '2'),
				'disc': 1,
				'track': 1,
				'duration': int(infos.get('DURATION', 0)),
				'isrc': None,
				'image': infos.get('EPISODE_IMAGE_MD5', '')
			}

		preferences = Preferences()
		preferences.link = link_episode
		preferences.song_metadata = episode_metadata
		preferences.quality_download = quality_download
		preferences.output_dir = output_dir
		preferences.ids = ids
		preferences.recursive_quality = recursive_quality
		preferences.recursive_download = recursive_download
		preferences.not_interface = not_interface
		preferences.method_save = method_save

		episode = DW_EPISODE(preferences).dw()

		return episode
	
	def download_smart(
		self, link,
		output_dir=stock_output,
		quality_download=stock_quality,
		recursive_quality=stock_recursive_quality,
		recursive_download=stock_recursive_download,
		not_interface=stock_not_interface,
		make_zip=stock_zip,
		method_save=method_save
	) -> Smart:

		link_is_valid(link)
		link = what_kind(link)
		smart = Smart()

		if "spotify.com" in link:
			source = "https://spotify.com"

		elif "deezer.com" in link:
			source = "https://deezer.com"

		smart.source = source

		if "track/" in link:
			if "deezer.com" in link:
				func = self.download_trackdee
				
			else:
				raise InvalidLink(link)

			track = func(
				link,
				output_dir=output_dir,
				quality_download=quality_download,
				recursive_quality=recursive_quality,
				recursive_download=recursive_download,
				not_interface=not_interface,
				method_save=method_save
			)

			smart.type = "track"
			smart.track = track

		elif "album/" in link:
			if "deezer.com" in link:
				func = self.download_albumdee

			else:
				raise InvalidLink(link)

			album = func(
				link,
				output_dir=output_dir,
				quality_download=quality_download,
				recursive_quality=recursive_quality,
				recursive_download=recursive_download,
				not_interface=not_interface,
				make_zip=make_zip,
				method_save=method_save
			)

			smart.type = "album"
			smart.album = album

		elif "playlist/" in link:
			if "deezer.com" in link:
				func = self.download_playlistdee

			else:
				raise InvalidLink(link)

			playlist = func(
				link,
				output_dir=output_dir,
				quality_download=quality_download,
				recursive_quality=recursive_quality,
				recursive_download=recursive_download,
				not_interface=not_interface,
				make_zip=make_zip,
				method_save=method_save
			)

			smart.type = "playlist"
			smart.playlist = playlist

		return smart
