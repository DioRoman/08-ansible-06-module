#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import subprocess
import json

def instance_exists(vm_name, folder_id, zone, module):
    try:
        result = subprocess.run([
            'yc', 'compute', 'instance', 'list',
            '--folder-id', folder_id,
            '--format', 'json'
        ], check=True, capture_output=True, text=True)
        data = json.loads(result.stdout)
        return any(inst['name'] == vm_name for inst in data)
    except subprocess.CalledProcessError as e:
        if e.stdout:
            try:
                data = json.loads(e.stdout)
                return any(inst['name'] == vm_name for inst in data)
            except Exception:
                pass
        return False
    except Exception as e:
        module.fail_json(msg=f"Не удалось проверить существование ВМ '{vm_name}': {str(e)}")

def run_yc_command(params):
    """
    Создаёт ВМ с заданными параметрами.
    """
    command = [
        'yc', 'compute', 'instance', 'create',
        '--name', params['vm_name'],
        '--zone', params['zone'],
        '--folder-id', params['folder_id'],
        '--platform', 'standard-v1',
        '--cores', str(params['core_count']),
        '--memory', str(params['memory_gb']),
        '--create-boot-disk', f"size={params['disk_size_gb']}GB,image-id={params['image_id']}",
        '--ssh-key', params['ssh_key_path'],
        '--preemptible'
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    module_args = dict(
        folder_id=dict(type='str', required=True),
        zone=dict(type='str', default='ru-central1-a'),
        vm_name=dict(type='str', required=True),
        core_count=dict(type='int', default=2),
        memory_gb=dict(type='int', default=4),
        image_id=dict(type='str', required=True),
        disk_size_gb=dict(type='int', default=20),
        ssh_key_path=dict(type='path', required=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    ssh_key_path = module.params['ssh_key_path']
    try:
        with open(ssh_key_path, 'r'):
            pass
    except Exception as e:
        module.fail_json(msg=f"Файл SSH-ключа не найден или недоступен: {ssh_key_path}\nОшибка: {str(e)}")

    # Проверяем существование ВМ (идемпотентность)
    exists = instance_exists(
        module.params['vm_name'],
        module.params['folder_id'],
        module.params['zone'],
        module
    )
    if exists:
        module.exit_json(changed=False, msg="ВМ уже существует — изменений не требуется")

    # Если ВМ нет — создаём
    success, output = run_yc_command(module.params)
    if success:
        module.exit_json(changed=True, msg="ВМ успешно создана", output=output)
    else:
        module.fail_json(msg="Ошибка при создании ВМ", error=output)

if __name__ == '__main__':
    main()
