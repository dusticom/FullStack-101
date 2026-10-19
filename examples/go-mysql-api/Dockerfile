FROM golang:1.26-bookworm AS dev
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

FROM dev AS build
RUN CGO_ENABLED=0 go build -trimpath -o /api .

FROM debian:bookworm-slim AS runtime
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=build /api /usr/local/bin/api
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/api"]
