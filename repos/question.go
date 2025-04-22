package repos

import (
	"errors"
	"sync"

	"lean/models"
)

type QuestionRepo struct {
	mu        sync.RWMutex
	questions map[int]models.Question
	counter   int
}

func NewQuestionRepo() *QuestionRepo {
	return &QuestionRepo{
		questions: make(map[int]models.Question),
	}
}

func (r *QuestionRepo) GetAll() []models.Question {
	r.mu.RLock()
	defer r.mu.RUnlock()

	all := make([]models.Question, 0, len(r.questions))
	for _, q := range r.questions {
		all = append(all, q)
	}

	return all
}

func (r *QuestionRepo) GetByID(id int) (models.Question, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	q, ok := r.questions[id]
	if !ok {
		return models.Question{}, errors.New("question not found")
	}

	return q, nil
}

func (r *QuestionRepo) Add(q models.Question) {
	r.mu.Lock()
	defer r.mu.Unlock()

	q.ID = r.counter
	r.questions[q.ID] = q

	r.counter++
}

func (r *QuestionRepo) Replace(id int, q models.Question) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.questions[id]; !exists {
		return errors.New("question not found")
	}

	r.questions[id] = q
	return nil
}

func (r *QuestionRepo) Delete(id int) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.questions[id]; !exists {
		return errors.New("question not found")
	}
	delete(r.questions, id)
	return nil
}
