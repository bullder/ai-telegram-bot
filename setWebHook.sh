curl --request POST \
  --url https://api.telegram.org/bot5908670254:${TELEGRAM_TOKEN}/setWebhook \
  --header 'content-type: application/json' \
  --data '{"url": "https://ajk7c7ptkh.execute-api.us-east-1.amazonaws.com/dev/my-custom-url"}'
