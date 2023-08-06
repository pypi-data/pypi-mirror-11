import os

opj = os.path.join
from ..util.helpers import mkdir
from .local import DRM_Local
from .lsf import DRM_LSF
from .ge import DRM_GE
from .. import TaskStatus, StageStatus, NOOP
import itertools as it
from operator import attrgetter
from ..core.cmd_fxn.signature import call


class JobManager(object):
    def __init__(self, get_submit_args, default_queue=None, cmd_wrapper=None):
        self.drms = dict(local=DRM_Local(self))  # always support local execution
        self.drms['lsf'] = DRM_LSF(self)
        self.drms['ge'] = DRM_GE(self)

        self.local_drm = DRM_Local(self)
        self.running_tasks = []
        self.get_submit_args = get_submit_args
        self.default_queue = default_queue
        self.cmd_wrapper = cmd_wrapper

    def submit(self, task):
        self.running_tasks.append(task)
        # task.status = TaskStatus.waiting

        if hasattr(task, 'cmd_fxn'):
            if self.cmd_wrapper:
                fxn = self.cmd_wrapper(task)(task.cmd_fxn)
            else:
                fxn = task.cmd_fxn
            command = call(fxn, task)
        else:
            command = task.tool._generate_command(task)

        if command == NOOP:
            task.NOOP = True
            task.status = TaskStatus.submitted
        else:
            mkdir(task.log_dir)
            self._create_command_sh(task, command)
            task.drm_native_specification = self.get_submit_args(task, default_queue=self.default_queue)
            assert task.drm is not None, 'task has no drm set'
            self.drms[task.drm].submit_job(task)
            task.status = TaskStatus.submitted

    def submit_tasks(self, tasks):
        # TODO figure out_dir how to parallelize this
        for t in tasks:
            self.submit(t)

            # The implementation below is failing because sqlite won't allow me to query across threads.  This can probably
            # be fixed...  This would allow task functions to be run and submitted concurrently, giving major speedups
            # for large workflows
            #
            # from multiprocessing.pool import ThreadPool
            #
            # p = ThreadPool()
            #
            # def preprocess(task):
            #     command = task.tool._generate_command(task)
            #     if command == NOOP:
            #         task.NOOP = True
            #     else:
            #         task.drm_native_specification = self.get_submit_args(task, default_queue=self.default_queue)
            #     task.status = TaskStatus.waiting
            #     return task, command
            #
            # def submit((task, command)):
            #     mkdir(task.log_dir)
            #     self._create_command_sh(task, command)
            #     self.drms[task.drm].submit_job(task)
            #
            # pre_processed = map(preprocess, tasks)
            # p.map(submit, pre_processed)
            # for t in tasks:
            #     t.status = TaskStatus.submitted

    def terminate(self):
        f = lambda t: t.drm
        for drm, tasks in it.groupby(sorted(self.running_tasks, key=f), f):
            tasks = list(tasks)
            self.drms[drm].kill_tasks(tasks)
            for task in tasks:
                task.status = TaskStatus.killed
                task.stage.status = StageStatus.killed

    def get_finished_tasks(self):
        """
        :returns: A completed task, or None if there are no tasks to wait for
        """
        for t in list(self.running_tasks):
            if t.NOOP:
                self.running_tasks.remove(t)
                yield t
        f = attrgetter('drm')
        for drm, tasks in it.groupby(sorted(self.running_tasks, key=f), f):
            for t in self.drms[drm].filter_is_done(list(tasks)):
                self.running_tasks.remove(t)
                # try:
                # t.update_from_profile_output()
                # except IOError as e:
                #     t.log.info(e)
                #     t.execution.status = ExecutionStatus.failed
                for k, v in self.drms[drm].get_task_return_data(t).items():
                    setattr(t, k, v)
                yield t

    def _create_command_sh(self, task, command):
        """Create a sh script that will execute a command"""
        with open(task.output_command_script_path, 'wb') as f:
            f.write(command)
        os.system('chmod 700 "{0}"'.format(task.output_command_script_path))

        # def get_command_str(self, task):
        #     "The command to be stored in the command.sh script"
        #     return task.output_command_script_path
        #
        #     # p = "psprofile{skip_profile} -w 100 -o {profile_out} {command_script_path}".format(
        #     # profile_out=task.output_profile_path,
        #     #     command_script_path=task.output_command_script_path,
        #     #     skip_profile=' --skip_profile' if task.skip_profile else ''
        #     # )
        #     return p
