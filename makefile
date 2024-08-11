install:
	bash install.sh

build:
	docker compose build parser

clean:
	docker compose down -v

clean-data:
	rm -rf ./data/*
