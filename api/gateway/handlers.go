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
	UserID string  `json:"userId"`
	ItemID string  `json:"itemId"`
	Total  float64 `json:"total"`
}

type createOrderResponse struct {
	ID     string  `json:"id"`
	Status string  `json:"status"`
	Total  float64 `json:"total"`
}

type capturePaymentResponse struct {
	ID      string  `json:"id"`
	OrderID string  `json:"orderId"`
	Amount  float64 `json:"amount"`
	Status  string  `json:"status"`
}

func RegisterHandlers(mux *http.ServeMux) {
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})
	mux.HandleFunc("/api/users", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		createUser(w, r)
	})
	mux.HandleFunc("/api/orders", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		createOrder(w, r)
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
	resp := createUserResponse{ID: fmt.Sprintf("user-%d", time.Now().UnixNano()), Email: req.Email, Name: req.Name}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(resp)
}

func createOrder(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	var req createOrderRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	if req.UserID == "" || req.ItemID == "" {
		http.Error(w, "userId and itemId are required", http.StatusBadRequest)
		return
	}
	resp := createOrderResponse{
		ID:     fmt.Sprintf("order-%d", time.Now().UnixNano()),
		Status: "CREATED",
		Total:  req.Total,
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(resp)
}
