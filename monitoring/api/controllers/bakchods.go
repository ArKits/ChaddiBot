package controllers

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/arkits/chaddi-tg/monitoring/api/dao"
	"github.com/gorilla/mux"
)

func GetAllBakchodsController(w http.ResponseWriter, r *http.Request) {

	allBakchods := dao.GetAllBakchods()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(allBakchods)
}

func GetBakchodByIDController(w http.ResponseWriter, r *http.Request) {

	vars := mux.Vars(r)

	bakchodID := vars["bakchodID"]

	log.Printf("GetBakchodByIDController bakchodID=%s", bakchodID)

	bakchod := dao.GetBakchodByID(bakchodID)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(bakchod)
}
