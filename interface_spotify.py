from Spotify.spotify import Spotify

path = "/home/henry/Documents/Stuff/Data From Services/Spotify"

spotify = Spotify(path, output="show", start_date=12)
#spotify.preprocess()
spotify.read()
#spotify.top_count("Track")
#spotify.top_count("Artist")
#spotify.top_count("Album")
#spotify.top_count("Platform")
#spotify.top_time("Track")
#spotify.histogram("Track")

