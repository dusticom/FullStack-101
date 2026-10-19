"""Regenerate the standalone Thai Go lesson and its downloadable example (stdlib only)."""
from pathlib import Path
from html import escape
import textwrap
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples' / 'go-mysql-api'
chapters = []


def code(source, label='Go'):
    source = textwrap.dedent(source).strip('\n')
    return f'<div class="code"><div class="code-top"><span>{escape(label)}</span><button class="copy" type="button">คัดลอก</button></div><pre><code>{escape(source)}</code></pre></div>'


def card(title, body):
    return f'<article class="card"><h3>{title}</h3>{body}</article>'


def note(body):
    return f'<aside class="note">{body}</aside>'


def table(headers, rows):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join(f'<th scope="col">{x}</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def chapter(anchor, title, summary, body):
    n = len(chapters) + 1
    chapters.append((anchor, title, f'<section id="{anchor}" aria-labelledby="{anchor}-title"><div class="chapter-heading"><span class="chapter-num">{n:02}</span><div><h2 id="{anchor}-title">{title}</h2><p>{summary}</p></div></div>{body}</section>'))


chapter('roadmap', 'เส้นทางจาก Syntax สู่ API', 'รู้ว่าจะเรียนอะไร และทำอะไรได้เมื่อจบแต่ละช่วง',
card('เป้าหมายของคอร์ส', '''<p>Go (มักเรียกว่า Golang) เป็นภาษาที่มีชนิดข้อมูลชัดเจนและคอมไพล์เป็น executable เหมาะกับงาน backend และบริการเครือข่าย คอร์สนี้พาเขียนภาษาให้เข้าใจก่อน แล้วนำไปสร้าง <strong>Product REST API ที่เก็บข้อมูลใน MySQL จริง</strong> ใช้ standard library เป็นหลักและเพิ่ม MySQL driver เพียงตัวเดียว</p><p>ควรรู้การใช้ terminal, ไฟล์และโฟลเดอร์ และแนวคิดตัวแปร/เงื่อนไขเบื้องต้น หากยังไม่เคยเขียนโปรแกรม ให้อ่านตัวอย่างพร้อมผลลัพธ์และทำแบบฝึกหัดทีละบท ไม่จำเป็นต้องรู้ framework มาก่อน</p>''') +
table(['ช่วง', 'เนื้อหา', 'ผลงาน / เวลาฝึกโดยประมาณ'], [
('พื้นฐาน • บท 2–6', 'ติดตั้ง, ตัวแปร, flow, collections, functions', 'โปรแกรมคำนวณตะกร้าสินค้า • 4–6 ชม.'),
('ออกแบบภาษา • บท 7–12', 'struct, interface, error, module, concurrency, test', 'แยกโค้ดเป็น package และทดสอบได้ • 5–7 ชม.'),
('สร้าง backend • บท 13–19', 'HTTP, REST, MySQL, pool, CRUD, validation', 'Product API ครบ Create/Read/Update/Delete • 6–8 ชม.'),
('นำไปใช้ • บท 20–24', 'transaction, รันระบบ, ทดสอบ, debugging, capstone', 'ตรวจความถูกต้องและต่อยอดเอง • 4–6 ชม.')]) +
note('เวลานี้เป็นเพียงแนวทางสำหรับผู้เรียนที่เคยเขียนโปรแกรม แนะนำแบ่งเป็น 4–6 ครั้งเรียนและเผื่อเวลาลองผิดลองถูก โค้ดบล็อกที่ระบุว่า “ส่วนหนึ่งของฟังก์ชัน” ต้องวางในฟังก์ชัน ไม่ใช่นำแต่ละบล็อกมาต่อเป็นไฟล์เดียว'))

chapter('setup', 'ติดตั้ง Go และรันโปรแกรมแรก', 'เข้าใจ package main, import, func main และวงจร run → format → build',
card('เตรียมเครื่อง', '''<ol><li>ติดตั้ง <a href="https://go.dev/doc/install">Go จากเว็บไซต์ทางการ</a> คอร์สและตัวอย่างกำหนดฐานเป็น <strong>Go 1.26+</strong> เลือก patch ที่ยังได้รับการแก้ไขความปลอดภัยของสายรุ่นที่ใช้งาน ไม่จำเป็นต้องตรง patch กับผู้สอน</li><li>ติดตั้ง editor เช่น VS Code พร้อม Go extension แล้วเปิด terminal ใหม่หลังติดตั้ง</li><li>ช่วง API ใช้ MySQL 8.4 ผ่าน Docker Compose หรือ MySQL ที่ติดตั้งเอง หากใช้ Docker ทั้งชุดไม่ต้องติดตั้ง Go บนเครื่อง</li></ol>''' + code('''go version
go env GOPATH GOMOD
mkdir hello-go
cd hello-go
go mod init example.com/hello-go''', 'Terminal • ใช้ได้ทั้ง PowerShell / Bash')) +
card('สร้าง main.go', code('''package main

import "fmt"

func main() {
    fmt.Println("สวัสดี Go")
}''', 'main.go • โปรแกรมสมบูรณ์') + '''<ul><li><code>package main</code> บอกว่า package นี้ใช้สร้างโปรแกรมที่รันได้</li><li><code>import "fmt"</code> นำ package สำหรับจัดรูปแบบข้อความมาใช้</li><li><code>func main()</code> คือจุดเริ่มทำงาน ไม่รับ argument และไม่คืนค่า</li><li>วงเล็บปีกกาเปิดวางบรรทัดเดียวกับ <code>func</code> โดยปกติไม่ใส่ semicolon เอง ใช้ <code>//</code> สำหรับ comment หนึ่งบรรทัด และ <code>/* ... */</code> สำหรับหลายบรรทัด</li></ul>''' + code('''go run .
# ผลลัพธ์: สวัสดี Go
go fmt ./...
go build -o hello .''', 'Terminal') + '''<p><code>go run</code> คอมไพล์และรันเพื่อทดลอง ส่วน <code>go build</code> สร้าง executable: Windows ใช้ <code>go build -o hello.exe .</code> แล้วรัน <code>.\\hello.exe</code>; macOS/Linux รัน <code>./hello</code> ไม่ต้องมี Go บนเครื่องปลายทางหาก build ให้ตรง OS/architecture และมี runtime dependencies ครบ</p>''') +
note('ในบทพื้นฐานให้ทำงานใน hello-go ส่วนโปรเจกต์ API อยู่คนละโฟลเดอร์และมี go.mod ของตัวเอง หากขึ้น “go.mod file not found” ให้ตรวจว่ากำลังอยู่ในโฟลเดอร์ module ที่ถูกต้อง'))

chapter('variables', 'ตัวแปร ชนิดข้อมูล และ String', 'เลือกชนิดข้อมูลให้เหมาะ และระวังความต่างระหว่าง byte กับตัวอักษร',
card('var, :=, const และ zero value', code('''var name string = "Mali"
age := 20                 // := ใช้ได้ภายในฟังก์ชันเท่านั้น
var active bool           // false
var count int             // 0
var description string    // ""
const vatRate = 0.07

age = 21                  // เปลี่ยนค่าด้วย =
fmt.Printf("%s อายุ %d active=%t\\n", name, age, active)
fmt.Println(count, description, vatRate)''', 'ส่วนหนึ่งของ func main • import fmt') + '''<p><code>:=</code> ให้ compiler อนุมานชนิดข้อมูล และต้องมีตัวแปรใหม่อย่างน้อยหนึ่งตัวใน scope เดียวกัน ห้ามประกาศซ้ำด้วย <code>age := 21</code> ใน scope เดิมโดยไม่มีตัวแปรใหม่ ตัวแปร local และ import ที่ประกาศแต่ไม่ใช้ทำให้ compile ไม่ผ่าน</p>''') +
table(['ชนิด', 'ใช้เมื่อ', 'ข้อควรระวัง'], [('int / int64','จำนวนเต็มทั่วไป / ID และจำนวนเงินใน API','int ขนาดขึ้นกับสถาปัตยกรรม; int64 กำหนดขนาดแน่นอน'), ('float64','ค่าทศนิยมในการคำนวณทั่วไป','ไม่เหมาะกับการเก็บจำนวนเงินที่ต้องตรงทุกสตางค์'), ('bool','true / false','ไม่แปลงเลข 0 หรือ string เป็น bool อัตโนมัติ'), ('string','ข้อความ UTF-8 ที่แก้ byte เดิมโดยตรงไม่ได้','len(s) นับ byte; range วน rune'), ('byte / rune','alias ของ uint8 / int32','byte ใช้ข้อมูลไบนารี; rune แทน Unicode code point')]) +
card('แปลงชนิดและทำงานกับข้อความ', code('''package main

import (
    "fmt"
    "strconv"
    "strings"
    "unicode/utf8"
)

func main() {
    n, err := strconv.Atoi("42")
    if err != nil {
        fmt.Println("ไม่ใช่จำนวนเต็ม:", err)
        return
    }
    text := "Goไทย"
    fmt.Println(n + 1)                         // 43
    fmt.Println(len(text))                     // 11 bytes
    fmt.Println(utf8.RuneCountInString(text))   // 5 code points
    fmt.Println(strings.TrimSpace(" Go "))     // Go
    fmt.Println(float64(5) / 2)                // 2.5
    fmt.Println(5 / 2)                         // 2 (หารจำนวนเต็ม)
}''', 'main.go • แทนเนื้อหาไฟล์เดิมแล้ว go run .') + '''<p>การ cast เป็น <code>string(65)</code> ได้อักขระ “A” ไม่ใช่ “65” ถ้าต้องการเลขในรูปข้อความใช้ <code>strconv.Itoa(65)</code> จำนวน rune ก็ยังไม่เท่ากับจำนวนตัวอักษรที่ตามองเห็นเสมอ เช่น อักษรไทยที่มีวรรณยุกต์ประกอบ</p>'''))

chapter('control', 'Operators, if, switch และ for', 'เขียนเงื่อนไขและทำซ้ำโดยไม่ซ่อนเส้นทางของโปรแกรม',
card('เงื่อนไขและตัวดำเนินการ', '''<p>คณิตศาสตร์ใช้ <code>+ - * / %</code> เปรียบเทียบใช้ <code>== != &lt; &lt;= &gt; &gt;=</code> และตรรกะใช้ <code>&amp;&amp; || !</code> การเปรียบเทียบต้องใช้ชนิดข้อมูลที่เข้ากันได้ ไม่มีการแปลงชนิดให้อัตโนมัติแบบบางภาษา</p>''' + code('''score := 82
if score >= 80 {
    fmt.Println("A")
} else if score >= 70 {
    fmt.Println("B")
} else {
    fmt.Println("ลองใหม่")
}

switch day := "Monday"; day {
case "Saturday", "Sunday":
    fmt.Println("วันหยุด")
default:
    fmt.Println("วันทำงาน")
}''', 'ส่วนหนึ่งของ func main • import fmt') + '''<p><code>switch</code> ไม่ไหลต่อไป case ถัดไปโดยอัตโนมัติจึงไม่ต้องใส่ break ทุก case ตัวแปรที่ประกาศใน <code>if</code> หรือ <code>switch</code> initializer ใช้ได้เฉพาะ scope ของคำสั่งนั้น</p>''') +
card('Go มีคำสั่งวนซ้ำหลักคือ for', code('''for i := 0; i < 3; i++ {
    fmt.Println(i) // 0, 1, 2
}

remaining := 2
for remaining > 0 { // รูปแบบเดียวกับ while
    remaining--
}

for _, name := range []string{"Mali", "Somchai"} {
    if name == "Mali" {
        continue
    }
    fmt.Println(name) // Somchai
}

for { // วนไม่สิ้นสุดจนกว่าจะ break / return
    break
}''', 'ส่วนหนึ่งของ func main • import fmt') + note('<code>i++</code> เป็น statement ไม่ใช่ expression จึงเขียน <code>x := i++</code> ไม่ได้ แบบฝึก: รับคะแนน 0–100 แล้วให้เกรด A/B/C/F และลองกรณี -1, 0, 79, 80, 100, 101')))

chapter('collections', 'Array, Slice และ Map', 'เก็บข้อมูลหลายรายการ และเข้าใจการแชร์ backing array',
card('Array มีขนาดตายตัว ส่วน Slice ยืดหยุ่น', code('''fixed := [3]int{10, 20, 30}
prices := []int{100, 200}
prices = append(prices, 300)
fmt.Println(fixed[0], len(prices), prices[1:]) // 10 3 [200 300]

original := []int{1, 2, 3}
view := original[:2]
view[0] = 99
fmt.Println(original) // [99 2 3] เพราะแชร์ backing array

cloned := make([]int, len(original))
copy(cloned, original)
cloned[0] = 0
fmt.Println(original[0]) // ยังเป็น 99

var empty []int // nil slice; len=0; append ได้
empty = append(empty, 7)
fmt.Println(empty)''', 'ส่วนหนึ่งของ func main • import fmt') + '''<p><code>len</code> คือจำนวนสมาชิกที่เข้าถึงได้ ส่วน <code>cap</code> คือความจุของ backing array นับจากจุดเริ่ม slice นั้น <code>append</code> อาจสร้าง array ใหม่ จึงต้องรับค่าที่คืนกลับเสมอ เข้าถึง index เกินขอบเขตทำให้ panic; การ copy slice เป็น shallow copy ถ้าสมาชิกเป็น pointer ก็ยังชี้ object เดิม</p>''') +
card('Map และ comma-ok', code('''stock := map[string]int{"GO-1": 5}
stock["GO-2"] = 0

quantity, exists := stock["GO-2"]
fmt.Println(quantity, exists) // 0 true: มีสินค้า แต่หมด stock
quantity, exists = stock["MISSING"]
fmt.Println(quantity, exists) // 0 false: ไม่มี key

delete(stock, "GO-1")
for sku, n := range stock {
    fmt.Println(sku, n)
}

var counts map[string]int
counts = make(map[string]int) // ต้องสร้างก่อนเขียน; อ่าน nil map ได้
counts["views"]++''', 'ส่วนหนึ่งของ func main • import fmt') + note('ลำดับการวน map ไม่แน่นอน และ map ปกติไม่ปลอดภัยสำหรับการอ่าน/เขียนพร้อมกันจากหลาย goroutine หากต้องเรียงผลลัพธ์ให้รวบรวม key และ sort หรือเรียงใน SQL ด้วย ORDER BY แบบฝึก: รวมราคาจาก slice และนับจำนวน SKU ด้วย map')))

chapter('functions', 'Function, Multiple Return และ Closure', 'แยกงานเป็นฟังก์ชันเล็ก และคืน error อย่างชัดเจน',
card('Parameters และผลลัพธ์หลายค่า', code('''package main

import (
    "fmt"
    "errors"
)

func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("cannot divide by zero")
    }
    return a / b, nil
}

func sum(values ...int) int {
    total := 0
    for _, n := range values {
        total += n
    }
    return total
}

func main() {
    result, err := divide(10, 2)
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Println(result)                 // 5
    fmt.Println(sum(1, 2, 3))           // 6
    fmt.Println(sum([]int{4, 5}...))    // 9
}''', 'main.go • โปรแกรมสมบูรณ์') + '''<p>Go ส่ง argument แบบ value: ฟังก์ชันได้รับสำเนาค่า แต่ค่าของ slice/map/pointer อาจยังอ้างถึงข้อมูลภายในชุดเดียวกัน รูปแบบ <code>(value, error)</code> ทำให้ผู้เรียกต้องตัดสินใจเมื่อทำงานไม่สำเร็จ ไม่ควรทิ้ง error ด้วย <code>_</code> โดยไม่มีเหตุผล</p>''') +
card('ฟังก์ชันเป็นค่าและสร้าง closure ได้', code('''func counter() func() int {
    n := 0
    return func() int {
        n++
        return n
    }
}

// ภายใน main:
// next := counter()
// fmt.Println(next(), next()) // 1 2''', 'ประกาศนอก main • closure จดจำตัวแปร n') + '''<p>Closure มีประโยชน์กับ callback และ middleware แต่ถ้าใช้ closure เดียวกันพร้อมกันหลาย goroutine ต้องป้องกันการเข้าถึง state เช่น n เอง แบบฝึก: เขียน <code>totalWithDiscount(prices []int64, discount int64) (int64, error)</code> โดยไม่ให้ส่วนลดติดลบหรือเกินยอดรวม</p>'''))

chapter('structs', 'Pointer, Struct, Method และ JSON', 'สร้าง model ที่ใช้ต่อได้ตั้งแต่ business logic ไปจนถึง HTTP response',
card('Pointer ชี้ไปยังค่าที่ต้องการเปลี่ยน', code('''type Product struct {
    ID          int64  `json:"id"`
    Name        string `json:"name"`
    PriceSatang int64  `json:"price_satang"`
}

func (p *Product) Rename(name string) {
    p.Name = name
}

func (p Product) PriceBaht() float64 {
    return float64(p.PriceSatang) / 100
}

// ภายใน main:
// p := Product{ID: 1, Name: "Go", PriceSatang: 25000}
// ptr := &p
// ptr.Rename("Go Book")
// fmt.Println(p.Name, p.PriceBaht()) // Go Book 250
// fmt.Println((*ptr).ID)            // 1; เขียน ptr.ID ได้เช่นกัน''', 'ประกาศ type/method นอก main') + '''<p><code>&amp;x</code> คือ address ของ x และ <code>*ptr</code> คือค่าที่ pointer ชี้อยู่ Receiver แบบ <code>*Product</code> เปลี่ยน object เดิมได้ ส่วน receiver แบบ <code>Product</code> ได้สำเนา struct ใช้ pointer receiver เมื่อแก้ state หรือไม่ต้องการ copy struct ใหญ่ Pointer ที่ยังไม่กำหนดค่าเป็น nil และ dereference nil จะ panic</p><p>Go ไม่มี class/inheritance แบบบางภาษา ใช้ struct, method และ composition แทน Field และชื่อฟังก์ชันที่ขึ้นต้นตัวพิมพ์ใหญ่เป็น exported; ตัวพิมพ์เล็กเข้าถึงได้ภายใน package</p>''') +
card('JSON tag เปลี่ยนชื่อ field ที่สื่อสารกับ client', code('''p := Product{ID: 1, Name: "หนังสือ Go", PriceSatang: 25000}
data, err := json.Marshal(p)
if err != nil {
    return // ในโปรแกรมจริงส่งต่อหรือจัดการ error ให้เหมาะสม
}
fmt.Println(string(data))
// {"id":1,"name":"หนังสือ Go","price_satang":25000}

var decoded Product
if err := json.Unmarshal(data, &decoded); err != nil {
    return
}''', 'ส่วนหนึ่งของฟังก์ชัน • import encoding/json และ fmt') + note('encoding/json อ่าน/เขียน exported fields เท่านั้น ต้องส่ง pointer ให้ Unmarshal เพื่อแก้ค่าปลายทาง nil slice encode เป็น null; slice ว่างที่สร้างแล้ว encode เป็น [] สำหรับราคาเก็บ int64 หน่วยสตางค์: 25000 = 250.00 บาท ไม่ใช้ float64 เก็บเงินใน API นี้')))

chapter('interfaces', 'Interface, Composition และ Generics', 'แยกสิ่งที่ต้องทำออกจากวิธีทำ เพื่อเปลี่ยนฐานข้อมูลและทดสอบได้',
card('Interface ระบุพฤติกรรม', code('''type Notifier interface {
    Send(message string) error
}

type ConsoleNotifier struct{}

func (ConsoleNotifier) Send(message string) error {
    fmt.Println(message)
    return nil
}

func welcome(n Notifier) error {
    return n.Send("Welcome to Go")
}

// ภายใน main: if err := welcome(ConsoleNotifier{}); err != nil { ... }''', 'ประกาศนอก main • import fmt • ... ใน comment คือจุดให้จัดการ error') + '''<p>ชนิดที่มี method ครบจะ implement interface โดยอัตโนมัติ ไม่ต้องเขียน implements แนะนำเริ่มจาก interface ขนาดเล็กฝั่งผู้ใช้งาน ใน API handler ต้องการแค่พฤติกรรม List/Get/Create จึงไม่ต้องรู้วิธีเชื่อม MySQL และสามารถใช้ fake ใน test ได้</p><p><code>any</code> เป็น alias ของ <code>interface{}</code> ใช้รับค่าได้ทุกชนิด แต่เสียการตรวจชนิดเฉพาะเจาะจง หากต้องตรวจ runtime ใช้ <code>value, ok := x.(string)</code> และตรวจ ok อย่าละเลย กรณี interface เก็บ typed nil pointer ตัว interface อาจไม่เท่ากับ nil</p>''') +
card('Generics ลดการเขียนฟังก์ชันซ้ำตามชนิดข้อมูล', code('''func First[T any](values []T) (T, bool) {
    if len(values) == 0 {
        var zero T
        return zero, false
    }
    return values[0], true
}

// ภายใน main:
// name, ok := First([]string{"Go", "MySQL"})
// fmt.Println(name, ok) // Go true''', 'ประกาศ generic function นอก main') + '''<p><code>T</code> เป็น type parameter, <code>any</code> คือ constraint ที่อนุญาตทุกชนิด ถ้าต้องใช้ค่าเป็น key ของ map ต้องใช้ constraint <code>comparable</code> แทน ไม่จำเป็นต้องใช้ generics ทุกจุด เริ่มด้วย concrete type แล้วเพิ่มเมื่อมีความซ้ำที่ชัดเจน</p>'''))

chapter('errors', 'Error, defer และ Resource Lifecycle', 'จัดการความล้มเหลวโดยไม่ทำให้ทั้ง API หยุด',
card('ห่อ error โดยยังตรวจสาเหตุเดิมได้', code('''var ErrNotFound = errors.New("not found")

func loadProduct(id int64) error {
    return fmt.Errorf("load product %d: %w", id, ErrNotFound)
}

// ภายในฟังก์ชันที่เรียก:
// err := loadProduct(10)
// if errors.Is(err, ErrNotFound) { /* ส่ง 404 */ }''', 'ประกาศนอก main • import errors และ fmt') + '''<p>ใช้ <code>%w</code> เมื่อต้องการ wrap; <code>errors.Is</code> ตรวจ sentinel ผ่าน error chain และ <code>errors.As</code> ดึง concrete error เช่น <code>*mysql.MySQLError</code> เพื่อเช็คเลข 1062 ของ duplicate key อย่าเทียบข้อความ error เพราะข้อความเปลี่ยนได้</p>''') +
card('defer ทำงานเมื่อฟังก์ชันจบ และเรียงย้อนลำดับ', code('''func showOrder() {
    defer fmt.Println("A")
    defer fmt.Println("B")
    fmt.Println("C")
}
// showOrder() แสดง C, B, A

func readConfig(path string) ([]byte, error) {
    file, err := os.Open(path)
    if err != nil {
        return nil, fmt.Errorf("open config: %w", err)
    }
    defer file.Close() // ตัวอย่างไฟล์อ่านอย่างเดียว
    return io.ReadAll(file)
}''', 'ประกาศนอก main • import fmt, os, io') + '''<p>วาง defer หลังตรวจว่าเปิด resource สำเร็จ เช่น rows.Close, file.Close, cancel, tx.Rollback ค่าของ argument ใน defer ถูกประเมินตอนลงทะเบียน ไม่ใช่ตอนรัน และ defer ใน loop จะรอจนฟังก์ชันทั้งหมดจบ อาจถือ resource นานเกินไป</p>''' + note('<code>panic</code> เหมาะกับความผิดปกติที่ไม่ควรเกิด ไม่ใช้แทน error สำหรับ JSON ผิดหรือหา row ไม่พบ <code>recover</code> ใช้ได้ภายใน deferred function ของ goroutine ที่ panic เท่านั้น และ <code>os.Exit</code> ไม่รัน defer โค้ด API จึงปิด resource ใน run() ก่อนให้ main ออกด้วย exit code')))

chapter('packages', 'Module, Package และโครงสร้างโปรเจกต์', 'เข้าใจ go.mod, go.sum และวิธีเรียกใช้ package ของตัวเอง',
card('Module ไม่ใช่สิ่งเดียวกับ Package', '''<p>Module คือกลุ่ม package ที่มี <code>go.mod</code> เป็นขอบเขต dependency ส่วน package มักตรงกับหนึ่งโฟลเดอร์ ไฟล์ .go ปกติในโฟลเดอร์เดียวกันต้องใช้ package เดียวกัน (test อาจใช้ package ที่ลงท้าย _test) ชื่อ module ในคอร์สใช้ example.com เป็นชื่อสาธิต ไม่ต้องมีเว็บไซต์จริงเพื่อรันในเครื่อง</p>''' + code('''hello-go/
  go.mod                   # module example.com/hello-go
  main.go                  # package main
  internal/money/money.go  # package money''', 'โครงสร้างตัวอย่าง') + code('''package money

func BahtToSatang(baht int64) int64 {
    return baht * 100
}''', 'internal/money/money.go') + code('''package main

import (
    "fmt"
    "example.com/hello-go/internal/money"
)

func main() {
    fmt.Println(money.BahtToSatang(250)) // 25000
}''', 'main.go') + code('''go mod tidy
go fmt ./...
go vet ./...
go test ./...
go build ./...''', 'Terminal') + '''<p><code>go.mod</code> ระบุ module, Go version และ dependencies ส่วน <code>go.sum</code> เก็บ checksums สำหรับตรวจสอบเนื้อหา dependency ควรเก็บทั้งคู่ใน version control <code>go mod tidy</code> เพิ่มของที่ใช้และลบของที่ไม่ใช้ ไม่ควรแก้ go.sum เอง โฟลเดอร์ internal จำกัดการ import ตามขอบเขต parent ที่ Go กำหนด</p>''') + note('โปรเจกต์ API นี้เริ่มจาก package main เดียวแยกไฟล์ตามหน้าที่เพื่อให้อ่านง่าย เมื่อใหญ่ขึ้นค่อยแยก cmd/api, internal/config, internal/product และ internal/database ไม่ต้องสร้างหลายชั้นโดยที่ยังไม่มีหน้าที่ต่างกัน'))

chapter('concurrency', 'Goroutine, Channel และ Context', 'ทำงานพร้อมกันอย่างมีขอบเขต และหยุดงานที่ไม่ต้องการแล้ว',
card('ส่งค่าผ่าน channel และรอให้ worker จบ', code('''package main

import (
    "fmt"
    "sync"
)

func main() {
    results := make(chan int)
    var wg sync.WaitGroup
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()
            results <- n * n
        }(i)
    }
    go func() {
        wg.Wait()
        close(results)
    }()
    for result := range results {
        fmt.Println(result) // 1, 4, 9 แต่ลำดับไม่แน่นอน
    }
}''', 'main.go • โปรแกรมสมบูรณ์') + '''<p><code>go f()</code> เริ่ม goroutine; main ไม่รอ goroutine เอง Channel แบบไม่ buffer จะส่ง/รับเมื่ออีกฝั่งพร้อม การรอส่งโดยไม่มีผู้รับทำให้ค้าง ผู้ส่งหรือผู้ควบคุมผู้ส่งควรเป็นฝ่าย close channel ห้ามส่งหลัง close และห้าม close ซ้ำ การ range channel จบเมื่อ channel ถูก close และอ่านค่าที่ค้างหมดแล้ว</p>''') +
card('Context ส่งการยกเลิกและ deadline ลงไปถึง DB', code('''ctx, cancel := context.WithTimeout(parentCtx, 3*time.Second)
defer cancel()

select {
case result := <-results:
    fmt.Println(result)
case <-ctx.Done():
    return ctx.Err()
}''', 'ส่วนหนึ่งของฟังก์ชันที่คืน error • import context, time, fmt; parentCtx/results มาจากผู้เรียก') + '''<p>ใน handler เริ่มจาก <code>r.Context()</code> เพื่อรับการยกเลิกเมื่อ client ตัดการเชื่อมต่อ ส่ง ctx เป็น parameter แรกไปยัง QueryContext/ExecContext อย่าแทนด้วย context.Background ระหว่างทาง เพราะจะตัดสาย cancellation</p>''' + note('HTTP server เรียก handler พร้อมกันได้อยู่แล้ว ไม่ต้องเปิด goroutine เพิ่มทุก query หากแชร์ map หรือ counter ต้องใช้ Mutex/atomic หรือออกแบบให้ worker เดียวเป็นเจ้าของ state Context ไม่ฆ่า goroutine เอง โค้ดต้องรับฟัง cancellation ด้วย ทดสอบ data race ด้วย go test -race; race detector ต้องใช้ toolchain/architecture ที่รองรับ')))

chapter('testing', 'Unit Test แบบ Table-driven', 'ทดสอบพฤติกรรมที่สำคัญ ไม่ยึดติดรายละเอียดภายใน',
card('ไฟล์ *_test.go และ testing.T', code('''package main

import "testing"

func TestDivide(t *testing.T) {
    tests := []struct {
        name string
        a, b, want float64
        wantErr bool
    }{
        {"normal", 10, 2, 5, false},
        {"zero denominator", 10, 0, 0, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := divide(tt.a, tt.b)
            if (err != nil) != tt.wantErr {
                t.Fatalf("err=%v wantErr=%v", err, tt.wantErr)
            }
            if !tt.wantErr && got != tt.want {
                t.Errorf("got=%v want=%v", got, tt.want)
            }
        })
    }
}''', 'main_test.go • ใช้คู่กับ divide จากบท Function') + code('''go test -v ./...
go test -cover ./...
go test -race ./...''', 'Terminal') + '''<p>Unit test แยก business rule หรือ handler ออกจากบริการภายนอก ส่วน integration test ตรวจว่า SQL, driver และ schema ทำงานร่วมกับ MySQL จริง ใช้ <code>httptest.NewRequest</code> และ <code>httptest.NewRecorder</code> ทดสอบ handler ได้โดยไม่ต้องเปิด port</p>''' + note('ถ้าเปลี่ยน main.go ไปเป็นตัวอย่างบทอื่นแล้ว ให้เก็บ divide ไว้ในฟังก์ชันหรือไฟล์ .go ของ package เดียวกันก่อนรันทดสอบ ตัวอย่างนี้ใช้เลขที่เปรียบเทียบ floating point ได้พอดี งานทศนิยมทั่วไปอาจต้องเปรียบเทียบด้วย tolerance')))

chapter('http', 'เริ่มสร้าง HTTP Server', 'Request → Router → Handler → Response',
card('API แรกโดยไม่ใช้ framework', code('''package main

import (
    "encoding/json"
    "log"
    "net/http"
    "time"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /hello/{name}", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json; charset=utf-8")
        if err := json.NewEncoder(w).Encode(map[string]string{
            "message": "Hello " + r.PathValue("name"),
        }); err != nil {
            log.Printf("encode response: %v", err)
        }
    })
    server := &http.Server{
        Addr: "127.0.0.1:8080", Handler: mux,
        ReadHeaderTimeout: 5 * time.Second,
        ReadTimeout: 5 * time.Second,
        WriteTimeout: 10 * time.Second,
        IdleTimeout: 60 * time.Second,
    }
    log.Fatal(server.ListenAndServe())
}''', 'main.go • โปรแกรมสมบูรณ์') + code('''curl -i http://localhost:8080/hello/Mali
# HTTP/1.1 200 OK
# Content-Type: application/json; charset=utf-8
# {"message":"Hello Mali"}''', 'Terminal • PowerShell เก่าใช้ curl.exe') + '''<p>Routing ที่ระบุ method และ <code>{name}</code> ใช้ ServeMux แบบ Go 1.22 ขึ้นไป ซึ่งอยู่ในฐานเวอร์ชันของคอร์สแล้ว <code>r.PathValue</code> อ่าน path parameter; <code>r.URL.Query().Get("limit")</code> อ่าน query parameter และ <code>r.Body</code> อ่าน request body</p><p>ตั้ง Header ก่อน WriteHeader/Write เสมอ ถ้าเขียน body โดยไม่กำหนด status จะได้ 200 และแก้ status ภายหลังไม่ได้ GET route ของ ServeMux รองรับ HEAD ด้วย การเขียน middleware คือห่อ http.Handler แล้วเรียก <code>next.ServeHTTP(w, r)</code> ดูตัวอย่างจริงใน api.go</p>'''))

chapter('rest', 'ออกแบบ Product REST API', 'ตกลง contract ก่อนเขียน SQL และ handler',
card('เส้นทางและรูปแบบข้อมูล', table(['Method / Path', 'ความหมาย', 'ผลสำเร็จ'], [('GET /health','ตรวจว่า API ติดต่อ DB ได้','200 หรือ 503 ถ้า DB ไม่พร้อม'),('GET /products?limit=20&amp;offset=0','อ่านรายการเรียงตาม id','200 พร้อม data เป็น array'),('GET /products/{id}','อ่านหนึ่งสินค้า','200 พร้อม data เป็น object'),('POST /products','สร้างสินค้าใหม่','201 พร้อม Location header'),('PUT /products/{id}','แทนที่ฟิลด์ที่แก้ไขได้ทั้งหมด','200 พร้อมข้อมูลหลังแก้'),('DELETE /products/{id}','ลบสินค้า','204 และไม่มี body')]) + code('''{
  "sku": "GO-BOOK-01",
  "name": "หนังสือ Go",
  "price_satang": 25000
}''', 'JSON request สำหรับ POST และ PUT') + code('''{
  "data": {
    "id": 1,
    "sku": "GO-BOOK-01",
    "name": "หนังสือ Go",
    "price_satang": 25000,
    "created_at": "2026-10-19T00:00:00Z"
  }
}''', 'ตัวอย่าง 201 response • id และเวลาจริงเปลี่ยนตามข้อมูล') + '''<p>PUT ต้องส่ง sku, name และ price_satang ครบทุกครั้ง หากต้องการแก้เฉพาะบาง field ให้เพิ่ม PATCH เป็นแบบฝึกหัด แยก request DTO ออกจาก response model เพื่อไม่ให้ client กำหนด id/created_at เอง Pagination จำกัด limit 1–100, offset 0–1,000,000 และไม่คืน total count เพื่อลด query เพิ่ม</p>''') +
card('ความหมายของ status ที่ API นี้ใช้', table(['Status','สถานการณ์'], [('400','id, query หรือ JSON/validation ไม่ถูกต้อง'),('404','ไม่พบสินค้า'),('409','SKU ชน unique constraint'),('413 / 415','Body เกิน 1 MiB / Content-Type ไม่ใช่ application/json'),('500','ความผิดพลาดภายใน เก็บรายละเอียดไว้ใน server log'),('504','request context หมดเวลาหรือถูกยกเลิก; กรณี client ปิดไปแล้วอาจส่ง response ไม่สำเร็จ')]) + note('Handler errors คืน JSON {"error":"..."} ส่วน route ที่ไม่พบและ method ที่ไม่รองรับใช้พฤติกรรมมาตรฐานของ net/http ซึ่งคืนข้อความ 404/405 การกำหนด error envelope ให้เหมือนกันทั้งระบบเป็นหัวข้อต่อยอดได้')))

chapter('mysql', 'ออกแบบตารางและเตรียม MySQL', 'ยืนยันความถูกต้องทั้งที่ API และในฐานข้อมูล',
card('Schema ของ Product API', code((EXAMPLE / 'schema.sql').read_text(encoding='utf-8'), 'schema.sql • โค้ดที่ใช้จริง') + '''<ul><li><code>BIGINT</code> สอดคล้องกับ int64 ของ Go; id เป็น PRIMARY KEY และ AUTO_INCREMENT</li><li><code>sku</code> มี UNIQUE index จึงตรวจซ้ำได้แม้มีสอง request พร้อมกัน ใช้ ascii_bin ให้การเปรียบเทียบ SKU ตรงตามตัวอักษร</li><li><code>name</code> ใช้ utf8mb4 เพื่อเก็บภาษาไทย/emoji; VARCHAR จำกัดจำนวนอักขระ ไม่ใช่ byte</li><li><code>price_satang</code> เป็นจำนวนเต็มและมี CHECK ไม่ให้ติดลบหรือเกินขอบเขต</li><li><code>created_at</code> ให้ DB เป็นผู้กำหนด และตั้ง session UTC เพื่อส่งเวลาอย่างสม่ำเสมอ</li></ul>''') +
card('SQL พื้นฐานที่ควรลองใน MySQL client', code('''INSERT INTO products (sku, name, price_satang)
VALUES ('GO-DEMO-1', 'หนังสือ Go', 25000);

SELECT id, sku, name, price_satang, created_at
FROM products ORDER BY id LIMIT 20 OFFSET 0;

UPDATE products SET price_satang = 29000 WHERE sku = 'GO-DEMO-1';
DELETE FROM products WHERE sku = 'GO-DEMO-1';''', 'SQL • ใช้กับฐานข้อมูลฝึก') + note('SELECT ที่ไม่มี ORDER BY ไม่รับประกันลำดับ อย่าใช้ root เป็นบัญชีแอป สำหรับการติดตั้งเองสร้าง go_course และ user ที่มีสิทธิ์เฉพาะ SELECT/INSERT/UPDATE/DELETE ส่วนสิทธิ์แก้ schema ให้แยกไว้กับ migration account Compose ในคอร์สสร้าง learner และใช้ volume เก็บข้อมูลให้')))

chapter('connection', 'เชื่อม Go กับ MySQL และ Connection Pool', 'sql.Open สร้าง handle; PingContext ยืนยันว่าต่อได้จริง',
card('ติดตั้ง driver ใน module ของ API', code('''go get github.com/go-sql-driver/mysql@v1.9.3
go mod tidy''', 'Terminal • ตัวอย่างที่ให้มามี go.mod/go.sum แล้ว ใช้ go mod download ได้เลย') + '''<p><code>database/sql</code> เป็น API กลาง แต่ไม่รู้ protocol ของ MySQL จึงต้องมี driver หากใช้ import แบบตั้งชื่อ package เราจะสร้าง mysql.Config และอ่าน MySQLError ได้ ส่วน blank import <code>_ "github.com/go-sql-driver/mysql"</code> ใช้เมื่อเพียงต้องการลงทะเบียน driver เท่านั้น</p>''' + code((EXAMPLE / 'db.go').read_text(encoding='utf-8'), 'db.go • ไฟล์สมบูรณ์ที่ใช้จริง') + '''<p><code>sql.DB</code> เป็น pool ที่ปลอดภัยต่อการใช้พร้อมกัน ไม่ใช่ connection เดี่ยว สร้างครั้งเดียวตอนเริ่มโปรแกรมและ Close เมื่อจบโปรแกรม ไม่สร้างใหม่ทุก request ค่าจำนวน connection ในตัวอย่างเป็นค่าฝึก ต้องปรับตาม workload และขีดจำกัด MySQL</p>''') +
card('อ่าน DSN และแยกเรื่องเวลาสองฝั่ง', code('''learner:password@tcp(127.0.0.1:3307)/go_course?parseTime=true''', 'รูปแบบ DSN เพื่อทำความเข้าใจ • โค้ดจริงสร้างด้วย Config.FormatDSN') + '''<p><code>ParseTime</code> ให้ driver scan วันที่เป็น time.Time; <code>Loc=UTC</code> ระบุ location ใน Go แต่ไม่ได้เปลี่ยน MySQL time_zone โค้ดจึงตั้ง session <code>time_zone='+00:00'</code> ด้วย timeout ของ driver จำกัด dial/read/write ส่วน context จำกัดเวลาของ operation ตาม request ใช้ทั้งสองชั้นให้เหมาะสม</p>''' + note('Go ไม่โหลด .env ให้อัตโนมัติ Compose อ่าน .env เพื่อแทนค่าใน compose.yaml แล้วส่ง environment เข้าสู่ container ถ้ารัน go run บนเครื่อง ต้องตั้ง DB_PASSWORD และตัวแปรอื่นใน shell เอง อย่า log DSN ที่มีรหัสผ่าน และใช้ DB_TLS=true พร้อม certificate ที่ตรวจสอบได้เมื่อเชื่อม DB ผ่านเครือข่ายจริง')))

chapter('crud', 'เขียน SQL CRUD ผ่าน Repository', 'QueryContext, QueryRowContext และ ExecContext ต่างกันอย่างไร',
card('เลือก method ตามผลลัพธ์ที่ต้องการ', table(['Method','ใช้กับ','ต้องตรวจอะไร'], [('QueryContext','SELECT ที่คืนหลายแถว','defer rows.Close, rows.Next, rows.Scan และ rows.Err'),('QueryRowContext','SELECT ที่คาดหนึ่งแถว','เรียก Scan เพื่อรับผล/ตรวจ error รวม sql.ErrNoRows'),('ExecContext','INSERT / UPDATE / DELETE','ตรวจ error, LastInsertId หรือ RowsAffected ตามงาน')]) + '''<p>ใช้ placeholder <code>?</code> แยกค่าข้อมูลจากคำสั่ง SQL เสมอ เช่น <code>WHERE id = ?</code> แล้วส่ง id เป็น argument ห้ามนำค่าจาก user ไปต่อ string ใน query หรือใช้ fmt.Sprintf สำหรับ value ส่วนชื่อ column, direction และชื่อ table แทนด้วย placeholder ไม่ได้ ถ้ารองรับ sort ต้องเลือกจาก allowlist</p>''' + code((EXAMPLE / 'store.go').read_text(encoding='utf-8'), 'store.go • model, interface และ CRUD ที่ใช้จริง') + '''<p>rows.Scan ต้องเรียงปลายทางให้ตรง SELECT และส่ง pointer ด้วย &amp; ทุกตัว การตรวจ rows.Err หลัง loop สำคัญเพราะ error อาจเกิดระหว่างอ่านผล ไม่ใช่ตอนเริ่ม query ถ้าไม่มีแถว List คืน slice ว่างที่สร้างแล้วเพื่อให้ JSON เป็น []</p>''') +
note('MySQL ปกติ RowsAffected ของ UPDATE นับแถวที่เปลี่ยนค่า ถ้าส่งค่าเดิมอาจได้ 0 แม้มีสินค้า โค้ดตั้ง ClientFoundRows=true เพื่อให้นับแถวที่ match WHERE จึงแยก “ไม่พบ” จาก “ค่าเดิม” ได้ ใน Create/Update มีการอ่านกลับหลังเขียนโดยไม่ครอบ transaction จึงอาจเห็นค่าจาก concurrent update; ระบบที่ต้องการความสอดคล้องเข้มงวดควรออกแบบ transaction หรือ optimistic locking เพิ่ม'))

chapter('validation', 'Validation และ Error Mapping', 'ตรวจข้อมูลก่อนถึง DB และไม่ส่งรายละเอียดภายในกลับ client',
card('กฎของ input ที่ใช้จริง', table(['Field','กฎ','เหตุผล'], [('sku','A–Z, 0–9, ขีดกลาง; 1–40 ตัว; ห้ามซ้ำ','รหัสสินค้าอ่านง่ายและตรวจด้วย unique constraint'),('name','TrimSpace แล้วมี 1–120 Unicode code points','ไม่รับชื่อว่างและสอดคล้อง VARCHAR(120)'),('price_satang','จำนวนเต็ม 0–1,000,000,000,000','สินค้าแจกฟรีเป็น 0 ได้; ไม่รับทศนิยม/ติดลบ'),('request body','JSON object เดียว, ไม่รับ field เกิน, ไม่เกิน 1 MiB','ลดความกำกวมและจำกัดการใช้หน่วยความจำ')]) + '''<p>ใช้ pointer ใน input DTO เพื่อแยก “ไม่ส่งค่า” กับ “ส่งศูนย์” เพราะ int64 ปกติจะเป็น 0 ทั้งสองกรณี Decoder.DisallowUnknownFields ป้องกันการพิมพ์ field ผิดแล้วถูกมองข้าม หลัง Decode ครั้งแรกต้อง Decode อีกครั้งและคาด io.EOF เพื่อยืนยันว่าไม่มี JSON ก้อนที่สอง</p>''' + code('''var body struct {
    SKU         *string `json:"sku"`
    Name        *string `json:"name"`
    PriceSatang *int64  `json:"price_satang"`
}
// ใช้ร่วมกับ MaxBytesReader, DisallowUnknownFields และ EOF check
// ดูฟังก์ชัน decodeInput ใน api.go ที่รวมทุกขั้นตอนแล้ว''', 'ส่วนหนึ่งของ decodeInput') + '''<p>Decoder มาตรฐานอาจรับชื่อ field แบบไม่สนตัวพิมพ์เล็ก/ใหญ่ และยอมรับ key ซ้ำโดยใช้ค่าที่มาภายหลังตามพฤติกรรม encoding/json ตัวอย่างนี้ไม่ได้เพิ่ม parser เพื่อปฏิเสธ duplicate keys หาก contract ต้องเข้มงวดกว่านี้ให้เพิ่มการตรวจพร้อม tests</p>''') +
card('แปลง error ตามความหมาย', code('''var dbErr *mysql.MySQLError
switch {
case errors.Is(err, sql.ErrNoRows):
    // 404: product not found
case errors.As(err, &dbErr) && dbErr.Number == 1062:
    // 409: sku already exists
case errors.Is(err, context.DeadlineExceeded):
    // 504: request timed out
default:
    // log รายละเอียดบน server; client เห็น 500 แบบทั่วไป
}''', 'แนวคิดใน storeError • โค้ดเต็มอยู่ในบทถัดไป') + note('การตรวจว่า SKU มีอยู่ก่อน INSERT ไม่เพียงพอสำหรับ concurrent requests ต้องให้ UNIQUE constraint เป็นผู้ตัดสินสุดท้าย และแปลง error 1062 เป็น 409 อย่านำ err.Error() ของ DB ส่งกลับ client เพราะอาจมีชื่อ table, query และข้อมูลภายใน')))

chapter('application', 'ประกอบ API ทั้งชุด', 'เห็นว่า routing, validation และ SQL ต่อกันอย่างไร',
card('เส้นทางของหนึ่ง request', '''<div class="flow" aria-label="ลำดับการทำงาน"><span>HTTP client</span><b>→</b><span>Timeout middleware</span><b>→</b><span>ServeMux / Handler</span><b>→</b><span>Validate DTO</span><b>→</b><span>productStore</span><b>→</b><span>MySQL</span></div><p>POST /products ถูกตรวจ content type และ body ก่อน จากนั้น handler เรียก store.Create ซึ่ง INSERT ด้วย parameters และอ่าน row กลับมา เมื่อสำเร็จ handler ตั้ง Location และส่ง 201 หาก DB ตอบ duplicate key จะไหลผ่าน storeError แล้วตอบ 409</p>''' + code('''go-mysql-api/
  go.mod / go.sum
  main.go             # เริ่ม/หยุด server และปิด DB pool
  db.go               # config และเปิด pool
  store.go            # model, interface, SQL
  api.go              # routes, DTO, response, middleware
  schema.sql
  Dockerfile / compose.yaml / .env.example
  api_test.go / integration_test.go
  requests.http / README.md''', 'โครงสร้างตัวอย่างที่ดาวน์โหลดได้')) +
card('api.go — Router และ Handlers', '''<p>อ่านตามลำดับ newHandler → decodeInput → create → storeError แล้วเปรียบเทียบ get/update/remove ส่วน middleware กำหนด request context timeout และบันทึก method/path/duration โดยไม่บันทึกรหัสผ่านหรือ request body</p>''' + '<details><summary>เปิดอ่าน api.go ทั้งไฟล์</summary>' + code((EXAMPLE / 'api.go').read_text(encoding='utf-8'), 'api.go • ไฟล์สมบูรณ์') + '</details>') +
card('main.go — Graceful Shutdown', code((EXAMPLE / 'main.go').read_text(encoding='utf-8'), 'main.go • ไฟล์สมบูรณ์') + '''<p>เมื่อรับ Ctrl+C หรือ SIGTERM จะหยุดรับงานใหม่และรอ request ที่ค้างภายใน 5 วินาที ถ้ายังไม่จบจะ Close server แล้วส่ง error กลับ main channel serverErr มี buffer 1 เพื่อให้ goroutine ส่งผลลัพธ์ได้แม้ main ยังอยู่ระหว่าง shutdown หลัง run จบ defer db.Close จึงปิด pool</p>''' + note('Timeout ไม่รับประกันว่าเขียน DB ไม่สำเร็จ หาก client ไม่ได้รับ response หลัง POST ต้องตรวจผลก่อน retry การออกแบบ idempotency key เป็นวิธีต่อยอดสำหรับธุรกรรมสำคัญ')))

chapter('transactions', 'Transaction: หลายคำสั่งต้องสำเร็จด้วยกัน', 'BeginTx → ทำงานผ่าน tx → Commit หรือ Rollback',
card('ตัวอย่างสร้างสินค้าสองชิ้นแบบ atomic', code('''func createPair(ctx context.Context, db *sql.DB, a, b ProductInput) error {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback() // หลัง Commit สำเร็จจะคืน ErrTxDone; ตั้งใจไม่ใช้ค่านี้

    for _, input := range []ProductInput{a, b} {
        _, err := tx.ExecContext(ctx,
            "INSERT INTO products (sku, name, price_satang) VALUES (?, ?, ?)",
            input.SKU, input.Name, input.PriceSatang)
        if err != nil {
            return fmt.Errorf("create pair: %w", err)
        }
    }
    return tx.Commit()
}''', 'ฟังก์ชันเพิ่มเติม • ใช้ schema เดิม • import context, database/sql, fmt') + '''<p>ถ้าชิ้นที่สอง SKU ซ้ำ การ return ทำให้ defer Rollback ยกเลิกชิ้นแรกด้วย ถ้าทุกคำสั่งผ่านแต่ Commit ล้มเหลวก็ต้องคืน error ห้ามรายงานว่าสำเร็จ ภายใน transaction ให้ใช้ tx.ExecContext/tx.QueryContext ทั้งหมด ไม่สลับไป db.ExecContext เพราะอาจใช้คนละ connection</p><p>Transaction รักษาความเป็น atomic แต่ไม่ได้แก้ทุกปัญหาการทำงานพร้อมกัน หากทำ read-modify-write ให้พิจารณา SELECT ... FOR UPDATE, atomic UPDATE หรือ version column ตามกฎของระบบ และเลือก isolation level ให้เหมาะสม</p>''' + note('ฟังก์ชันนี้เป็นแบบฝึกเสริม ยังไม่มี endpoint ในตัวอย่าง ใช้ชื่อ SKU ใหม่สองตัวเพื่อทดลอง แล้วลองให้ตัวที่สองชน SKU เดิมและตรวจว่าตัวแรกไม่ถูกบันทึก อย่าถือ transaction ค้างระหว่างเรียก external API หรือรอ input ผู้ใช้')))

chapter('run', 'Workshop: เปิด MySQL และเรียก API จริง', 'รันได้ทั้งแบบ Docker ทั้งชุด และ Go บนเครื่อง',
card('ดาวน์โหลดแล้วเริ่มระบบ', '''<p><a class="download" href="examples/go-mysql-api.zip" download>ดาวน์โหลด Product API (.zip)</a> หรือเปิดโฟลเดอร์ <code>examples/go-mysql-api</code> ใน repo เปิด terminal ในโฟลเดอร์ที่มี compose.yaml</p>''' + code('''Copy-Item .env.example .env
# แก้ MYSQL_ROOT_PASSWORD และ MYSQL_PASSWORD ใน .env
docker compose up -d --build --wait
docker compose logs api
curl.exe -i http://localhost:8080/health''', 'PowerShell • ต้องเปิด Docker Engine') + code('''cp .env.example .env
# แก้รหัสผ่านทั้งสองค่าใน .env
docker compose up -d --build --wait
curl -i http://localhost:8080/health''', 'macOS / Linux') + '''<p>Compose เปิด MySQL ที่ 127.0.0.1:3307 และ API ที่ 127.0.0.1:8080 ค่ารหัสผ่านใน .env.example ใช้สำหรับฝึกเท่านั้น ไม่ใช้กับระบบจริง Healthcheck รอให้เชื่อม DB และเห็น table ก่อนเริ่ม API การ build ครั้งแรกต้องมี internet เพื่อดาวน์โหลด images และ Go modules</p>''') +
card('ทดลอง CRUD ทีละขั้นด้วย PowerShell', code('''$body = @{ sku = 'GO-BOOK-01'; name = 'หนังสือ Go'; price_satang = 25000 } | ConvertTo-Json
$created = Invoke-RestMethod -Method Post -Uri http://localhost:8080/products -ContentType 'application/json; charset=utf-8' -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
$productId = $created.data.id

Invoke-RestMethod "http://localhost:8080/products/$productId"
Invoke-RestMethod 'http://localhost:8080/products?limit=20&offset=0'

$body = @{ sku = 'GO-BOOK-01'; name = 'Go ฉบับใหม่'; price_satang = 29000 } | ConvertTo-Json
Invoke-RestMethod -Method Put -Uri "http://localhost:8080/products/$productId" -ContentType 'application/json; charset=utf-8' -Body ([System.Text.Encoding]::UTF8.GetBytes($body))

Invoke-RestMethod -Method Delete -Uri "http://localhost:8080/products/$productId"''', 'PowerShell • เก็บ ID จาก response ไม่สมมติว่าเป็น 1') + '''<p>ผลที่คาด: POST คืน data และ id; GET เห็นข้อมูล; PUT เปลี่ยนชื่อและราคา; DELETE ไม่มี response body เมื่อ GET id เดิมอีกครั้งจะได้ 404 หรือเปิด <a href="examples/go-mysql-api/requests.http">requests.http</a> ด้วย VS Code REST Client และแก้ ID ตามผล POST</p>''') +
card('ตัวอย่าง curl สำหรับ Bash', code('''curl -i -X POST http://localhost:8080/products \\
  -H 'Content-Type: application/json' \\
  -d '{"sku":"GO-CURL-01","name":"Go Book","price_satang":25000}'

# แทน 123 ด้วย id ที่ POST คืนมา
curl -i http://localhost:8080/products/123
curl -i 'http://localhost:8080/products?limit=20&offset=0'
curl -i -X PUT http://localhost:8080/products/123 \\
  -H 'Content-Type: application/json' \\
  -d '{"sku":"GO-CURL-01","name":"Go Book Revised","price_satang":29000}'
curl -i -X DELETE http://localhost:8080/products/123''', 'Bash • backslash ต่อบรรทัด; ไม่ใช่ syntax ของ PowerShell')) +
card('ใช้ Go บนเครื่อง และ MySQL จาก Compose', code('''docker compose up -d --wait db
$env:DB_HOST = '127.0.0.1'
$env:DB_PORT = '3307'
$env:DB_USER = 'learner'
$env:DB_NAME = 'go_course'
$env:DB_PASSWORD = 'รหัสเดียวกับ MYSQL_PASSWORD ใน .env'
go mod download
go run .''', 'PowerShell • ไม่เปิด container api พร้อมกันบน port เดียวกัน') + '''<p>ถ้าก่อนหน้านี้เปิด API ใน Compose อยู่ ให้ <code>docker compose stop api</code> ก่อน ภายใน Compose ใช้ DB_HOST=db และ DB_PORT=3306 แต่เมื่อ Go อยู่บนเครื่องใช้ 127.0.0.1 และ published port 3307 อ่านคำสั่ง Bash และวิธีใช้ MySQL ที่ติดตั้งเองได้ใน <a href="examples/go-mysql-api/README.md">README ของตัวอย่าง</a></p>'''))

chapter('verify', 'ทดสอบ API และข้อมูลที่บันทึกจริง', 'ตรวจทั้ง input ผิด เส้นทางสำเร็จ และพฤติกรรมของ MySQL',
card('รันทดสอบที่มีให้', code('''go test -v ./...
go vet ./...

# ใช้ MySQL จริง + race detector ผ่าน Linux container
docker compose --profile test run --build --rm test''', 'Terminal • ทำงานในโฟลเดอร์ go-mysql-api') + '''<p><code>go test</code> ปกติไม่ต้องมี DB และ skip TestMySQLCRUD หากไม่ได้ตั้ง INTEGRATION_DB=1 ส่วน Compose test ส่ง environment ที่จำเป็นและเริ่มฐานข้อมูลก่อน tests สร้าง SKU ของตัวเองและ cleanup เฉพาะ record นั้น ไม่ใช้ TRUNCATE</p>''' + table(['ระดับ','สิ่งที่ตรวจ'], [('Handler unit tests','id/query ผิด, JSON ขาด/เกิน/null, negative/fractional price, ชื่อภาษาไทยยาวเกิน, 1 MiB limit, error mapping และไม่เผย SQL'),('MySQL integration','สร้าง/อ่าน/แก้/ลบ, SKU ซ้ำ, UPDATE ค่าเดิม, ภาษาไทย, ราคา 0, pagination, empty [], created_at และ transaction rollback'),('Manual exercise','ดู status/header/body ด้วย client และตรวจแถวผ่าน MySQL client')])) +
card('ลองทดสอบโดยไม่อ่านโค้ดก่อน', '''<ol><li>POST SKU เดิมสองครั้ง คาด 201 แล้ว 409 และใน DB ต้องมีเพียงหนึ่งแถว</li><li>PUT ค่าเดิมทั้งหมด คาด 200 ไม่ใช่ 404</li><li>ส่ง price_satang เป็น 0 คาดสำเร็จ; ส่ง -1 หรือ 1.5 คาด 400</li><li>ส่ง field ที่ไม่ได้กำหนด หรือ JSON สอง object ต่อกัน คาด 400</li><li>GET /products?limit=101 หรือ /products/abc คาด 400</li><li>DELETE แล้ว GET id เดิม คาด 204 แล้ว 404 และ response 204 ต้องไม่มี body</li></ol>''' + code('''docker compose exec db mysql -u learner -p go_course
-- พิมพ์ MYSQL_PASSWORD เมื่อถูกถาม แล้วลอง:
SELECT id, sku, name, price_satang, created_at FROM products ORDER BY id;
SHOW CREATE TABLE products;
EXPLAIN SELECT id, sku FROM products WHERE sku = 'GO-BOOK-01';''', 'MySQL client • บรรทัดแรกเป็นคำสั่ง shell ที่เหลือรันใน mysql>') + '''<p>อ่าน EXPLAIN ว่า query ใช้ unique index หรือไม่ ชุดตัวอย่างไม่มี benchmark และไม่ได้อ้างว่าค่า pool/timeout นี้รองรับทุก workload ต้องวัดด้วยข้อมูลและโหลดของระบบจริง</p>'''))

chapter('debug', 'แก้ปัญหาที่พบบ่อย และเตรียมก่อนใช้งานจริง', 'วินิจฉัยจากชั้นของปัญหา: shell → server → network → database',
card('Troubleshooting', table(['อาการ','ตรวจและแก้'], [('go: command not found','ติดตั้ง Go แล้วเปิด terminal ใหม่; ตรวจ PATH และ go version'),('undefined / unused import','ตรวจ package, ไฟล์ที่กำลังรัน และชื่อ exported; ใช้ go run . เพื่อรวมทั้ง package'),('bind: address already in use','หยุด server ที่ใช้ port อยู่ หรือเปลี่ยน API_PORT / HTTP_ADDR ตามโหมดที่รัน'),('connection refused','ตรวจ docker compose ps / logs db; ใช้ DB_HOST/PORT ให้ตรงว่าแอปอยู่บนเครื่องหรือใน container'),('Access denied','ตรวจ user/password; การแก้ .env ไม่เปลี่ยนบัญชีใน volume เดิม'),('Table products does not exist','init SQL รันเฉพาะ data directory ใหม่; เปิด mysql client แล้ว SOURCE schema ตาม README'),('Scan เวลาไม่สำเร็จ','ตรวจ ParseTime=true และชนิดปลายทาง time.Time ให้ตรง column'),('UPDATE ค่าเดิมได้ 404','ต้องใช้ ClientFoundRows=true หรือออกแบบวิธีเช็คแถวที่ match ต่างหาก'),('SKU ซ้ำได้ 409','เป็นผลที่คาดจาก UNIQUE constraint; เปลี่ยน SKU หรือแก้สินค้าด้วย PUT'),('Test integration ถูก skip','ตั้ง INTEGRATION_DB=1 พร้อม DB variables หรือใช้ Compose test profile')])) +
card('การเก็บข้อมูลและขอบเขตระบบฝึก', code('''docker compose logs --tail 100 api db
docker compose ps
docker compose down''', 'Terminal • down เก็บ named volume ไว้') + '''<p>schema.sql และ environment สร้างบัญชีถูกใช้ตอน data volume ว่างครั้งแรก ไม่ใช่ระบบ migration ถ้าต้องเปลี่ยน schema หลังมีข้อมูลให้เขียน migration และทดสอบย้อนกลับ ห้ามคาดว่าแก้ไฟล์ init แล้ว restart จะเปลี่ยน table เดิม</p>''' + note('<strong>คำสั่ง docker compose down -v ลบข้อมูลทั้งหมดใน volume ของ Compose project นี้</strong> ใช้เฉพาะฐานข้อมูลฝึกที่ยอมลบทิ้งได้ คำสั่ง down ปกติไม่ลบ named volume') + '''<p>ตัวอย่างนี้ bind localhost และยังไม่มีระบบผู้ใช้/สิทธิ์ ก่อนนำไปให้ผู้อื่นเข้าถึง เพิ่ม authentication และ authorization, ใช้ secrets ภายนอก repository, เปิด HTTPS และ DB TLS, กำหนด CORS origin เมื่อมี frontend คนละ origin, ทำ migration/backup, health/readiness checks, logging/metrics และ rate limit ตามความต้องการ CORS ไม่ใช่การตรวจสิทธิ์และไม่ป้องกันการเรียกผ่าน curl</p>'''))

chapter('practice', 'แบบฝึกหัดและโปรเจกต์จบคอร์ส', 'เปลี่ยนจากอ่านตามตัวอย่าง เป็นอธิบายและออกแบบเอง',
card('ฝึกตามลำดับความยาก', table(['งาน','สิ่งที่ต้องทำ','เกณฑ์ตรวจ'], [('1 • Syntax','รวมราคาสินค้าและคำนวณส่วนลดเป็นสตางค์','มีกรณีตะกร้าว่าง/ส่วนลดติดลบ และ table-driven tests'),('2 • Search','เพิ่ม GET /products?q=Go โดยใช้ LIKE parameter','ไม่ต่อ user input เข้า SQL; กำหนดให้ชัดว่า % และ _ เป็น wildcard หรือ escape'),('3 • PATCH','แก้เฉพาะ field ที่ส่งมา','แยก missing/null/zero; ปฏิเสธ body ที่ไม่มี field แก้ไข'),('4 • Category','เพิ่ม categories และ category_id','มี foreign key, JOIN และทดสอบ category ที่ไม่มีอยู่'),('5 • Transaction','เพิ่ม POST /product-pairs จาก createPair','ถ้ารายการที่สองผิดต้องไม่มีรายการแรกค้าง'),('6 • Concurrent update','เพิ่ม version และตรวจ optimistic locking','สอง client แก้ version เดียวกัน สำเร็จเพียงรายเดียว อีกคนได้ 409')])) +
card('แนวคำตอบสั้น: รวมยอดโดยไม่ยอมให้ราคาติดลบ', code('''func total(prices []int64) (int64, error) {
    var sum int64
    const maxInt64 = int64(1<<63 - 1)
    for _, price := range prices {
        if price < 0 {
            return 0, errors.New("negative price")
        }
        if price > maxInt64-sum {
            return 0, errors.New("total overflow")
        }
        sum += price
    }
    return sum, nil
}''', 'ฟังก์ชันเสริม • import errors') + '''<p>ทดสอบ [] → 0, [100,250] → 350, [-1] → error และ [MaxInt64,1] → overflow อย่าลืมว่าจำนวนเต็มมีขอบเขต แม้ใช้ int64</p>''') +
card('Capstone: Inventory API', '''<p>ต่อยอด Product API ให้มี category, quantity และการจองสินค้าแบบ transaction เขียน API contract ก่อน จากนั้น schema/migration → repository → handler → tests → คู่มือรัน</p><ul><li>ข้อมูลต้องอยู่ใน MySQL หลัง restart และรองรับชื่อภาษาไทย</li><li>ตรวจ input, ใช้ SQL parameters และ map error เป็น HTTP status สม่ำเสมอ</li><li>จำนวน stock ห้ามติดลบ แม้มี request พร้อมกันสองรายการ</li><li>มี tests ของกรณีสำเร็จ/ไม่พบ/ซ้ำ/rollback และวิธีรันจากเครื่องใหม่</li><li>อธิบายได้ว่า pool, context, unique constraint และ transaction แก้ปัญหาใด</li></ul>''') +
card('ทบทวนความเข้าใจ • เปิดเฉลยหลังลองตอบ', ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in [
('1. := ต่างจาก = อย่างไร?', ':= ประกาศและกำหนดค่าภายในฟังก์ชัน โดยต้องมีตัวแปรใหม่ใน scope อย่างน้อยหนึ่งตัว; = กำหนดค่าให้ตัวแปรเดิม'),
('2. ทำไม len("ไทย") ไม่ใช่ 3?', 'len(string) นับ byte ของ UTF-8 จึงได้ 9; การนับ Unicode code points ใช้ utf8.RuneCountInString และไม่เท่ากับจำนวน grapheme เสมอ'),
('3. ทำไมแก้ slice แล้วต้นฉบับเปลี่ยน?', 'slice copy descriptor แต่ยังอ้าง backing array ร่วมกัน การแยกข้อมูลต้องสร้าง slice ใหม่และ copy สมาชิก'),
('4. sql.Open สำเร็จหมายถึง DB พร้อมหรือยัง?', 'ยังไม่แน่นอน เพราะเป็นการเตรียม handle/pool; ต้อง PingContext เพื่อยืนยันว่าต่อได้ในขณะนั้น'),
('5. QueryRowContext พบว่าไม่มีข้อมูลตอนไหน?', 'เมื่อเรียก Scan แล้วได้ sql.ErrNoRows ให้ map เป็น 404 สำหรับการอ่านสินค้าหนึ่งรายการ'),
('6. ตรวจ SKU ก่อน INSERT เพียงอย่างเดียวพอไหม?', 'ไม่พอ สอง request อาจตรวจพร้อมกันแล้วต่างเห็นว่ายังไม่มี ต้องมี UNIQUE constraint และจัดการ duplicate key'),
('7. ทำไมอัปเดตค่าเดิมอาจได้ RowsAffected=0?', 'MySQL ปกตินับแถวที่เปลี่ยนค่า ตัวอย่างตั้ง ClientFoundRows=true เพื่อนับแถวที่ match และไม่ส่ง 404 ผิด'),
('8. ปิด context หมายความว่า DB ไม่ได้เขียนแน่นอนหรือไม่?', 'ไม่แน่นอน โดยเฉพาะเมื่อผลลัพธ์สูญหายระหว่างทาง ต้องตรวจสถานะและออกแบบ idempotency สำหรับการ retry ที่สำคัญ')])))

