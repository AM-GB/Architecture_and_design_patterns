import os
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: template name
    :param folder: the folder where we are looking for the template
    :param kwargs: parameters
    :return:
    """
    # dir = os.path.abspath(os.curdir)
    print(dir)
    # creating an environment object
    env = Environment()
    # specify the folder to search for templates
    env.loader = FileSystemLoader(folder)
    # print(template_name)
    # print("*"*50)
    # we find the template in the environment
    template = env.get_template(template_name)
    print(template)
    # rendering a template with parameters
    return template.render(**kwargs)
