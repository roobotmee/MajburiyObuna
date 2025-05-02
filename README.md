
# 🔒 Aiogram Subscription Check Middleware

Bu middleware `Aiogram` frameworki uchun yozilgan bo‘lib, foydalanuvchilar botdan foydalanishdan oldin rasmiy kanallarga obuna bo‘lganligini tekshiradi. Agar foydalanuvchi barcha talab qilingan kanallarga obuna bo‘lmagan bo‘lsa, ularga kanal havolalari bilan xabar yuboriladi va keyingi jarayonlar to‘xtatiladi.

---

## 🧩 Vazifasi

Middleware foydalanuvchi tomonidan yuborilgan har bir xabar yoki callback query (tugma bosilishi)dan oldin quyidagi ishlarni bajaradi:

1. Foydalanuvchining Telegram `user_id`ini aniqlaydi.
2. `CHANNELS` ro‘yxatidagi har bir kanal uchun:
   - Foydalanuvchi obuna bo‘lganmi yoki yo‘qligini `check()` funksiyasi orqali tekshiradi.
   - Kanalga havola bilan tugma yaratadi. Agar foydalanuvchi obuna bo‘lgan bo‘lsa ✅ belgisi, bo‘lmagan bo‘lsa ❌ belgisi bilan ko‘rsatiladi.
3. Agar foydalanuvchi birorta ham kanalga obuna bo‘lmagan bo‘lsa:
   - Ularga obuna bo‘lishni so‘rovchi xabar va tugmalar yuboriladi.
   - `CancelHandler` yordamida xabar yoki tugma bosishdan keyingi ish jarayoni to‘xtatiladi.

---

## 🏗 Foydalanish

### 1. `data/config.py` faylida `CHANNELS` ro‘yxatini e'lon qiling:

```python
CHANNELS = [
    -1001234567890,  # @kanal1
    -1009876543210,  # @kanal2
]
```

### 2. `data/check_sub.py` faylida `check` funksiyasi bo‘lishi kerak:

```python
from loader import bot

async def check(user_id: int, kanal_id: int) -> int:
    try:
        member = await bot.get_chat_member(chat_id=kanal_id, user_id=user_id)
        if member.status in ("member", "creator", "administrator"):
            return 1
        else:
            return 0
    except:
        return 0
```

### 3. Middleware'ni `dispatcher`ga qo‘shing:

```python
from middlewares.subscription import Asosiy

dp.middleware.setup(Asosiy())
```

---

## 🖼 Foydalanuvchiga chiqadigan xabar

```html
Botimizdan foydalanish uchun rasmiy kanalimizga <b>obuna bo'ling</b> va <b>Tekshirish</b> tugmasini bosing.
```

Tugmalarda har bir kanal nomi va unga tegishli taklif havolasi ko‘rsatiladi. Obuna bo‘lishdan so‘ng "🔄 Tekshirish" tugmasi orqali foydalanuvchi holatini qayta tekshiradi.

---

## 📌 Eslatma

- `export_invite_link()` faqat bot kanal admini bo‘lsa ishlaydi.
- Ushbu middleware `message` va `callback_query` turidagi yangilanishlar (`update`) uchun ishlaydi.
- Obuna bo‘lmagan foydalanuvchilarning barcha keyingi xabarlari bloklanadi.
