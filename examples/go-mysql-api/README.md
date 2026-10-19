# Go + MySQL: Product REST API

โปรเจกต์ประกอบ [บทเรียน Go](../../golang-teaching.html) ใช้ Go 1.26+, standard library `net/http`, `database/sql` และ MySQL 8.4 ไม่มี ORM เพื่อให้เห็น SQL และการจัดการ error โดยตรง

## เริ่มด้วย Docker (ไม่จำเป็นต้องติดตั้ง Go บนเครื่อง)

เปิด terminal ในโฟลเดอร์นี้ ต้องติดตั้ง Docker พร้อม Compose และเปิด Docker Engine ก่อน

```powershell
Copy-Item .env.example .env
```

macOS / Linux ใช้ `cp .env.example .env` แทน จากนั้นแก้รหัสผ่านทั้งสองค่าใน `.env` แล้วรัน:

```sh
docker compose up -d --build --wait
docker compose logs api
curl -i http://localhost:8080/health
```

PowerShell รุ่นเก่าที่ `curl` เป็น alias ให้ใช้ `curl.exe` หรือ `Invoke-RestMethod` ตัวอย่าง:

```powershell
$body = @{ sku = 'GO-BOOK-01'; name = 'หนังสือ Go'; price_satang = 25000 } | ConvertTo-Json
$created = Invoke-RestMethod -Method Post -Uri http://localhost:8080/products -ContentType 'application/json; charset=utf-8' -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
$productId = $created.data.id
Invoke-RestMethod "http://localhost:8080/products/$productId"
Invoke-RestMethod 'http://localhost:8080/products?limit=20&offset=0'
$body = @{ sku = 'GO-BOOK-01'; name = 'หนังสือ Go ฉบับใหม่'; price_satang = 29000 } | ConvertTo-Json
Invoke-RestMethod -Method Put -Uri "http://localhost:8080/products/$productId" -ContentType 'application/json; charset=utf-8' -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
Invoke-RestMethod -Method Delete -Uri "http://localhost:8080/products/$productId"
```

หรือเปิด `requests.http` ด้วย VS Code REST Client แล้วส่ง request ทีละรายการ โดยแก้ ID ให้ตรงกับผล POST ใช้ SKU ใหม่หากสร้างซ้ำ

| Method | Path | ผลสำเร็จ |
| --- | --- | --- |
| GET | `/health` | 200 เมื่อ ping DB ได้, 503 เมื่อไม่ได้ |
| GET | `/products?limit=20&offset=0` | 200 พร้อม `data`, `limit`, `offset` |
| GET | `/products/{id}` | 200 พร้อม `data` |
| POST | `/products` | 201 พร้อม `data` และ `Location` |
| PUT | `/products/{id}` | 200 พร้อม `data` ต้องส่งครบทั้งสามฟิลด์ |
| DELETE | `/products/{id}` | 204 ไม่มี body |

Body ของ POST/PUT: `{"sku":"GO-1","name":"หนังสือ Go","price_satang":25000}`

SKU ใช้ A-Z, 0-9, ขีดกลาง 1–40 ตัวและห้ามซ้ำ ชื่อ trim ช่องว่างแล้วต้องมี 1–120 Unicode code points ราคา 0–1,000,000,000,000 สตางค์เป็นจำนวนเต็ม ไม่รับฟิลด์เกิน, null หรือ JSON หลายก้อน Body จำกัด 1 MiB

Error ใน handler มีรูปแบบ `{"error":"..."}`: 400 input ผิด, 404 ไม่มีสินค้า, 409 SKU ซ้ำ, 413 body ใหญ่, 415 content type ผิด, 500 ข้อผิดพลาดภายใน, 504 context หมดเวลา ส่วน route ที่ไม่พบและ method ที่ไม่รองรับใช้ response มาตรฐานของ `net/http` (404/405 แบบข้อความ)

## รัน Go บนเครื่องและใช้ MySQL ใน Docker

ติดตั้ง Go 1.26+ จาก https://go.dev/doc/install แล้วรันเฉพาะฐานข้อมูล:

```sh
docker compose up -d --wait db
go mod download
```

PowerShell ตั้งค่าแยกจาก `.env` เพราะ Go ไม่โหลดไฟล์นี้อัตโนมัติ:

```powershell
$env:DB_HOST = '127.0.0.1'
$env:DB_PORT = '3307'
$env:DB_USER = 'learner'
$env:DB_NAME = 'go_course'
$env:DB_PASSWORD = 'รหัสเดียวกับ MYSQL_PASSWORD ใน .env'
go run .
```

macOS / Linux:

```sh
export DB_HOST=127.0.0.1 DB_PORT=3307 DB_USER=learner DB_NAME=go_course
export DB_PASSWORD='รหัสเดียวกับ MYSQL_PASSWORD ใน .env'
go run .
```

