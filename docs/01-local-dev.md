# Local Development

1. Install Bazelisk, Docker, Node.js, Go, Python, and Rust.
2. Run `make generate` to build protobufs and install web dependencies.
3. Use `docker compose up --build` to start services, Postgres, and the gateway.
4. Access the UI at http://localhost:3000.
5. Execute `bazel test //...` to validate unit tests.
