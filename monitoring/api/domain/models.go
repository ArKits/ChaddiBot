package domain

import "database/sql"

type Bakchod struct {
	Id       string         `json:"id"`
	Username sql.NullString `json:"username"`
}
