import boto3
import sys
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')


def filter_instances(project):
    instances = []

    if project:
         filter = [{'Name':'tag:Project', 'Values':[project]}]
         instances= ec2.instances.filter(Filters=filter)
    else:
        instances=ec2.instances.all()
    return instances




@click.group()
def cli():
    """shotty manages snapshots"""

@cli.group('volumes')
def volumes():
    """Commands for volumes"""


@cli.group('instances')
def instances():
    """Commands for instances"""

@volumes.command('list')
@click.option('--project', default=None, help="Only instances for the project (tag Project:<name>)") 


def list_volumes(project):
    """List Volumes"""

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(f"Volumes: {v}")
 #       tags={t['Key']: t['Value'] for t in i.tags or []}
 #       print(", ".join((
 #           i.id,
 #           i.instance_type,
 #           i.placement['AvailabilityZone'],
 #           i.state['Name'],
 #           i.public_dns_name,
 #           tags.get('Project', '<no project>')
 #           )))
    return

@instances.command('list')
@click.option('--project', default=None, help="Only instances for the project (tag Project:<name>)") 

def list_instances(project):
    """List instances"""

    instances = filter_instances(project)

    for i in instances:
        tags={t['Key']: t['Value'] for t in i.tags or []}
        print(", ".join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))
    return

@instances.command('stop')
@click.option('--project', default=None,
                help='Only instances for prokect')

def stop_instances(project):
    """Stop instances"""

    instances = filter_instances(project)


    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    return

@instances.command('start')
@click.option('--project', default=None, help='Only instance for project')

def start_instances(project):
    """Start instances"""

    instances = filter_instances(project)
    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()
    return




if __name__ == '__main__':
    cli()

