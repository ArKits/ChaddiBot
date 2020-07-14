package dao

import (
	"log"

	"gopkg.in/guregu/null.v4"
)

type Bakchod struct {
	Id        string      `json:"id"`
	Username  null.String `json:"username"`
	FirstName null.String `json:"first_name"`
	Lastseen  null.String `json:"lastseen"`
	Rokda     float32     `json:"rokda"`
	History   JSONString  `json:"history"`
	Modifiers JSONString  `json:"modifiers"`
}

// GetAllBakchods retrives all Bakchods from the database
func GetAllBakchods() []Bakchod {

	rows, err := Db.Query("SELECT id, username, first_name, lastseen, rokda, history, modifiers FROM bakchods;")
	if err != nil {
		log.Panicf("Panic during GetAllBakchods! %v", err)
	}

	var bakchods []Bakchod

	for rows.Next() {

		var bakchod Bakchod

		err = rows.Scan(
			&bakchod.Id,
			&bakchod.Username,
			&bakchod.FirstName,
			&bakchod.Lastseen,
			&bakchod.Rokda,
			&bakchod.History,
			&bakchod.Modifiers,
		)

		if err != nil {
			log.Panicf("Panic! %v", err)
		}

		bakchods = append(bakchods, bakchod)

	}

	rows.Close()

	return bakchods
}

// GetBakchodByID retrives a Bakchod from the database based on the ID
func GetBakchodByID(bakchodID string) Bakchod {

	var bakchod Bakchod

	query := `SELECT id, username, first_name, lastseen, rokda, history, modifiers FROM bakchods WHERE id = ?;`
	err := Db.QueryRow(query, bakchodID).Scan(
		&bakchod.Id,
		&bakchod.Username,
		&bakchod.FirstName,
		&bakchod.Lastseen,
		&bakchod.Rokda,
		&bakchod.History,
		&bakchod.Modifiers,
	)
	if err != nil {
		log.Panicf("Panic during GetBakchodByID! %v", err)
	}

	return bakchod
}
