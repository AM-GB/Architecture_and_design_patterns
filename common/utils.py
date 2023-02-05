def menu_count(context):
    count = 0
    for k, i in context.items():
        count = count + 1 if 'menu' in k else count
    return count


def menu_selected(context = {}, number_menu_tabs=0, menu_tab_number=0):
    for n in range(1, number_menu_tabs+1):
        selected = f'selected{n}'
        if n == menu_tab_number:
            context[selected] = 'selected'
        else:
            context[selected] = ''
    return context


if __name__ == '__main__':
    pass
