package server

import (
    "bytes"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHealthz(t *testing.T) {
    handler := New()
    req := httptest.NewRequest(http.MethodGet, "/healthz", nil)
    rr := httptest.NewRecorder()
    handler.ServeHTTP(rr, req)
    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200, got %d", rr.Code)
    }
}

func TestCreateUser(t *testing.T) {
    handler := New()
    req := httptest.NewRequest(http.MethodPost, "/users", bytes.NewBufferString(`{"email":"test@example.com","name":"Tester"}`))
    rr := httptest.NewRecorder()
    handler.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200, got %d", rr.Code)
    }
}
