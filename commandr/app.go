package main

import (
	"commandr/backend/services"
	"context"
)

// App struct
type App struct {
	ctx         context.Context
	chatService *services.ChatService
}

type ChatResponse struct {
	Content string `json:"content"`
}

// NewApp creates a new App application struct
func NewApp(chatService *services.ChatService) *App {
	return &App{
		chatService: chatService,
	}
}

// startup is called when the app starts. The context is saved
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
}

// SendMessage sends a message to the chat service and returns a response
func (a *App) SendMessage(message string, temperature float64) (*ChatResponse, error) {
	response, err := a.chatService.GenerateResponse(a.ctx, message, temperature)
	if err != nil {
		return nil, err
	}

	return &ChatResponse{
		Content: response.Text,
	}, nil
}

// ClearChat clears the current conversation
func (a *App) ClearChat() error {
	a.chatService.CreateConversation("New Chat")
	return nil
}
