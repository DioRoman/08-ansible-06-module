# 08-ansible-06-module

# Краткое описание модулей Ansible

## 1. Модуль создания и обновления файла (`my_own_module`)

Модуль предназначен для создания текстового файла по заданному пути с указанным содержимым. Позволяет автоматически создавать родительские директории. Если файл существует, но его содержимое отличается от переданного, модуль перезапишет файл; если содержимое совпадает — изменений не вносит (идемпотентность).

**Основные параметры:**
- `path` — путь к создаваемому файлу;
- `content` — содержимое для записи в файл.

**Ключевые особенности:**
- Создаёт файл с требуемым содержимым, либо обновляет существующий.
- Самостоятельно создаёт директории по пути при необходимости.
- Поддерживает режим проверки (check mode).

---

## 2. Модуль создания виртуальной машины в Yandex Cloud через CLI (`create_vm`)

Модуль автоматизирует создание виртуальной машины (ВМ) в Yandex Cloud с помощью официальной утилиты CLI (`yc`). Проверяет, существует ли ВМ с заданным именем (работает идемпотентно) и создаёт новую только при отсутствии существующей. Поддерживается передача параметров, таких как количество CPU, объём памяти, размер диска, ID образа, зона размещения и путь к публичному SSH-ключу.

**Основные параметры:**
- `folder_id` — идентификатор папки Yandex Cloud;
- `zone` — зона размещения;
- `vm_name` — имя создаваемой ВМ;
- `core_count`, `memory_gb`, `disk_size_gb` — ресурсы ВМ;
- `image_id` — ID образа диска;
- `ssh_key_path` — путь к публичному SSH-ключу.

**Ключевые особенности:**
- Полная идемпотентность (ВМ с тем же именем не пересоздаётся).
- Проверка наличия SSH-ключа и прав на создание ресурсов.
- Перед использованием требует существующих VPC и Подсети (VPC и Subnets).
- Не изменяет существующую ВМ.

---

## Ссылки и скриншоты.

**Collection**

https://github.com/DioRoman/08-ansible-06-module/tree/main/my_own_namespace/yandex_cloud_elk

https://github.com/DioRoman/08-ansible-06-module/tree/main/my_own_namespace/yandex_vm

**tar.gz архив**

https://github.com/DioRoman/08-ansible-06-module/blob/main/test_own_module/my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz

https://github.com/DioRoman/08-ansible-06-module/blob/main/test_vm/my_own_namespace-yandex_vm-1.0.0.tar.gz

Скриншоты

**пункты 4, 6**

<img width="1583" height="195" alt="Снимок экрана 2025-08-07 122602" src="https://github.com/user-attachments/assets/f58eb591-21be-4bd1-9328-044ad54911b2" />

<img width="1574" height="680" alt="Снимок экрана 2025-08-07 122747" src="https://github.com/user-attachments/assets/9fd4f8c6-9e6c-44e9-bc32-db25263efc5e" />

<img width="1601" height="871" alt="Снимок экрана 2025-08-07 123055" src="https://github.com/user-attachments/assets/f9057566-c8e2-49ab-931e-cff170744a6a" />

**пункты 15, 16**

<img width="1585" height="673" alt="Снимок экрана 2025-08-07 125626" src="https://github.com/user-attachments/assets/c8cf642d-0235-44b1-a6a9-5a3ee367f2c7" />

<img width="1911" height="619" alt="Снимок экрана 2025-08-07 101937" src="https://github.com/user-attachments/assets/5045aca6-66d9-4a45-b100-3aa982c77d26" />

<img width="1906" height="525" alt="Снимок экрана 2025-08-07 101943" src="https://github.com/user-attachments/assets/1f2efcf5-f223-4556-8ab8-2b7034ce6551" />

<img width="1765" height="369" alt="Снимок экрана 2025-08-07 101955" src="https://github.com/user-attachments/assets/cae09a68-cc8d-4283-aab2-c3d344aa8bcd" />






