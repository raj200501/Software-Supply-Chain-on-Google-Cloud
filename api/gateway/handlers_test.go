package main

import (
    "bytes"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestCreateUserRoute(t *testing.T) {
    mux := http.NewServeMux()
    RegisterHandlers(mux)
    req := httptest.NewRequest(http.MethodPost, "/api/users", bytes.NewBufferString(`{"email":"test@example.com"}`))
    rr := httptest.NewRecorder()
    mux.ServeHTTP(rr, req)
    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200, got %d", rr.Code)
    }
}
