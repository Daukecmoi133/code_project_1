from PIL import Image
import os

path_v = os.path.join(os.path.dirname(__file__), 'images')

def count_frames(filename):
    with Image.open(filename) as img:
        frames = 0
        try:
            while True:
                img.seek(img.tell() + 1)
                frames += 1
        except EOFError:
            return frames

print(count_frames(os.path.join(path_v, 'voice_gi.gif')))
