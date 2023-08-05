import getpass
import ConfigParser
import logging
import sys
import time
from os.path import join, expanduser
import traceback

import service.auth
import service.instance
import service.provider
import service.macfile
import service.infrastructure
import maccli.facade.macfile
import maccli.service.configuration
import maccli.helper.macfile
from view.view_generic import show_error, show
import view.view_location
import view.view_instance
import view.view_cookbook
import view.view_generic
import view.view_resource
import view.view_infrastructure
import maccli.view.view_hardware
from config import AUTH_SECTION, USER_OPTION, APIKEY_OPTION, MAC_FILE, EXCEPTION_EXIT_CODE, CONFIGURATION_FAILED, \
    CREATION_FAILED
from maccli.helper.exception import MacParseEnvException, MacErrorCreatingTier, MacParseParamException, \
    MacResourceException


def help():
    view.view_generic.general_help()


def login():
    try:
        view.view_generic.show("")
        view.view_generic.show("If you don't have credentials, please register at https://manageacloud.com")
        view.view_generic.show("")
        username = raw_input("Username or email: ")
        password = getpass.getpass()

        user, api_key = service.auth.authenticate(username, password)
        if api_key is not None:
            config = ConfigParser.ConfigParser()
            config.add_section(AUTH_SECTION)
            config.set(AUTH_SECTION, USER_OPTION, user)
            config.set(AUTH_SECTION, APIKEY_OPTION, api_key)
            with open(join(expanduser('~'), MAC_FILE), 'w') as cfgfile:
                config.write(cfgfile)
            print("Login succeeded!")

    except KeyboardInterrupt as e:
        show_error("")
        show_error("Authentication cancelled.")

    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def no_credentials():
    show("You need to login into Manageacloud.com")
    show()
    show("    mac login")
    show()
    show("If you do not have an account, you can register one at https://manageacloud.com/register")


def instance_list():
    try:
        json = service.instance.list_instances()
        view.view_instance.show_instances(json)

    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_ssh(ids, command):
    try:
        for instance_id in ids:
            if command is None:
                service.instance.ssh_interactive_instance(instance_id)
            else:
                service.instance.ssh_command_instance(instance_id, command)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_create(cookbook_tag, deployment, location, servername, provider, release, branch, hardware, lifespan,
                    environments, hd, port):
    try:
        if cookbook_tag is None:
            view.view_instance.show_instance_create_help()

        elif location is None:
            locations_json = service.provider.list_locations(cookbook_tag, provider, release)
            if locations_json is not None:
                show()
                show("--location parameter not set. You must choose the location.")
                show()
                show("Available locations:")
                show()
                if len(locations_json):
                    view.view_location.show_locations(locations_json)
                    view.view_instance.show_create_example_with_parameters(cookbook_tag, deployment,
                                                                           locations_json[0]['id'], servername,
                                                                           provider, release, branch, hardware)

                else:
                    show("There is not locations available for configuration %s and provider %s" % (
                        cookbook_tag, provider))

                view.view_instance.show_instance_help()
        elif deployment == "production" and hardware is None or \
                                        deployment == "testing" and provider is not "manageacloud" and hardware is None:
            hardwares = service.provider.list_hardwares(provider, location, cookbook_tag, release)
            show()
            show("--hardware not found. You must choose the hardware.")
            show()
            show("Available hardware:")
            show()
            view.view_hardware.show_hardwares(hardwares)
            if (len(hardwares) > 0):
                view.view_instance.show_create_example_with_parameters(cookbook_tag, deployment, location, servername,
                                                                       provider, release, branch, hardwares[0]['id'])
        else:
            """ Execute create instance """
            instance = service.instance.create_instance(cookbook_tag, deployment, location, servername, provider,
                                                        release,
                                                        branch, hardware, lifespan, environments, hd, port)
            if instance is not None:
                view.view_instance.show_instance(instance)

            view.view_generic.show("")
            view.view_generic.show("To monitor the creation progress:")
            view.view_generic.show("")
            view.view_generic.show("watch mac instance list")
            view.view_generic.show("")
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_destroy_help():
    view.view_instance.show_instance_destroy_help()


