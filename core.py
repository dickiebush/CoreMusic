from twilio.rest import TwilioRestClient as TRC
from lxml import html
import requests
import pandas as pd
from models import song
#from routes import conn


#####################
#  helper functions #
#####################
def try_to_text(row):

    client = twilio_client()
    twilio_number = "+18133363411"
    ## what will change here is we will iterate over every customer and change my_artists
    ## to be their list of artists they like, and then send it to their phone number
    ## not a big change at all
    ## LEFTOFF
    my_artists = ["Young Thug", "A$AP Rocky", "Migos", "2 Chainz", "Quavo", "Lil Uzi Vert", "Gucci Mane", "Migos", "Wiz Khalifa", "Drake", "Future", "21 Savage", "Lil Yachty", "Post Malone", "J. Cole"]

    # open up hnhh link 
    hnhh_html = requests.get(row.links)

    # parse the soundcloud player url 
    try:
        soundcloud_url = html.fromstring(hnhh_html.content).get_element_by_id("soundcloud_player")
        soundcloud_html = str(requests.get(soundcloud_url.attrib['src']).content)

        # find substring of tracks id 
        start = soundcloud_html.find(".com/tracks/") + len(".com/tracks/")
        end   = soundcloud_html.find("\"", start)
        id    = soundcloud_html[start:end]

        url = ("soundcloud://tracks/{}".format(id))
    except:
        print("no soundcloud avaiable")
        url = row.links
    # if any of my artists are the artist of this current row, send me a text with the song name and link
    if (any([artist in row.artists for artist in my_artists])):
        body = "{} dropped a new song called {}, heres the link {}".format(row.artists, row.song_names, url)
        # send text message currently to me only 
        client.messages.create(to = "+18139095372", from_ = twilio_number, body = body)
        print("sent a text")
   

def twilio_client():
    account_sid   = "AC79432a906b5df034fa4604d80dee6079"
    auth_token    = "077422f1a2129d43670ca8b802cef484"
    return TRC(account_sid, auth_token)

######################
#    begin script    #
######################

def run_script(db=None):
    
    base_url = "http://hotnewhiphop.com"
    
    # css/html tags for html parsing
    artist_tag = "gridItem-trackInfo-artist"
    song_tag   = "gridItem-trackInfo-title"
    url_tag    = "gridItem-cover-anchor"

    # read in old master list csv file
    url_html = requests.get(base_url + "/songs")

    # call from_string function to create into parsable tree 
    # then find all elements with the correct tags
    artists_tree = html.fromstring(url_html.content).find_class(artist_tag)
    song_tree    = html.fromstring(url_html.content).find_class(song_tag)
    url_tree     = html.fromstring(url_html.content).find_class(url_tag)

    # extract text_content() for all elements of trees
    artists = [artist.text_content() for artist in artists_tree]
    songs   = [song.text_content()   for song   in song_tree]
    urls    = [url.attrib["href"]    for url    in url_tree]

    # remove all nbsp; for all artists, normalize all "Feat." into '&'
    artists = [artist.replace(u"\xa0", u" ") for artist in artists]
    artists = [artist.replace("Feat.", " & ") for artist in artists]

    # remove all nbsp; for songs
    songs = [song.replace(u"\xa0", u" ") for song in songs]

    # add base url to all song link URLs
    urls = [''.join([base_url,url]) for url in urls]
   
    # read in all songs we have already texted about
    #old_master_list = pd.read_sql("select * from songs", con=db.engine)

    old_master_list = pd.read_csv("master_list.csv", encoding='latin1')
    # create data frame of all songs on website, as these are latest songs we've analyzed 
    new_master_list = pd.DataFrame({'artists': artists, 'song_names': songs, "links":urls})

    # remove all songs we have already seen previously 
    ## this needs to remove the corresponding artist and song and URL 
    artists    = [artist for url,artist in zip(urls,artists) if url not in old_master_list.links.values]
    songs      = [song   for song in songs if song not in old_master_list.song_names.values]
    urls       = [url for url in urls if url not in old_master_list.links.values]
    

    # new songs with only new songs we havent seen
    new_songs = pd.DataFrame({'artists': artists, 'song_names': songs, "links":urls})

    # send texts for all those songs
    if len(new_songs > 0):
        new_songs.apply(lambda x: try_to_text(x), axis = 1)
    else:
        print("We have already updated all songs")

    #new_song = song("hey", "hii", "yooo")
    #db.session.add(new_song)
    #db.session.commit()
    # write to CSV for later iteration 
    new_master_list.to_csv("master_list.csv")
    #new_master_list.to_sql(name="songs",con= db.engine, if_exists='replace')


run_script()