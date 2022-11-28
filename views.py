from my_first_framework.templator import render

context = {
    'title': '',
    'logoname1': 'Свой',
    'logoname2': 'сайт',
    'logotext': 'Реализация сайта на своем wsgi-фреймворке',
    'menu1': 'Домашняя',
    'menu2': 'Примеры',
    'menu3': 'Текст',
    'menu4': 'Контакты',
}

def menu_selected(context = {}, number_menu_tabs=0, menu_tab_number=0):
    for n in range(1, number_menu_tabs+1):
        selected = f'selected{n}'
        if n == menu_tab_number:
            context[selected] = 'selected'
        else:
            context[selected] = ''
    return context

class Index:
    def __call__(self, request):
        context['title'] = 'Домашняя'
        menu_selected(context, 4, 1)
        return '200 OK', render('index.html', context=context)


class Examples:
    def __call__(self, request):
        context['title'] = 'Примеры'
        menu_selected(context, 4, 2)
        return '200 OK', render('examples.html', context=context)


class Page:
    def __call__(self, request):
        context['title'] = 'Страница'
        menu_selected(context, 4, 3)
        return '200 OK', render('page.html', context=context)


class Contact:
    def __call__(self, request):
        context['title'] = 'Контакты'
        menu_selected(context, 4, 4)
        print(context)
        return '200 OK', render('contact.html', context=context)
