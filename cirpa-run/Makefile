DOCKER := $(shell which docker)
IMAGE := ${USER}-cirpa-test
EXAMPLEIMAGE := ${USER}-cirpa-example
RUN := $(DOCKER) run -it --rm

all: build test

build:
	$(DOCKER) build -t ${IMAGE} .

test: build
	$(RUN) $(IMAGE)

pep8: build
	$(RUN) $(IMAGE) -e flake8

buildexample:
	$(DOCKER) build -t $(EXAMPLEIMAGE)  -f Dockerfile.example .

example: buildexample
	$(RUN) $(EXAMPLEIMAGE)


clean:
	$(DOCKER) rmi -f $(IMAGE)
	$(DOCKER) rmi -f $(EXAMPLEIMAGE)

.PHONY: all build test
