package main

import (
	"embed"
	"log"
	"os"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"go.uber.org/zap"

	"commandr/backend/api"

	"commandr/backend/services"

	"commandr/backend/utils"
)

//go:embed frontend/dist
var assets embed.FS

func main() {
	// Initialize logger
	utils.InitLogger()

	// Create Cohere API client
	cohereAPI, err := api.NewCohereAPI(os.Getenv("COHERE_API_KEY"))
	if err != nil {
		log.Fatal(err)
	}

	// Create chat service
	chatService := services.NewChatService(cohereAPI)

	// Create application
	app := NewApp(chatService)

	// Create application with options
	err = wails.Run(&options.App{
		Title:            "CommandR",
		Width:            1024,
		Height:           768,
		Assets:           assets,
		BackgroundColour: &options.RGBA{R: 27, G: 38, B: 54, A: 1},
		OnStartup:        app.startup,
		Bind: []interface{}{
			app,
		},
	})

	if err != nil {
		utils.Logger.Fatal("Error running application", zap.Error(err))
	}
}