ถ้าเปลี่ยน `MYSQL_PORT` ให้เปลี่ยน `DB_PORT` ตามด้วย API บนเครื่อง bind `127.0.0.1:8080`; ใน container ใช้ `HTTP_ADDR=:8080` ส่วน DB host ภายใน Compose คือ `db:3306` ไม่ใช่ `localhost:3307`

กรณีใช้ MySQL ที่ติดตั้งเอง: สร้าง database `go_course` (utf8mb4), รัน `schema.sql`, สร้าง user สำหรับแอปและให้สิทธิ์ SELECT/INSERT/UPDATE/DELETE เฉพาะ database นี้ ตั้ง `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` ให้ตรง ระบบจริงใช้ TLS โดยตั้ง `DB_TLS=true` และใบรับรองที่ตรวจสอบได้

## ทดสอบ

```sh
go test ./...
go vet ./...
```

คำสั่งแรกทดสอบ handler โดยไม่ใช้ DB และ skip integration test หากไม่ได้ตั้ง `INTEGRATION_DB=1` ส่วนการทดสอบกับ MySQL จริงผ่าน Compose:

```sh
docker compose --profile test run --build --rm test
```

ตรวจ CRUD, ภาษาไทย, duplicate SKU, unchanged UPDATE, pagination, DELETE และ rollback พร้อม race detector โดยสร้าง/ลบเฉพาะ record ของ test ใช้ฐานข้อมูลสำหรับฝึกเท่านั้น หากรันบนเครื่องหลังตั้ง DB variables แล้ว ใช้ `$env:INTEGRATION_DB='1'; go test -race -count=1 ./...` (race detector บน Windows ต้องมี C compiler ที่รองรับ) หรือใช้คำสั่ง Compose ด้านบน

## โครงสร้างและสิ่งที่ต้องเข้าใจ

- `main.go`: lifecycle, HTTP timeouts และ graceful shutdown
- `db.go`: configuration, connection pool, startup ping และ MySQL driver
- `store.go`: model, interface และ SQL CRUD; `ClientFoundRows=true` ป้องกัน UPDATE ค่าเดิมถูกตีความว่าไม่มีแถว
- `api.go`: routing, middleware, validation และ HTTP error mapping
- `schema.sql`: table, unique constraint และ check constraint
- `api_test.go`: validation และ error responses โดยใช้ fake store
- `integration_test.go`: handler + MySQL จริง

`sql.DB` เป็น pool ใช้ร่วมกัน ไม่เปิด/ปิดทุก request; `parseTime` แปลงวันที่เป็น `time.Time` และกำหนดทั้ง Go location และ MySQL session เป็น UTC คำสั่ง Query ใช้ `?` parameters เสมอ

## แก้ปัญหาและหยุดระบบ

- Port ชน: เปลี่ยน `API_PORT` หรือ `MYSQL_PORT` ใน `.env` แล้วรัน `docker compose up -d` ใหม่
- DB ยังไม่พร้อม: `docker compose ps` และ `docker compose logs db` การรันครั้งแรกใช้เวลาสร้างฐานข้อมูล
- Access denied หลังแก้ `.env`: user/password ถูกสร้างเมื่อ data volume ว่างครั้งแรก การเปลี่ยน environment ไม่เปลี่ยนบัญชีเดิม ให้ใช้รหัสเดิมหรือแก้บัญชีใน MySQL
- Table ไม่มี: init SQL รันเฉพาะ volume ใหม่ ตรวจ schema ด้วย `docker compose exec db mysql -u learner -p go_course` และใช้ `SOURCE /docker-entrypoint-initdb.d/001-schema.sql;` สำหรับฐานข้อมูลฝึกเดิมที่ยังไม่มีตาราง (ไม่ใช่ migration สำหรับแก้ schema เดิม)
- `docker compose down` หยุดและลบ container/network แต่เก็บข้อมูลใน named volume ไว้ คำสั่ง `docker compose down -v` จะลบข้อมูลฝึกทั้งหมดใน volume ของ Compose project นี้ ใช้เมื่อยอมรับการสูญเสียข้อมูลแล้วเท่านั้น

นี่เป็นระบบฝึกบน localhost ยังไม่มี authentication/authorization ก่อนใช้จริงให้เพิ่มการตรวจสิทธิ์, secrets management, TLS, migration tooling, monitoring และนโยบายสำรองข้อมูล การ retry POST หลัง timeout อาจสร้างซ้ำได้ ควรออกแบบ idempotency สำหรับงานที่ต้องรับประกันผล

อ้างอิง: [Go database guide](https://go.dev/doc/database/), [net/http](https://pkg.go.dev/net/http), [MySQL driver v1.9.3](https://github.com/go-sql-driver/mysql/tree/v1.9.3), [MySQL image](https://github.com/docker-library/docs/tree/master/mysql)
