# !/usr/bin/env python

import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import ansible.constants as C
from ansible import context
from optparse import Values
from ansible.utils.sentinel import Sentinel


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):
    def __init__(self):
        self.options = {'verbosity': 0, 'ask_pass': False, 'private_key_file': None, 'remote_user': None,
                        'connection': 'smart', 'timeout': 10, 'ssh_common_args': '', 'sftp_extra_args': '',
                        'scp_extra_args': '', 'ssh_extra_args': '', 'force_handlers': False, 'flush_cache': None,
                        'become': False, 'become_method': 'sudo', 'become_user': None, 'become_ask_pass': False,
                        'tags': ['all'], 'skip_tags': [], 'check': False, 'syntax': None, 'diff': False,
                        'inventory': '/Users/caishichao/Code/AnsibleCentrolManagement/inventory/hosts.uat',
                        'listhosts': None, 'subset': None, 'extra_vars': [], 'ask_vault_pass': False,
                        'vault_password_files': [], 'vault_ids': [], 'forks': 5, 'module_path': None, 'listtasks': None,
                        'listtags': None, 'step': None, 'start_at_task': None, 'args': ['fake']}
        self.ops = Values(self.options)

        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()

        self.inventory = InventoryManager(loader=self.loader, sources=[self.options['inventory']])

        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def runansible(self, host_list, task_list):

        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                # options=self.ops,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
                # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreachable'] = {}

        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = json.dumps(result._result)

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result['msg']

        print(results_raw)

    def get_result(self):
        results_raw = {'success': {}, 'failed': {}, "unreachable": {}}

        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = json.dumps(result._result)

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result['msg']

        return results_raw

    def playbookrun(self, host_list, playbook_path, extra_var):

        # self.variable_manager._extra_vars = {'customer': 'test', 'disabled': 'yes'}
        self.variable_manager._extra_vars = extra_var
        sources = ','.join(host_list)
        if len(host_list) == 1:
            sources += ','
        self.inventory = InventoryManager(loader=self.loader, sources=sources)
        context._init_global_context(self.ops)

        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, passwords=self.passwords)
        playbook._tqm._stdout_callback = self.results_callback
        result = playbook.run()
        return result


if __name__ == "__main__":
    a = AnsibleApi()
    host_list = ["192.168.116.131"]
    a.playbookrun(host_list, ["./restart_service.yaml"], {"app": "alertmanager"})
    # host_list = ["10.21.72.64"]
    # host_list = ["10.21.72.217"]
    # a.playbookrun(host_list, ["./perf_deploy.yaml"], {"app": "m3dbnode"})
    print(a.get_result())


    """
    master: 启动ansible  python3 ansi_api_28.py
    node: 查看alert 是否重启
    [root@prome-node01 ~]# grep ansible /var/log/messages
        Jul 24 01:05:17 prome-node01 ansible-systemd: Invoked with no_block=False force=None name=alertmanager daemon_reexec=False enabled=None daemon_reload=False state=restarted masked=None scope=None user=None
    """
