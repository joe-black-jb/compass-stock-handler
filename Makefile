.PHONY: docker venv

build:
	docker build --platform linux/amd64 -t compass-stock-handler:test .

deploy:
	sh ./scripts/deploy.sh

venv:
	sh ./scripts/venv.sh

util:
	ENV=local python utils.py
