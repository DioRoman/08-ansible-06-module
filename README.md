# 08-ansible-06-module

cd /mnt/c/Users/rlyst/Netology/08-ansible-06-module

cd /mnt/c/Users/rlyst/Netology/08-ansible-06-module/ansible
python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt
. hacking/env-setup
deactivate

. venv/bin/activate && . hacking/env-setup

python -m ansible.modules.my_own_module payload.json

ansible-playbook -i localhost, test.yml --connection=local

ansible-galaxy collection init my_own_namespace.yandex_cloud_elk

ansible-galaxy collection build