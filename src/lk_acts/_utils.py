import os

from utils import dt, logx

log = logx.get_logger('lk_acts')


def get_dir_name(config):
    year = config['year']
    num = config['num']
    name = config['name']

    name_kebab = dt.to_kebab(name)

    return os.path.join(
        'data',
        f'{year}-{num:04d}-{name_kebab}',
    )


def get_file_name(config, ext):
    dir_config = get_dir_name(config)
    if not os.path.exists(dir_config):
        os.mkdir(dir_config)

    return os.path.join(
        dir_config,
        f'data.{ext}',
    )
