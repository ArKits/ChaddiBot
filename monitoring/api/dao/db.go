package dao

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3"
	"github.com/spf13/viper"
)

// Db is the presistent connection to the sqlite database
var Db *sql.DB

// InitializeDb by opening the connection to the database and make sure it works
func InitializeDb() {

	dbPath := viper.GetString("chaddi.db.path")

	log.Printf("Initializing DB... dbPath=%s", dbPath)

	conn, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		log.Panicf("Panic during sql.Open! %v", err)
	}

	Db = conn

}

// JSONString is a JSON object in a string representation
type JSONString map[string]interface{}

// Scan implements the Scanner interface for handling JSONString when read from the database
func (js *JSONString) Scan(value interface{}) error {

	jsonAsAString := fmt.Sprintf("%v", value)

	// Unmarshal or Decode the JSON to the interface.
	json.Unmarshal([]byte(jsonAsAString), &js)

	return nil
}
