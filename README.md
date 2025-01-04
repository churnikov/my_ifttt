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
sudo docker run -v /path/to/source/my_ifttt/my_ifttt/:/code -it tg2readwise python3 /code/setup_tg.py
# Follow instructions
docker-compose up -d --build
```
