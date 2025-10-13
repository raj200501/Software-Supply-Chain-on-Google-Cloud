package server

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

type apiResponse struct {
	ID    string `json:"id"`
	Email string `json:"email"`
	Name  string `json:"name"`
}

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
	body := `{"email":"test@example.com","name":"Tester"}`
	req := httptest.NewRequest(http.MethodPost, "/users", strings.NewReader(body))
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rr.Code)
	}

	var resp apiResponse
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode response: %v", err)
	}
	if resp.ID == "" {
		t.Fatalf("expected non-empty ID")
	}
	if resp.Email != "test@example.com" || resp.Name != "Tester" {
		t.Fatalf("unexpected response: %+v", resp)
	}
}

func TestCreateUserValidation(t *testing.T) {
	handler := New()
	req := httptest.NewRequest(http.MethodPost, "/users", strings.NewReader(`{"email":""}`))
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if rr.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", rr.Code)
	}
}
