package main

import (
	"log"
	"net/http"

	"github.com/arkits/chaddi-tg/monitoring/api/controllers"
	"github.com/arkits/chaddi-tg/monitoring/api/dao"
	"github.com/spf13/viper"
)

func main() {

	SetupConfig()

	port := viper.GetString("server.port")

	dao.InitializeDb()

	http.HandleFunc("/chaddi/", controllers.VersionController)
	http.HandleFunc("/chaddi/bakchods/", controllers.BakchodsController)

	log.Printf("Starting chaddi-api on http://localhost:%v", port)
	http.ListenAndServe(":"+port, nil)
}

// SetupConfig -  Setup the application config by reading the config file via Viper
func SetupConfig() {
	viper.SetConfigName("config")
	viper.AddConfigPath(".")

	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("Error reading config file! - %s", err)
	}

}
