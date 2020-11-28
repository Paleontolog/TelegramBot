package main

import (
	"log"
	"os"

	"github.com/Syfaro/telegram-bot-api"
)

func main() {

	apiKey := os.Getenv("API_KEY")

	if apiKey == "" {
		log.Panic("No Api key")
		return
	}

	bot, err := tgbotapi.NewBotAPI(apiKey)
	if err != nil {
		log.Panic(err)
	}

	bot.Debug = true

	log.Printf("Authorized on account %s", bot.Self.UserName)

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates, err := bot.GetUpdatesChan(u)

	for update := range updates {

		if update.ChannelPost.Text == "" {
			continue
		}

		log.Printf("[%s] %s", update.ChannelPost.From, update.ChannelPost.Text)

		msg := tgbotapi.NewMessage(update.ChannelPost.Chat.ID, update.ChannelPost.Text)
		msg.ReplyToMessageID = update.ChannelPost.MessageID

		_, _ = bot.Send(msg)
	}
}
