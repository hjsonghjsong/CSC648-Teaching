package handlers

import (
	"encoding/json"
	"net/http"
	"strconv"

	"lean/models"
	"lean/services"

	"github.com/go-chi/chi/v5"
)

type QuestionHandler struct {
	service *services.QuestionService
}

func NewQuestionHandler(service *services.QuestionService) *QuestionHandler {
	return &QuestionHandler{service: service}
}

func (h *QuestionHandler) RegisterRoutes(r chi.Router) {
	r.Get("/questions", h.ListQuestions)
	r.Get("/questions/{id}", h.GetQuestion)
	r.Get("/questions/random", h.GetRandomQuestions)
	r.Post("/questions", h.CreateQuestion)
	r.Put("/questions/{id}", h.ReplaceQuestion)
	r.Delete("/questions/{id}", h.DeleteQuestion)
}

func (h *QuestionHandler) ListQuestions(w http.ResponseWriter, r *http.Request) {
	tag := r.URL.Query().Get("tag")
	limitStr := r.URL.Query().Get("n")

	limit := 0
	if limitStr != "" {
		l, err := strconv.Atoi(limitStr)
		if err != nil {
			http.Error(w, "invalid limit number", http.StatusBadRequest)
			return
		}
		limit = l
	}

	questions := h.service.List(tag, limit)
	respondJSON(w, http.StatusOK, questions)
}

func (h *QuestionHandler) GetQuestion(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(chi.URLParam(r, "id"))
	if err != nil {
		http.Error(w, "invalid question id", http.StatusBadRequest)
		return
	}

	q, err := h.service.Get(id)
	if err != nil {
		http.Error(w, "question not found", http.StatusNotFound)
		return
	}

	respondJSON(w, http.StatusOK, q)
}

func (h *QuestionHandler) GetRandomQuestions(w http.ResponseWriter, r *http.Request) {
	n := 5
	limitStr := r.URL.Query().Get("n")

	if limitStr != "" {
		l, err := strconv.Atoi(limitStr)
		if err != nil {
			http.Error(w, "invalid limit number", http.StatusBadRequest)
			return
		}
		n = l
	}

	questions := h.service.Random(n)
	respondJSON(w, http.StatusOK, questions)
}

func (h *QuestionHandler) CreateQuestion(w http.ResponseWriter, r *http.Request) {
	var q models.Question
	if err := json.NewDecoder(r.Body).Decode(&q); err != nil {
		http.Error(w, "invalid JSON", http.StatusBadRequest)
		return
	}

	if err := h.service.Create(q); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusCreated)
}

func (h *QuestionHandler) ReplaceQuestion(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(chi.URLParam(r, "id"))
	if err != nil {
		http.Error(w, "invalid question id", http.StatusBadRequest)
		return
	}

	var q models.Question

	if err := json.NewDecoder(r.Body).Decode(&q); err != nil {
		http.Error(w, "invalid JSON", http.StatusBadRequest)
		return
	}

	if err := h.service.Update(id, q); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

func (h *QuestionHandler) DeleteQuestion(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(chi.URLParam(r, "id"))
	if err != nil {
		http.Error(w, "invalid question id", http.StatusBadRequest)
		return
	}

	if err := h.service.Delete(id); err != nil {
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

func respondJSON(w http.ResponseWriter, code int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(payload)
}
