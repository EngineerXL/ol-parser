install:
	bash install.sh

clean:
	docker volume rm ol-parser_db-volume-pg-ol

clean-data:
	rm -rf ./data/*
