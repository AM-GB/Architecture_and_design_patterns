from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: template name
    :param folder: the folder where we are looking for the template
    :param kwargs: parameters
    :return:
    """
    # creating an environment object
    env = Environment()
    # specify the folder to search for templates
    env.loader = FileSystemLoader(folder)
    # we find the template in the environment
    template = env.get_template(template_name)
    # rendering a template with parameters
    return template.render(**kwargs)
