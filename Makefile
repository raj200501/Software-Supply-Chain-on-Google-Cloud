SHELL := /bin/bash

.DEFAULT_GOAL := help

help: ## Print common commands
@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: deps
deps: ## Install language-specific dependencies
@echo "Install dependencies manually as needed (Go, Node, Python, Rust)."

.PHONY: generate
generate: ## Generate protobufs and install frontend deps
bazel build //api/proto:platform_proto
npm --prefix apps/web install

.PHONY: compose-up
compose-up: ## Launch docker-compose stack
docker compose up --build

.PHONY: compose-down
compose-down: ## Stop docker-compose stack
docker compose down -v

.PHONY: kind-up
kind-up: ## Create local kind cluster with registry
scripts/kind-up.sh

.PHONY: kind-down
kind-down: ## Delete kind cluster
scripts/kind-down.sh

.PHONY: test
test: ## Run bazel test
bazel test //...

.PHONY: fmt
fmt: ## Run formatters across all languages
scripts/format.sh

