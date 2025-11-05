# Cyber-security

Kiberxavfsizlik bo‘yicha ta’limiy/laboratoriya loyihasi. Repozitoriya ruxsat etilgan test muhitlarida himoya, monitoring va barqarorlikni o‘rganish uchun turli vositalar, skriptlar va namunalarni jamlaydi.

> Muhim: Ushbu materiallar faqat qonuniy, etik va ruxsat etilgan sharoitlarda foydalanish uchun mo‘ljallangan. Uchinchi shaxslarga tegishli tizim va tarmoqlarda ruxsatsiz faoliyat qat’iyan taqiqlanadi. Muallif(lar) noqonuniy foydalanish oqibatlari uchun javobgar emas.

## Mundarija
- [Xususiyatlar](#xususiyatlar)
- [Tuzilma](#tuzilma)
- [Talablar](#talablar)
- [Boshlash](#boshlash)
- [Modullar haqida qisqacha](#modullar-haqida-qisqacha)
- [Rivojlantirish](#rivojlantirish)
- [Xavfsiz va mas’uliyatli foydalanish](#xavfsiz-va-masuliyatli-foydalanish)
- [Hissa qo‘shish](#hissa-qoshish)
- [Yo‘l xaritasi (Roadmap)](#yol-xaritasi-roadmap)
- [Savol-javob (FAQ)](#savol-javob-faq)
- [Litsenziya](#litsenziya)

## Xususiyatlar
- Ta’limiy maqsadlarda yuklama va tarmoq ssenariylarini model qilish
- O‘z infratuzilmangizni sinashga yordam beruvchi namuna skriptlar
- Izolyatsiyalangan laboratoriya muhitida ishlatishga qulaylik
- Go va Python asosidagi komponentlar

## Tuzilma
Quyida asosiy kataloglar va fayllar:
```
.
├── Ddos/         # DDoS/DoS bilan bog‘liq tadqiqot/namunalar (faqat ruxsat bilan)
├── Fludilka/     # Trafik “flood” generatori namunalar (faqat ruxsat bilan)
├── artillery/    # Trafik/yuklama ssenariylari
├── botnet/       # Ta’limiy konsept va simulyatsiyalar
├── dos/          # Oddiy DoS ssenariylari
├── gobuster/     # Veb katalog/subdomen qidiruviga oid materiallar
├── hulk/         # HULK uslubidagi HTTP bosim ssenariylari (faqat ruxsat bilan)
├── locust/       # Python asosidagi yuklama testlari (Locust)
├── scanapp/      # Skanner/analiz ilovalari uchun materiallar
├── vpn_server/   # VPN server konfiguratsiya/skriptlari
└── polibiy.py    # Polibiy shifri bilan ishlash uchun skript
```

Tezkor havolalar:
- [Ddos](https://github.com/NurbekLDM/Cyber-security/tree/main/Ddos)
- [Fludilka](https://github.com/NurbekLDM/Cyber-security/tree/main/Fludilka)
- [artillery](https://github.com/NurbekLDM/Cyber-security/tree/main/artillery)
- [botnet](https://github.com/NurbekLDM/Cyber-security/tree/main/botnet)
- [dos](https://github.com/NurbekLDM/Cyber-security/tree/main/dos)
- [gobuster](https://github.com/NurbekLDM/Cyber-security/tree/main/gobuster)
- [hulk](https://github.com/NurbekLDM/Cyber-security/tree/main/hulk)
- [locust](https://github.com/NurbekLDM/Cyber-security/tree/main/locust)
- [scanapp](https://github.com/NurbekLDM/Cyber-security/tree/main/scanapp)
- [vpn_server](https://github.com/NurbekLDM/Cyber-security/tree/main/vpn_server)
- [polibiy.py](https://github.com/NurbekLDM/Cyber-security/blob/main/polibiy.py)

Texnologiyalar: Go, Python, Docker (Dockerfile), Shell, Makefile

## Talablar
- Go (so‘nggi barqaror versiya tavsiya etiladi)
- Python 3.10+ (virtual muhit tavsiya etiladi)
- Git
- Docker (ixtiyoriy, izolyatsiyalangan laboratoriya uchun)
- Bash/PowerShell

## Boshlash
1) Repozitoriyani klonlang:
```bash
git clone https://github.com/NurbekLDM/Cyber-security.git
cd Cyber-security
```

2) (Ixtiyoriy) Python virtual muhit:
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
```

3) Har bir modul papkasi ichida alohida sozlamalar/yo‘riqnoma bo‘lishi mumkin. Shu papkada ko‘rsatilgan ko‘rsatmalarga amal qiling.

4) Xavfsiz laboratoriya:
- Testlarni faqat izolyatsiyalangan muhitda (VM/konteyner, ajratilgan subnet) bajaring.
- Tarmoq yuklamasi/trafigiga ta’sir qiluvchi skriptlar uchun maxsus test segmentidan foydalaning.
- Hech qachon ruxsatsiz tashqi resurslarga yo‘naltirmang.

## Modullar haqida qisqacha
- DDoS/DoS (Ddos, dos, hulk): Barqarorlik va himoyani o‘rganish maqsadida yuklama ssenariylari. Real tizimlarda ruxsat bilangina qo‘llash mumkin.
- Gobuster: O‘z loyihalaringizda katalog va subdomenlarni aniqlash (qonuniy testlar uchun).
- Locust: Foydalanuvchi oqimlarini simulyatsiya qilib, ishlash ko‘rsatkichlarini baholash.
- Artillery: Trafik ssenariylarini modellashtirish va kuzatish.
- Botnet: Ta’limiy konsept va simulyatsiya (real muhitga qo‘llash taqiqlanadi).
- VPN Server: Xavfsiz test tarmoqlarini tashkil etish uchun yordamchi konfiguratsiyalar.
- Polibiy: Kriptografiya asoslari (Polibiy shifri) bilan tanishish.

Eslatma: Agar modul ichida README/yo‘riqnoma bo‘lmasa, Issue orqali bildirishingiz yoki PR orqali qo‘shishingiz mumkin.

## Rivojlantirish
- Kod uslubi:
  - Go: `gofmt`, `golangci-lint`
  - Python: `black`, `ruff`, `pytest` (zaruratga ko‘ra)
- Test: Har modul uchun alohida test muhiti yarating, tarmoq aloqalarini izolyatsiya qiling.
- Docker: Ta’sir doirasini cheklash va takrorlanuvchan muhit uchun konteynerlardan foydalaning.
- Versiya nazorati: Kichik o‘zgarishlar uchun kichik commitlar, ma’noli commit xabarlari yozing.

## Xavfsiz va mas’uliyatli foydalanish
- Faqat o‘zingizga tegishli yoki yozma ruxsat berilgan tizimlarda ishlating.
- Uchinchi tomon infratuzilmalariga zarar yetkazish, xizmat ko‘rsatishni to‘xtatish (DoS/DDoS), ruxsatsiz skanerlash qat’iyan man etiladi.
- Huquqiy va etik me’yorlarga rioya qiling; nojo‘ya foydalanish uchun muallif(lar) javobgar emas.

## Hissa qo‘shish
Taklif va tuzatishlar mamnuniyat bilan qabul qilinadi. PR ochishdan oldin:
- O‘zgarish maqsadi va ta’sirini qisqacha tushuntiring.
- Zarur hujjatlarni yangilang (README/kommentlar).
- Etik va huquqiy cheklovlarga to‘liq mosligini tekshiring.

## Yo‘l xaritasi (Roadmap)
- [ ] Har bir modul uchun alohida README/yo‘riqnoma
- [ ] Litsenziya faylini qo‘shish (MIT/Apache-2.0 tavsiya etiladi)
- [ ] CI/Lint/Test ish jarayonlarini qo‘shish (GitHub Actions)
- [ ] Docker Compose bilan sinov muhiti namunasi
- [ ] Namuna laboratoriya ssenariylari (faqat izolyatsiyalangan muhit uchun)

## Savol-javob (FAQ)
- Savol: Ushbu repodan real tizimlarda foydalanish mumkinmi?
  - Javob: Yo‘q. Faqat ruxsat etilgan test/lab muhitlarida.
- Savol: Nima uchun ba’zi papkalarda README yo‘q?
  - Javob: Loyiha rivojlanish jarayonida. Issue/PR orqali hissa qo‘shishingiz mumkin.
- Savol: Qanday muhit tavsiya qilasiz?
  - Javob: VM/konteynerga ajratilgan, internetdan uzilgan (air-gapped yoki cheklangan) test segmenti.

## Litsenziya
Hozircha loyiha litsenziyalanmagan. Ochiq manbada tarqatish uchun mos litsenziya (masalan, MIT yoki Apache-2.0) qo‘shish tavsiya etiladi.