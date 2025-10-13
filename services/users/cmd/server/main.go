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
}
