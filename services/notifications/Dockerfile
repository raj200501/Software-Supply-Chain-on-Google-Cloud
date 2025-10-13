# syntax=docker/dockerfile:1
FROM rust:1.72 AS builder
WORKDIR /usr/src/app
COPY Cargo.toml ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src
COPY src ./src
RUN cargo build --release

FROM gcr.io/distroless/cc
COPY --from=builder /usr/src/app/target/release/notifications /notifications
EXPOSE 8084
ENTRYPOINT ["/notifications"]
