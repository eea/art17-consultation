from flask_principal import Permission, RoleNeed


def get_default_period():
    return '1'


def admin_perm():
    return Permission(RoleNeed('admin'))


def expert_perm():
    return Permission(RoleNeed('expert'))
