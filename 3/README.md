# ДЗ-3

## Как открыть страницу

Для получения доступа к странице с Prometheus требуется подключиться к виртуальной машине по ssh с пробрасыванием портов.

Пример:
```bash
ssh sre-course -L 9090:127.0.0.1:9090
```

Тогда на `localhost:9090` вы сможете увидеть работающий Prometheus.

Для настройки файрвола была использована утилита ufw, [туториал](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands).

## Решение

### Установка Node Exporter

Для этого достаточно выполнить инструкцию из `TASK.pdf`.

Проверить этот пункт можно если открыть в браузере `localhost:9090` и изучить конфиг/метрики.

### Отключение лишних модулей

Согласно [документации](https://github.com/prometheus/node_exporter) по-умолчанию включено очень много коллекторов. Оставим только:
* `cpu`,
* `diskstats`,
* `filesystem`,
* `loadavg`,
* `meminfo`,
* `netstat`,
* `sockstat`,
* `time`.

Сделать это можно если при запуске сервиса добавить `--collector.disable-defaults --collector.<name> ...`. 
Проверить какие модули были в этоге оставлены можно по лейблам метрики `node_scrape_collector_duration_seconds` или заглянув в конфигурацию запуска для Node Exporter в systemd: `/lib/systemd/system/node_exporter.service`.

### Скрипт для Textfile-collector

Мы хотим сделать скрипт, который будет наполнять текстовый файл, который затем будет использовать Textfile-collector. 

Напишем скрипт `get_directory_sizes.py`, который вычисляет размер директорий из заданного списка. Например, так можно следить не стало ли у нас слишком много логов.

Чтобы заставить все это работать требуется регулярно запускать этот скрипт:
1. Переместим скрипт в место для скриптов и дадим ему соответствующие права:
```bash
cp ~/MIPT_SRE/3/get_directory_sizes.py  /usr/local/bin/get_directory_sizes
chmod +x /usr/local/bin/get_directory_sizes 
```
2. Через cron будем запускать скрипт каждую минуту:
```bash
* * * * * root python3 /usr/local/bin/get_directory_sizes
```