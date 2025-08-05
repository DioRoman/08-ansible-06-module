#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_yc_command(params):
    # Формируем команду yc CLI для создания VM
    command = [
        'yc', 'compute', 'instance', 'create',
        '--name', params['vm_name'],
        '--zone', params['zone'],
        '--folder-id', params['folder_id'],
        '--platform', 'standard-v1',
        '--cores', str(params['core_count']),
        '--memory', str(params['memory_gb']),
        '--create-boot-disk', f"size={params['disk_size_gb']}GB,image-family={params['image_family']}",
        '--ssh-key', params['ssh_key']
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return (True, result.stdout)
    except subprocess.CalledProcessError as e:
        return (False, e.stderr)

def main():
    module_args = dict(
        folder_id=dict(type='str', required=True),
        zone=dict(type='str', required=False, default='ru-central1-a'),
        vm_name=dict(type='str', required=True),
        core_count=dict(type='int', required=False, default=2),
        memory_gb=dict(type='int', required=False, default=4),
        image_family=dict(type='str', required=False, default='ubuntu-2004-lts'),
        disk_size_gb=dict(type='int', required=False, default=20),
        ssh_key_path=dict(type='path', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # Читаем содержимое SSH ключа
    try:
        with open(module.params['ssh_key_path'], 'r') as f:
            ssh_key = f.read().strip()
    except Exception as e:
        module.fail_json(msg=f"Не удалось прочитать SSH ключ: {str(e)}")

    params = dict(module.params)
    params['ssh_key'] = ssh_key

    success, output = run_yc_command(params)

    if success:
        module.exit_json(changed=True, msg="ВМ успешно создана", output=output)
    else:
        module.fail_json(msg="Ошибка при создании ВМ", error=output)

if __name__ == '__main__':
    main()
