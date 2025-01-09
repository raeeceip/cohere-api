package models

import (
    "time"
    "github.com/google/uuid"
)

type Message struct {
    ID        string    `json:"id"`
    Role      string    `json:"role"`
    Content   string    `json:"content"`
    Timestamp time.Time `json:"timestamp"`
}

type Conversation struct {
    ID        string    `json:"id"`
    Title     string    `json:"title"`
    Messages  []Message `json:"messages"`
    CreatedAt time.Time `json:"createdAt"`
}

func NewConversation(title string) *Conversation {
    return &Conversation{
        ID:        uuid.New().String(),
        Title:     title,
        Messages:  make([]Message, 0),
        CreatedAt: time.Now(),
    }
}

func (c *Conversation) AddMessage(role, content string) Message {
    msg := Message{
        ID:        uuid.New().String(),
        Role:      role,
        Content:   content,
        Timestamp: time.Now(),
    }
    c.Messages = append(c.Messages, msg)
    return msg
}
