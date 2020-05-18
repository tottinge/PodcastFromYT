"""
Generate the XML to add an entry to an rss feed.

See notes inside print function.
"""
import sys
import os
import json
import eyed3
import re
import uuid
from datetime import datetime
from pytz import timezone
from shutil import copyfile
from box import Box
import xml.etree.cElementTree as ET
from xml.sax.saxutils import escape
from config import author_name, author_email, itunes_image, TARGET_DIR

HOUR_SECS = 60*60
MIN_SECS = 60

author_full_email = f'{author_email} ({author_name})'


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

def make_url(new_filename):
    return f'{host_site}/{new_filename}'

def format_duration(duration):
    duration = str(int(duration)).zfill(6)
    hours = duration[:2]
    minutes = duration[2:4]
    seconds = duration[4:]
    return f'{hours}:{minutes}:{seconds}'

def clean_title(title):
    if '|' in title:
        _, title = title.split('|')
    return escape(title.strip())

CENTRAL = timezone('US/Central')
def RFC822_date():
    now = datetime.now(tz=CENTRAL)
    return now.strftime('%a, %d %b %Y %X %z')

def print_stanza(file_size, new_filename, youtube_json):
    """ the hack 
    In this case, I just use string interpolation and rely upon xmllint and feed validators.
    It works because I spent the time fixing it when it didn't not because it's algorithmically
    likely. It's trial-and-error and copy-the-example. Not good.
    """
    guid = uuid.uuid4().hex
    duration = format_duration(youtube_json.duration)
    length_in_bytes = str(file_size)
    title = clean_title(youtube_json.title)
    return f"""
        <item>
        <title>{title}</title>
        <link>{youtube_json.webpage_url}</link>
        <author>{author_full_email}</author>
        <pubDate>{RFC822_date()}</pubDate>
        <guid isPermaLink="false">{guid}</guid>
        <enclosure url="{make_url(new_filename)}" length="{length_in_bytes}" type="audio/mp3"/>
        <itunes:author>{author_email}</itunes:author>
        <itunes:image href="{itunes_image}" />
        <itunes:duration>{duration}</itunes:duration>
        <description>{youtube_json.description}</description>
        </item>
    """



def make_xml(new_filename, file_size, youtube_json):
    """ real engineering
    Rather than relying on string interpolation, I construct HTML nodes.
    The library providers have a vested interest in being valid, so I rely upon
    them and the community to build a good parser/builder/manipulator.
    """
    item = ET.Element('item')
    def add_sub(*args):
        return ET.SubElement(item, *args)

    add_sub('title' ).text = clean_title(youtube_json.title)
    add_sub('link').text = youtube_json.webpage_url
    add_sub('author').text = author_full_email
    add_sub('pubDate').text = RFC822_date()
    add_sub('guid', {'isPermaLink':'false'}).text = uuid.uuid4().hex
    add_sub('enclosure', {'url':make_url(new_filename), 'length':str(file_size), 'type':'audio/mp3'})
    add_sub('itunes:author').text = author_email
    add_sub('itunes:image').text = itunes_image
    add_sub('itunes:duration').text = format_duration(youtube_json.duration)
    add_sub('description').text = escape(youtube_json.description)
    return item

def add_new_item(doc, new_item):
    channel = doc.find('channel')
    top_item = channel.find('item')
    top_item_location = channel.getchildren().index(top_item)
    channel.insert(top_item_location, new_item)
    

def print_stanza_and_copy_file(sourcefile):
    # Collect data
    filesize = os.stat(sourcefile).st_size
    base_filename,_ = os.path.splitext(sourcefile)
    jdoc = get_youtube_json_for(base_filename)
    new_filename = create_mp3_filename_from_title(jdoc.title)

    # Create/print the XML for the new entry
    xml = print_stanza(filesize, new_filename, jdoc)
    print(xml)
    
    # Copy file
    targetfile = os.path.join(TARGET_DIR, new_filename)
    copyfile(sourcefile, targetfile)


if __name__ == "__main__":
    if len(sys.argv) <2:
        print("what mp3 files do you want? No parameters given.")
        exit(1)
    for sourcefile in sys.argv[1:]:
        if not sourcefile.endswith('mp3'):
            print(f'{sourcefile} is not an mp3? Skipping.')
            continue
        print_stanza_and_copy_file(sourcefile)
