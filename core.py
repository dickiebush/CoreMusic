from twilio.rest import TwilioRestClient as TRC
from lxml import html
import requests
import pandas as pd
from models import Song, db, User
from routes import app
import re
#from routes import conn


#####################
#  helper functions #
#####################

def try_to_text(row):

    client = twilio_client()
    twilio_number = "+18133363411"

    # open up hnhh link 
    hnhh_html = requests.get(row.url)

    # parse for the soundcloud player url 
    try:
        # find soundcloud player and extra the link it send you to
        soundcloud_html = html.fromstring(hnhh_html.content).get_element_by_id("soundcloud_player")
        soundcloud_url = str(requests.get(soundcloud_html.attrib['src']).content)

        # find substring of tracks id 
        start = soundcloud_html.find(".com/tracks/") + len(".com/tracks/")
        end   = soundcloud_html.find("\"", start)
        id    = soundcloud_html[start:end]

        # create url for opening in soundcloud app
        url = ("soundcloud://tracks/{}".format(id))
    except:

        # didn't find soundcloud player, try for youtue player 
        try:

        # find the youtube link class, then find its link attribute
        youtube_player_html = html.fromstring(hnhh_html.content).find_class("mixtape-userInteraction-playerLink youtube-only")[0]
        youtube_link_desktop = youtube_player_html.attrib['href']

        # create into mobile schema by substringing the youtube id
        start = youtube_link_desktop.find("/watch?v=")
        youtube_link_mobile = "youtube://" + youtube_link_desktop[start+len("/watch?v="):]

        url = youtube_link_mobile

        # didn't find either, send to hnhh website 
        except:
        url = row.url
        
    with app.app_context():

        for user in User.query.all():

            if user.artists.lower() == 'rap':
                user_artists = ["Lil Yachty", "Travi$ Scott", "A$AP Rocky", "Kendrick Lamar", "Young Thug", "2 Chainz", "J. Cole", "Wiz Khalifa" \
                "Berner", "Future", "Kanye West", "Gucci Mane", "Drake", "Juicy J", "Post Malone", "Kodak Black",
                "A Boogie wit da Hoodie","21 Savage", "Mac Miller", "Kyle", "Big Sean", "Quavo", "Migos"]
            else:
                user_artists = re.split(',\s*', user.artists)
            
            # if any of my artists are the artist of this current row, send me a text with the song name and link
            if (any([artist in row.artist for artist in user_artists])):
                body = "{} dropped a new song called {}, heres the link {}".format(row.artist, row.song_name, url)
                # send text message currently to me only 
                client.messages.create(to = "+1{}".format(user.number), from_ = twilio_number, body = body)
                print("Found your song, sent a text to {}".format(user))
            else:
                print("New song was not good")
   

def twilio_client():
    account_sid   = "AC79432a906b5df034fa4604d80dee6079"
    auth_token    = "077422f1a2129d43670ca8b802cef484"
    return TRC(account_sid, auth_token)

######################
#    begin script    #
######################

def run_script(db):
    

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
   

    with app.app_context():
        # read in all songs we have already texted about
        old_master_list = pd.read_sql("select * from songs", con=db.engine)

    #old_master_list = pd.read_csv("master_list.csv", encoding='latin1')
    # create data frame of all songs on website, as these are latest songs we've analyzed 
    new_master_list = pd.DataFrame({'url':urls, 'song_name': songs,  'artist': artists})

   #print(new_master_list)
    #print(old_master_list)
    # remove all songs we have already seen previously 
    ## this needs to remove the corresponding artist and song and URL 
    artists    = [artist for url,artist in zip(urls,artists) if url not in old_master_list.url.values]
    songs      = [song   for song in songs if song not in old_master_list.song_name.values]
    urls       = [url for url in urls if url not in old_master_list.url.values]
    

    # new songs with only new songs we havent seen
    new_songs = pd.DataFrame({'url': urls, 'song_name': songs, 'artist':artists})

    # send texts for all those songs
    if len(new_songs > 0):
        new_songs.apply(lambda x: try_to_text(x), axis = 1)
    else:
        print("We have already updated all songs")

    #new_song = song("hey", "hii", "yooo")
    #db.session.add(new_song)
    #db.session.commit()
    # write to CSV for later iteration 
    #new_master_list.to_csv("master_list.csv")
    with app.app_context():
        new_master_list.to_sql(name="songs",con= db.engine, if_exists='replace')

run_script(db)
