# Домашние задание по лекции тестирование

## Запуск в Docker

```bash
git clone https://github.com/Kargina/hh_api_tests_homework.git
cd hh_api_tests_homework
docker build . -t api_tests
docker run -e HH_API_TOKEN=<YOUR_TOKEN> api_tests
```