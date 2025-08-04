#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import subprocess
import json

def run_yc_command(args):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        return None, err.decode()
    return out.decode(), None

def main():
    module_args = dict(
        name=dict(type='str', required=True),
        folder_id=dict(type='str', required=True),
        zone=dict(type='str', required=True),
        platform=dict(type='str', default='standard-v1'),
        cores=dict(type='int', default=2),
        memory=dict(type='int', default=4),
        disk_size=dict(type='int', default=16),
        image_family=dict(type='str', required=True),
        image_folder_id=dict(type='str', required=False, default=None),
        network_id=dict(type='str', required=True),
        subnet_id=dict(type='str', required=True),
        service_account=dict(type='str', required=False, default=None)
    )

    result = dict(changed=False)

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Формируем команду для yc cli
    cmd = [
        'yc', 'compute', 'instance', 'create',
        '--name', module.params['name'],
        '--folder-id', module.params['folder_id'],
        '--zone', module.params['zone'],
        '--platform', module.params['platform'],
        '--cores', str(module.params['cores']),
        '--memory', f"{module.params['memory']}G",
        '--create-boot-disk', f"type=network-ssd,size={module.params['disk_size']}GB,image-family={module.params['image_family']}"
    ]

    if module.params['image_folder_id']:
        cmd[-1] += f",image-folder-id={module.params['image_folder_id']}"

    cmd += ['--network-interface', f"subnet-id={module.params['subnet_id']}"]

    if module.params['service_account']:
        cmd += ['--service-account-id', module.params['service_account']]

    if module.check_mode:
        module.exit_json(changed=True, meta=cmd)

    out, err = run_yc_command(cmd)
    if err:
        module.fail_json(msg='yc create failed: ' + err)
    result['changed'] = True
    result['output'] = json.loads(out) if out else out
    module.exit_json(**result)

if __name__ == '__main__':
    main()
