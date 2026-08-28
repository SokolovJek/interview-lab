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
|  ├── src/
|  ├── api/
|  │   └── auth.js
|  ├── components/
|  │   └── auth/
|  │       ├── RegisterForm.vue
|  │       └── LoginForm.vue
|  ├── views/
|  │   └── auth/
|  │       ├── RegisterView.vue
|  │       └── LoginView.vue
|  ├── stores/
|  │   └── auth.js
|  ├── router/
|  │   └── index.js
|  ├── App.vue
|  └── main.js
├── index.html
├── package.json
└── vite.config.js
```

### Полезные команды:
```

```