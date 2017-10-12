## init
```bash
mkdir data
mkdir result
```

## get all history urls
```bash
curl "https://coinmarketcap.com/historical/" | pup "div.col-xs-6 li a attr{href}" | awk '$0="https://coinmarketcap.com"$0' > urls.txt
```

## download all history urls
```bash
# wget -i data/urls.txt
while read -r url; do
    wget -O "data/$(echo "$url" | cut -d/ -f 5).html" $url
done < data/urls.txt
```

## convert all to csv
```bash
for i in $(ls data/*.html); do python2 html2csv.py $i ; done
```

## download most recent data and name with ".last." and then convert to csv as well
```bash
cd data
wget https://coinmarketcap.com/all/views/all/
python ../html2csv.py index.html
mv index.html.0.csv $(date +%Y%m%d).html.last.csv
```

## process and save sorted result
```bash
python read.py | mlr --csv sort -n 'lastRank' | xsv select '!lastDate' > result/sorted.csv
```
