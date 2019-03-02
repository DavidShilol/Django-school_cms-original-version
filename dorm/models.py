from django.db import models
from django.contrib.auth.models import AbstractUser


class NewUser(AbstractUser):
	name = models.CharField('name', default='', max_length=100)
	idcard = models.CharField('idcard', default='', max_length=100)
	phone = models.CharField('phone', default='', max_length=100)
	sex = models.CharField('sex', default='', max_length=100)
	kind = models.CharField('kind', default='', max_length=100)
	
	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name


class Building(models.Model):
	number = models.IntegerField('number', default=0)
	high = models.IntegerField('high', default=0)
	room = models.IntegerField('room', default=0)
	begintime = models.DateField('begintime', null=True)
	sex = models.CharField('sex', default='', max_length=100)

	def __repr__(self):
		return 'Building-{}'.format(self.number)


class Room(models.Model):
	number = models.IntegerField('number', default=0)
	volume = models.IntegerField('volume', default=0)
	cost = models.IntegerField('cost', default=0)
	building_number = models.ForeignKey('Building', on_delete=models.CASCADE, related_name='building_number', null=True)
	free = models.IntegerField('free', default=0)

	def __str__(self):
		return 'room-{}'.format(self.number)

	def __repr__(self):
		return 'room-{}'.format(self.number)


class Student(models.Model):
	number = models.CharField('number', default='', max_length=100)
	name = models.CharField('name', default='', max_length=100)
	sex = models.CharField('sex', default='', max_length=100)
	nation = models.CharField('nation', default='', max_length=100)
	major = models.CharField('major', default='', max_length=100)
	class_grade = models.CharField('class_grade', default='', max_length=100)
	phone = models.CharField('phone', default='', max_length=100)
	room_number = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='room_number', null=True)
	teacher = models.ForeignKey('NewUser', on_delete=models.CASCADE, related_name='teacher', null=True)

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name


# class 

