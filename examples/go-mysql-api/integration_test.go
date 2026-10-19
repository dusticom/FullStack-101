package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"
)

func TestMySQLCRUD(t *testing.T) {
	if os.Getenv("INTEGRATION_DB") != "1" {
		t.Skip("set INTEGRATION_DB=1 to test against the learning MySQL database")
	}
	ctx := context.Background()
	db, err := openDB(ctx)
	if err != nil {
		t.Fatal(err)
	}
	defer db.Close()
	sku := fmt.Sprintf("TEST-%d", time.Now().UnixNano())
	defer db.ExecContext(ctx, "DELETE FROM products WHERE sku = ?", sku)
	handler := newHandler(&mysqlStore{db: db})
	request := func(method, path, body string, want int) *httptest.ResponseRecorder {
		t.Helper()
		r := httptest.NewRequest(method, path, strings.NewReader(body))
		r.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()
		handler.ServeHTTP(w, r)
		if w.Code != want {
			t.Fatalf("%s %s: got %d want %d: %s", method, path, w.Code, want, w.Body.String())
		}
		return w
	}
	request("GET", "/health", "", 200)
	body := fmt.Sprintf(`{"sku":%q,"name":"หนังสือ Go","price_satang":25000}`, sku)
	w := request("POST", "/products", body, 201)
	var created struct{ Data Product `json:"data"` }
	if err := json.Unmarshal(w.Body.Bytes(), &created); err != nil {
		t.Fatal(err)
	}
	if created.Data.ID <= 0 || created.Data.CreatedAt.IsZero() || created.Data.PriceSatang != 25000 || created.Data.Name != "หนังสือ Go" {
		t.Fatalf("bad stored product: %+v", created.Data)
	}
	path := fmt.Sprintf("/products/%d", created.Data.ID)
	request("POST", "/products", body, 409)
	request("GET", path, "", 200)
	request("PUT", path, body, 200) // Unchanged UPDATE must not become 404.
	updated := fmt.Sprintf(`{"sku":%q,"name":"Go ฉบับใหม่","price_satang":0}`, sku)
	request("PUT", path, updated, 200)
	w = request("GET", path, "", 200)
	if !strings.Contains(w.Body.String(), `"price_satang":0`) || !strings.Contains(w.Body.String(), "Go ฉบับใหม่") {
		t.Fatalf("update not persisted: %s", w.Body.String())
	}
	request("GET", "/products?limit=1&offset=0", "", 200)
	w = request("GET", "/products?limit=1&offset=1000000", "", 200)
	if !strings.Contains(w.Body.String(), `"data":[]`) {
		t.Fatalf("empty page must be []: %s", w.Body.String())
	}
	w = request("DELETE", path, "", 204)
	if w.Body.Len() != 0 {
		t.Fatal("204 must have no body")
	}
	request("GET", path, "", 404)
	request("DELETE", path, "", 404)
	request("PUT", path, body, 404)

	// Verify that a rolled-back insert is never visible after the transaction.
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		t.Fatal(err)
	}
	defer tx.Rollback()
	if _, err := tx.ExecContext(ctx, "INSERT INTO products (sku, name, price_satang) VALUES (?, ?, ?)", sku, "Rollback", 0); err != nil {
		t.Fatal(err)
	}
	if err := tx.Rollback(); err != nil {
		t.Fatal(err)
	}
	var count int
	if err := db.QueryRowContext(ctx, "SELECT COUNT(*) FROM products WHERE sku = ?", sku).Scan(&count); err != nil || count != 0 {
		t.Fatalf("rollback failed: count=%d err=%v", count, err)
	}
}
