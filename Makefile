LOAN=foo

get_data:
	curl http://api.kivaws.org/v1/loans/$(LOAN).json | python -mjson.tool > data/$(LOAN).json

load_list:
	curl_load_list.sh

chart:
	open chart.html
