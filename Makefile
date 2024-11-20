.PHONY: docker pyenv

build:
	docker build --platform linux/amd64 -t compass-stock-handler:test .

deploy:
	sh ./scripts/deploy.sh

pyenv:
	sh ./scripts/pyenv.sh

util:
	ENV=local python utils.py
