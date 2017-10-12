# init
mkdir data
mkdir result

# get all history urls
curl "https://coinmarketcap.com/historical/" | pup "div.col-xs-6 li a attr{href}" | awk '$0="https://coinmarketcap.com"$0' > urls.txt

# download all history urls
# wget -i data/urls.txt
while read -r url; do
    wget -O "data/$(echo "$url" | cut -d/ -f 5).html" $url
done < data/urls.txt

# convert all to csv
for i in $(ls data/*.html); do python2 html2csv.py $i ; done

# download most recent data and name with ".last." and then convert to csv as well
cd data
wget https://coinmarketcap.com/all/views/all/
python ../html2csv.py index.html
mv index.html.0.csv $(date +%Y%m%d).html.last.csv


# process and save sorted result
python read.py | mlr --csv sort -n 'lastRank' | xsv select '!lastDate' > result/sorted.csv