sources = [
('Go installation', 'https://go.dev/doc/install', 'ขั้นตอนติดตั้งและตรวจ version'),
('Go language specification', 'https://go.dev/ref/spec', 'ไวยากรณ์และกฎของภาษา'),
('A Tour of Go', 'https://go.dev/tour/list', 'แบบฝึก syntax, methods และ concurrency'),
('Go tutorials', 'https://go.dev/doc/tutorial/', 'module, tests และ generics'),
('net/http และ ServeMux', 'https://pkg.go.dev/net/http#ServeMux', 'routing, handler และ server'),
('Routing enhancements', 'https://go.dev/blog/routing-enhancements', 'method patterns และ path wildcards ตั้งแต่ Go 1.22'),
('database/sql guide', 'https://go.dev/doc/database/', 'query, connection pool และ context'),
('SQL injection prevention', 'https://go.dev/doc/database/sql-injection', 'แยก parameter ออกจาก SQL text'),
('Transactions', 'https://go.dev/doc/database/execute-transactions', 'BeginTx, Commit และ Rollback'),
('MySQL driver v1.9.3', 'https://github.com/go-sql-driver/mysql/tree/v1.9.3', 'driver version ที่ตัวอย่าง pin ไว้'),
('MySQL Docker image', 'https://github.com/docker-library/docs/tree/master/mysql', 'environment, volume และ init scripts'),
]

