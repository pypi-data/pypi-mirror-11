from django.core.urlresolvers import reverse
from django.core.urlresolvers import NoReverseMatch


class MenuBase(object):
    """
    Base class that generates menu list.
    """
    def __init__(self):
        self.path = ''
        self.is_staff = False
        self.is_superuser = False
        self.is_authenticated = False

    def save_user_state(self, request):
        """
        Given a request object, store the current user attributes
        """
        self.path = request.path
        self.is_staff = request.user.is_staff
        self.is_superuser = request.user.is_superuser
        self.is_authenticated = request.user.is_authenticated()

    def is_true(self, item_dict, key):
        """
        Given a menu item dictionary, and a key, it returns True if key is set to True
        else returns False
        """
        yep = item_dict.get(key, False)
        return yep

    def show_to_all(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be shown
        for both authenticated and unauthenticated users. (e.g. a `contact` menu item)
        """
        show = self.is_true(item_dict, 'pre_login_visible') and \
            self.is_true(item_dict, 'post_login_visible')
        return show

    def show_to_authenticated(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be only shown
        to authenticated users. (e.g. a `logout` menu item)
        """
        show = self.is_true(item_dict, 'post_login_visible') and self.is_authenticated
        return show

    def show_to_unauthenticated(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be only shown
        to unauthenticated users. (e.g. a `login` menu item)
        """
        show = self.is_true(item_dict, 'pre_login_visible') and not self.is_authenticated
        return show

    def is_superuser_safe(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be only shown
        to super users. (e.g. a `admin` menu item)
        """
        yep = True
        if self.is_true(item_dict, 'superuser_required') and not self.is_superuser:
            yep = False
        return yep

    def is_staff_safe(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be only shown
        to staff users. (e.g. a `limited admin` menu item)
        """
        yep = True
        if self.is_true(item_dict, 'staff_required') and not self.is_staff:
            yep = False
        return yep

    def get_url(self, item_dict):
        """
        Given a menu item dictionary, it returns the URL or an empty string.
        """
        final_url = ''
        url = item_dict.get('url', '')
        try:
            final_url = reverse(url)
        except NoReverseMatch:
            final_url = url
        return final_url

    def has_url(self, item_dict):
        """
        Given a menu item dictionary, it returns true if a URL is set.
        """
        if not self.get_url(item_dict):
            return False
        return True

    def set_breadcrums(self, menu_list, best_match_url):
        """
        Given a menu list, it marks the best match url as selected, which
        can be used as breadcrumbs
        """
        matched_index = -1
        for item in menu_list:
            if best_match_url == item['url']:
                matched_index = menu_list.index(item)
                break
        if matched_index > -1:
            menu_list[matched_index]['selected'] = True

    def get_menu_list(self, list_dict):
        """
        A generator that returns only the visible menu items.
        """
        for item in list_dict:
            if not self.has_url(item):
                continue
            if self.show_to_all(item):
                pass
            elif self.show_to_authenticated(item):
                pass
            elif self.show_to_unauthenticated(item):
                pass
            else:
                continue
            if not self.is_superuser_safe(item):
                continue
            if not self.is_staff_safe(item):
                continue
            yield item

    def generate_menu(self, list_dict):
        """
        Given a list of dictionaries, returns a menu list.
        """
        best_match_url = ''
        visible_menu = []
        for item in self.get_menu_list(list_dict):
            url = self.get_url(item)

            # record the based matched url on the requested path
            if len(url) > 1 and url in self.path:
                if len(best_match_url) < len(url):
                    best_match_url = url

            item['url'] = url
            visible_menu.append(item)

        self.set_breadcrums(visible_menu, best_match_url)
        return visible_menu


class Menu(MenuBase):
    """
    Class that generates menu list.
    """
    def __call__(self, request, list_dict):
        self.save_user_state(request)
        return self.generate_menu(list_dict)

generate_menu = Menu()
