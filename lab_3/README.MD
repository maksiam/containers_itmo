1) Ответ на вопрос: важен ли порядок выполнения этих манифестов? Почему?
Да, последовательность выполнения этих манифестов имеет значение, и вот почему:
Сначала необходимо создать ConfigMap, так как он содержит параметры окружения (например, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD), которые понадобятся поду, описанному в Deployment. Эта информация в Deployment передаётся через envFrom, который ссылается на ConfigMap. Если ConfigMap отсутствует на момент создания Deployment, он не сможет загрузить нужные параметры, и контейнеры не запустятся.
Service, как правило, создаётся после ConfigMap, но до Deployment. Он создаёт сетевую инфраструктуру, позволяющую другим компонентам подключаться к базе данных или взаимодействовать внутри кластера. Хотя это не критично для запуска подов Deployment, желательно, чтобы Service был создан заранее, чтобы обеспечить доступность сети сразу после их запуска.
Deployment нужно разворачивать в последнюю очередь, так как он зависит от настроек среды из ConfigMap и предполагает наличие внешнего доступа через сеть, настроенную с помощью Service.
Следовательно, правильная последовательность развертывания манифестов такова:
1. ConfigMap
2. Service
3. Deployment

Нарушение этого порядка может привести к ошибкам: Deployment не сможет получить необходимые настройки из ConfigMap или не будет доступен через Service сразу после запуска.

2) Вопрос: что (и почему) произойдет, если отскейлить количество реплик postgres-deployment в 0, затем обратно в 1, после чего попробовать снова зайти на Nextcloud?
Когда вы уменьшаете количество реплик Postgres до 0, все экземпляры базы данных в кластере прекращают свою работу. В этот период Nextcloud теряет доступ к базе данных, так как она выключена. После того как вы возвращаете количество реплик Postgres обратно к 1, база данных снова запускается. Однако, Nextcloud может по-прежнему испытывать трудности с подключением к базе данных, так как она утрачивала подключение к ней и не повторяет попытку автоматически.

Скриншоты в порядке выполнения работы:  
<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_3/screenshots/photo_5_2024-12-12_20-36-23.jpg" />
</p>

<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_3/screenshots/photo_3_2024-12-12_20-36-23.jpg" />
</p>

<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_3/screenshots/photo_2_2024-12-12_20-36-23.jpg"  />
</p>

<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_3/screenshots/photo_6_2024-12-12_20-36-23.jpg" />
</p>

<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_3/screenshots/photo_4_2024-12-12_20-36-23.jpg"  />
</p>

<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_3/screenshots/photo_8_2024-12-12_20-36-23.jpg"  />
</p>

<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_3/screenshots/photo_1_2024-12-12_20-36-23.jpg" />
</p>

<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_3/screenshots/photo_7_2024-12-12_20-36-23.jpg" />
</p>

