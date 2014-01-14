from flask_principal import Permission, RoleNeed

CONCLUSION_CLASSES = {
    'FV': 'FV',
    'U1': 'U1',
    'U1-': 'U1M',
    'U1+': 'U1P',
    'U2': 'U2',
    'U2-': 'U2M',
    'U2+': 'U2P',
    'XX': 'XX',
    'NA': 'NA',
    'XU': 'XU',
    'U2?': 'U2U',
    'U1?': 'U1U',
    'FV?': 'FVU',
    'XX?': 'XXU',
    'XU?': 'XUU',
}

COUNTRY_ASSESSMENTS = {
    'FV':  'Favourable (FV)',
    'U1':  'Inadequate (U1)',
    'U1-': 'Inadequate and deteriorating (U1-)',
    'U1+': 'Inadequate but improving (U1+)',
    'U2':  'Bad (U2)',
    'U2-': 'Bad and deteriorating (U2-)',
    'U2+': 'Bad but improving (U2+)',
    'XX':  'Unknown (XX)',
    'NA':  'Imposible to be assesed',
}


def get_default_period():
    return '1'


def admin_perm():
    return Permission(RoleNeed('admin'))


def expert_perm():
    return Permission(RoleNeed('expert'))
