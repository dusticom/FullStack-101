package main

import (
	"context"
	"database/sql"
	"time"
)

type Product struct {
	ID         int64     `json:"id"`
	SKU        string    `json:"sku"`
	Name       string    `json:"name"`
	PriceSatang int64    `json:"price_satang"`
	CreatedAt  time.Time `json:"created_at"`
}

type ProductInput struct {
	SKU         string `json:"sku"`
	Name        string `json:"name"`
	PriceSatang int64  `json:"price_satang"`
}

// The HTTP layer depends on behavior, so tests can provide a fake store.
type productStore interface {
	Ping(context.Context) error
	List(context.Context, int, int) ([]Product, error)
	Get(context.Context, int64) (Product, error)
	Create(context.Context, ProductInput) (Product, error)
	Update(context.Context, int64, ProductInput) (Product, error)
	Delete(context.Context, int64) error
}

type mysqlStore struct{ db *sql.DB }

func (s *mysqlStore) Ping(ctx context.Context) error { return s.db.PingContext(ctx) }

func (s *mysqlStore) List(ctx context.Context, limit, offset int) ([]Product, error) {
	rows, err := s.db.QueryContext(ctx,
		`SELECT id, sku, name, price_satang, created_at FROM products ORDER BY id LIMIT ? OFFSET ?`,
		limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	products := make([]Product, 0) // Encode an empty collection as [], not null.
	for rows.Next() {
		var p Product
		if err := rows.Scan(&p.ID, &p.SKU, &p.Name, &p.PriceSatang, &p.CreatedAt); err != nil {
			return nil, err
		}
		products = append(products, p)
	}
	return products, rows.Err()
}

func (s *mysqlStore) Get(ctx context.Context, id int64) (Product, error) {
	var p Product
	err := s.db.QueryRowContext(ctx,
		`SELECT id, sku, name, price_satang, created_at FROM products WHERE id = ?`, id).
		Scan(&p.ID, &p.SKU, &p.Name, &p.PriceSatang, &p.CreatedAt)
	return p, err
}

func (s *mysqlStore) Create(ctx context.Context, input ProductInput) (Product, error) {
	result, err := s.db.ExecContext(ctx,
		`INSERT INTO products (sku, name, price_satang) VALUES (?, ?, ?)`,
		input.SKU, input.Name, input.PriceSatang)
	if err != nil {
		return Product{}, err
	}
	id, err := result.LastInsertId()
	if err != nil {
		return Product{}, err
	}
	return s.Get(ctx, id)
}

func (s *mysqlStore) Update(ctx context.Context, id int64, input ProductInput) (Product, error) {
	result, err := s.db.ExecContext(ctx,
		`UPDATE products SET sku = ?, name = ?, price_satang = ? WHERE id = ?`,
		input.SKU, input.Name, input.PriceSatang, id)
	if err != nil {
		return Product{}, err
	}
	if err := requireRow(result); err != nil {
		return Product{}, err
	}
	return s.Get(ctx, id)
}

func (s *mysqlStore) Delete(ctx context.Context, id int64) error {
	result, err := s.db.ExecContext(ctx, `DELETE FROM products WHERE id = ?`, id)
	if err != nil {
		return err
	}
	return requireRow(result)
}

func requireRow(result sql.Result) error {
	n, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if n == 0 {
		return sql.ErrNoRows
	}
	return nil
}

var _ productStore = (*mysqlStore)(nil)
