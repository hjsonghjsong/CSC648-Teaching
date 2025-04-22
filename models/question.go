package models

type Question struct {
	ID      int      `json:"id"`
	Text    string   `json:"text"`
	Choices []string `json:"choices"`
	Answer  string   `json:"answer"`
	Tags    []string `json:"tags,omitempty"`
}
