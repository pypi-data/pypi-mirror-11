# -*- coding: utf-8 -*-
import uuid
import md5
import os
import traceback
import time
from copy import deepcopy

import redis

from poliglo.utils import select_dict_el, make_request, to_json, json_loads, convert_object_to_unicode

REDIS_KEY_QUEUE = 'queue:%s'
REDIS_KEY_QUEUE_FINALIZED = 'queue:finalized'
REDIS_KEY_INSTANCES = 'workflows:%s:workflow_instances'
REDIS_KEY_ONE_INSTANCE = "workflows:%s:workflow_instances:%s"
REDIS_KEY_INSTANCE_WORKER_FINALIZED_JOBS = "workflows:%s:workflow_instances:%s:workers:%s:finalized"
REDIS_KEY_INSTANCE_WORKER_JOBS = "workflows:%s:workflow_instances:%s:workers:%s:jobs_ids:%s"
REDIS_KEY_INSTANCE_WORKER_ERRORS = "workflows:%s:workflow_instances:%s:workers:%s:errors"
REDIS_KEY_INSTANCE_WORKER_DISCARDED = "workflows:%s:workflow_instances:%s:workers:%s:discarded"

POLIGLO_SERVER_URL_WORKER_CONFIG = "%s/meta_workers/%s/config"
POLIGLO_SERVER_URL_WORKER_WORKFLOWS = "%s/meta_workers/%s/workflows"

# Start Preparation methods
def get_connection(worker_config, target='redis'):
    if target == 'redis':
        return redis.StrictRedis(
            host=worker_config.get('REDIS_HOST'),
            port=worker_config.get('REDIS_PORT'),
            db=worker_config.get('REDIS_DB')
        )

def get_config(master_mind_url, meta_worker):
    _, _, content = make_request(POLIGLO_SERVER_URL_WORKER_CONFIG % (master_mind_url, meta_worker))
    worker_config = json_loads(content)
    return worker_config

def get_worker_workflow_data(worker_workflows, data, worker_id):
    worker_workflow_data = worker_workflows.get(select_dict_el(data, 'workflow_instance.workflow'), {}).get(worker_id, {})

    if worker_workflow_data is None:
        worker_workflow_data = {}
    # TODO: check if deepcopy this is only needed for testing purpose
    return deepcopy(worker_workflow_data)

def prepare_worker(master_mind_url, meta_worker):
    _, _, content = make_request(POLIGLO_SERVER_URL_WORKER_WORKFLOWS % (master_mind_url, meta_worker))
    worker_workflows = json_loads(content)
    worker_config = get_config(master_mind_url, meta_worker)

    connection = get_connection(worker_config)
    return worker_workflows, connection

def get_inputs(data, worker_workflow_data):
    inputs = worker_workflow_data.get('default_inputs', {})
    select_inputs = select_dict_el(worker_workflow_data, 'before.select_inputs', {})
    for input_key, selector in select_inputs.iteritems():
        inputs[input_key] = select_dict_el(data, selector)
    inputs.update(data.get('inputs', {}))
    return inputs

def get_job_data(raw_data, encoding='utf-8'):
    data_to_loads = raw_data
    if not isinstance(raw_data, unicode):
        data_to_loads = raw_data.decode(encoding)
    return json_loads(data_to_loads)

# End Preparation methods

# Start Status and Stats methods

def add_data_to_next_worker(connection, output, raw_data):
    connection.lpush(REDIS_KEY_QUEUE % output, raw_data)

def update_done_jobs(connection, workflow, instance_id, worker_id, job_id):
    connection.sadd(
        REDIS_KEY_INSTANCE_WORKER_JOBS % (workflow, instance_id, worker_id, 'done'),
        job_id
    )

def add_new_job_id(connection, workflow, instance_id, worker, job_id):
    connection.sadd(
        REDIS_KEY_INSTANCE_WORKER_JOBS % (
            workflow, instance_id, worker, 'total'
        ), job_id
    )