def instance_update_help():
    view.view_instance.show_instance_update_help()


def instance_ssh_help():
    view.view_instance.show_instance_ssh_help()


def instance_destroy(ids):
    try:
        maccli.logger.debug("Destroying instances %s " % ids)
        instances = []
        for instance_id in ids:
            maccli.logger.debug("Destroying instance %s " % instance_id)
            instance = service.instance.destroy_instance(instance_id)
            instances.append(instance)

        if instances is not None:
            view.view_instance.show_instances(instances)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_update(ids):
    try:
        maccli.logger.debug("Updating instances %s " % ids)
        instances = []
        for instance_id in ids:
            maccli.logger.debug("Updating instance %s " % instance_id)
            instance = service.instance.update_configuration("", instance_id)
            instances.append(instance)

        if instances is not None:
            view.view_instance.show_instances(instances)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_help():
    view.view_instance.show_instance_help()


def configuration_list():
    try:
        configurations = service.configuration.list_configurations()
        view.view_cookbook.show_configurations(configurations)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def configuration_search(keywords, show_url):
    try:
        configurations = service.configuration.search_configurations(keywords)
        if show_url:
            view.view_cookbook.show_configurations_url(configurations)
        else:
            view.view_cookbook.show_configurations(configurations)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def configuration_help():
    view.view_cookbook.show_configurations_help()


def convert_to_yaml(args):
    yaml = service.macfile.convert_args_to_yaml(args)
    view.view_generic.show(yaml)


