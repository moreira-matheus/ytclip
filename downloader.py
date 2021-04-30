import json
from ytclip import YTClip

OUTPUT_FOLDER = './output'

LINK_FIELD = 'link'
START_FIELD = 'start_cut'
END_FIELD = 'end_cut'
EXT_FIELD = 'extension'

with open('config.json', 'r') as file:
	config = json.load(file)

for video in config:
    clip = YTClip(link=video[LINK_FIELD], extension=video[EXT_FIELD])
    clip.get_video()
    clip.dowload(output_folder=OUTPUT_FOLDER)
    clip.create_subclip(video[START_FIELD], video[END_FIELD])