css = '''
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:80px}body{margin:0;background:#f3f6fa;color:#172b41;font:16px/1.85 "Segoe UI",Tahoma,system-ui,sans-serif}a{color:#006582;text-underline-offset:4px}button,input{font:inherit}button{cursor:pointer}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #dc7800;outline-offset:4px}.skip{position:absolute;top:-100px;left:12px;z-index:100;background:white;padding:10px}.skip:focus{top:10px}.hero{background:radial-gradient(ellipse at top right,#075c76,transparent 65%),#0c1e30;color:#fff;padding:55px max(24px,calc((100vw - 1230px)/2)) 48px}.eyebrow{color:#86e2ed;font-size:.8rem;letter-spacing:.15em;font-weight:700}.hero h1{font-size:clamp(2.5rem,6vw,4rem);line-height:1.3;margin:12px 0}.hero h1 span{color:#7ce2ee}.hero p{max-width:740px;color:#cfdee9;font-size:1.08rem}.badges{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0}.badges span{border:1px solid #447082;padding:3px 12px;border-radius:999px;font-size:.8rem}.hero-links{display:flex;gap:20px;flex-wrap:wrap}.hero-links a{color:#b6f0f5}.toolbar{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid #d4e0e9;padding:10px 24px;display:flex;gap:16px;align-items:center;justify-content:space-between;box-shadow:0 2px 10px #15364f08}.toolbar a{text-decoration:none;font-weight:600}.toolbar button{padding:4px 14px;background:white;border:1px solid #b7cbd8;border-radius:6px;color:#315068}.reading-track{position:absolute;height:3px;bottom:-1px;left:0;background:#008eab;width:0}.layout{max-width:1280px;margin:auto;display:grid;grid-template-columns:242px minmax(0,1fr);gap:32px;padding:32px 24px 64px}.toc{align-self:start;position:sticky;top:80px;max-height:calc(100vh - 105px);overflow:auto;padding:4px 12px 15px 0}.toc h2{font-size:1rem;margin:0 0 14px}.toc a{display:block;text-decoration:none;font-size:.81rem;padding:7px 8px;border-left:2px solid #cddbe5;color:#456074;line-height:1.65}.toc a:hover,.toc a.active{border-color:#008eab;background:#e2f3f6;color:#005a70}.toc small{display:block;margin:16px 8px;color:#587185}.chapter-heading{display:flex;align-items:flex-start;gap:16px;margin-bottom:20px;border-bottom:2px solid #c8dee7;padding-bottom:18px}.chapter-num{color:#007b97;font-size:1.7rem;font-weight:800;line-height:1.6}.chapter-heading h2{font-size:1.55rem;line-height:1.6;margin:0}.chapter-heading p{color:#5a7081;margin:4px 0 0;font-size:.92rem}section{margin-bottom:52px;scroll-margin-top:80px;min-width:0}.card{background:#fff;border:1px solid #d6e2eb;border-radius:12px;padding:24px;margin-bottom:18px;box-shadow:0 4px 16px #18374d04}.card h3{margin:0 0 14px;font-size:1.12rem;color:#163b55}.card p{margin:12px 0}.card p:first-of-type{margin-top:0}.card ul,.card ol{padding-left:24px}.card li{margin:6px 0}.note{padding:18px 20px;margin:18px 0;border-left:4px solid #0795ab;background:#e8f6f8;border-radius:0 8px 8px 0;font-size:.93rem;color:#24566a}.code{margin:18px 0;border:1px solid #254055;background:#0e1c2b;border-radius:9px;overflow:hidden}.code-top{background:#182c3e;color:#a6c6d9;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:8px 14px;font-size:.75rem;line-height:1.6}.copy{flex-shrink:0;background:#233e53;color:#d9eef7;border:1px solid #49667b;border-radius:5px;padding:2px 10px;font-size:.75rem}pre{margin:0;overflow:auto;padding:20px;color:#e3edf7;tab-size:4;font-size:.85rem;line-height:1.8;font-family:Consolas,"Cascadia Code",monospace}code{font-family:Consolas,"Cascadia Code",monospace;font-size:.9em;overflow-wrap:anywhere}p code,li code,td code{color:#006581;background:#edf5f8;padding:1px 5px;border-radius:4px}pre code{font:inherit;overflow-wrap:normal}.table-wrap{overflow:auto;border:1px solid #d5e1eb;border-radius:8px;margin:18px 0}table{width:100%;border-collapse:collapse;font-size:.9rem;min-width:540px}th{text-align:left;background:#eaf2f7;color:#244b64}th,td{padding:12px 15px;border-bottom:1px solid #dbe5ed;vertical-align:top}tr:last-child td{border-bottom:0}tbody tr:nth-child(even){background:#f7fafc}details{border:1px solid #d5e2eb;border-radius:8px;margin:12px 0;padding:12px 16px}summary{cursor:pointer;font-weight:600;color:#13617b}details .code{margin-bottom:0}.flow{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:.82rem}.flow span{background:#e3f2f6;border:1px solid #bbd8e3;padding:8px 12px;border-radius:6px}.flow b{color:#4f819a}.download{display:inline-block;background:#006c85;color:white;padding:9px 17px;border-radius:7px;text-decoration:none;font-weight:600}.sources{border-top:1px solid #c9dce6;padding-top:20px}.sources li{font-size:.9rem;margin:7px 0}footer{background:#0c1e30;color:#abc5d8;padding:30px 24px;text-align:center;font-size:.85rem}footer a{color:#91dae8}.copy-status{font-size:.8rem;color:#49677c;min-height:1.7em} @media(max-width:940px){.layout{grid-template-columns:1fr}.toc{position:static;max-height:none;border:1px solid #cedee7;border-radius:10px;padding:18px;background:#fff}.toc nav{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px 14px}.toc small{margin-bottom:0}.hero{padding:36px 24px}.layout{gap:30px}.toolbar{font-size:.85rem}}@media(max-width:540px){body{font-size:15px}.layout{padding:24px 14px}.card{padding:18px 16px}.chapter-heading h2{font-size:1.25rem}.hero h1{font-size:2.5rem}.toc nav{grid-template-columns:1fr}.toolbar{padding:10px 14px}.toolbar button{font-size:.75rem}.code-top{padding:8px 10px}pre{padding:16px;font-size:.78rem}.hero-links{gap:12px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{body{background:white;color:black;font-size:11pt}.hero{background:white;color:black;padding:0 0 20px}.hero p,.eyebrow,.hero h1 span{color:black}.badges span{color:black;border-color:#aaa}.hero-links,.toc,.toolbar,.copy,.skip,.copy-status{display:none}.layout{display:block;padding:0;max-width:none}.card{box-shadow:none;border-color:#ccc;break-inside:auto}.chapter-heading{break-after:avoid}h2,h3,summary{break-after:avoid}section{margin-bottom:28px}.code,.code-top{background:#f4f4f4;border-color:#ccc;color:#000}pre{color:black;white-space:pre-wrap;overflow-wrap:anywhere;font-size:8pt}table{min-width:0;font-size:9pt}.table-wrap{overflow:visible}a{color:black}.note{background:#f5f5f5;color:black}footer{background:white;color:black}}
'''

