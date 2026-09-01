### Установка dev среды:

1. Установка зависимостей
```
cd frontend
npm create vite@latest . -- --template vue
npm install
npm install axios pinia vue-router
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 🚀 Запуск
```
cd frontend
npm run dev
```

2. Настройка Vite (vite.config.js)


### Иерархия папок:
```
frontend/
├── src/
│   ├── api/                          # 📡 API-запросы к бэкенду
│   │   ├── auth.js                   # Авторизация: login, logout, register
│   │   └── questions.js              # Работа с вопросами: CRUD, статистика
│   │
│   ├── components/                   # 🧩 Переиспользуемые компоненты
│   │   ├── layout/                   # Компоненты макета страницы
│   │   │   ├── AppLayout.vue         # Основной макет с топбаром и футером
│   │   │   └── TopBar.vue            # Верхняя панель с навигацией
│   │   │
│   │   └── auth/                     # Компоненты аутентификации
│   │       ├── LoginForm.vue         # Форма входа (email + password)
│   │       └── RegisterForm.vue      # Форма регистрации нового пользователя
│   │
│   ├── views/                        # 📄 Страницы приложения
│   │   ├── auth/                     # Страницы аутентификации
│   │   │   ├── LoginView.vue         # Страница входа
│   │   │   └── RegisterView.vue      # Страница регистрации
│   │   │
│   │   ├── HomeView.vue              # Главная страница после входа
│   │   ├── DashboardView.vue         # 📊 Дашборд со статистикой
│   │   ├── PracticeView.vue          # 🎯 Практика: вопросы и ответы
│   │   └── ProfileView.vue           # 👤 Профиль пользователя
│   │
│   ├── stores/                       # 📦 Управление состоянием (Pinia)
│   │   ├── auth.js                   # Авторизация: user, token, login, logout
│   │   └── questions.js              # Вопросы: список, статусы, статистика
│   │
│   ├── router/                       # 🚦 Маршрутизация (Vue Router)
│   │   └── index.js                  # Настройка маршрутов и защита (guards)
│   │
│   ├── App.vue                       # 🏠 Корневой компонент приложения
│   ├── main.js                       # 🔧 Точка входа: создание Vue-приложения
│   └── style.css                     # 🎨 Глобальные стили
│
├── index.html                        # 📄 HTML-шаблон
├── package.json                      # 📦 Зависимости и скрипты
├── vite.config.js                    # ⚙️ Конфигурация Vite
└── .env                              # 🔐 Переменные окружения (API_URL)
```

### Полезные команды:
```

```
