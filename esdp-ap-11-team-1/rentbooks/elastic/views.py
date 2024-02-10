import logging
import json
import base64
from django.http import JsonResponse
from elasticsearch_dsl import connections, Search
from elasticsearch_dsl.query import MultiMatch, Match, Term
from rest_framework import status
from rest_framework.views import APIView

from books.models import Composition, Book
from elastic.document import CompositionElastic, Person
import time      
from accounts.models import CompositionTest

        
def elastic(request, *args, **kwargs):

    # initiate the default connection to elasticsearch
    connections.create_connection(hosts=['http://elasticsearch1:9200'])
    # create the empty index
    Person.init()
    CompositionElastic.init()
    logging.info(f"{Composition.objects.all()=}")
    for composition in Composition.objects.all():
        logging.info(f"{composition.name=}, {composition.author=}, {composition.id_genre.name=} ")
    for composition in Composition.objects.all():
        CompositionElastic(meta={'id': composition.id}, name=composition.name, name_folded=composition.name, author=composition.author, genre=composition.id_genre.name).save()
    CompositionElastic(meta={'id': 2}, name='leb', name_folded='leb', author='Sasha', genre='Приключения').save()
    CompositionElastic(meta={'id': 3}, name='Gleb leb', author='Sasha', genre='Приключения').save()
    
    CompositionElastic._index.refresh()
    s = CompositionElastic.search()
    text = 'Ужасы'
    s.query = MultiMatch(
            query=text,
            type="bool_prefix",
            fields=["name", "name._2gram", "name._3gram"],
        )
    response = s.execute()
    for h in response:
            print("%15s: %25s" % (text, h.name))
            logging.info(f"{text=} {h=} ,======================== {h.name=}, ====================== {response}")
    
    
    # index some sample data
    names = [
        "Andy Warhol",
        "Ahlphonse Mucha",
        "Henri de Toulouse-Lautrec",
        "Jára Cimrman",
    ]
    for id, name in enumerate(names):
        Person(_id=id, name=name).save()

    # refresh index manually to make changes live
    Person._index.refresh()

    # run some suggestions
    for text in ("já", "Cimr", "toulouse", "Henri Tou", "a"):
        s = Person.search()

        s.query = MultiMatch(
            query=text,
            type="bool_prefix",
            fields=["name", "name._2gram", "name._3gram"],
        )

        response = s.execute()

        # print out all the options we got
        for h in response:
            print("%15s: %25s" % (text, h.name))
            logging.info(f"{text=} {h=} ,======================== {h.name=}, ====================== {response}")
    s = CompositionElastic.search()
    text = 'Gleb'
    s.query = Match(
        name={
            "query": text,
            "fuzziness": "AUTO",
        }
    )
    response = s.execute()
    for h in response:
            print("%15s: %25s" % (text, h.name))
            logging.info(f"text={text} {h=} {h.meta.id=} {h.to_dict()=},======================== {h.name=}, ====================== {response.to_dict()=}")
    data = {'net': 'daaaaa'}
    return JsonResponse(data)


class SearchBookApiView(APIView):
    
    def post(self, request):
        connections.create_connection(hosts=['http://elasticsearch1:9200'])
        CompositionElastic.init()
        # for composition in Composition.objects.all():
        #     logging.info(f"{composition.name=}, {composition.author=}, {composition.id_genre.name=} ")
        #     CompositionElastic(meta={'id': composition.id}, name=composition.name, name_folded=composition.name, author=composition.author, genre=composition.id_genre.name).save()
        
        try:
            search_request = request.data.get('search_request', '')
            result = []
            s = CompositionElastic.search()
            s.query = MultiMatch(
                query=search_request,
                type="bool_prefix",
                fields=["name", "name._1gram", "name._2gram", "name._3gram", "author", "description", "genre"],
                fuzziness="AUTO",
            )
            response = s.execute()
            composition_ids = [h.meta.id for h in response]
            result = Composition.objects.filter(id_Composition__in=composition_ids)

            compositions = []
            for composition in result:
                book = Book.objects.all().filter(id_composition=composition.id).first()
                compositions.append(
                    {
                        'id': composition.id,
                        'name': composition.name,
                        'author': composition.author,
                        'description': composition.description,
                        'coverphoto': base64.b64encode(book.coverphoto.read()).decode('utf-8'),
                    }
                )

            return JsonResponse({'books': compositions}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class SerachTest(APIView):
    def post(self, request):
        start_time = time.time()
        connections.create_connection(hosts=['http://elasticsearch1:9200'])
        CompositionElastic.init()
        try:
            search_request = request.data.get('search_request', '')
            for i in range(0, 10_000, 2):
                s = CompositionElastic.search()
                s.query = Term(name=i)
                response = s.execute()
                composition_ids = [h.meta.id for h in response]
            end_time = time.time()
            execution_time = end_time - start_time
            return JsonResponse({'response': composition_ids, 'time':execution_time})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
       
        
class SearchMongo(APIView):
    def post(self, request):
        try:
            start_time = time.time()
            search_request = request.data.get('search_request', '')
            for i in range(0, 10_000, 2):
                response = Composition.objects.filter(name=str(i)).first()
                logging.info(response.id_Composition)
            end_time = time.time()
            execution_time = end_time - start_time
            logging.info(f"{response}-------------------")
            logging.info(f"{search_request}-------------------")
            return JsonResponse({'response': response.id_Composition, "time":execution_time})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        

class SearchPsql(APIView):
    def post(self, request):
        try:
            start_time = time.time()
            search_request = request.data.get('search_request', '')
            for i in range(0, 10_000, 2):
                response = CompositionTest.objects.filter(name=str(i)).first()
                logging.info(response.id)
            end_time = time.time()
            execution_time = end_time - start_time
            logging.info(f"{response}-------------------")
            logging.info(f"{search_request}-------------------")
            return JsonResponse({'response': response.id, "time":execution_time})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        
        