script = '''
const live = document.getElementById('copy-status');
document.querySelectorAll('.copy').forEach(button => {
  button.addEventListener('click', async () => {
    const text = button.closest('.code').querySelector('code').textContent;
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error('clipboard unavailable');
      await navigator.clipboard.writeText(text);
      button.textContent = 'คัดลอกแล้ว';
      live.textContent = 'คัดลอกโค้ดแล้ว';
      setTimeout(() => { button.textContent = 'คัดลอก'; }, 1800);
    } catch {
      const range = document.createRange();
      range.selectNodeContents(button.closest('.code').querySelector('code'));
      const selection = window.getSelection();
      selection.removeAllRanges(); selection.addRange(range);
      button.textContent = 'กด Ctrl+C / ⌘C';
      live.textContent = 'เลือกโค้ดให้แล้ว กด Ctrl+C หรือ Command+C เพื่อคัดลอก';
    }
  });
});
document.getElementById('print').addEventListener('click', () => {
  const closed = [...document.querySelectorAll('details:not([open])')];
  closed.forEach(detail => { detail.open = true; });
  const restore = () => {
    closed.forEach(detail => { detail.open = false; });
    window.removeEventListener('afterprint', restore);
  };
  window.addEventListener('afterprint', restore);
  window.print();
});
const track = document.querySelector('.reading-track');
const links = [...document.querySelectorAll('.toc nav a')];
const sections = [...document.querySelectorAll('main section')];
function updateReading() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  track.style.width = (max > 0 ? Math.min(100, window.scrollY / max * 100) : 100) + '%';
  let current = sections[0];
  for (const section of sections) if (section.getBoundingClientRect().top <= 160) current = section;
  links.forEach(link => {
    const active = link.hash === '#' + current.id;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
  });
}
let scheduled = false;
window.addEventListener('scroll', () => {
  if (scheduled) return;
  scheduled = true;
  requestAnimationFrame(() => { updateReading(); scheduled = false; });
}, {passive:true});
window.addEventListener('resize', updateReading);
updateReading();
'''

