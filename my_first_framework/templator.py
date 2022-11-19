from jinja2 import Template
from os.path import join


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: template name
    :param folder: the folder where we are looking for the template
    :param kwargs: parameters
    :return:
    """
    file_path = join(folder, template_name)
    # Opening the template by name
    with open(file_path, encoding='utf-8') as f:
        # Читаем
        template = Template(f.read())
    # rendering a template with parameters
    return template.render(**kwargs)
