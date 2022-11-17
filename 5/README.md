# ДЗ-5

## Как открыть страницу ElasticSearch

Для получения доступа к странице с Prometheus требуется подключиться к виртуальной машине по ssh с пробрасыванием портов.

Пример:
```bash
ssh sre-course -L 5601:127.0.0.1:5601
```

Тогда на `localhost:5601` вы сможете увидеть работающий Elasticsearch.

Для настройки файрвола была использована утилита ufw, [туториал](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands).

## Решение

1. Перенос сервиса из HW-4 на порт 9199. В противном случае 9200 оказывается занят, а это стандартный порт для Elasticsearch. 
   Я пробовал сконфигурировать Elasticsearch и Kibana так чтобы Elastic находился на другом порту, но у меня возникли проблемы.
2. Уменьшение размера heap для jvm при старте Elasticsearch до 1ГБ. Иначе почти вся память машины оказывается занята.
   Настройки положил в `/etc/elasticserach/jvm.options.d/jvm.options`. Инструкцию по настройке прочитал в `etc/elasticsearch/jvm.options`.
3. Подготовка данных для входа в ElasticSearch. Сейчас они лежат в `/home/ubuntu/kibana/kibana-access.txt` по аналогии с действиями в тексте задания.
