package controllers

import (
	"encoding/json"
	"net/http"

	"github.com/arkits/chaddi-tg/monitoring/api/dao"
)

func BakchodsController(w http.ResponseWriter, r *http.Request) {

	allBakchods := dao.GetAllBakchods()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(allBakchods)
}
