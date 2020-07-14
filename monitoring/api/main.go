package main

import (
	"log"
	"net/http"

	"github.com/arkits/chaddi-tg/monitoring/api/domain"
	"github.com/spf13/viper"
)

func main() {

	SetupConfig()

	port := viper.GetString("server.port")

	log.Printf("Starting chaddi-api on http://localhost:%v", port)

	http.HandleFunc("/chaddi/", domain.VersionController)
	http.HandleFunc("/chaddi/bakchods/", domain.BakchodController)

	http.ListenAndServe(":"+port, nil)
}

func SetupConfig() {
	viper.SetConfigName("config")
	viper.AddConfigPath(".")

	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("Error reading config file! - %s", err)
	}

}
