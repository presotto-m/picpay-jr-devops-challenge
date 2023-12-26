package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/go-redis/redis"
	"github.com/rs/cors"
)

func main() {
	redisHost := "picpay-jr-devops-challenge-redis-1" // Altere para o host correto do seu servidor Redis
	redisPort := "6379"

	mux := http.NewServeMux()

	mux.HandleFunc("/health", func(writer http.ResponseWriter, request *http.Request) {
		if request.Method == "OPTIONS" {
			writer.WriteHeader(http.StatusOK)
			return
		}
		fmt.Fprintf(writer, "up")
	})

	mux.HandleFunc("/data", func(writer http.ResponseWriter, request *http.Request) {
		client := redis.NewClient(&redis.Options{Addr: redisHost + ":" + redisPort})
		val, err := client.Get(client.Context(), "SHAREDKEY").Result()
		if err != nil {
			http.Error(writer, err.Error(), http.StatusInternalServerError)
			return
		}
		fmt.Fprintf(writer, val)
	})

	handler := cors.New(cors.Options{
		AllowedOrigins: []string{"*"},
		AllowedHeaders: []string{"*"},
	}).Handler(mux)

	log.Fatal(http.ListenAndServe(":8081", handler))
}
