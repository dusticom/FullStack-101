package main

import (
	"context"
	"database/sql"
	"fmt"
	"net"
	"os"
	"time"

	"github.com/go-sql-driver/mysql"
)

func env(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func openDB(ctx context.Context) (*sql.DB, error) {
	if os.Getenv("DB_PASSWORD") == "" {
		return nil, fmt.Errorf("DB_PASSWORD is required")
	}
	cfg := mysql.NewConfig()
	cfg.User = env("DB_USER", "learner")
	cfg.Passwd = os.Getenv("DB_PASSWORD")
	cfg.Net = "tcp"
	cfg.Addr = net.JoinHostPort(env("DB_HOST", "127.0.0.1"), env("DB_PORT", "3306"))
	cfg.DBName = env("DB_NAME", "go_course")
	cfg.ParseTime = true
	cfg.Loc = time.UTC
	cfg.ClientFoundRows = true // UPDATE with unchanged values still matches one row.
	cfg.Timeout = 5 * time.Second
	cfg.ReadTimeout = 5 * time.Second
	cfg.WriteTimeout = 5 * time.Second
	cfg.Params = map[string]string{"charset": "utf8mb4", "time_zone": "'+00:00'"}
	// For a remote DB set DB_TLS=true and use a hostname matching its certificate.
	cfg.TLSConfig = os.Getenv("DB_TLS")
	db, err := sql.Open("mysql", cfg.FormatDSN())
	if err != nil {
		return nil, fmt.Errorf("open database: %w", err)
	}
	db.SetMaxOpenConns(10)
	db.SetMaxIdleConns(10)
	db.SetConnMaxLifetime(3 * time.Minute)
	db.SetConnMaxIdleTime(time.Minute)
	pingCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()
	if err := db.PingContext(pingCtx); err != nil {
		_ = db.Close()
		return nil, fmt.Errorf("ping database: %w", err)
	}
	return db, nil
}
