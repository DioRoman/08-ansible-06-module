# 08-ansible-06-module

git clone https://github.com/ansible/ansible.git

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


cd /mnt/c/Users/rlyst/Netology/08-ansible-06-module/my_own_namespace/yandex_cloud_elk

ansible-galaxy collection init my_own_namespace.yandex_cloud_elk

ansible-galaxy collection build

cd /mnt/c/Users/rlyst/Netology/08-ansible-06-module/Test

ansible-galaxy collection install my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz --force

ansible-playbook -i localhost, playbook.yml --connection=local

ansible-galaxy collection init my_own_namespace.yandex_vm


cd /mnt/c/Users/rlyst/Netology/08-ansible-06-module/my_own_namespace/yandex_vm

ansible-galaxy collection build

cd /mnt/c/Users/rlyst/Netology/08-ansible-06-module/test_vm/

ansible-galaxy collection install my_own_namespace-yandex_vm-1.0.0.tar.gz --force

ansible-playbook -i localhost, create_vm.yml --connection=local
