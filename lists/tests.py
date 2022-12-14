from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest, HttpResponse
from lists.models import Item, List

# Create your tests here.

# class SmokeTest(TestCase):

#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)

class ListViewTest(TestCase):
    
    def test_list_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get(f'/lists/{list_.id}/')

        self.assertContains(response, 'itemey 1')  
        self.assertContains(response, 'itemey 2')  
    
    # def test_uses_list_template(self):
    #     response = self.client.get('/lists/the-only-list-in-the-world/')
    #     self.assertTemplateUsed(response, 'list.html')

class HomePage(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # Using the Django test client to obtain the HttpResponse object from the url
        response = self.client.get('/')  

        # Using the assertTemplateUsed function to check if the expected template is being returned
        self.assertTemplateUsed(response, 'home.html')  

    # def test_can_save_a_POST_request(self):
    #     # Send a post request to the '/' route and test the return HttpResponse object content
    #     response = self.client.post('/', data={'item_text': 'A new list item'})

    #     # Counting number of items in table and and asserting
    #     self.assertEqual(Item.objects.count(), 1)  
    #     new_item = Item.objects.first()  
    #     self.assertEqual(new_item.text, 'A new list item')  

    def test_redirect_after_a_POST_request(self):
        # Send a post request to the '/' route and test the return HttpResponse object content
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    # def test_displays_all_list_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')

    #     response = self.client.get('/')

    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())
    
class ListAndItemModelsTest(TestCase):

     def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

    
