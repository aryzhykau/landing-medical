# Ваша компания — медицинские изделия

Адаптивный лендинг о легализации медицинских изделий, выходе на рынок России и СНГ и запуске производства.

Сайт работает без сборки, npm-зависимостей и серверной части. Готовые файлы находятся в `dist/`.

## Локальный просмотр

```sh
python3 -m http.server 4173 --directory dist
```

Открыть http://localhost:4173.

## Проверка перед публикацией

```sh
node --check dist/app.js
python3 scripts/check_site.py
```

## Автоматическая публикация

Workflow `.github/workflows/deploy-pages.yml` проверяет сайт и публикует содержимое `dist/` в GitHub Pages при каждом push в `main`. Также доступен ручной запуск через Actions → Deploy landing to GitHub Pages → Run workflow.

В настройках репозитория **Settings → Pages → Build and deployment → Source** должен быть выбран **GitHub Actions**. Дополнительные секреты не нужны: публикация использует автоматически предоставляемый `GITHUB_TOKEN` и OIDC.

Для бесплатного аккаунта GitHub репозиторий должен быть публичным. GitHub Pro поддерживает GitHub Pages из приватных репозиториев. Сам сайт GitHub Pages доступен публично.

Документация: [публикация через GitHub Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Изменение контента

- `dist/index.html` — русский текст, название компании, реквизиты и ссылки на контакты.
- `dist/styles.css` — оформление и адаптация под размеры экрана.
- `dist/app.js` — мобильное меню и год в подвале.
- `dist/assets/` — изображение и favicon.

Название «Ваша компания» и реквизиты оставлены временными. Английская и китайская версии будут добавлены после утверждения русского текста; сейчас соответствующие пункты переключателя отключены.

Файл `.openai/hosting.json` хранит идентификатор первоначальной версии в Sites. Workflow GitHub Pages публикует только `dist/`; служебные файлы в сайт не попадают.
