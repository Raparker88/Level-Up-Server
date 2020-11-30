"""Game model module"""
from django.db import models


class Game(models.Model):
    """Game database model"""
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    title = models.CharField(max_length=75)
    maker = models.CharField(max_length=50)
    gametype = models.ForeignKey("GameType", on_delete=models.CASCADE)


    @property
    def is_user_creator(self):
        return self.__is_user_creator

    @is_user_creator.setter
    def is_user_creator(self, value):
        self.__is_user_creator = value