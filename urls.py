from datetime import date
from views import Index, Examples, Page, Contact, ContentList, CreateCategory, \
                    CopyContent, CreateContent


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/exam/': Examples(),
    '/page/': Page(),
    '/contact/': Contact(),
    '/content-list/': ContentList(),
    '/create-content/': CreateContent(),
    '/create-category/': CreateCategory(),
    '/copy-content/': CopyContent(),
}
