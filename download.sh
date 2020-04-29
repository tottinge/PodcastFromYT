echo "Args are 0:$0, 1:$1, 2:$2"
limit=${1:-2}
youtube-dl --extract-audio \
    --audio-format mp3 \
    --write-info-json \
    --max-downloads ${limit}  \
    https://www.youtube.com/channel/UCMwCSEyUk59V8IQADpdn5PA
