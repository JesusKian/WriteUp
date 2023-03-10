package config

import (
	"github.com/JesusKian/WriteUp/src/structure"
	_ "github.com/go-sql-driver/mysql"
	"github.com/joho/godotenv"

	"log"
	"os"
)

var (
	logFile        *os.File       = &os.File{}
	err            error          = nil
	PWD            string         = ""
	EnvData        structure.Data = structure.Data{}

	// Log Info
	flags = log.Lshortfile
	// Sturct For Information Log
	infoLog = log.New(os.Stdout, "[INFO] ", flags)
	// Sturct For Error Log
	ErrorLog = log.New(os.Stdout, "[ERROR] ", flags)
	// Struct For Default Log
	defaultLog = log.New(os.Stderr, "[SYS] ", flags)
)

func SetLog(_logType string, _msg string) {
	PWD, err = os.Getwd()
	if err != nil {
		ErrorLog.Println("config.SetLog() -> Couldn't Get Output Of 'os.Getwd()'")
		os.Exit(1)
	}

	logFile, err = os.OpenFile(PWD+"/log/log.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		ErrorLog.Println(`
		Invalid Directory -> /log
		Invalid File -> /log/log.log
		`)
		os.Exit(1)
	}

	switch _logType {
	case "I":
		infoLog.SetOutput(logFile)
		infoLog.Println(_msg)

	case "E":
		ErrorLog.SetOutput(logFile)
		ErrorLog.Println(_msg)

	case "D":
		defaultLog.SetOutput(logFile)
		defaultLog.Println(_msg)

	default:
		ErrorLog.SetOutput(logFile)
		ErrorLog.Printf("SetLog() -> Trying To Add Log Without Valid LogType '%s'", _logType)
	}

	logFile.Close()
}

func ReadENV() {
	godotenv.Load("config.env")

	EnvData = structure.Data{
		MysqlUsername:  os.Getenv("MYSQL_USERNAME"),
		MysqlPassword:  os.Getenv("MYSQL_PASSWORD"),
		TelegramApi:    os.Getenv("TELEGRAM_API"),
		DiscordWebhook: os.Getenv("DISCORD_WEBHOOK"),
		ChannelName:    os.Getenv("CHANNEL_NAME"),
	}
}

func init() {
	ReadENV()

	log.SetFlags(log.Ldate | log.Ltime)
	infoLog.SetFlags(log.Ldate | log.Ltime)
	ErrorLog.SetFlags(log.Ldate | log.Ltime)
	SetLog("I", "config.init() -> Flags Setuped")
}
