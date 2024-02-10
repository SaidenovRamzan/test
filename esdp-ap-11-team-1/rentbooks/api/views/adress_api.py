from rest_framework.views import APIView
from rest_framework.response import Response
from yandex_geocoder import Client
from yandex_geocoder.exceptions import NothingFound
from decimal import Decimal
import requests
import typing



class AdressIsValidApi(APIView):
    def post(self, request):
        client = Client("58e3f0b7-4b3f-4375-afee-1c084e4ef7ea")
        value:str = request.data.get('adress')
        location = client.coordinates(value)
        try:
            data = self._request(f"{location[0]},{location[1]}")["GeoObjectCollection"]["featureMember"]
            respon = []
            for i in data:
                if i.get("GeoObject").get("metaDataProperty").get("GeocoderMetaData").get("Address").get("country_code")=='KZ':
                    print(i.get("GeoObject").get("metaDataProperty").get("GeocoderMetaData").get("text"))
                    respon.append(i.get("GeoObject").get("metaDataProperty").get("GeocoderMetaData").get("text"))
            got: str = data[0]["GeoObject"]
            return Response(self._request(f"{location[0]},{location[1]}"))
            location = client.coordinates(value)
            if (45 <= location[0].quantize(exp=Decimal('1')) <= 87) and ( 40 <= location[1].quantize(exp=Decimal('1')) <= 50):
                adress = client.address(location[0], location[1])
                parts = adress.split(',')
                cleaned_parts = [part.strip() for part in parts]
                if cleaned_parts[-1] == value.split()[-1]:
                    return Response("OK")
                return Response(adress)
            else:
                return Response({"adress":value})
        except NothingFound:
            return Response({"adress":value})
           
    def contains_original_address(self, origin_adress: str, adress: list[str])-> bool:
        origin_adress = origin_adress.split()
        for i in origin_adress:
            print(f"{adress=}")
            print(f"{i=}")
            print(type(i) )
            if i not in adress:
                return False
            elif type(i) is list:
                for j in i:
                    print(f"{j=}")
                    if j not in i:
                        return False
        return True
    
    def _request(self, address: str) -> dict[str, typing.Any]:
        response = requests.get(
            "https://geocode-maps.yandex.ru/1.x/",
            params=dict(format="json", apikey="58e3f0b7-4b3f-4375-afee-1c084e4ef7ea", geocode=address, kind='province'),
        )

        if response.status_code == 200:
            got: dict[str, typing.Any] = response.json()["response"]
            return got

            