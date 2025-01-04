# Setup telegram

Fill `.env` file with the following

Get TELEGRAM keys from telegram client api docs.
```env
TELEGRAM_API_ID=
TELEGRAM_API_HASH=
READWISE_API_TOKEN=
DEBUG=False
```

```shell
docker build -t tg2readwise .
docker run -v /path/to/code/my-ifttt:/code -it tg2readwise /code/setup_tg.py
# Follow instructions
docker-compose up -d
```