def update_workflow_instance(connection, workflow, workflow_instance_id, data=None):
    if data is None:
        data = {}
    pipe = connection.pipeline()
    data['update_time'] = time.time()
    for key, value in data.iteritems():
        pipe.hset(
            REDIS_KEY_ONE_INSTANCE % (workflow, workflow_instance_id),
            key,
            value
        )
    pipe.execute()

def workflow_instance_exists(connection, workflow, workflow_instance_id):
    return connection.exists(REDIS_KEY_ONE_INSTANCE % (workflow, workflow_instance_id))

def stats_add_new_instance(connection, workflow, workflow_instance_info):
    connection.zadd(REDIS_KEY_INSTANCES % workflow, time.time(), to_json(workflow_instance_info))

# End Status and Stats methods


def write_one_output(connection, output_meta_worker, output_worker_id, data):
    new_job_id = str(uuid.uuid4())
    data['jobs_ids'] = data['jobs_ids'] + [new_job_id]
    data['workflow_instance']['worker_id'] = output_worker_id
    data['workflow_instance']['meta_worker'] = output_meta_worker
    add_new_job_id(connection, data['workflow_instance']['workflow'], data['workflow_instance']['id'], output_worker_id, new_job_id)

    add_data_to_next_worker(connection, output_meta_worker, to_json(data))

def prepare_write_output(data, workflow_instance_data, worker_id):
    new_data = deepcopy(data)
    if not new_data['workflow_instance'].get('workers'):
        new_data['workflow_instance']['workers'] = []
    new_data['workflow_instance']['workers'].append(worker_id)
    if not new_data.get('workers_output'):
        new_data['workers_output'] = {}
    new_data['workers_output'][worker_id] = workflow_instance_data
    new_data['inputs'] = workflow_instance_data
    return new_data

def write_outputs(connection, data, workflow_instance_data, worker_workflow_data):
    data = prepare_write_output(data, workflow_instance_data, data['workflow_instance']['worker_id'])
    update_workflow_instance(connection, data['workflow_instance']['workflow'], data['workflow_instance']['id'])
    pipe = connection.pipeline()
    workers_outputs_types = worker_workflow_data.get('__next_workers_types', [])
    for i, output_worker_id in enumerate(worker_workflow_data.get('next_workers', [])):
        write_one_output(connection, workers_outputs_types[i], output_worker_id, data)
    pipe.execute()

def write_finalized_job(data, workflow_instance_data, worker_id, connection):
    data = prepare_write_output(data, workflow_instance_data, worker_id)
    connection.zadd(
        REDIS_KEY_INSTANCE_WORKER_FINALIZED_JOBS % (
            data['workflow_instance']['workflow'], data['workflow_instance']['id'], worker_id
        ),
        time.time(),
        to_json(data)
    )
    connection.lpush(
        REDIS_KEY_QUEUE_FINALIZED,
        to_json({
            'workflow': data['workflow_instance']['workflow'],
            'workflow_instance_id': data['workflow_instance']['id'],
            'workflow_instance_name': data['workflow_instance']['name'],
            'meta_worker': data['workflow_instance']['meta_worker'],
            'worker_id': worker_id
        })
    )

def start_workflow_instance(connection, workflow, start_meta_worker, start_worker_id, workflow_instance_name, data):
    workflow_instance_id = md5.new(workflow_instance_name).hexdigest()

    exists_workflow_instance_before = workflow_instance_exists(connection, workflow, workflow_instance_id)
    if not exists_workflow_instance_before:
        workflow_instance_data = {
            'name': workflow_instance_name,
            'start_time': time.time(),
            'start_worker_id': start_worker_id,
            'start_meta_worker': start_meta_worker
        }
        update_workflow_instance(connection, workflow, workflow_instance_id, workflow_instance_data)
    to_send_data = {
        'inputs': data,
        'workflow_instance': {
            'workflow': workflow,
            'id': workflow_instance_id,
            'name': workflow_instance_name,
            'start_time': time.time(),
            'start_worker_id': start_worker_id,
            'start_meta_worker': start_meta_worker
        },
        'jobs_ids': [],
        'workers_output': {
            'initial': data
        },
        'workers': []
    }

    if not exists_workflow_instance_before:
        stats_add_new_instance(connection, workflow, to_send_data['workflow_instance'])

    write_one_output(connection, start_meta_worker, start_worker_id, to_send_data)

    return workflow_instance_id

