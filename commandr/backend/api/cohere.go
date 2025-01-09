// backend/api/cohere.go
package api

import (
	"context"

	cohere "github.com/cohere-ai/cohere-go/v2"
	client "github.com/cohere-ai/cohere-go/v2/client"
)

type CohereAPI struct {
	client *client.Client
}

func NewCohereAPI(apiKey string) (*CohereAPI, error) {
	co := client.NewClient(client.WithToken(apiKey))
	return &CohereAPI{client: co}, nil
}

func (c *CohereAPI) GenerateResponse(ctx context.Context, messages []cohere.ChatMessage, temperature float64) (*cohere.NonStreamedChatResponse, error) {
	// Convert messages to the format expected by the new API
	latestMessage := ""
	if len(messages) > 0 {
		latestMessage = messages[len(messages)-1].Message
	}

	// Create chat request with the new API format
	resp, err := c.client.Chat(
		ctx,
		&cohere.ChatRequest{
			Message:     latestMessage,
			Temperature: &temperature,
			// Add any additional parameters as needed
		},
	)

	return resp, err
}
