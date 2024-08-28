DOCKER := $(shell which docker)
IMAGE := ${USER}-cirpa-utils-test
RUN := $(DOCKER) run -it --rm

all: build test

build:
	$(DOCKER) build -t ${IMAGE} .

test: build
	$(RUN) $(IMAGE)

pep8: build
	$(RUN) $(IMAGE) -e flake8

clean:
	$(DOCKER) rmi -f $(IMAGE)

.PHONY: all build test
