// backend/services/chat.go
package services

import (
	"context"
	"sync"

	"commandr/backend/api"
	"commandr/backend/models"

	cohere "github.com/cohere-ai/cohere-go/v2"
)

type ChatService struct {
	cohereAPI     *api.CohereAPI
	conversations map[string]*models.Conversation
	currentConvID string
	mu            sync.RWMutex
}

func NewChatService(cohereAPI *api.CohereAPI) *ChatService {
	return &ChatService{
		cohereAPI:     cohereAPI,
		conversations: make(map[string]*models.Conversation),
	}
}

func (s *ChatService) CreateConversation(title string) *models.Conversation {
	s.mu.Lock()
	defer s.mu.Unlock()

	conv := models.NewConversation(title)
	s.conversations[conv.ID] = conv
	s.currentConvID = conv.ID
	return conv
}

func (s *ChatService) GetCurrentConversation() *models.Conversation {
	s.mu.RLock()
	defer s.mu.RUnlock()

	return s.conversations[s.currentConvID]
}

func (s *ChatService) GenerateResponse(ctx context.Context, content string, temperature float64) (*cohere.NonStreamedChatResponse, error) {
	// Create a message slice with just the current message for now
	// We can expand this later to include conversation history if needed
	messages := []cohere.ChatMessage{
		{
			Message: content,
		},
	}

	return s.cohereAPI.GenerateResponse(ctx, messages, temperature)
}
