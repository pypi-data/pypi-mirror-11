import os
import tempfile

import pexpect

import maccli.dao.api_instance
import maccli.helper.cmd
import maccli.helper.simplecache
from maccli.helper.exception import InstanceDoesNotExistException, InstanceNotReadyException


def list_instances():
    """
        List available instances in the account
    """
    return maccli.dao.api_instance.get_list()


def list_by_infrastructure(name, version):
    instances = maccli.dao.api_instance.get_list()
    filtered_instances = []
    for instance in instances:
        if 'metadata' in instance and 'infrastructure' in instance['metadata'] and 'name' in instance['metadata'][
            'infrastructure']:
            infrastructure_name = instance['metadata']['infrastructure']['name']
        else:
            infrastructure_name = ""

        if 'metadata' in instance and 'infrastructure' in instance['metadata'] and 'version' in instance['metadata'][
            'infrastructure']:
            infrastructure_version = instance['metadata']['infrastructure']['version']
        else:
            infrastructure_version = ""

        if infrastructure_name == name and infrastructure_version == version:
            filtered_instances.append(instance)

    return filtered_instances


def ssh_command_instance(instance_id, cmd):

    rc, stdout, stderr = -1, "", ""
    cache_hash = maccli.helper.simplecache.hash_value(cmd)
    cache_key = 'ssh_%s_%s' % (instance_id, cache_hash)
    cached_value = maccli.helper.simplecache.get(cache_key)  # read from cache

    if cached_value is not None:
        rc = cached_value['rc']
        stdout = cached_value['stdout']
        stderr = cached_value['stderr']
    else:

        instance = maccli.dao.api_instance.credentials(instance_id)

        if instance is None:
            raise InstanceDoesNotExistException(instance_id)

        if not (instance['privateKey'] or instance['password']):
            raise InstanceNotReadyException(instance_id)

        if instance is not None and (instance['privateKey'] or instance['password']):
            if instance['privateKey']:
                tmp_fpath = tempfile.mkstemp()
                try:
                    with open(tmp_fpath[1], "wb") as f:
                        f.write(bytes(instance['privateKey']))

                    command = "ssh %s@%s -i %s %s" % (instance['user'], instance['ip'], f.name, cmd)
                    rc, stdout, stderr = maccli.helper.cmd.run(command)

                finally:
                    os.remove(tmp_fpath[1])
            else:
                """ Authentication with password """
                print("NOT IMPLEMENTED")
                exit(1)
                # command = "ssh %s@%s %s" % (instance['user'], instance['ip'], cmd)
                # child = pexpect.spawn(command)
                # i = child.expect(['.* password:', "yes/no"], timeout=60)
                # if i == 1:
                #     child.sendline("yes")
                #     child.expect('.* password:', timeout=60)
                #
                # child.sendline(instance['password'])
                # child.interact()

        # save cache
        if not rc:
            cached_value = {
                'rc': rc,
                'stdout': stdout,
                'stderr': stderr
            }
            maccli.helper.simplecache.set_value(cache_key, cached_value)

    return rc, stdout, stderr


def ssh_interactive_instance(instance_id):
    """
        ssh to an existing instance for an interactive session
    """
    stdout = None
    instance = maccli.dao.api_instance.credentials(instance_id)

    if instance is not None:

        if instance['privateKey']:
            """ Authentication with private key """
            tmp_fpath = tempfile.mkstemp()
            try:
                with open(tmp_fpath[1], "wb") as f:
                    f.write(bytes(instance['privateKey']))

                command = "ssh %s@%s -i %s " % (instance['user'], instance['ip'], f.name)
                os.system(command)

            finally:
                os.remove(tmp_fpath[1])

        else:
            """ Authentication with password """
            command = "ssh %s@%s" % (instance['user'], instance['ip'])
            child = pexpect.spawn(command)
            i = child.expect(['.* password:', "yes/no"], timeout=60)
            if i == 1:
                child.sendline("yes")
                child.expect('.* password:', timeout=60)

            child.sendline(instance['password'])
            child.interact()

    return stdout

def create_instance(cookbook_tag, deployment, location, servername, provider, release, branch, hardware, lifespan,
                    environments, hd, port, metadata=None, applyChanges=True):
    """
        List available instances in the account
    """
    return maccli.dao.api_instance.create(cookbook_tag, deployment, location, servername, provider, release, branch,
                                          hardware, lifespan, environments, hd, port, metadata, applyChanges)


def destroy_instance(instanceid):
    """

    Destroy the server

    :param servername:
    :return:
    """
    return maccli.dao.api_instance.destroy(instanceid)


def credentials(servername, session_id):
    """

    Gets the server credentials: public ip, username, password and private key

    :param instance_id;
    :return:
    """
    return maccli.dao.api_instance.credentials(servername, session_id)


def facts(instance_id):
    """

    Returns facts about the system

    :param instance_id;
    :return:
    """
    return maccli.dao.api_instance.facts(instance_id)


def log(instance_id):
    """

    Returns server logs

    :param instance_id;
    :return:
    """
    return maccli.dao.api_instance.log(instance_id)


def lifespan(instance_id, amount):
    """

    Set new instance lifespan

    :param instance_id;
    :return:
    """
    return maccli.dao.api_instance.update(instance_id, amount)


def _get_environment(role, infrastructure):
    environment = None

    if 'environment' in role.keys():
        environment = role['environment']

    if 'environment' in infrastructure.keys():
        if environment is not None:
            environment = environment + infrastructure["environment"]
        else:
            environment = infrastructure["environment"]

    return environment


def metadata(macfile_root, infrastructure_key, role_key, role, infrastructure):
    """
    Generate the json metadata to create an instance
    """
    meta = macfile_root
    meta['macfile_role_name'] = role_key
    meta['macfile_infrastructure_name'] = infrastructure_key
    environment = _get_environment(role, infrastructure)
    if environment is not None:
        meta['environment_raw'] = environment
    return meta


def update_configuration(cookbook_tag, instance_id, new_metadata=None):
    """
    Update server configuration with given cookbook

    :param cookbook_tag:
    :param instance_id:
    :return:
    """

    return maccli.dao.api_instance.update_configuration(cookbook_tag, instance_id, new_metadata)