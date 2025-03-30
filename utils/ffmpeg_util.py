import ffmpeg
import os

def convert_video(input_path):
    output_path = input_path.rsplit(".", 1)[0] + "_converted.mp4"
    
    ffmpeg.input(input_path).output(output_path, vcodec='libx264', preset='ultrafast').run()
    return output_path
