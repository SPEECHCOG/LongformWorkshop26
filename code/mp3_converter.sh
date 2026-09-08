mkdir -p wav

for f in *.mp3; do
    ffmpeg -i "$f" -ac 1 -ar 16000 -c:a pcm_s16le "wav/${f%.mp3}.wav"
done

echo "Successfully converted data from mp3 to wav."