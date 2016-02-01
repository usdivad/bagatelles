dir_original=`pwd`
dir_wavs="/Users/usdivad/Documents/music/bagatelles/seize/samples_export/guitar_intro"
filename_to_replace="guitar_intro "
cd $dir_wavs
for f in *.wav
do
    echo "doing $f"
    ffmpeg -i "$f" "$f.mp3"
done

rename "s/$filename_to_replace//" *.mp3
rename "s/.wav//" *.mp3

cd $dir_original