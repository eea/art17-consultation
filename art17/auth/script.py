from flask.ext.script import Manager, Option
from flask.ext.security.script import (
    CreateUserCommand as BaseCreateUserCommand,
    CreateRoleCommand,
    AddRoleCommand,
    RemoveRoleCommand,
    DeactivateUserCommand,
    ActivateUserCommand,
)
from art17.auth import plone_acl_manager
from art17.auth.common import get_ldap_user_info
from art17 import models


class CreateUserCommand(BaseCreateUserCommand):

    option_list = BaseCreateUserCommand.option_list + (
        Option('-i', '--id', dest='id', default=None),
        Option('-l', '--ldap', dest='is_ldap', action='store_true'),
        Option('-n', '--name', dest='name'),
    )

    def run(self, **kwargs):
        user_id = kwargs['id']
        is_ldap_user = kwargs['is_ldap']

        if is_ldap_user:
            ldap_user_info = get_ldap_user_info(user_id)
            if ldap_user_info is None:
                print "No such LDAP user: %r" % user_id
                return
            kwargs['password'] = 'password is ignored'
            kwargs['email'] = ldap_user_info['email']

        super(CreateUserCommand, self).run(**kwargs)

        if is_ldap_user:
            models.RegisteredUser.query.get(user_id).password = None
            models.db.session.commit()


user_manager = Manager()
user_manager.add_command('create', CreateUserCommand())
user_manager.add_command('deactivate', DeactivateUserCommand())
user_manager.add_command('activate', ActivateUserCommand())


@user_manager.command
def ls():
    for user in models.RegisteredUser.query:
        print "{u.id} <{u.email}>".format(u=user)


@user_manager.command
def activate(user_id):
    from art17.auth.common import set_user_active
    user = models.RegisteredUser.query.get(user_id)
    set_user_active(user, True)
    print "user", user.id, "has been activated"
    if not user.is_ldap:
        print "user", user.id, "has been created in Plone"


@user_manager.command
def deactivate(user_id):
    from art17.auth.common import set_user_active
    user = models.RegisteredUser.query.get(user_id)
    set_user_active(user, False)
    print "user", user.id, "has been deactivated"
    if not user.is_ldap:
        print "user", user.id, "has been removed from Plone"


@user_manager.command
def remove(user_id):
    user = models.RegisteredUser.query.get(user_id)
    models.db.session.delete(user)
    models.db.session.commit()


@user_manager.command
def info(user_id):
    user = models.RegisteredUser.query.get(user_id)
    print user.id
    print "name: %r" % user.name
    print "active:", user.active
    print "ldap:", user.is_ldap
    print "roles:", [r.name for r in user.roles]


@user_manager.command
def reset_password(user_id):
    from flask.ext.security.utils import encrypt_password
    user = models.RegisteredUser.query.get(user_id)
    if user.is_ldap:
        print "Can't change password for EIONET users"
        return
    plaintext_password = raw_input("new password: ").decode('utf-8')
    user.password = encrypt_password(plaintext_password)
    models.db.session.commit()
    print "password for %s has been changed" % user_id
    if user.active:
        plone_acl_manager.edit(user_id, plaintext_password)
        print "The Plone password has been changed"


role_manager = Manager()
role_manager.add_command('create', CreateRoleCommand())
role_manager.add_command('add', AddRoleCommand())
role_manager.add_command('remove', RemoveRoleCommand())


@role_manager.command
def ls():
    for role in models.Role.query:
        print "{r.name}: {r.description}".format(r=role)


@role_manager.command
def members(role):
    role_ob = models.Role.query.filter_by(name=role).first()
    if role_ob is None:
        print 'No such role %r' % role
        return
    for user in role_ob.users:
        print "{u.id} <{u.email}>".format(u=user)
