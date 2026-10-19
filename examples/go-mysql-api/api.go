package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log/slog"
	"mime"
	"net/http"
	"regexp"
	"strconv"
	"strings"
	"time"
	"unicode/utf8"

	"github.com/go-sql-driver/mysql"
)

type api struct{ store productStore }

func newHandler(store productStore) http.Handler {
	a := &api{store: store}
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", a.health)
	mux.HandleFunc("GET /products", a.list)
	mux.HandleFunc("GET /products/{id}", a.get)
	mux.HandleFunc("POST /products", a.create)
	mux.HandleFunc("PUT /products/{id}", a.update)
	mux.HandleFunc("DELETE /products/{id}", a.remove)
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		ctx, cancel := context.WithTimeout(r.Context(), 3*time.Second)
		defer cancel()
		mux.ServeHTTP(w, r.WithContext(ctx))
		slog.Info("request", "method", r.Method, "path", r.URL.Path, "duration", time.Since(start))
	})
}

func writeJSON(w http.ResponseWriter, status int, body any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	if body != nil {
		if err := json.NewEncoder(w).Encode(body); err != nil {
			slog.Error("encode response", "error", err)
		}
	}
}

func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]string{"error": message})
}

func storeError(w http.ResponseWriter, err error) {
	var mysqlErr *mysql.MySQLError
	switch {
	case errors.Is(err, sql.ErrNoRows):
		writeError(w, http.StatusNotFound, "product not found")
	case errors.As(err, &mysqlErr) && mysqlErr.Number == 1062:
		writeError(w, http.StatusConflict, "sku already exists")
	case errors.Is(err, context.DeadlineExceeded), errors.Is(err, context.Canceled):
		writeError(w, http.StatusGatewayTimeout, "request timed out")
	default:
		slog.Error("database operation", "error", err)
		writeError(w, http.StatusInternalServerError, "internal server error")
	}
}

func (a *api) health(w http.ResponseWriter, r *http.Request) {
	if err := a.store.Ping(r.Context()); err != nil {
		writeError(w, http.StatusServiceUnavailable, "database unavailable")
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func queryInt(r *http.Request, key string, fallback, min, max int) (int, error) {
	values, exists := r.URL.Query()[key]
	if !exists {
		return fallback, nil
	}
	if len(values) != 1 || values[0] == "" {
		return 0, fmt.Errorf("invalid %s", key)
	}
	n, err := strconv.Atoi(values[0])
	if err != nil || n < min || n > max {
		return 0, fmt.Errorf("%s must be between %d and %d", key, min, max)
	}
	return n, nil
}

func (a *api) list(w http.ResponseWriter, r *http.Request) {
	limit, err := queryInt(r, "limit", 20, 1, 100)
	if err != nil {
		writeError(w, 400, err.Error())
		return
	}
	offset, err := queryInt(r, "offset", 0, 0, 1_000_000)
	if err != nil {
		writeError(w, 400, err.Error())
		return
	}
	products, err := a.store.List(r.Context(), limit, offset)
	if err != nil {
		storeError(w, err)
		return
	}
	writeJSON(w, 200, map[string]any{"data": products, "limit": limit, "offset": offset})
}

func pathID(w http.ResponseWriter, r *http.Request) (int64, bool) {
	id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
	if err != nil || id <= 0 {
		writeError(w, 400, "id must be a positive integer")
		return 0, false
	}
	return id, true
}

func (a *api) get(w http.ResponseWriter, r *http.Request) {
	id, ok := pathID(w, r)
	if !ok {
		return
	}
	p, err := a.store.Get(r.Context(), id)
	if err != nil {
		storeError(w, err)
		return
	}
	writeJSON(w, 200, map[string]any{"data": p})
}

var skuPattern = regexp.MustCompile(`^[A-Z0-9-]{1,40}$`)

func decodeInput(w http.ResponseWriter, r *http.Request) (ProductInput, bool) {
	mediaType, _, err := mime.ParseMediaType(r.Header.Get("Content-Type"))
	if err != nil || mediaType != "application/json" {
		writeError(w, 415, "Content-Type must be application/json")
		return ProductInput{}, false
	}
	r.Body = http.MaxBytesReader(w, r.Body, 1<<20)
	defer r.Body.Close()
	// Pointers distinguish missing/null from valid zero (a free product).
	var body struct {
		SKU         *string `json:"sku"`
		Name        *string `json:"name"`
		PriceSatang *int64  `json:"price_satang"`
	}
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	decodeErr := decoder.Decode(&body)
	if decodeErr == nil {
		var extra any
		decodeErr = decoder.Decode(&extra)
		if errors.Is(decodeErr, io.EOF) {
			decodeErr = nil
		} else if decodeErr == nil {
			decodeErr = errors.New("more than one JSON value")
		}
	}
	if decodeErr != nil {
		var tooLarge *http.MaxBytesError
		if errors.As(decodeErr, &tooLarge) {
			writeError(w, 413, "body exceeds 1 MiB")
		} else {
			writeError(w, 400, "body must contain exactly one valid product JSON object")
		}
		return ProductInput{}, false
	}
	if body.SKU == nil || body.Name == nil || body.PriceSatang == nil {
		writeError(w, 400, "sku, name and price_satang are required and cannot be null")
		return ProductInput{}, false
	}
	input := ProductInput{SKU: *body.SKU, Name: strings.TrimSpace(*body.Name), PriceSatang: *body.PriceSatang}
	if !skuPattern.MatchString(input.SKU) || input.Name == "" || utf8.RuneCountInString(input.Name) > 120 ||
		input.PriceSatang < 0 || input.PriceSatang > 1_000_000_000_000 {
		writeError(w, 400, "sku: A-Z/0-9/hyphen 1-40; name: 1-120 characters; price_satang: 0-1000000000000")
		return ProductInput{}, false
	}
	return input, true
}

func (a *api) create(w http.ResponseWriter, r *http.Request) {
	input, ok := decodeInput(w, r)
	if !ok {
		return
	}
	p, err := a.store.Create(r.Context(), input)
	if err != nil {
		storeError(w, err)
		return
	}
	w.Header().Set("Location", fmt.Sprintf("/products/%d", p.ID))
	writeJSON(w, http.StatusCreated, map[string]any{"data": p})
}

func (a *api) update(w http.ResponseWriter, r *http.Request) {
	id, ok := pathID(w, r)
	if !ok {
		return
	}
	input, ok := decodeInput(w, r)
	if !ok {
		return
	}
	p, err := a.store.Update(r.Context(), id, input)
	if err != nil {
		storeError(w, err)
		return
	}
	writeJSON(w, 200, map[string]any{"data": p})
}

func (a *api) remove(w http.ResponseWriter, r *http.Request) {
	id, ok := pathID(w, r)
	if !ok {
		return
	}
	if err := a.store.Delete(r.Context(), id); err != nil {
		storeError(w, err)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}