def write_error_job(connection, worker_id, raw_data, error):
    metric_name = 'errors'
    try:
        data = json_loads(raw_data)
        if not data.get('workers_error'):
            data['workers_error'] = {}
        data['workers_error'][worker_id] = {
            'error': str(error), 'traceback': traceback.format_exc()
        }
        metric_name = REDIS_KEY_INSTANCE_WORKER_ERRORS % (
            data['workflow_instance']['workflow'], data['workflow_instance']['id'], worker_id
        )
    except Exception, e:
        data = {'workers_error': {}, 'raw_data': raw_data}
        data['workers_error'][worker_id] = {
            'error': 'cannot json_loads', 'traceback': traceback.format_exc()
        }
        metric_name = REDIS_KEY_INSTANCE_WORKER_ERRORS % (
            'unknown', 'unknown', worker_id
        )
    try:
        json_encoded = to_json(data)
    except Exception, e:
        json_encoded = to_json(convert_object_to_unicode(data))
    connection.zadd(metric_name, time.time(), json_encoded)


def default_main_inside(connection, worker_workflows, queue_message, workflow_instance_func, *args, **kwargs):
    if queue_message is not None:
        raw_data = queue_message[1]
        try:
            data = get_job_data(raw_data)
            last_job_id = data['jobs_ids'][-1]
            worker_id = data['workflow_instance']['worker_id']
            worker_workflow_data = get_worker_workflow_data(worker_workflows, data, data['workflow_instance']['worker_id'])
            nodata = True
            for workflow_instance_data in workflow_instance_func(worker_workflow_data, data, *args, **kwargs):
                nodata = False
                if not workflow_instance_data:
                    workflow_instance_data = {}
                if workflow_instance_data.get('__next_workers'):
                    worker_workflow_data['next_workers'] = workflow_instance_data.get('__next_workers', [])
                if len(worker_workflow_data.get('next_workers', [])) == 0:
                    write_finalized_job(data, workflow_instance_data, worker_id, connection)
                    continue
                write_outputs(connection, data, workflow_instance_data, worker_workflow_data)
            if nodata:
                workflow_instance_data = {}
                write_finalized_job(data, workflow_instance_data, worker_id, connection)
            update_done_jobs(
                connection, data['workflow_instance']['workflow'], data['workflow_instance']['id'], worker_id, last_job_id
            )
        except Exception, e:
            worker_id = 'unknown'
            try:
                worker_id = data['workflow_instance']['worker_id']
            except Exception, e:
                pass
            write_error_job(connection, worker_id, raw_data, e)
        # TODO: Manage if worker fails and message is lost

def pre_default_main_inside(
    connection, worker_workflows, meta_worker, workflow_instance_func, *args, **kwargs
):
    queue_message = connection.brpop([REDIS_KEY_QUEUE % meta_worker,])
    default_main_inside(connection, worker_workflows, queue_message, workflow_instance_func, *args, **kwargs)


def default_main(master_mind_url, meta_worker, workflow_instance_func, *args, **kwargs):
    worker_workflows, connection = prepare_worker(master_mind_url, meta_worker)
    if os.environ.get('TRY_INPUT'):
        import pprint
        workflow_id = os.environ.get('WORKFLOW_ID')
        raw_data = open(os.environ.get('TRY_INPUT')).read()
        data = get_job_data(raw_data)
        worker_workflow_data = get_worker_workflow_data(worker_workflows, data, data['workflow_instance']['worker_id'])
        pprint.pprint(list(workflow_instance_func(worker_workflow_data, data, *args, **kwargs)))
        return None
    print ' [*] Waiting for data. To exit press CTRL+C'
    while True:
        pre_default_main_inside(connection, worker_workflows, meta_worker, workflow_instance_func, *args, **kwargs)
