package domain

import (
	"encoding/json"
	"net/http"
)

func BakchodController(w http.ResponseWriter, r *http.Request) {

	allBakchods := GetAllBakchods()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(allBakchods)
}
