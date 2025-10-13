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

load("@rules_go//go:deps.bzl", "go_rules_dependencies", "go_register_toolchains")

go_rules_dependencies()

go_register_toolchains(version = "1.21.5")

load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

gazelle_dependencies()

load("@bazel_gazelle//:def.bzl", "gazelle")

gazelle(name = "gazelle")
