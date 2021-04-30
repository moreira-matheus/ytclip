import string
from pytube import YouTube
from moviepy.editor import VideoFileClip

MAX_LEN_TITLE = 32
CODECS = {'mp4': 'mpeg4',
          'avi': 'png',
		  'ogv': 'libvorbis',
		  'webm': 'libvpx'}

class YTClip:
	def __init__(self, link, extension):
		self.link = link
		self.extension = extension
		self.video = None
		self.stream = None
		self.title = ''
		self.output_folder = './'

	def __process_title(self, title):
		new_title = title.replace(' ', '_')\
			.translate(str.maketrans('', '', string.punctuation))
		length = min([len(new_title), MAX_LEN_TITLE])
		return new_title[:length]

	def _get_clip_fname(self):
		print('FNAME:', self.title + '.' + self.extension)
		return self.title + '.' + self.extension

	def _get_subclip_path(self):
		full_path = self._get_full_path()
		new_path = full_path.replace('.' + self.extension, '_CUT.' + self.extension)
		return new_path

	def _get_full_path(self):
		return self.output_folder + '/' + self._get_clip_fname()

	def get_video(self):
		self.video = YouTube(self.link)
		self.title = self.__process_title(self.video.title)

	def dowload(self, output_folder='./'):
		self.output_folder = output_folder
		self.stream = self.video.streams\
			.filter(file_extension=self.extension)\
				.get_highest_resolution()

		try:
			self.stream.download(self.output_folder, self.title)
		except Exception as ex:
			print(ex)
			exit(1)

	def create_subclip(self, t_start, t_end):
		clip = VideoFileClip(self._get_full_path()).subclip(t_start, t_end)
		clip.write_videofile(self._get_subclip_path(),\
			codec=CODECS.get(self.extension, None))