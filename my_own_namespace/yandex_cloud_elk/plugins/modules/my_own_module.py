#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

version_added: "1.0.0"

description: >
    This module creates a text file at a given path with provided content.

options:
    path:
        description: Path where the text file will be created.
        required: true
        type: str
    content:
        description: Content to write into the file.
        required: true
        type: str
    new:
        description:
            - Ignored. Left for compatibility.
        required: false
        type: bool

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Create file with content
  my_namespace.my_collection.my_test:
    path: "/tmp/testfile.txt"
    content: "Hello, world!"
'''

RETURN = r'''
changed:
    description: Whether the file was created or updated.
    type: bool
    returned: always
path:
    description: Path of the file.
    type: str
    returned: always
content:
    description: Content written to the file.
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    result['path'] = path
    result['content'] = content

    changed = False

    # Check existence and content only if not in check mode
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                current = f.read()
            if current != content:
                changed = True
        except Exception as e:
            module.fail_json(msg="Could not read existing file: %s" % str(e), **result)
    else:
        changed = True

    if module.check_mode:
        result['changed'] = changed
        module.exit_json(**result)

    if changed:
        # Make sure directory exists
        parent = os.path.dirname(path)
        if parent and not os.path.exists(parent):
            try:
                os.makedirs(parent)
            except Exception as e:
                module.fail_json(msg="Failed to create directory %s: %s" % (parent, str(e)), **result)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            module.fail_json(msg="Failed to write file: %s" % str(e), **result)
        result['changed'] = True
    else:
        result['changed'] = False

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
