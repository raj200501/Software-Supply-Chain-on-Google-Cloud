workspace(name = "slsa_bazel_gke_reference")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_go",
    sha256 = "9f8f5bc9d32b13dbd9f769ade44507bf44a085f869651d81d77ec2a3f8b80b9a",
    urls = ["https://github.com/bazelbuild/rules_go/releases/download/v0.44.0/rules_go-v0.44.0.tar.gz"],
)

http_archive(
    name = "bazel_gazelle",
    sha256 = "c1a93af37b8d90d5b2014b1b64e26dcacb2f6afb59f13d05a99dbf211a58f3a4",
    urls = ["https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.32.0/bazel-gazelle-v0.32.0.tar.gz"],
)

http_archive(
    name = "rules_python",
    sha256 = "7f3cbcf2d5c4abfa1cf5da2f2e6239900cb3be4696939857a8df0eaef86ca27c",
    urls = ["https://github.com/bazelbuild/rules_python/releases/download/0.27.1/rules_python-0.27.1.tar.gz"],
)

http_archive(
    name = "rules_nodejs",
    sha256 = "3cf9d2b322b0a44132e9307095a8aa9015ae049631b7d831bdb9fee9601e606f",
    urls = ["https://github.com/bazelbuild/rules_nodejs/releases/download/6.1.0/rules_nodejs-6.1.0.tar.gz"],
)

http_archive(
    name = "rules_rust",
    sha256 = "a9a5d0f0c4e892e15eaa05f1135bf2c94b8e8b0e6d7bf600cb0bb0e4bcea90c0",
    urls = ["https://github.com/bazelbuild/rules_rust/releases/download/0.40.0/rules_rust-v0.40.0.tar.gz"],
)

http_archive(
    name = "rules_jvm_external",
    sha256 = "353a811d873d61bb64abd0c4da25d4a317053cf88df8b98cbfbacfea3888bc62",
    urls = ["https://github.com/bazelbuild/rules_jvm_external/releases/download/4.6/rules_jvm_external-4.6.zip"],
)

load("@rules_go//go:deps.bzl", "go_rules_dependencies", "go_register_toolchains")
load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")
load("@rules_python//python:pip.bzl", "pip_install")
load("@rules_nodejs//nodejs:repositories.bzl", "nodejs_register_toolchains")
load("@rules_rust//rust:repositories.bzl", "rust_repositories")
load("@rules_rust//crate_universe:repositories.bzl", "crate_universe_dependencies")
load("@rules_rust//crate_universe:setup.bzl", "crate_universe")
load("@rules_jvm_external//:defs.bzl", "maven_install")

# Go toolchains and deps
go_rules_dependencies()
go_register_toolchains(version = "1.21.5")

gazelle_dependencies()

gazelle(name = "gazelle")

# Python dependencies managed via pip_install.
pip_install(
    name = "orders_requirements",
    requirements = "services/orders/requirements.txt",
)

# Node toolchain and packages
nodejs_register_toolchains(version = "18.18.2")

# Rust toolchain
rust_repositories(version = "1.72.0")

crate_universe_dependencies()

crate_universe(
    name = "notifications_crates",
    edition = "2021",
    crates = {
        "actix-web": "4.4.1",
        "serde": "1.0.195",
        "serde_json": "1.0.113",
        "tokio": {"version": "1.35.1", "default_features": False, "features": ["macros", "rt-multi-thread"]},
        "chrono": {"version": "0.4.31", "features": ["clock", "std"]},
    },
)

load("@notifications_crates//:defs.bzl", "notifications_crates_fetch")

notifications_crates_fetch()

# Java dependencies via maven_install
maven_install(
    name = "inventory_maven", 
    artifacts = [
        "org.springframework.boot:spring-boot-starter-web:3.2.2",
        "org.springframework.boot:spring-boot-starter-actuator:3.2.2",
        "org.springframework.boot:spring-boot-starter-test:3.2.2",
        "io.micrometer:micrometer-registry-prometheus:1.12.2",
        "org.postgresql:postgresql:42.7.1",
        "org.flywaydb:flyway-core:10.7.1",
        "org.assertj:assertj-core:3.24.2",
    ],
    repositories = [
        "https://repo1.maven.org/maven2",
    ],
)
load("@rules_go//go:deps.bzl", "go_rules_dependencies", "go_register_toolchains")

go_rules_dependencies()

go_register_toolchains(version = "1.21.5")

load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

gazelle_dependencies()

load("@bazel_gazelle//:def.bzl", "gazelle")

gazelle(name = "gazelle")
