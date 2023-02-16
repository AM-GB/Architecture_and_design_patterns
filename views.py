from my_first_framework.templator import render

from patterns.сreational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import AddUrl, Debug
from patterns.behavioral_patterns import ListView, CreateView, BaseSerializer
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from common.utils import menu_count, menu_selected
from common.config import CONTEXT

site = Engine()
logger = Logger('main')
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

context = CONTEXT
context['objects_list'] = []

MENU_COUNT = menu_count(context=context)

@AddUrl(url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        context['list_categories'] = site.categories
        context['title'] = 'Домашняя'
        menu_selected(context, MENU_COUNT, 1)
        return '200 OK', render('index.html', context=context)


@AddUrl(url='/exam/')
class Examples:
    def __call__(self, request):
        context['title'] = 'Примеры'
        menu_selected(context, MENU_COUNT, 2)
        return '200 OK', render('examples.html', context=context)


@AddUrl(url='/page/')
class Page:
    def __call__(self, request):
        context['title'] = 'Страница'
        menu_selected(context, MENU_COUNT, 3)
        return '200 OK', render('page.html', context=context)


@AddUrl(url='/contact/')
class Contact:
    def __call__(self, request):
        context['title'] = 'Контакты'
        menu_selected(context, MENU_COUNT, 4)
        print(context)
        return '200 OK', render('contact.html', context=context)


@AddUrl(url='/content-list/')
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


@AddUrl(url='/create-content/')
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


@AddUrl(url='/create_category/')
class CreateCategory:
    def __call__(self, request):
        # context['list_categories'] = site.categories
        context['title'] = 'Создание Категории'

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
            
            context['title'] = 'Домашняя'
            return '200 OK', render('index.html', context=context)
        else:
            context['title'] = 'Создание Категории'
            return '200 OK', render('create_category.html',
                                    context=context)


@AddUrl(url='/copy-content/')
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


@AddUrl(url='/customer_list/')
class CustomerListView(ListView):
    queryset = site.customers
    template_name = 'customer_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('customer')
        return mapper.all()

    def get_context_data(self):
        menu_selected(context, MENU_COUNT, 1)
        self.context = context
        return super().get_context_data()


@AddUrl(url='/create_customer/')
class CustomerCreateView(CreateView):
    template_name = 'create_customer.html'

    def get_context_data(self):
        return context

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('user', name)
        site.customers.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()
        # print(site.customers)


@AddUrl(url='/add_customer/')
class AddCustomerByContentCreateView(CreateView):
    template_name = 'add_customer.html'
    

    def get_context_data(self):
        self.context = {**super().get_context_data(), **context}
        # print(self.context)
        self.context['content'] = site.content
        self.context['customers'] = site.customers
        return self.context

    def create_obj(self, data: dict):
        content_name = data['content_name']
        content_name = site.decode_value(content_name)
        content = site.get_content(content_name)
        customer_name = data['customer_name']
        customer_name = site.decode_value(customer_name)
        customer = site.get_customer(customer_name)
        content.add_customer(customer)
        # print(customer.content)
        # print('*'*50)


@AddUrl(url='/api/')
class CourseApi:
    @Debug(name='ContentApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.content).save()
