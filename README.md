HTTP to MQTT
============

Until I figure out how to funnel mqtt from tailscale with auth, this is easier

Send it an a POST payload, it will transfer it to MQTT

```
$ docker build -t http_to_mqtt .
$ docker run -it -p 3000:3000 \
  -e BIND_PORT=3000 \
  -e API_KEY=foo \
  -e MQTT_HOST=mosquitto.my.domain.com \
  http_to_mqtt
```

