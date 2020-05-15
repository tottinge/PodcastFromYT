import unittest
from box import Box
import xml.etree.cElementTree as ET
from getmeta import make_xml, add_new_item

class TestXMLMaker(unittest.TestCase):
    def setUp(self):
        # Easier to fake than to read a proper json
        self.mp3 = Box({
            'info':{'size_bytes':'2048'},
            })
        self.youtube = Box({
            'title':'Fake Title For Episode',
            'duration':'2364',
            'description':'some kind of crazy description',
            'webpage_url':'some.podcast.page/stuff.html'
            })

    def test_fields_are_well_formed(self):
        filename = "somefile.mp3"
        mp3 = self.mp3
        youtube = self.youtube

        result = make_xml(filename, mp3, youtube)

        self.assertIn('Fake Title', result.find('title').text )
        self.assertIn('00:23:64', result.find('itunes:duration').text )
        self.assertIn('2048', result.find('enclosure').attrib['length'])
        self.assertIn(filename, result.find('enclosure').attrib['url'])
        self.assertEqual(youtube.description, result.find('description').text)
        

    def test_insert_at_top_of_list(self):
        from io import BytesIO
        doc = ET.parse(BytesIO(test_data))
        channel = doc.find('channel')
        old_first = doc.find('channel/item')
        expected_index = channel.getchildren().index(old_first)
        

        new_item = make_xml('test_insert', self.mp3, self.youtube)
        add_new_item(doc, new_item)

        now_first = doc.find('channel/item')
        self.assertEqual(now_first, new_item)
        
        
test_data = b"""
<rss xmlns:ns0="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:ns1="http://www.w3.org/2005/Atom" version="2.0">
    <channel>
        <title>The Modern Agile Show</title>
        <link>http://www.modernagile.org</link>
        <description>Over the past decade, innovative companies, software industry thought leaders and lean/agile pioneers have discovered simpler, sturdier, more streamlined ways to be agile. These modern approaches share a focus on producing exceptional outcomes and growing an outstanding culture. Today, it makes far more sense to bypass antiquated agility in favor of modern approaches. Modern agile methods are defined by four guiding principles: Make People Awesome; Make Safety a Prerequisite; Experiment and Learn Rapidly and Deliver Value Continuously. World famous organizations like Google, Amazon, AirBnB, Etsy and others are living proof of the power of these four principles. However, you don&#8217;t need to be a name brand company to leverage modern agile wisdom.</description>
        <ns0:summary>Over the past decade, innovative companies, software industry thought leaders and lean/agile pioneers have discovered simpler, sturdier, more streamlined ways to be agile. These modern approaches share a focus on producing exceptional outcomes and growing an outstanding culture. Today, it makes far more sense to bypass antiquated agility in favor of modern approaches. Modern agile methods are defined by four guiding principles: Make People Awesome; Make Safety a Prerequisite; Experiment and Learn Rapidly and Deliver Value Continuously. World famous organizations like Google, Amazon, AirBnB, Etsy and others are living proof of the power of these four principles. However, you don&#8217;t need to be a name brand company to leverage modern agile wisdom.</ns0:summary>
        <ns0:category text="Education" />
        <ns0:explicit>no</ns0:explicit>
        <ns0:subtitle>Agile for Every Endeavor</ns0:subtitle>
        <language>en-US</language>
        <ns0:author>Joshua Kerievsky</ns0:author>
        <ns0:owner>
            <ns0:name>Joshua Kerievsky</ns0:name>
            <ns0:email>joshua@industriallogic.com</ns0:email>
        </ns0:owner>
        <ns1:link href="http://modernagile.github.io/podcast" rel="self" type="application/rss+xml" />

        <image>
            <url>http://www.modernagile.org/podcast/cover_144.jpg</url>
            <title>The Modern Agile Show</title>
            <link>http://www.modernagile.org/podcast</link>
        </image>

        <ns0:image href="http://www.modernagile.org/podcast/cover_1400.jpg" />

        <item>
            <title>Show Intro Four Principles Tom DeMarco Story</title>
            <ns0:author>Joshua Kerievsky</ns0:author>
            <author>joshua@industriallogic.com (Joshua Kerievsky)</author>
            <ns0:image href="http://www.modernagile.org/podcast/cover_1400.jpg" />
            <enclosure length="23746385" type="audio/mp3" url="http://www.modernagile.org/podcast/ModernAgileShow%201%20%20Show%20Intro%20Four%20Principles%20Tom%20DeMarco%20Story.mp3" />
            <link>https://www.youtube.com/watch?v=NGz69OVmmOA</link>
            <guid isPermaLink="false">197c40dd40e1db0a19c23428a7c1801f86d4e8bb</guid>
            <pubDate>Mon, 19 Dec 2016 19:55:14 -0200</pubDate>
            <ns0:duration>00:12:22</ns0:duration>
            <description>Episode #1 Why Modern Agile? A brief guide to Modern Agile's four principles. Who is Joshua Kerievsky? A "Make People Awesome" story from Tom DeMarco's classic book, Slack.</description>
        </item>
    </channel>
</rss>"""
