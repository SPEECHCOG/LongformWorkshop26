mkdir -p wav

for f in *.wav; do
    ffmpeg -i "$f"*-ac 1 -ar 16000 "$wav/{f%.wav}.wav*
done