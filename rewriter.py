import os
from getmeta import get_youtube_json_for, create_mp3_filename_from_title, make_xml, add_new_item
import xml.etree.cElementTree as ET
import vkbeautify as beautify

ORIGINAL = '../podcastMA/index.rss'
TARGET = 'ATTEMPT.rss'
MP3 = "Modern Agile Show #44 _ Interview with Jeff 'Cheezy' Morgan-wpbVe8l3CXM.mp3"

def rewrite_rss_file(oldname, newname, mp3file):
    if oldname == newname:
        raise Exception("old and new name should not be the same - unsafe.")

    # Why duplicate all of this? Isn't this just one thing? 
    filesize = os.stat(mp3file).st_size
    base_filename,_ = os.path.splitext(mp3file)
    youtube = get_youtube_json_for(base_filename)
    new_filename = create_mp3_filename_from_title(youtube.title)


    # This seems simple enough
    new_podcast = make_xml(new_filename, filesize, youtube)

    # Read, append, write (what OUGHT to be here)
    document = ET.parse(oldname)
    add_new_item(document, new_podcast)
    with open(newname,"w") as docfile
        docfile.write( beautify.xml(document) )
    
