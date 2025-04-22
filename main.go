package main

import (
	"log"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"

	"lean/handlers"
	"lean/repos"
	"lean/services"
)

func main() {
	r := chi.NewRouter()
	r.Use(middleware.Logger)

	repo := repos.NewQuestionRepo()
	service := services.NewQuestionService(repo)
	handler := handlers.NewQuestionHandler(service)

	handler.RegisterRoutes(r)

	err := http.ListenAndServe(":8080", r)
	if err != nil {
		log.Fatal(err)
	}
}

