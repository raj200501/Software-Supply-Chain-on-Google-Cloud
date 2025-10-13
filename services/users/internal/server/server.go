package server

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

// New returns an HTTP handler implementing the minimal users API.
func New() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})
	mux.HandleFunc("/users", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
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
	})
	return mux
}
