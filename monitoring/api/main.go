package main

import (
	"log"
	"net/http"

	"github.com/arkits/chaddi-tg/monitoring/api/controllers"
	"github.com/arkits/chaddi-tg/monitoring/api/dao"
	"github.com/gorilla/mux"
	"github.com/spf13/viper"
)

func main() {

	SetupConfig()

	port := viper.GetString("server.port")

	dao.InitializeDb()

	r := mux.NewRouter()

	r.HandleFunc("/", controllers.VersionController).Methods(http.MethodGet)
	r.HandleFunc("/chaddi", controllers.VersionController).Methods(http.MethodGet)

	r.HandleFunc("/chaddi/bakchods", controllers.GetAllBakchodsController).Methods(http.MethodGet, http.MethodOptions)
	r.HandleFunc("/chaddi/bakchods/{bakchodID}", controllers.GetBakchodByIDController).Methods(http.MethodGet, http.MethodOptions)

	r.Use(controllers.LoggingMiddleware)
	r.Use(mux.CORSMethodMiddleware(r))

	log.Printf("Starting chaddi-api on http://localhost:%v", port)
	http.ListenAndServe(":"+port, r)

}

// SetupConfig -  Setup the application config by reading the config file via Viper
func SetupConfig() {
	viper.SetConfigName("config")
	viper.AddConfigPath(".")

	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("Error reading config file! - %s", err)
	}

}
