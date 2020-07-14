package controllers

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"

	"github.com/arkits/chaddi-tg/monitoring/api/dao"
	"github.com/arkits/chaddi-tg/monitoring/api/models"
	"github.com/gorilla/mux"
)

// GetAllBakchodsController handles the GET /bakchod query by returning
// all the Bakchods from the database
func GetAllBakchodsController(w http.ResponseWriter, r *http.Request) {

	log.Printf("GetAllBakchodsController")

	allBakchods := dao.GetAllBakchods()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(allBakchods)
}

// GetBakchodByIDController handles the GET /bakchod/id query by returning
// the requested Bakchod	 from the database
func GetBakchodByIDController(w http.ResponseWriter, r *http.Request) {

	vars := mux.Vars(r)

	bakchodID := vars["bakchodID"]

	log.Printf("GetBakchodByIDController bakchodID=%s", bakchodID)

	w.Header().Set("Content-Type", "application/json")

	bakchod, err := dao.GetBakchodByID(bakchodID)
	if err != nil {
		log.Printf("Received error in GetBakchodByIDController - %s", err)

		w.WriteHeader(http.StatusBadRequest)

		var httpResponseError models.HttpResponseError

		if err == sql.ErrNoRows {
			httpResponseError.Name = "sql.ErrNoRows"
		} else {
			httpResponseError.Name = err.Error()
		}

		httpResponseError.Description = err.Error()
		json.NewEncoder(w).Encode(httpResponseError)

		return
	}

	json.NewEncoder(w).Encode(bakchod)
}
