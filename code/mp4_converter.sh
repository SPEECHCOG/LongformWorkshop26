mkdir -p wav

for f in *.mp4; do
    ffmpeg -i "$f" -vn -ac 1 -ar 16000 -c:a pcm_s16le "wav/${f%.mp4}.wav"
done

echo "Successfully converted data from mp4 to wav."