package domain

import (
	"database/sql"
	"log"

	_ "github.com/mattn/go-sqlite3"
	"github.com/spf13/viper"
)

func GetAllBakchods() []Bakchod {

	dbPath := viper.GetString("chaddi.db.path")

	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		log.Panicf("Panic! %v", err)
	}

	rows, err := db.Query("SELECT id, username FROM bakchods")
	if err != nil {
		log.Panicf("Panic! %v", err)
	}

	var bakchods []Bakchod

	for rows.Next() {

		var bakchod Bakchod

		err = rows.Scan(&bakchod.Id, &bakchod.Username)

		if err != nil {
			log.Panicf("Panic! %v", err)
		}

		bakchods = append(bakchods, bakchod)

	}

	rows.Close()

	return bakchods
}
