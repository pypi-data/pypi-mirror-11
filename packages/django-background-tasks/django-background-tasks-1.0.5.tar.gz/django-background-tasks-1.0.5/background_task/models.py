from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
import django
import inspect


from django.utils import timezone
from datetime import datetime, timedelta

from hashlib import sha1
import traceback
import logging
from compat import StringIO
from background_task.models_completed import CompletedTask 
import json

 

# inspired by http://github.com/tobi/delayed_job
# 

# Django 1.6 renamed Manager's get_query_set to get_queryset, and the old
# function will be removed entirely in 1.8. We work back to 1.4, so use a
# metaclass to not worry about it.
# from https://github.com/mysociety/mapit/blob/master/mapit/djangopatch.py#L14-L42

try:
    from django.utils import six
except ImportError:  # Django < 1.4.2
    import six 
    
    
if django.get_version() < '1.6':
    class GetQuerySetMetaclass(type):
        def __new__(cls, name, bases, attrs):
            new_class = super(GetQuerySetMetaclass, cls).__new__(cls, name, bases, attrs)

            old_method_name = 'get_query_set'
            new_method_name = 'get_queryset'
            for base in inspect.getmro(new_class):
                old_method = base.__dict__.get(old_method_name)
                new_method = base.__dict__.get(new_method_name)

                if not new_method and old_method:
                    setattr(base, new_method_name, old_method)
                if not old_method and new_method:
                    setattr(base, old_method_name, new_method)

            return new_class
elif django.get_version() < '1.8':
    # Nothing to do, make an empty metaclass
    from django.db.models.manager import RenameManagerMethods

    class GetQuerySetMetaclass(RenameManagerMethods):
        pass
else:
    class GetQuerySetMetaclass(type):
        pass
        
        
class TaskManager(six.with_metaclass(GetQuerySetMetaclass, models.Manager)):
    
    def find_available(self):
        now = timezone.now()
        qs = self.unlocked(now)
        ready = qs.filter(run_at__lte=now, failed_at=None)
        return ready.order_by('-priority', 'run_at')

    def unlocked(self, now):
        max_run_time = getattr(settings, 'MAX_RUN_TIME', 3600)
        qs = self.get_queryset()
        expires_at = now - timedelta(seconds=max_run_time)
        unlocked = Q(locked_by=None) | Q(locked_at__lt=expires_at)
        return qs.filter(unlocked)

    def new_task(self, task_name, args=None, kwargs=None,
                 run_at=None, priority=0):
        args = args or ()
        kwargs = kwargs or {}
        if run_at is None:
            run_at = timezone.now()

        task_params = json.dumps((args, kwargs))
        task_hash = sha1((task_name + task_params).encode()).hexdigest()

        return Task(task_name=task_name,
                    task_params=task_params,
                    task_hash=task_hash,
                    priority=priority,
                    run_at=run_at)

    def get_task(self, task_name, args=None, kwargs=None):
        args = args or ()
        kwargs = kwargs or {}
        task_params = json.dumps((args, kwargs))
        task_hash = sha1(task_name + task_params).hexdigest()
        qs = self.get_queryset()
        return qs.filter(task_hash=task_hash)

    def drop_task(self, task_name, args=None, kwargs=None):
        return self.get_task(task_name, args, kwargs).delete()

@python_2_unicode_compatible
class Task(models.Model):
    # the "name" of the task/function to be run
    task_name = models.CharField(max_length=255, db_index=True)
    # the json encoded parameters to pass to the task
    task_params = models.TextField()
    # a sha1 hash of the name and params, to lookup already scheduled tasks
    task_hash = models.CharField(max_length=40, db_index=True)

    # what priority the task has
    priority = models.IntegerField(default=0, db_index=True)
    # when the task should be run
    run_at = models.DateTimeField(db_index=True)

    # how many times the task has been tried
    attempts = models.IntegerField(default=0, db_index=True)
    # when the task last failed
    failed_at = models.DateTimeField(db_index=True, null=True, blank=True)
    # details of the error that occurred
    last_error = models.TextField(blank=True)

    # details of who's trying to run the task at the moment
    locked_by = models.CharField(max_length=64, db_index=True,
                                 null=True, blank=True)
    locked_at = models.DateTimeField(db_index=True, null=True, blank=True)

    objects = TaskManager()

    def params(self):
        args, kwargs = json.loads(self.task_params)
        # need to coerce kwargs keys to str
        kwargs = dict((str(k), v) for k, v in kwargs.items())
        return args, kwargs

    def lock(self, locked_by):
        now = timezone.now()
        unlocked = Task.objects.unlocked(now).filter(pk=self.pk)
        updated = unlocked.update(locked_by=locked_by, locked_at=now)
        if updated:
            return Task.objects.get(pk=self.pk)
        return None

    def _extract_error(self, type, err, tb):
        file = StringIO()
        traceback.print_exception(type, err, tb, None, file)
        return file.getvalue()

    def reschedule(self, type, err, traceback):
        self.last_error = self._extract_error(type, err, traceback)
        max_attempts = getattr(settings, 'MAX_ATTEMPTS', 25)

        if self.attempts >= max_attempts:
            self.failed_at = timezone.now()
            logging.warn('Marking task %s as failed', self)
        else:
            self.attempts += 1
            backoff = timedelta(seconds=(self.attempts ** 4) + 5)
            self.run_at = timezone.now() + backoff
            logging.warn('Rescheduling task %s for %s later at %s', self,
                backoff, self.run_at)

        # and unlock
        self.locked_by = None
        self.locked_at = None

        self.save()

    def save(self, *arg, **kw):
        # force NULL rather than empty string
        self.locked_by = self.locked_by or None
        return super(Task, self).save(*arg, **kw)

    def __str__(self):
        return u'Task(%s)' % self.task_name

    class Meta:
        db_table = 'background_task'
