#import py_m3u
#import py_m3u.directives
#from m3u_parser import M3uParser



#myparser1 = py_m3u.M3UParser()
#myParser1 = M3uParser()
pathToM3uFile = r"C:\Users\konta\Music\Playlists\Queue_Schlafen ASNR.m3u"

import sys
import io
import shutil
import os.path

class track():
    def __init__(self, length, artist, title, path):
        self.length = length
        self.artist = artist
        self.title = title
        self.path = path


"""  
    song info lines are formatted like:
    EXTINF:419,Alice In Chains - Rotten Apple
    length (seconds)
    Song title
    file name - relative or absolute path of file
    ../Minus The Bear - Planet of Ice/Minus The Bear_Planet of Ice_01_Burying Luck.mp3
"""

def parsem3u(infile):
    try:
        assert(isinstance(infile, io.TextIOWrapper))
    except AssertionError:
        infile = open(infile,'r')

    """
        All M3U files start with #EXTM3U.
        If the first line doesn't start with this, we're either
        not working with an M3U or the file we got is corrupted.
    """

    line = infile.readline()
    if not line.startswith('#EXTM3U'):
       return

    # initialize playlist variables before reading file
    playlist=[]
    song=track(None,None,None, None)

    for line in infile:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            # pull length and title from #EXTINF line
            length, artistTitle = line.split('#EXTINF:')[1].split(',',1)
            artist, title = artistTitle.split('-', 1)
            song=track(length, artist, title, None)
        elif (len(line) != 0):
            # pull song path from all other, non-blank lines
            song.path=line
            playlist.append(song)
            # reset the song variable so it doesn't use the same EXTINF more than once
            song=track(None,None,None, None)

    infile.close()

    return playlist

"""
Identifies duplicates (by filepath) and renames the song title, the file name 
and creates a copy of the original file with the new name.
"""
    
def renameDuplicates(playlist):
    
    songDictionary = {}
    overallduplicates = 0
    for item in playlist:

        if item.path not in songDictionary: 

            songDictionary[item.path] = 1

        else:
            overallduplicates += 1 
            numeralToAdd = str(songDictionary[item.path])
            songDictionary[item.path] += 1 #increment occurence counter

            #modify title and path string by adding the number of previous occurences as a literal to it 
            item.title += " " + numeralToAdd
            origRoot, origExt = os.path.splitext(item.path)
            origRoot += numeralToAdd
            newPath = os.path.normpath(origRoot + origExt)
            
            #copy file with new path
            #shutil.copy(item.path, newPath)
            print("Copy "+item.path+" to "+newPath+".")
            #update playlist with modify path and title
            item.path = newPath
            
    print("Found " + str(duplicatesCounter) + " duplicates.")
        

# for now, just pull the track info and print it onscreen
# get the M3U file path from the first command line argument
def main():
    pathToPlaylist=r"examples\Playlists\Queue_Schlafen ASNR.m3u" #sys.argv[1]
    m3uFile = open(pathToPlaylist, 'r', encoding='utf-8')
    playlist = parsem3u(m3uFile)
    renameDuplicates(playlist)
    for track in playlist:
        print (track.artist, track.title, track.length, track.path)
    exit(0)

if __name__ == '__main__':
    main()
    

#myfile1 = open(pathToM3uFile, 'r', encoding='utf-8')
#gen = myparser1.load(myfile1)
myParser1.parse_m3u(pathToM3uFile)
myParser1.reset_operations()
playlist = myParser1.get_list()
print("Lenght playlist: ",len(playlist))


item_count = 0

duplicatesCounter = {}
for item in gen:
    item_count += 1
    if isinstance(item, py_m3u.directives.EXTINF):
        print(item.artist)
        audioRef = next(gen)
        if isinstance(audioRef, py_m3u.AudioFileRef):
            print("Source: ", audioRef.source)
            if audioRef.source in duplicatesCounter:
                duplicatesCounter[audioRef.source] = duplicatesCounter[audioRef.source]+1
            else:
                duplicatesCounter[audioRef.source] = 0
            print("Source: ", audioRef.source, " found ", duplicatesCounter[audioRef.source], " times in list.")

print(f"Item count is {item_count}")
print(myfile1)

