.PHONY: docker

build:
	docker build --platform linux/amd64 -t compass-stock-handler:test .

deploy:
	sh ./scripts/deploy.sh
