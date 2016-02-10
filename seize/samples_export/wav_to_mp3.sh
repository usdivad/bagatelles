dir_original=`pwd`
dir_wavs=$1 # e.g. "guitar_intro"
dir_wavs_full="/Users/usdivad/Documents/music/bagatelles/seize/samples_export/$dir_wavs"
# filename_to_replace="guitar_intro "
filename_to_replace=$2

cd $dir_wavs_full
for f in *.wav
do
    echo "doing $f"
    ffmpeg -i "$f" "$f.mp3"
done

rename -f "s/$filename_to_replace//" *.mp3
rename -f "s/.wav//" *.mp3

cd $dir_original

echo "done!"