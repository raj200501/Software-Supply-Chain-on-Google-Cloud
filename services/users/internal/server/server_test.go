package server

import (
    "bytes"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestCreateUser(t *testing.T) {
    handler := New()
    req := httptest.NewRequest(http.MethodPost, "/users", bytes.NewBufferString(`{"email":"test@example.com"}`))
    rr := httptest.NewRecorder()
    handler.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200, got %d", rr.Code)
    }
}
