curl http://api.kivaws.org/v1/lenders/$1/loans.json?ids_only=true | python -mjson.tool > $1.json
