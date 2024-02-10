from elastic.views import elastic, SearchBookApiView, SerachTest, SearchMongo, SearchPsql
from django.urls import path

urlpatterns = [
    path('elastic', elastic, name='elastic'),
    path('elastic_1', SearchBookApiView.as_view(), name='search_book1'),
    path('elastic_test', SerachTest.as_view(), name='search_book2'),
    path('elastic_test2', SearchMongo.as_view(), name='search_book3'),
    path('elastic_test3', SearchPsql.as_view(), name='search_book4'),
    
]
