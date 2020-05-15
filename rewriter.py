import getmeta

ORIGINAL = '../podcastMA/index.rss'
TARGET = 'ATTEMPT.rss'
MP3 = "Modern Agile Show #44 _ Interview with Jeff 'Cheezy' Morgan-wpbVe8l3CXM.mp3"

getmeta.rewrite_rss_file(ORIGINAL, TARGET, MP3)
