package models

type HttpResponseError struct {
	Name        string `json:"error_name"`
	Description string `json:"error_description"`
}
