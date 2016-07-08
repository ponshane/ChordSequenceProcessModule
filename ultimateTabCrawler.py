import requests
import re
import time
import mongoConnect
from io import StringIO, BytesIO
from lxml import etree
from lxml import html
from datetime import datetime

#db instance comes from mongoConnect
collection = mongoConnect.db.Chord_Tabs_Config_Test

def UltimateCrawler(Song, Artist):

    res = requests.get("https://www.ultimate-guitar.com/search.php?search_type=title&order=&value="+Song+"+"+Artist)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(res.text), parser)

    each_href = tree.xpath('//table[@class="tresults"]//tr//td//a[@class="song result-link" or @class="js-tp_link"]/@href')
    each_type = tree.xpath('//table[@class="tresults"]//tr//strong//text()')

    each_ratdig = []
    tr = tree.find('//table[@class="tresults"]')

    for td in tr.findall('tr/td[@class="gray4"]'):
        elem2 = td.find('span/b[@class="ratdig"]')
        if elem2 is not None:
            each_ratdig.append(elem2.text)
        else:
            each_ratdig.append("0")

    each_ratdig = map(int, each_ratdig)

    top_ranking_tabs = dict()
    max_ratdig = 0

    assert len(each_href) == len(each_ratdig)
    assert len(each_href) == len(each_type)

    for href, ratdig, one_type in zip(each_href, each_ratdig, each_type):
        if (ratdig >= max_ratdig) & (one_type == "chords"):
            max_ratdig = ratdig
            top_ranking_tabs["href"] = href
            top_ranking_tabs["ratdig"] = ratdig
            top_ranking_tabs["type"] = one_type

    # print each_href, each_ratdig, each_type
    print top_ranking_tabs

    try:
        res_tab = requests.get(top_ranking_tabs["href"])
    except requests.exceptions.ConnectionError:
        print "We got connectionError"
        time.sleep(10)
        res_tab = requests.get(top_ranking_tabs["href"])

    tab_tree = html.fromstring(res_tab.content)
    chord_list = tab_tree.xpath(".//pre[@class='js-tab-content']")
    chord_list = etree.tostring(chord_list[0], encoding='unicode').split('\n\n\n')

    ExtractedPattern = list()
    p = re.compile(ur'<span>(.*?)<\/span>')
    # print chord_list

    for segmentation in chord_list:
        match = re.findall(p, segmentation)
        if match:
            print match
            ExtractedPattern.append(match)
    print ExtractedPattern

    Insert_Data = top_ranking_tabs
    Insert_Data["song"] = Song
    Insert_Data["artist"] = Artist
    Insert_Data["chord_list"] = ExtractedPattern

    Insert_boolean = collection.insert_one(Insert_Data).inserted_id

    if Insert_boolean:
        print Insert_Data["song"], Insert_Data["artist"]
    else:
        print "Error"


def UltimateCrawler_Multiple_version(Song, Artist):
    song_str = Song.replace('_', ' ')
    artist_str = Artist.replace('_', ' ')

    res = requests.get("https://www.ultimate-guitar.com/search.php?search_type=title&order=&value="+song_str+"+"+artist_str)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(res.text), parser)

    each_href = tree.xpath('//table[@class="tresults"]//tr//td//a[@class="song result-link js-search-version--link" or @class="js-tp_link"]/@href')
    each_type = tree.xpath('//table[@class="tresults"]//tr//strong//text()')

    each_ratdig = []
    each_rating = []

    tr = tree.find('//table[@class="tresults"]')

    for td in tr.findall('tr/td[@class="gray4"]'):
        elem2 = td.find('span/b[@class="ratdig"]')
        if elem2 is not None:
            each_ratdig.append(elem2.text)
        else:
            each_ratdig.append("0")

        rating = td.find('span[@class="rating"]')

        if rating is not None:
            full_rating = int(rating.xpath('count(span[@class="icon-rating-sm icon-rating-sm__active"])'))
            half_rating = int(rating.xpath('count(span[@class="icon-rating-sm icon-rating-sm__half"])'))
            each_rating.append(full_rating+(half_rating*0.5))
            # rating = etree.tostring(rating[0], encoding='unicode')
            # print full_rating, half_rating
        else:
            each_rating.append(0)
            #print "There is no rating."

    each_ratdig = map(int, each_ratdig)

    total_ranking_tabs = list()
    for href, ratdig, rating, one_type in zip(each_href, each_ratdig, each_rating, each_type):
        if one_type == "chords":
            ranking_tabs = dict()
            ranking_tabs["href"] = href
            ranking_tabs["ratdig"] = ratdig
            ranking_tabs["rating"] = rating
            ranking_tabs["type"] = one_type
            total_ranking_tabs.append(ranking_tabs)

    print each_href, each_ratdig, each_rating, each_type
    scrapeTab(total_ranking_tabs, Song, Artist)


def scrapeTab(tabs_list, song, artist):
    print tabs_list
    for tab in tabs_list:
        try:
            res_tab = requests.get(tab["href"])
        except requests.exceptions.ConnectionError:
            print "We got connectionError"
            time.sleep(10)
            res_tab = requests.get(tab["href"])

        tab_tree = html.fromstring(res_tab.content)
        chord_list = tab_tree.xpath(".//pre[@class='js-tab-content']")
        chord_list = etree.tostring(chord_list[0], encoding='unicode').split('\n\n\n')

        ExtractedPattern = list()
        p = re.compile(ur'<span>(.*?)<\/span>')
        # print chord_list

        for segmentation in chord_list:
            match = re.findall(p, segmentation)
            if match:
                print match
                ExtractedPattern.append(match)
                print ExtractedPattern

        Insert_Data = tab
        Insert_Data["song"] = song
        Insert_Data["artist"] = artist
        Insert_Data["chord_list"] = ExtractedPattern
        Insert_Data["download_time"] = datetime.now()
        #print Insert_Data

        Insert_boolean = collection.insert_one(Insert_Data).inserted_id

        if Insert_boolean:
            print Insert_Data["song"], Insert_Data["artist"]
        else:
            print "Error"

def main():
    """this is test."""
    UltimateCrawler_Multiple_version("greatest_love_of_all", "whitney_houston")

if __name__ == "__main__":
    main()
