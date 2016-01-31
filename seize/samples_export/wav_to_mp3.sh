dir="/Users/usdivad/Documents/music/bagatelles/seize/samples_export/guitar_intro"
cd $dir
for f in *.wav
do
    echo "doing $f"
    ffmpeg -i "$f" "$f.mp3"
done