package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

type orderResponse struct {
	ID       string  `json:"id"`
	Status   string  `json:"status"`
	Total    float64 `json:"total"`
	Quantity int     `json:"quantity"`
}

type userResponse struct {
	ID    string `json:"id"`
	Email string `json:"email"`
	Name  string `json:"name"`
}

type inventoryResponse []inventoryItem

func TestHealthEndpoints(t *testing.T) {
	mux := http.NewServeMux()
	RegisterHandlers(mux)

	tests := []struct {
		name   string
		path   string
		status int
	}{
		{name: "healthz", path: "/healthz", status: http.StatusOK},
		{name: "readyz", path: "/readyz", status: http.StatusOK},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodGet, tc.path, nil)
			rr := httptest.NewRecorder()

			mux.ServeHTTP(rr, req)

			if rr.Code != tc.status {
				t.Fatalf("expected status %d, got %d", tc.status, rr.Code)
			}
		})
	}
}

func TestCreateUser(t *testing.T) {
	mux := http.NewServeMux()
	RegisterHandlers(mux)

	body := bytes.NewBufferString(`{"email":"test@example.com","name":"Tester"}`)
	req := httptest.NewRequest(http.MethodPost, "/v1/users", body)
	rr := httptest.NewRecorder()

	mux.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("expected status 200, got %d", rr.Code)
	}

	var resp userResponse
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("decode response: %v", err)
	}
	if resp.ID == "" || resp.Email != "test@example.com" || resp.Name != "Tester" {
		t.Fatalf("unexpected response: %#v", resp)
	}
}

func TestCreateOrder(t *testing.T) {
	mux := http.NewServeMux()
	RegisterHandlers(mux)

	body := bytes.NewBufferString(`{"userId":"user-1","itemId":"starter-kit","quantity":1,"total":25.0}`)
	req := httptest.NewRequest(http.MethodPost, "/v1/orders", body)
	rr := httptest.NewRecorder()

	mux.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("expected status 200, got %d", rr.Code)
	}

	var resp orderResponse
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("decode response: %v", err)
	}
	if resp.ID == "" || resp.Status != "CREATED" || resp.Quantity != 1 {
		t.Fatalf("unexpected response: %#v", resp)
	}
}

func TestListInventory(t *testing.T) {
	mux := http.NewServeMux()
	RegisterHandlers(mux)

	req := httptest.NewRequest(http.MethodGet, "/v1/inventory", nil)
	rr := httptest.NewRecorder()

	mux.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("expected status 200, got %d", rr.Code)
	}

	var resp inventoryResponse
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("decode response: %v", err)
	}
	if len(resp) == 0 {
		t.Fatalf("expected inventory items")
	}
}
