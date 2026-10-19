# FullStack-101

เว็บไซต์รวมสื่อการสอนสำหรับผู้เริ่มต้นและผู้ที่ต้องการทบทวนการพัฒนาเว็บแบบ Full Stack เนื้อหาแต่ละหัวข้อเป็นหน้า HTML แบบสแตนด์อโลน อ่านได้จากเบราว์เซอร์ทันที

## หัวข้อการเรียนรู้

| หมวด | บทเรียน |
| --- | --- |
| Frontend | CSS Styling, JavaScript ES6+, React, Next.js + Redux + TypeScript |
| Backend | Go (Golang) + MySQL, Express.js + TypeScript, NestJS, Laravel, Ruby on Rails |
| Data | SQL Fundamentals, MySQL Database |
| เครื่องมือและระบบ | Git Version Control, Linux Command Line, Docker |

หน้าเริ่มต้นคือ [`index.html`](index.html) ซึ่งเชื่อมไปยังบทเรียนทั้งหมด

## เริ่มใช้งาน

หน้าเว็บบทเรียนไม่มีขั้นตอนติดตั้งแพ็กเกจหรือ build เนื่องจากเป็น Static HTML ส่วนโปรเจกต์ API ประกอบบทเรียน Go มีขั้นตอนรันแยกใน [คู่มือตัวอย่าง](examples/go-mysql-api/README.md)

1. Clone โปรเจกต์

   ```bash
   git clone https://github.com/dusticom/FullStack-101.git
   cd FullStack-101
   ```

2. เปิด `index.html` ด้วยเว็บเบราว์เซอร์ หรือใช้ส่วนขยาย Live Server ของ VS Code เพื่อดูผลระหว่างแก้ไข

ตัวอย่างการเปิดด้วย Python (หากติดตั้งไว้แล้ว):

```bash
python -m http.server 8000
```

จากนั้นไปที่ [http://localhost:8000](http://localhost:8000)

## โครงสร้างโปรเจกต์

```text
.
├── index.html                              # หน้ารวมบทเรียน
├── css-teaching.html
├── docker-teaching.html
├── express-typescript-teaching.html
├── git-teaching.html
├── golang-teaching.html                     # Go 24 บท ตั้งแต่ syntax ถึง API + MySQL
├── examples/go-mysql-api/                   # โค้ด CRUD, Compose, schema และ tests
├── examples/go-mysql-api.zip                # โค้ดตัวอย่างสำหรับดาวน์โหลด
├── tools/build_go_lesson.py                 # สร้างหน้า Go และ zip ใหม่ (Python stdlib)
├── javascript-es6-teaching.html
├── laravel-teaching.html
├── linux-teaching.html
├── mysql-teaching.html
├── nestjs-teaching.html
├── nextjs-redux-typescript-teaching.html
├── react-teaching.html
├── ruby-on-rails-teaching.html
├── sql-teaching.html
└── .github/workflows/static.yml             # Deploy ไปยัง GitHub Pages
```

## การเพิ่มหรือแก้ไขบทเรียน

บทเรียน [Go (Golang) + MySQL](golang-teaching.html) มี 24 บท พร้อมโค้ด CRUD ที่ใช้ `net/http` และ `database/sql`, Docker Compose สำหรับ MySQL 8.4, แบบฝึกหัด และ unit/integration tests อ่านหน้า HTML ได้ทันที หากแก้เนื้อหาบทเรียนหรือโค้ดตัวอย่าง ให้รัน `python tools/build_go_lesson.py` เพื่ออัปเดตหน้า HTML และ zip ที่ดาวน์โหลดให้ตรงกัน ไม่จำเป็นต้องรัน script เพื่อเปิดอ่านบทเรียน

1. สร้างหรือแก้ไขไฟล์ `*-teaching.html` โดยระบุ `<meta charset="UTF-8">` เพื่อรองรับภาษาไทย
2. เพิ่มการ์ดลิงก์ของบทเรียนใน `index.html`
3. เปิดตรวจสอบบนเบราว์เซอร์ทั้งหน้าจอคอมพิวเตอร์และมือถือ
4. Commit และ push ขึ้นสาขา `main`

## การเผยแพร่

เมื่อมีการ push ไปยังสาขา `main` GitHub Actions จะ deploy ไฟล์ Static ทั้งหมดไปยัง GitHub Pages อัตโนมัติ ผ่าน workflow ที่ [`static.yml`](.github/workflows/static.yml)

## เทคโนโลยี

- HTML5 และ CSS3
- JavaScript ที่ฝังในแต่ละหน้าเมื่อจำเป็น
- Google Fonts: Inter และ Prompt
- GitHub Actions / GitHub Pages

## License

ยังไม่มีการระบุสัญญาอนุญาต (license) สำหรับโปรเจกต์นี้
