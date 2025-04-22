package services

import (
	"errors"
	"math/rand/v2"
	"slices"

	"lean/models"
)

type QuestionRepo interface {
	GetAll() []models.Question
	GetByID(id int) (models.Question, error)
	Add(q models.Question)
	Replace(id int, q models.Question) error
	Delete(id int) error
}

type QuestionService struct {
	repo QuestionRepo
}

func NewQuestionService(r QuestionRepo) *QuestionService {
	return &QuestionService{repo: r}
}

func (s *QuestionService) List(tag string, limit int) []models.Question {
	questions := s.repo.GetAll()
	if tag != "" {
		questions = FilterByTag(questions, tag)
	}
	if limit > 0 && limit < len(questions) {
		questions = questions[:limit]
	}
	return questions
}

func (s *QuestionService) Get(id int) (models.Question, error) {
	return s.repo.GetByID(id)
}

func (s *QuestionService) Create(q models.Question) error {
	if err := ValidateQuestion(q); err != nil {
		return err
	}
	s.repo.Add(q)
	return nil
}

func (s *QuestionService) Update(id int, q models.Question) error {
	if err := ValidateQuestion(q); err != nil {
		return err
	}
	return s.repo.Replace(id, q)
}

func (s *QuestionService) Delete(id int) error {
	return s.repo.Delete(id)
}

func (s *QuestionService) Random(n int) []models.Question {
	all := s.repo.GetAll()
	return RandomSample(all, n)
}

func FilterByTag(questions []models.Question, tag string) []models.Question {
	filtered := []models.Question{}
	for _, q := range questions {
		if slices.Contains(q.Tags, tag) {
			filtered = append(filtered, q)
		}
	}
	return filtered
}

func RandomSample(questions []models.Question, n int) []models.Question {
	cpy := make([]models.Question, len(questions))
	copy(cpy, questions)

	rand.Shuffle(len(cpy), func(i, j int) {
		cpy[i], cpy[j] = cpy[j], cpy[i]
	})

	if n > len(cpy) {
		n = len(cpy)
	}

	return cpy[:n]
}

func ValidateQuestion(q models.Question) error {
	if q.Text == "" {
		return errors.New("question text is required")
	}

	if len(q.Choices) < 2 {
		return errors.New("at least two choices are required")
	}

	found := slices.Contains(q.Choices, q.Answer)

	if !found {
		return errors.New("answer must be one of the choices")
	}

	return nil
}