def process_macfile(file, resume, params, quiet, on_failure):
    try:

        raw = maccli.service.macfile.load_macfile(file)
        try:
            raw = maccli.service.macfile.parse_params(raw, params)
        except MacParseParamException, e:
            view.view_generic.show_error(e.message)
            exit(11)

        root, roles, infrastructures, actions, resources = maccli.service.macfile.parse_macfile(raw)

        if not resume:

            existing_instances = service.instance.list_by_infrastructure(root['name'], root['version'])

            if len(existing_instances) > 0:
                view.view_generic.show()
                view.view_generic.show()
                view.view_generic.show_error(
                    "There are active instances for infrastructure %s and version %s" % (root['name'], root['version']))
                view.view_generic.show()
                view.view_generic.show()
                view.view_instance.show_instances(existing_instances)
                view.view_infrastructure.show_infrastructure_resources(infrastructures, [])
                view.view_generic.show()
                view.view_generic.show()
                view.view_generic.show(
                    "Instances must be destroyed before attempting to create another "
                    "infrastructure using the same version.")
                view.view_generic.show("")
                view.view_generic.show("To destroy instances:")
                view.view_generic.show("    mac instance destroy <instance id or name>")
                view.view_generic.show("")
                exit(7)

            if quiet:
                view.view_generic.show("Infrastructure %s version %s" % (root['name'], root['version']))
            else:
                view.view_generic.header("Infrastructure %s version %s" % (root['name'], root['version']), "=")

            roles_created = {}
            try:
                """ Create all the servers """
                maccli.logger.debug("Create servers")
                for infrastructure_key in infrastructures:
                    infrastructure = infrastructures[infrastructure_key]
                    maccli.logger.debug("Processing infrastructure %s" % infrastructure_key)

                    # type of infrastructure manageacloud instance
                    if 'role' in infrastructure:
                        maccli.logger.debug("Type role")
                        infrastructure_role = infrastructure['role']
                        if quiet:
                            view.view_generic.show(
                                "[%s][%s] Infrastructure tier" % (infrastructure_key, infrastructure['role']))
                        else:
                            view.view_generic.header(
                                "[%s][%s] Infrastructure tier" % (infrastructure_key, infrastructure['role']))
                        role_raw = roles[infrastructure_role]["instance create"]
                        metadata = service.instance.metadata(root, infrastructure_key, infrastructure_role, role_raw,
                                                             infrastructure)
                        instances = maccli.facade.macfile.create_tier(role_raw, infrastructure, metadata, quiet)
                        roles_created[infrastructure_role] = instances



            except MacErrorCreatingTier:
                view.view_generic.show_error("ERROR: An error happened while creating tier. Server failed.")
                view.view_generic.show_error("HINT: Use 'mac instance log <instance id>' for details")
                view.view_generic.show("Task raised errors.")
                exit(5)

            except MacParseEnvException as e:
                view.view_generic.show_error(
                    "ERROR: An error happened parsing environments." + str(type(e)) + str(e.args))
                view.view_generic.show("Task raised errors.")
                exit(6)

        finish = False
        infrastructure_resources_failed = False
        infrastructure_resources_processed = []  # looks for the non-instance infrastructure
        while not finish:
            processing_instances = service.instance.list_by_infrastructure(root['name'], root['version'])
            if not quiet:
                view.view_generic.clear()
                view.view_instance.show_instances(processing_instances)
                view.view_infrastructure.show_infrastructure_resources(infrastructures, infrastructure_resources_processed)

            # apply configuration to the instances
            maccli.facade.macfile.apply_instance_infrastructure_changes(processing_instances, root['name'], root['version'], quiet, infrastructures, infrastructure_resources_processed)

            # check instances has been processed
            finish = True
            for instance in processing_instances:
                if not (instance['status'].startswith("Ready") or instance['status'] == CREATION_FAILED or instance['status'] == CONFIGURATION_FAILED):
                    finish = False
                if on_failure is not None and (instance['status'] == CREATION_FAILED or instance['status'] == CONFIGURATION_FAILED):
                    finish = True

            # process resources
            try:
                processed_resources_part, finish_resources = maccli.facade.macfile.apply_resources(processing_instances, infrastructure_resources_processed, processing_instances, roles, infrastructures, actions, resources, quiet)
                maccli.logger.debug("Resources processed this run: %s " % processed_resources_part)
                infrastructure_resources_processed = infrastructure_resources_processed + processed_resources_part
                maccli.logger.debug("Total resources processed: %s " % infrastructure_resources_processed)
                finish = finish and finish_resources
            except MacResourceException:
                infrastructure_resources_failed = True
                finish = True

            if not finish:
                time.sleep(3)

        instances_processed = service.instance.list_by_infrastructure(root['name'], root['version'])
        if not quiet:
            view.view_generic.clear()
        view.view_instance.show_instances(instances_processed)
        view.view_infrastructure.show_infrastructure_resources(infrastructures, infrastructure_resources_processed)
        view.view_generic.show("")
        view.view_resource.show_resources(infrastructure_resources_processed)

        # Clean up if failure
        instances_failed = maccli.facade.macfile.clean_up(instances_processed, on_failure)

        if instances_failed or infrastructure_resources_failed:
            view.view_generic.show("")
            view.view_generic.show("Infrastructure failed.")
            view.view_generic.show("")
            view.view_generic.show("Logs available at")
            view.view_generic.show("    mac instance log <instance id or name>")
            exit(12)
        else:
            view.view_generic.show("Infrastructure created successfully.")
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            traceback.print_exc(file=sys.stdout)
        else:
            show_error(e)

        sys.exit(EXCEPTION_EXIT_CODE)


def instance_fact(instance_id):
    try:
        json = service.instance.facts(instance_id)
        view.view_instance.show_facts(json)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_log(instance_id):
    try:
        json = service.instance.log(instance_id)
        view.view_instance.show_logs(json)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_lifespan(instance_id, amount):
    try:
        instance = service.instance.lifespan(instance_id, amount)
        view.view_instance.show_instance(instance)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_list():
    try:
        infrastructure = service.infrastructure.list_infrastructure()
        view.view_infrastructure.show_infrastructure(infrastructure)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_search(name, version):
    try:
        infrastructure = service.infrastructure.search_instances(name, version)
        view.view_infrastructure.show_infrastructure_instances(infrastructure)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_lifespan(amount, name, version):
    try:
        infrastructure = service.infrastructure.lifespan(amount, name, version)
        view.view_infrastructure.show_infrastructure_instances(infrastructure)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)
