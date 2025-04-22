package services

import (
	"testing"

	"lean/models"
)

func TestValidateQuestion(t *testing.T) {
	tests := []struct {
		name    string
		input   models.Question
		wantErr bool
	}{
		{
			name: "valid question",
			input: models.Question{
				Text:    "What is 2 + 2?",
				Choices: []string{"3", "4"},
				Answer:  "4",
			},
			wantErr: false,
		},
		{
			name: "missing text",
			input: models.Question{
				Choices: []string{"3", "4"},
				Answer:  "4",
			},
			wantErr: true,
		},
		{
			name: "not enough choices",
			input: models.Question{
				Text:    "What is 2 + 2?",
				Choices: []string{"4"},
				Answer:  "4",
			},
			wantErr: true,
		},
		{
			name: "answer not in choices",
			input: models.Question{
				Text:    "What is 2 + 2?",
				Choices: []string{"3", "5"},
				Answer:  "4",
			},
			wantErr: true,
		},
	}

	for _, tc := range tests {
		err := ValidateQuestion(tc.input)
		if tc.wantErr && err == nil {
			t.Errorf("%s: expected error, got nil", tc.name)
		}
		if !tc.wantErr && err != nil {
			t.Errorf("%s: unexpected error: %v", tc.name, err)
		}
	}
}

func TestFilterByTag(t *testing.T) {
	questions := []models.Question{
		{ID: 1, Tags: []string{"math", "easy"}},
		{ID: 2, Tags: []string{"science"}},
		{ID: 3, Tags: []string{"math"}},
	}

	result := FilterByTag(questions, "math")
	if len(result) != 2 {
		t.Errorf("expected 2 questions with 'math' tag, got %d", len(result))
	}
}

func TestRandomSample(t *testing.T) {
	questions := []models.Question{
		{ID: 1}, {ID: 2}, {ID: 3}, {ID: 4}, {ID: 5},
	}

	// Test that n > len returns all items
	result := RandomSample(questions, 10)
	if len(result) != len(questions) {
		t.Errorf("expected all questions when n > len, got %d", len(result))
	}

	// Test fixed length
	n := 3
	result = RandomSample(questions, n)
	if len(result) != n {
		t.Errorf("expected %d questions, got %d", n, len(result))
	}
}
