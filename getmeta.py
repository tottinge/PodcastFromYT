import sys
from os.path import join as pathjoin
from os.path import splitext
import json
import eyed3
import re
import uuid
from datetime import datetime
from shutil import copyfile
from box import Box

TARGET_DIR="/Users/tottinge/Projects/podcastMA/"

def get_tags_for(base_filename):
    mp3_filename = base_filename+'.mp3'
    return eyed3.load(mp3_filename)

def get_youtube_json_for(base_filename):
    json_filename = base_filename + '.info.json'
    return Box( json.load( open(json_filename)));

def create_mp3_filename_from_title(title):
    unspaced = title.replace(' ', '_')
    without_punctuation = re.sub('\W', '', unspaced)
    return without_punctuation.replace('__', '_') + '.mp3'

HOUR_SECS = 60*60
MIN_SECS = 60
def format_duration(duration):
    hours = int(duration / HOUR_SECS)
    minutes = int((duration % HOUR_SECS) / MIN_SECS)
    seconds = int(duration % MIN_SECS)
    return f"{hours}:{minutes}:{seconds}"


def print_stanza(base_filename, new_filename, youtube_json):
    tags = get_tags_for(base_filename)
    new_filename = create_mp3_filename_from_title(youtube_json.title)
    guid = uuid.uuid4().hex
    duration = format_duration(youtube_json.duration)
    length_in_bytes = tags.info.size_bytes
    upload_date_ctime = datetime.now().ctime()

    print(f"""
    <item>
      <title>{youtube_json.title}</title>
      <itunes:author>joshua@industriallogic.com</itunes:author>
      <author>joshua@industriallogic.com</author>

      <itunes:image href="http://www.modernagile.org/podcast/cover_1400.jpg" />
      <enclosure url="http://www.modernagile.org/podcast/{new_filename}" length="{length_in_bytes}" type="audio/mp3"/>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{upload_date_ctime}</pubDate>
      <itunes:duration>{duration}</itunes:duration>
      <description>{youtube_json.description}</description>
    </item>
    """)


def process_file(sourcefile):
    base_filename,_ = splitext(sourcefile)
    jdoc = get_youtube_json_for(base_filename)
    new_filename = create_mp3_filename_from_title(jdoc.title)
    print_stanza(base_filename, new_filename, jdoc)

    targetfile = pathjoin(TARGET_DIR, new_filename)
    copyfile(sourcefile, targetfile)

if __name__ == "__main__":
    print(f'args are {sys.argv}')
    sourcefile = '#ModernAgileShow 39 _ Interview with David Parker-S8UyNaRL09o.mp3'
    process_file(sourcefile)
