# Testing Strategy and End-to-End Scenarios

This repository includes comprehensive automated testing ranging from unit coverage in each service to cross-service end-to-end (E2E) scenarios.

## Unit tests

- `bazel test //services/users/...` executes Go unit tests for the users service.
- `bazel test //services/orders:unit_tests` runs pytest-based tests via rules_python.
- `bazel test //services/inventory:test` invokes JUnit tests wrapped by rules_jvm.
- `bazel test //services/payments:test` executes Node.js Jest tests.
- `bazel test //services/notifications:test` executes Rust unit tests via rules_rust.

All tests are wired into GitHub Actions (`ci/github/workflows/ci.yaml`) and Cloud Build pipelines.

## Integration tests

Integration tests live under `tests/integration`. They use docker-compose to bring up dependent services and validate inter-service communication, database migrations, and message flows.

Run them locally with:

```bash
make test-integration
```

The Make target orchestrates Bazel to build test containers, then executes the test suite using `pytest` against the running stack.

## End-to-end tests

The top-level E2E scenario is implemented in `tests/e2e/test_happy_path.py` and performs the following steps:

1. Creates a user via the gateway REST API.
2. Creates an order referencing seeded inventory.
3. Triggers a payment, which in turn calls the notifications service.
4. Verifies that inventory levels decrease and the notification endpoint recorded the event.

Use `make test-e2e` to execute the scenario. When running against Kubernetes, set the `GATEWAY_URL` environment variable to the cluster ingress endpoint.

## Adding new tests

1. Create the test under the relevant language-specific directory.
2. Register the test target inside the service's `BUILD.bazel` file.
3. Update GitHub Actions and Cloud Build to include the new target if it is not covered by `bazel test //...`.
4. Document new test flows in this file.

## Test data

Seed data is managed via `db/migrations` and `scripts/dev-seed.sh`. The migrations run automatically when services start. The seed script populates additional sample users, orders, and inventory useful for manual testing.
