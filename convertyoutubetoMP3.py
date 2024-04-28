import os
from pytube import Playlist
from moviepy.editor import VideoFileClip
import socket

def capitalize_each_word(s):
    return ' '.join(word.capitalize() for word in s.split())

def download_playlist(playlist_url, save_directory):
    # Extract playlist ID from the URL
    playlist_id = playlist_url.split("list=")[-1]
    playlist = Playlist(f"https://www.youtube.com/playlist?list={playlist_id}")
    
    # Create directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Download each video in the playlist
    for video in playlist.videos:
        try:
            # Fetch video metadata
            artist = capitalize_each_word(video.author)
            title = capitalize_each_word(video.title)

            # Download video
            video.streams.filter(only_audio=True).first().download(output_path=save_directory, filename=f"{artist} - {title}.mp3")
        except (socket.gaierror, Exception) as e:
            print(f"Error downloading {video.title}: {e}")
            continue

def convert_videos_to_mp3(input_directory, output_directory):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Convert each video in the input directory to MP3
    for filename in os.listdir(input_directory):
        if filename.endswith('.mp4'):
            mp4_file = os.path.join(input_directory, filename)
            mp3_file = os.path.splitext(filename)[0] + ".mp3"
            mp3_file = os.path.join(output_directory, mp3_file)
            try:
                video = VideoFileClip(mp4_file)
                video.audio.write_audiofile(mp3_file)
                video.close()
                os.remove(mp4_file)
            except Exception as e:
                print(f"Error converting {filename}: {e}")
                continue

if __name__ == "__main__":
    playlist_url = input("Enter the URL of the YouTube playlist: ")
    output_directory = input("Enter the directory where you want to save the converted MP3 files: ")
    download_playlist(playlist_url, output_directory)
    
    input_directory = output_directory
    convert_videos_to_mp3(input_directory, output_directory)
