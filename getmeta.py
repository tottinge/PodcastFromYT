"""
Generate the XML to add an entry to an rss feed.

See notes inside print function.
"""
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

def clean_title(title):
    return title

central = timezone('US/Central')
def RFC822_date():
    now = datetime.now(tz=central)
    return now.strftime('%a, %d %b %Y %X %z')

def print_stanza(base_filename, new_filename, youtube_json):
    """This is almost perfectly wrong.
    It's handy to print while we work things out in absence of unit tests.
    But really, printing an interpolated string is awful. 
    We should REALLY be opening the index.rss and inserting the <item> nodes
    directly instead of copy paste. This is pretty dumb, really.
    But it works okay for right now, and helps us get a start.
    It's not THE ANSWER.
    It's for right now, only.
    """
    tags = get_tags_for(base_filename)
    new_filename = create_mp3_filename_from_title(youtube_json.title)
    guid = uuid.uuid4().hex
    duration = format_duration(youtube_json.duration)
    length_in_bytes = tags.info.size_bytes
    title = clean_title(youtube_json.title)

    print(f"""
    <item>
      <title>{title}</title>
      <link>{youtube_json.webpage_url}</link>
      <author>joshua@industriallogic.com (Joshua Kerievsky)</author>
      <pubDate>{RFC822_date()}</pubDate>
      <guid isPermaLink="false">{guid}</guid>
      <enclosure url="http://www.modernagile.org/podcast/{new_filename}" length="{length_in_bytes}" type="audio/mp3"/>
      <itunes:author>joshua@industriallogic.com</itunes:author>
      <itunes:image href="http://www.modernagile.org/podcast/cover_1400.jpg" />
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
