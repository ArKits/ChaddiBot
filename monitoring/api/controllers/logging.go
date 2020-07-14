package controllers

import (
	"log"
	"net/http"
)

// LoggingMiddleware logs incoming HTTP requests
func LoggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		log.Printf("%s - %s | %s", r.Method, r.RequestURI, r.RemoteAddr)

		next.ServeHTTP(w, r)
	})
}
