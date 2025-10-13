package main

import (
    "log"
    "net/http"
)

func main() {
    mux := http.NewServeMux()
    RegisterHandlers(mux)
    log.Println("gateway listening on :8080")
    if err := http.ListenAndServe(":8080", mux); err != nil {
        log.Fatalf("server exited: %v", err)
    }
}
