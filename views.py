from my_first_framework.templator import render

from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')

context = {
    'title': '',
    'logoname1': 'Свой',
    'logoname2': 'сайт',
    'logotext': 'Реализация сайта на своем wsgi-фреймворке',
    'menu1': 'Домашняя',
    'menu2': 'Примеры',
    'menu3': 'Текст',
    'menu4': 'Контакты',
    'objects_list': site.categories,
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
        context['list_categories'] = site.categories
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


class ContentList:
    def __call__(self, request):
        logger.log('list content')
        try:
            # print(request)
            print(request['params']['id'])
            category = site.find_category_by_id(
                int(request['params']['id']))
            print(category)
            return '200 OK', render('content_list.html', context = context,
                                    objects_list=category.content,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No content have been added yet'


class CreateContent:
    category_id = -1

    def __call__(self, request):
        if request['request_method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                
                category = site.find_category_by_id(int(self.category_id))

                content = site.create_content('second type', name, category)
                site.content.append(content)

            return '200 OK', render('content_list.html',
                                    context=context,
                                    objects_list=category.content,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_content.html',
                                        context=context,
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


class CreateCategory:
    def __call__(self, request):
        context['list_categories'] = site.categories
        context['title'] = ''

        if request['request_method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = site.decode_value(name)
            
            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', context=context)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    context=context)


class CopyContent:
    def __call__(self, request):
        request_params = request['params']

        try:
            name = request_params['name']

            old_content = site.get_content(name)
            if old_content:
                new_name = f'copy_{name}'
                new_content = old_content.clone()
                new_content.name = new_name
                site.content.append(new_content)
                
            return '200 OK', render('content_list.html', context = context,
                                    objects_list=site.content,
                                    name=new_content.category.name)
        except KeyError:
            return '200 OK', 'No content have been added yet'