toc = ''.join(f'<a href="#{anchor}">{i:02} · {title}</a>' for i, (anchor, title, _) in enumerate(chapters, 1))
refs = ''.join(f'<li><a href="{url}">{title}</a> — {description}</li>' for title, url, description in sources)
output = f'''<!DOCTYPE html>
<html lang="th"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="สื่อการสอน Go ภาษาไทยอย่างละเอียด ตั้งแต่ syntax, struct, concurrency, testing จนถึง REST API เชื่อม MySQL พร้อมโปรเจกต์ CRUD และ Docker Compose">
<title>Go (Golang) ตั้งแต่ Syntax ถึง REST API + MySQL | FullStack-101</title>
<style>{css}</style></head><body>
<a class="skip" href="#content">ข้ามไปเนื้อหาบทเรียน</a>
<header class="hero"><div class="eyebrow">FULLSTACK-101 / BACKEND LEARNING PATH</div><h1>Go จากพื้นฐาน<br>สู่ <span>API + MySQL</span></h1>
<p>สื่อการสอนภาษาไทยแบบลงมือทำ ตั้งแต่ syntax จนถึง REST API ที่เก็บข้อมูลจริง พร้อมคำอธิบาย โค้ดครบชุด แบบฝึกหัด และการทดสอบ</p>
<div class="badges"><span>24 บทเรียน</span><span>Go 1.26+</span><span>net/http</span><span>database/sql</span><span>MySQL 8.4</span><span>CRUD Workshop</span></div>
<div class="hero-links"><a href="#roadmap">เริ่มเส้นทางการเรียน →</a><a href="examples/go-mysql-api.zip" download>ดาวน์โหลดโค้ดตัวอย่าง ↓</a></div></header>
<div class="toolbar"><a href="index.html">← ศูนย์รวมบทเรียน</a><a href="#run">ไป Workshop</a><button id="print" type="button">พิมพ์ / บันทึก PDF</button><div class="reading-track" aria-hidden="true"></div></div>
<div class="layout"><aside class="toc"><h2>สารบัญบทเรียน</h2><nav aria-label="สารบัญ Go">{toc}</nav><small>อ่านตามลำดับ หรือเลือกหัวข้อเพื่อทบทวน<br><a href="#sources">เอกสารอ้างอิง ↗</a></small></aside>
<main id="content"><div id="copy-status" class="copy-status" role="status" aria-live="polite"></div>
{''.join(body for _, _, body in chapters)}
<section class="sources" id="sources" aria-labelledby="sources-title"><h2 id="sources-title">เอกสารอ้างอิงและอ่านต่อ</h2><p>ตัวอย่างและแบบฝึกหัดเขียนสำหรับคอร์สนี้ ตรวจพฤติกรรมภาษาและ API เทียบเอกสารทางการเมื่อ 19 ตุลาคม 2026 ตัวอย่าง pin driver v1.9.3 เพื่อให้ฝึกตามได้ ส่วน Go/MySQL image tag อาจได้รับ patch ใหม่</p><ul>{refs}</ul><p>แก้ไขเนื้อหาได้ที่ tools/build_go_lesson.py แล้วรัน python tools/build_go_lesson.py เพื่อสร้างหน้านี้และ zip ใหม่ โปรเจกต์ API อยู่ใน examples/go-mysql-api</p></section>
</main></div><footer>FullStack-101 · Go / REST API / MySQL<br><a href="index.html">กลับไปเลือกบทเรียนอื่น</a></footer><script>{script}</script></body></html>'''

assert len(chapters) == 24
(ROOT / 'golang-teaching.html').write_text(output, encoding='utf-8')
with zipfile.ZipFile(ROOT / 'examples' / 'go-mysql-api.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(EXAMPLE.iterdir()):
        if path.is_file() and (path.name in {'.env.example', '.gitignore', '.dockerignore', 'Dockerfile', 'README.md', 'compose.yaml', 'go.mod', 'go.sum', 'schema.sql', 'requests.http'} or path.suffix == '.go'):
            archive.write(path, f'go-mysql-api/{path.name}')
print(f'Built {len(chapters)} chapters, {len(output):,} characters and examples/go-mysql-api.zip')
