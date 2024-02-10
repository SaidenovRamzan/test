from rest_framework import serializers
from books.models import Comment, FavoriteBook
from rents.models import UserShelf, OrderOfRent, UserImages


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = ('id', 'user', 'composition_id', 'text', 'date_publish')


class FavoriteBookSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FavoriteBook
        fields = ('id', 'composition_id', 'user')


class UserShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShelf
        fields = '__all__'


class OrderOfRentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    usershelf = serializers.ReadOnlyField(source='rents.usershelf')
    class Meta:
        model = OrderOfRent
        fields = '__all__'
        
        
class UserImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserImages
        fields = ('book_shelf', 'image')
