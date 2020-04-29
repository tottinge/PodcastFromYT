import sys
from os.path import join as pathjoin
from os.path import splitext
import json
import eyed3
import re
import uuid
from datetime import datetime
from pytz import timezone
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
    duration = str(int(duration)).zfill(6)
    hours = duration[:2]
    minutes = duration[2:4]
    seconds = duration[4:]
    return f"{hours}:{minutes}:{seconds}"


central = timezone('US/Central')
def RFC822_date():
    now = datetime.now(tz=central)
    return now.strftime('%a, %d %b %Y %X %z')

def print_stanza(base_filename, new_filename, youtube_json):
    tags = get_tags_for(base_filename)
    new_filename = create_mp3_filename_from_title(youtube_json.title)
    guid = uuid.uuid4().hex
    duration = format_duration(youtube_json.duration)
    length_in_bytes = tags.info.size_bytes

    print(f"""
    <item>
      <title>{youtube_json.title}</title>
      <itunes:author>joshua@industriallogic.com</itunes:author>
      <author>joshua@industriallogic.com (Joshua Kerievsky)</author>

      <itunes:image href="http://www.modernagile.org/podcast/cover_1400.jpg" />
      <enclosure url="http://www.modernagile.org/podcast/{new_filename}" length="{length_in_bytes}" type="audio/mp3"/>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{RFC822_date()}</pubDate>
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
    if len(sys.argv) <2:
        print("what mp3 files do you want? No parameters given.")
        exit(1)
    for sourcefile in sys.argv[1:]:
        process_file(sourcefile)
