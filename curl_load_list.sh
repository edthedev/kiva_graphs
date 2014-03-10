for page in "1" "2" "3" "4"; do
	# curl http://api.kivaws.org/v1/lenders/$1/loans.json?ids_only=true&page=$page&sort_by=newest | python -mjson.tool > $1.$page.json
	curl -G -d ids_only=true -d sort_by=newest -d page=$page http://api.kivaws.org/v1/lenders/$1/loans.json > data/$1.$page.json 
done
