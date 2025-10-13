package main

import (
    "log"
    "net/http"

    usersserver "github.com/example/slsa-bazel-gke-reference/services/users/internal/server"
)

func main() {
    srv := usersserver.New()
    log.Println("users service listening on :5001")
    log.Fatal(http.ListenAndServe(":5001", srv))
}
