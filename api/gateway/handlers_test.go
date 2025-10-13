package main

import (
    "bytes"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHealthz(t *testing.T) {
    mux := http.NewServeMux()
    RegisterHandlers(mux)

    req := httptest.NewRequest(http.MethodGet, "/healthz", nil)
    rr := httptest.NewRecorder()
    mux.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200, got %d", rr.Code)
    }
}

func TestCreateUserRoute(t *testing.T) {
    mux := http.NewServeMux()
    RegisterHandlers(mux)
    req := httptest.NewRequest(http.MethodPost, "/api/users", bytes.NewBufferString(`{"email":"test@example.com","name":"Tester"}`))
    rr := httptest.NewRecorder()
    mux.ServeHTTP(rr, req)
    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200, got %d", rr.Code)
    }
}

func TestCreateOrderRoute(t *testing.T) {
    mux := http.NewServeMux()
    RegisterHandlers(mux)
    req := httptest.NewRequest(http.MethodPost, "/api/orders", bytes.NewBufferString(`{"userId":"user-1","itemId":"item-1","total":25.0}`))
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
