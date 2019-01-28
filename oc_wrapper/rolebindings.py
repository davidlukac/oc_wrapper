import json
import subprocess

from typing import List

from oc_wrapper.model.RoleBinding import RoleBinding


class RoleBindings(object):

    def __init__(self, ci_mode=True):
        super(RoleBindings, self).__init__()
        self.ci_mode = ci_mode

    def get(self, namespace=None):
        # type: (str) -> List[RoleBinding]
        if namespace is None:
            namespace_arg = ['--all-namespaces=true']

        else:
            namespace_arg = ['--namespace', str(namespace)]

        cmd = ['oc', 'get', 'rolebindings'] + namespace_arg + ['--output=json']
        cmd_str = ' '.join(cmd)
        print("Calling: '{}'.".format(cmd_str))

        json_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        d = json.loads(json_out)

        bindings = []

        for item in d.get('items'):
            if item.get('kind') == 'RoleBinding':
                bindings.append(RoleBinding(item))

        return bindings

    def has(self, role, group, namespace=None):
        # type: (str, str, str) -> bool
        bindings = self.get(namespace)

        return len([b for b in bindings
                    if b.role_ref.name == role and group in
                    [s.name for s in b.subjects if s.kind.lower() == 'group']]) > 0
