import glob
import subprocess

files = glob.glob('*.aiff')
for file in files:
    outfile = file.replace('.aiff', '.mp3')
    subprocess.call(['ffmpeg', '-i', file, outfile])
