package controllers

import (
	"encoding/json"
	"net/http"
)

// Version encapsulates the version of the application
type Version struct {
	Name    string `json:"name"`
	Version string `json:"version"`
}

// VersionController handles the /version query
func VersionController(w http.ResponseWriter, r *http.Request) {
	v := Version{
		Name:    "chaddi-api",
		Version: "0.0.1",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(v)
}
