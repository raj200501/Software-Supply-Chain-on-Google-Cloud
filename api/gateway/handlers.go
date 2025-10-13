package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type createUserRequest struct {
	Email string `json:"email"`
	Name  string `json:"name"`
}

type createUserResponse struct {
	ID    string `json:"id"`
	Email string `json:"email"`
	Name  string `json:"name"`
}

type createOrderRequest struct {
	UserID   string  `json:"userId"`
	ItemID   string  `json:"itemId"`
	Quantity int     `json:"quantity"`
	Total    float64 `json:"total"`
}

type createOrderResponse struct {
	ID       string  `json:"id"`
	Status   string  `json:"status"`
	Total    float64 `json:"total"`
	Quantity int     `json:"quantity"`
}

type inventoryItem struct {
	SKU      string  `json:"sku"`
	Name     string  `json:"name"`
	Quantity int     `json:"quantity"`
	Price    float64 `json:"price"`
}

func RegisterHandlers(mux *http.ServeMux) {
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, _ *http.Request) {
		respondJSON(w, http.StatusOK, map[string]string{"status": "ok"})
	})
	mux.HandleFunc("/readyz", func(w http.ResponseWriter, _ *http.Request) {
		respondJSON(w, http.StatusOK, map[string]string{"status": "ready"})
	})
	mux.HandleFunc("/v1/users", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		createUser(w, r)
	})
	mux.HandleFunc("/v1/orders", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		createOrder(w, r)
	})
	mux.HandleFunc("/v1/inventory", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		listInventory(w)
	})
}

func createUser(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()

	var req createUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	if req.Email == "" || req.Name == "" {
		http.Error(w, "email and name are required", http.StatusBadRequest)
		return
	}

	respondJSON(w, http.StatusOK, createUserResponse{
		ID:    fmt.Sprintf("user-%d", time.Now().UnixNano()),
		Email: req.Email,
		Name:  req.Name,
	})
}

func createOrder(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()

	var req createOrderRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	if req.UserID == "" || req.ItemID == "" || req.Quantity <= 0 {
		http.Error(w, "userId, itemId, and quantity are required", http.StatusBadRequest)
		return
	}

	respondJSON(w, http.StatusOK, createOrderResponse{
		ID:       fmt.Sprintf("order-%d", time.Now().UnixNano()),
		Status:   "CREATED",
		Total:    req.Total,
		Quantity: req.Quantity,
	})
}

func listInventory(w http.ResponseWriter) {
	items := []inventoryItem{
		{SKU: "starter-kit", Name: "Starter Kit", Quantity: 42, Price: 25.00},
		{SKU: "pro-upgrade", Name: "Pro Upgrade", Quantity: 15, Price: 99.00},
	}
	respondJSON(w, http.StatusOK, items)
}

func respondJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}
