echo start;
while read line; do
	youtube-dl "$line" --default-search gsearch -x --audio-format mp3 --min-views 500000 --geo-bypass -i --embed-thumbnail
done <$1
