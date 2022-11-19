from my_first_framework.templator import render

context = {
    'logoname1': 'Свой',
    'logoname2': 'сайт',
    'logotext': 'Реализация сайта на своем wsgi-фреймворке',
    'menu1': 'Домашняя',
    'menu2': 'Примеры',
    'menu3': 'Текст',
    'menu4': 'Контакты',
}


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', context=context)


class Examples:
    def __call__(self, request):
        return '200 OK', render('examples.html', context=context)


class Page:
    def __call__(self, request):
        return '200 OK', render('page.html', context=context)


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', context=context)
