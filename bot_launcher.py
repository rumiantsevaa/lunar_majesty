- name: Show final status
        if: always()
        name: Moon Data Parser and Processor

on:
  workflow_dispatch:

jobs:
  parse-and-process:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run and save parser output
        run: |
          python parse_data.py > moon_data.json
          echo "✅ Данные луны сохранены в moon_data.json"
          ls -la moon_data.json

      - name: Read JSON to env var
        id: json
        run: |
          CONTENT=$(cat moon_data.json | python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin)))')
          echo "MOON_JSON=$CONTENT" >> $GITHUB_ENV
          echo "✅ JSON данные загружены в переменную окружения"

      - name: Launch bot with Selenium
        env:
          PA_USERNAME: ${{ secrets.PA_USERNAME }}
          PA_PASSWORD: ${{ secrets.PA_PASSWORD }}
          MOON_JSON: ${{ env.MOON_JSON }}
        run: |
          echo "🚀 Запуск бота с обработкой данных..."
          python bot_launcher.py

      - name: Verify processed file
        run: |
          if [ -f "moon_data_processed.json" ]; then
            echo "✅ Обработанный файл создан успешно!"
            echo "📊 Размер файла: $(wc -c < moon_data_processed.json) байт"
            echo "📝 Первые 200 символов:"
            head -c 200 moon_data_processed.json
            echo ""
            echo "..."
          else
            echo "❌ Обработанный файл не найден"
            ls -la *.json || echo "Нет JSON файлов"
          fi

      - name: Upload processed result
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: moon-data-processed
          path: |
            moon_data.json
            moon_data_processed.json
          retention-days: 30

      - name: Show final status
        run: |
          echo "📋 Итоговый статус:"
          ls -la *.json || echo "Нет JSON файлов"
          echo "✅ Workflow завершен"
