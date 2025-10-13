package server

import (
    "encoding/json"
    "net/http"
)

type createUserRequest struct {
    Email string `json:"email"`
}

type createUserResponse struct {
    ID    string `json:"id"`
    Email string `json:"email"`
}

// New returns an HTTP handler implementing the minimal users API.
func New() http.Handler {
    mux := http.NewServeMux()
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
        resp := createUserResponse{ID: "user-1", Email: req.Email}
        w.Header().Set("Content-Type", "application/json")
        _ = json.NewEncoder(w).Encode(resp)
    })
    return mux
}
