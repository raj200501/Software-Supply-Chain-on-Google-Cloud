SHELL := /bin/bash

.DEFAULT_GOAL := help

help: ## Print common commands
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: deps
deps: ## Install language-specific dependencies
	@echo "Install dependencies manually as needed (Go, Node, Python, Rust)."
	@echo "Run asdf install if you use the provided .tool-versions file."

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

.PHONY: lint
lint: ## Run multi-language linters
	golangci-lint run ./...
	flake8 services/orders
	npm --prefix apps/web run lint
	cargo fmt --manifest-path services/notifications/Cargo.toml -- --check
	mvn -f services/inventory/pom.xml -q spotless:check

.PHONY: fmt
fmt: ## Run formatters across all languages
	scripts/format.sh

.PHONY: test-integration
test-integration: ## Run integration tests
	pytest tests/integration

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	pytest tests/e2e

.PHONY: skaffold-dev
skaffold-dev: ## Run skaffold dev against kind
	skaffold dev --profile=dev

.PHONY: skaffold-run
skaffold-run: ## Deploy to prod profile
	skaffold run --profile=prod

.PHONY: terraform-apply
terraform-apply: ## Apply Terraform infrastructure
	cd infra/terraform && terraform init && terraform apply -auto-approve

.PHONY: terraform-destroy
terraform-destroy: ## Destroy Terraform infrastructure
	cd infra/terraform && terraform destroy -auto-approve

.PHONY: dev-seed
dev-seed: ## Seed demo data through the gateway
	scripts/dev-seed.sh
