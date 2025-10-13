package main

import (
	"log"
	"net/http"
	"os"

	usersserver "github.com/example/slsa-bazel-gke-reference/services/users/internal/server"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8081"
	}
	addr := ":" + port
	srv := usersserver.New()
	log.Printf("users service listening on %s", addr)
	log.Fatal(http.ListenAndServe(addr, srv))
    "log"
    "net/http"

    usersserver "github.com/example/slsa-bazel-gke-reference/services/users/internal/server"
)

func main() {
    srv := usersserver.New()
    log.Println("users service listening on :5001")
    log.Fatal(http.ListenAndServe(":5001", srv))
}
