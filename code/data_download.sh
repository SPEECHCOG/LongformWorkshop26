mkdir -p data/recordings
mkdir -p data/recordings/wav
cd data/recordings
curl -L -O "https://gin.g-node.org/LAAC-LSCP/vandam-data/raw/master/recordings/converted/standard/BN32_010007.wav"
ffmpeg -hide_banner -loglevel error -ss 0 -i BN32_010007.wav -t 600 -c copy wav/BN32_010007_part_1.wav
ffmpeg -hide_banner -loglevel error -ss 600 -i BN32_010007.wav -t 600 -c copy wav/BN32_010007_part_2.wav
#rm BN32_010007.wav
echo "Successfully downloaded example data."
cd ..