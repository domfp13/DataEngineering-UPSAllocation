# -*- coding: utf-8 -*-
# Created by Luis Enrique Fuentes Plata

SHELL = /bin/bash

include .env

.DEFAULT_GOAL := help

IMAGE_NAME := cc-python-registry:latest
AWS_ACCESS_KEY_ID=$(shell cat ~/.aws/credentials | grep aws_access_key_id | cut -d '=' -f 2)
AWS_SECRET_ACCESS_KEY=$(shell cat ~/.aws/credentials | grep aws_secret_access_key | cut -d '=' -f 2)

.PHONY: setup
setup: ## 1.-Create Docker Image based on Dockerfile
	@ echo "********** Building image **********"
	@ docker image build --rm -t ${IMAGE_NAME} .
	@ echo "********** Cleanup **********"
	@ docker image prune -f

.PHONY: start
start: ## 2.- For local testing
	@ echo "Creating and Starting services"
	@ $(MAKE) setup
	@ docker container run --rm -d --name runner cc-python-registry:latest

.PHONY: clean
clean: ## 2.- For local testing
	@ echo "Cleaning Task"
	@ docker container stop runner

.PHONY: run-local
run-local: ## 2.-Run Code locally
	@ echo "Creating and Starting services"
	@ $(MAKE) setup
	@ docker container run --rm \
	  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
 	  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
 	  -e BUCKET_NAME=${BUCKET_NAME} \
	  --name Dr460nized ${IMAGE_NAME}

.PHONY: run
run: ## 3.-Run Code server
	@ echo "Creating and Starting services"
	@ $(MAKE) setup
	@ docker container run --rm \
 	  -e BUCKET_NAME=${BUCKET_NAME} \
	  --name Dr460nized ${IMAGE_NAME}

help: ## 4.-Show all the target formulas
	@ echo "Please use \`make <target>' where <target> is one of"
	@ perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'
