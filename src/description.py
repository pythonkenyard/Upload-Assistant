#Generate additional info for the description from mediainfo of each file.
#relies on the information in the mediainfo and the file naming.

#todo: add 

from pymediainfo import MediaInfo
from guessit import guessit

class mediainfo_parser():
    def __init__(self, meta):
    self.meta = meta  
    pass
    
    def get_media_info(folder_location,files_list):
        episode_descriptions = ""
        for file in files_list:
            mediainfo = MediaInfo.parse(f"{folloc}/{file}", output="", full=False)
            mediainfoobject = MediaInfo.parse(f"{folloc}/{file}")
            #print(mediainfo)
            try:
                fileattributes = guessit(file)

                filetitle = fileattributes['title']
                season = fileattributes['season']
                season = str(season).zfill(2)
                episode = fileattributes['episode']
                episode = str(episode).zfill(2)
                try:
                    episode_title = fileattributes['episode_title']
                except:
                    episode_title = " "
            except:
                print("cannot get file attributes")
            try:
                synopsis_search = re.search("SYNOPSIS\s+:\s(.+)",mediainfo)
                synopsis = synopsis_search.group(1)
            except:
                print("no synopsis")
            try:
                bitrate_search = re.findall("Bit rate\s+:\s(.+)",mediainfo)
                print(str(bitrate_search))
                bitrate = bitrate_search[0]
            except:
                bitrate = "unknown"
            if "Text" in mediainfo:
                contains_subtitles = "yes"
                #todo: Add language parser here. add link to flags of subtitle languages
            else:
                contains_subtitles = "no"
            if "Menu" in mediainfo:
                contains_chapters = "yes"
                #todo: total these and summarise?

            else: contains_chapters = "no"
            if "Credits" in mediainfo:
                contains_chapters = contains_chapters + " + Credits timing"
            try:
                audio_format = get_audio_id(mediainfoobject)
            except:
                audio_format = "unknown"
            try:
                audio_bitrate = bitrate_search[1]
            except: audio_bitrate = "unknown"
            try: 
                video_container = get_video_id(mediainfoobject)
            except: video_container = "unknown"


            episode_descriptions = f"{episode_descriptions}\n\n[b][color=teal][size=4]Episode {episode} {episode_title}[/size][/color][/b]\n
            Video Setting..{video_container}\n
            Video Bitrate..{bitrate}\n
            Audio Format...{audio_format}\n
            Audio Bitrate..{audio_bitrate}\n
            Subtitles......{contains_subtitles}\n
            Chapters.......{contains_chapters}\n
            Synopsis: [i]{synopsis}[/i]"
       
        return episode_descriptions
