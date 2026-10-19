package main

import (
	"context"
	"database/sql"
	"errors"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/go-sql-driver/mysql"
)

type fakeStore struct {
	productStore
	err error
}

func (f fakeStore) Ping(context.Context) error { return f.err }
func (f fakeStore) Get(context.Context, int64) (Product, error) {
	return Product{ID: 1, SKU: "GO-1", Name: "Book", PriceSatang: 0}, f.err
}
func (f fakeStore) Create(_ context.Context, input ProductInput) (Product, error) {
	return Product{ID: 1, SKU: input.SKU, Name: input.Name, PriceSatang: input.PriceSatang}, f.err
}

func TestInvalidRequestsNeverReachStore(t *testing.T) {
	tests := []struct {
		name, method, path, body, contentType string
		want int
	}{
		{"bad id", "GET", "/products/abc", "", "", 400},
		{"negative id", "GET", "/products/-1", "", "", 400},
		{"overflow id", "GET", "/products/999999999999999999999", "", "", 400},
		{"limit bound", "GET", "/products?limit=101", "", "", 400},
		{"empty limit", "GET", "/products?limit=", "", "", 400},
		{"repeated limit", "GET", "/products?limit=1&limit=2", "", "", 400},
		{"negative offset", "GET", "/products?offset=-1", "", "", 400},
		{"wrong method", "PATCH", "/products/1", "", "", 405},
		{"content type", "POST", "/products", `{}`, "text/plain", 415},
		{"empty body", "POST", "/products", ``, "application/json", 400},
		{"null body", "POST", "/products", `null`, "application/json", 400},
		{"missing field", "POST", "/products", `{"sku":"A","name":"B"}`, "application/json", 400},
		{"null field", "POST", "/products", `{"sku":"A","name":"B","price_satang":null}`, "application/json", 400},
		{"unknown field", "POST", "/products", `{"sku":"A","name":"B","price_satang":0,"admin":true}`, "application/json", 400},
		{"negative price", "POST", "/products", `{"sku":"A","name":"B","price_satang":-1}`, "application/json", 400},
		{"fractional price", "POST", "/products", `{"sku":"A","name":"B","price_satang":1.1}`, "application/json", 400},
		{"bad sku", "POST", "/products", `{"sku":"a b","name":"B","price_satang":0}`, "application/json", 400},
		{"blank name", "POST", "/products", `{"sku":"A","name":"  ","price_satang":0}`, "application/json", 400},
		{"long Thai name", "POST", "/products", `{"sku":"A","name":"` + strings.Repeat("ก", 121) + `","price_satang":0}`, "application/json", 400},
		{"two objects", "POST", "/products", `{"sku":"A","name":"B","price_satang":0} {}`, "application/json", 400},
		{"trailing garbage", "POST", "/products", `{"sku":"A","name":"B","price_satang":0} x`, "application/json", 400},
		{"large body", "POST", "/products", `{"sku":"A","name":"` + strings.Repeat("a", 1<<20) + `","price_satang":0}`, "application/json", 413},
	}
	// A nil store intentionally fails if validation ever calls the database.
	handler := newHandler(nil)
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			r := httptest.NewRequest(tt.method, tt.path, strings.NewReader(tt.body))
			r.Header.Set("Content-Type", tt.contentType)
			w := httptest.NewRecorder()
			handler.ServeHTTP(w, r)
			if w.Code != tt.want {
				t.Fatalf("status=%d want=%d body=%s", w.Code, tt.want, w.Body.String())
			}
		})
	}
}

func TestCreateFreeThaiProduct(t *testing.T) {
	r := httptest.NewRequest("POST", "/products", strings.NewReader(`{"sku":"GO-1","name":" หนังสือ Go ","price_satang":0}`))
	r.Header.Set("Content-Type", "application/json; charset=utf-8")
	w := httptest.NewRecorder()
	newHandler(fakeStore{}).ServeHTTP(w, r)
	if w.Code != 201 || w.Header().Get("Location") != "/products/1" ||
		!strings.Contains(w.Body.String(), `"name":"หนังสือ Go"`) {
		t.Fatalf("unexpected response: %d %s", w.Code, w.Body.String())
	}
}

func TestStoreErrors(t *testing.T) {
	for _, tt := range []struct {
		err error
		want int
	}{
		{sql.ErrNoRows, 404},
		{&mysql.MySQLError{Number: 1062, Message: "secret SQL"}, 409},
		{context.DeadlineExceeded, 504},
		{errors.New("secret SQL"), 500},
	} {
		w := httptest.NewRecorder()
		newHandler(fakeStore{err: tt.err}).ServeHTTP(w, httptest.NewRequest("GET", "/products/1", nil))
		if w.Code != tt.want || strings.Contains(w.Body.String(), "secret SQL") {
			t.Fatalf("unexpected response: %d %s", w.Code, w.Body.String())
		}
	}
}

func TestHealthDatabaseUnavailable(t *testing.T) {
	w := httptest.NewRecorder()
	newHandler(fakeStore{err: errors.New("offline")}).ServeHTTP(w, httptest.NewRequest("GET", "/health", nil))
	if w.Code != 503 {
		t.Fatalf("status=%d want=503", w.Code)
	}
}
