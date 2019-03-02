from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView
from django.http import HttpResponse
from .models import NewUser, Building, Room, Student
from datetime import datetime
import json


class LoginView(View):
	def get(self, request):
		return render(request, 'dorm/login.html')

	def post(self, request):
		info = {}
		info['idcard'] = request.POST.get('idcard', '')
		info['password'] = request.POST.get('password', '')
		if request.POST.get('checkbox2', ''):
			info['kind'] = 'teacher'
		else:
			info['kind'] = 'dormadmin'
		print(info['kind'])
		if NewUser.objects.filter(idcard=info['idcard'], password=info['password'], kind=info['kind']).exists():
			user = NewUser.objects.get(idcard=info['idcard'], password=info['password'])
			request.session['name'] = user.name
			request.session['kind'] = user.kind
			if info['kind'] == 'dormadmin':
				return redirect(reverse('dorm:DormadminIndex'))
			else:
				return redirect(reverse('dorm:TeacherIndex'))
		else:
			return render(request, 'dorm/login.html', {'errorinfo': '账户或密码错误！'})


def logout(request):
	del request.session['name']
	del request.session['kind']
	return redirect(reverse('dorm:login'))


class RegisterView(View):
	def get(self, request):
		return render(request, 'dorm/register.html')

	def post(self, request):
		info = {}
		info['name'] = request.POST.get('name', '')
		info['idcard'] = request.POST.get('idcard', '')
		info['password'] = request.POST.get('password', '')
		info['password_again'] = request.POST.get('password_again', '')
		info['phone'] = request.POST.get('phone', '')
		info['sex'] = request.POST.get('sex', '')
		info['kind'] = request.POST.get('kind', '')
		print(info)
		if not NewUser.objects.filter(idcard=info['idcard']):
			user = NewUser(name=info['name'], idcard=info['idcard'], password=info['password'], 
			phone=info['phone'], sex=info['sex'], kind=info['kind'], username=info['name'])
			user.save()
			return redirect(reverse('dorm:login'))
		else:
			return render(request, 'dorm/register.html', {'errorinfo': '用户已存在'})


def DormadminIndex(request):
	info = {}
	info['name'] = request.session.get('name', '')
	info['kind'] = request.session.get('kind', '')
	if info['name'] and info['kind'] == 'dormadmin':
		return render(request, 'dorm/dormadmin_index.html', info)
	else:
		return redirect(reverse('dorm:login'))


class BuildingView(View):
	def get(self, request):	
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		context = {}
		context['building_list'] = Building.objects.all().order_by('number')
		context['kind'] = self.request.session.get('kind', '')
		return render(request, 'dorm/building_view.html', context)

	def post(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if request.is_ajax():
			if request.POST.get('option', '') == 'edit':
				array = request.POST.getlist('arr[]', '')
				building = Building.objects.get(number=int(array[0]))
				building.number = int(array[0])
				building.high = int(array[1])
				building.room = int(array[2])
				building.begintime = datetime.strptime(array[3], '%Y-%m-%d')
				building.sex = array[4]
				building.save()
				return render(request, 'dorm/building_view.html')
			elif request.POST.get('option', '') == 'delete':
				building = Building.objects.get(number=request.POST.get('number', ''))
				building.delete()
				return render(request, 'dorm/building_view.html')
		if request.POST.get('add', ''):
			info = {}
			info['number'] = int(request.POST.get('number', ''))
			info['high'] = int(request.POST.get('high', ''))
			info['room'] = int(request.POST.get('room', ''))
			info['begintime'] = datetime.strptime(request.POST.get('begintime', ''), '%Y-%m-%d')
			info['sex'] = request.POST.get('sex', '')
			building = Building(number=info['number'], high=info['high'], room=info['room'], 
				begintime=info['begintime'], sex=info['sex'])
			building.save()
			return redirect(reverse('dorm:BuildingView'))
		return render(request, 'dorm/building_view.html')


class RoomView(View):
	def get(self, request, building_num):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		building = Building.objects.get(number=building_num)
		room_list = Room.objects.filter(building_number=building)
		context = {'room_list': room_list, 'kind': request.session.get('kind', '')}
		return render(request, 'dorm/room_view.html', context)
	
	def post(self, request, building_num):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if request.POST.get('add', ''):
			info = {}
			info['number'] = int(request.POST.get('number', '0'))
			info['volume'] = int(request.POST.get('volume', '0'))
			info['cost'] = int(request.POST.get('cost', '0'))
			info['building_num'] = Building.objects.get(number=building_num)
			info['free'] = int(request.POST.get('free', '0'))
			room = Room(number=info['number'], volume=info['volume'], cost=info['cost'], building_number=info['building_num'], free=info['free'])
			room.save()
			return redirect(reverse('dorm:RoomView', args=(building_num,)))
		if request.is_ajax():
			if request.POST.get('option', '') == 'edit':
				array = request.POST.getlist('arr[]', '')
				info = {}
				info['number'] = int(array[0])
				info['volume'] = int(array[1])
				info['cost'] = int(array[2])
				info['building_number'] = Building.objects.get(number=building_num)
				info['free'] = int(array[4])
				room = Room.objects.get(number=info['number'])
				room.volume = info['volume']
				room.cost = info['cost']
				room.building_number = info['building_number']
				room.free = info['free']
				room.save()
				return render(request, 'dorm/room_view.html')
			elif request.POST.get('option', '') == 'delete':
				number = request.POST.get('number', '')
				building = Building.objects.get(number=building_num)
				room = building.building_number.get(number=number)
				room.delete()
				return render(request, 'dorm/room_view.html')
		return render(request, 'dorm/room_view.html')


def TeacherIndex(request):
	info = {}
	info['name'] = request.session.get('name', '')
	info['kind'] = request.session.get('kind', '')
	if info['name'] and info['kind'] == 'teacher':
		return render(request, 'dorm/teacher_index.html', info)
	else:
		return redirect(reverse('dorm:login'))


class StudentView(View):
	def get(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		user = NewUser.objects.get(name=request.session.get('name', 'null'))
		student_list = user.teacher.all()
		info = {'kind': request.session.get('kind', ''), 'student_list': student_list}
		info['nation_list'] = ['汉族', '蒙古族', '回族', '藏族', '维吾尔族', '苗族', '彝族', '壮族', '布依族', '朝鲜族', \
		'满族', '侗族', '瑶族', '白族', '土家族', '哈尼族', '哈萨克族', '傣族', '黎族', '僳僳族', '佤族', '畲族', \
		'高山族', '拉祜族', '水族', '东乡族', '纳西族', '景颇族', '柯尔克孜族', '土族', '达斡尔族', '仫佬族', \
		'羌族', '布朗族', '撒拉族', '毛南族', '仡佬族', '锡伯族', '阿昌族', '普米族', '塔吉克族', '怒族', \
		'乌孜别克族', '俄罗斯族', '鄂温克族', '德昂族', '保安族', '裕固族', '京族', '塔塔尔族', '独龙族', \
		'鄂伦春族', '赫哲族', '门巴族', '珞巴族', '基诺族']
		info['major_list'] = ['计算机系', '自动化系', '测控技术系', '信息工程系', '化学工程与工艺', '环境工程', \
		'能源化学工程', '卓越工程师计划', '国际教育合作']
		class_grade_list = []
		grade_list = [str(x) for x in range(15, 20)]
		class_list = [str(x) for x in range(1, 21)]
		for x in grade_list:
			for y in class_list:
				if len(y) == 1:
					class_grade_list.append(x+'0'+y)
				else:
					class_grade_list.append(x+y)
		info['class_grade_list'] = class_grade_list
		return render(request, 'dorm/student_view.html', info)

	def post(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if request.POST.get('add', ''):
			info = {}
			info['number'] = request.POST.get('number', '')
			info['name'] = request.POST.get('name', '')
			info['sex'] = request.POST.get('sex', '')
			info['nation'] = request.POST.get('nation', '')
			info['major'] = request.POST.get('major', '')
			info['class_grade'] = request.POST.get('class_grade', '')
			info['phone'] = request.POST.get('phone', '')
			info['teacher'] = request.session.get('name', '')
			user = NewUser.objects.get(name=info['teacher'])
			student = Student(number=info['number'], name=info['name'], sex=info['sex'], nation=info['nation'], 
			major=info['major'], class_grade=info['class_grade'], phone=info['phone'], teacher=user)
			student.save()
			return redirect(reverse('dorm:StudentView'))
		if request.is_ajax():
			if request.POST.get('option', '') == 'edit':
				array = request.POST.getlist('arr[]', '')
				info = {}
				info['number'] = array[0]
				info['name'] = array[1]
				info['sex'] = array[2]
				info['nation'] = array[3]
				info['major'] = array[4]
				info['class_grade'] = array[5]
				info['phone'] = array[6]
				student = Student.objects.get(number=info['number'])
				student.number = info['number']
				student.name = info['name']
				student.sex = info['sex']
				student.nation = info['nation']
				student.major = info['major']
				student.class_grade = info['class_grade']
				student.phone = info['phone']
				student.save()
				return render(request, 'dorm/student_view.html', info)
			elif request.POST.get('option', '') == 'delete':
				student = Student.objects.get(number=request.POST.get('number', ''))
				student.delete()
				return render(request, 'dorm/student_view.html')
		return render(request, 'dorm/student_view.html')


class RoomDetailView(View):
	def get(self, request, building_num, room_num):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		building = Building.objects.get(number=building_num)
		room = building.building_number.get(number=room_num)
		students = room.room_number.all()
		info = {}
		info['student_list'] = students
		info['kind'] = request.session.get('kind', '')
		return render(request, 'dorm/room_detail.html', info)

	def post(self, request, building_num, room_num):
		info ={}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if request.is_ajax():
			if request.POST.get('option', '') == 'delete':
				student = Student.objects.get(number=request.POST.get('number', ''))
				room = student.room_number
				room.free += 1
				room.save()
				student.room_number = None
				student.save()
		return redirect(reverse('dorm:RoomDetail', args=(building_num, room_num,)))


class StudentSearch(View):
	def get(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if ''.join(request.GET.values()):
			info = {}
			info['name'] = request.session.get('name', '')
			info['kind'] = request.session.get('kind', '')
			info['student_name'] = request.GET.get('student_name', '')
			info['number'] = request.GET.get('number', '')
			info['teacher_name'] = request.GET.get('teacher_name', '')
			if ''.join(info.values()):
				teacher = NewUser.objects.filter(name__contains=info.get('teacher_name', ''), kind='teacher')
				students = [t.teacher.all() for t in teacher]
				student_list = [s.filter(name__contains=info.get('student_name', ''), 
					number__contains=info.get('number', '')) for s in students]
				info['student_list'] = student_list
		return render(request, 'dorm/student_search.html', info)
			

	def post(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if request.is_ajax():
			if request.POST.get('option', '') == 'edit':
				array = request.POST.getlist('arr[]', '')
				info = {}
				info['number'] = array[0]
				info['name'] = array[1]
				info['building_number'] = Building.objects.get(number=int(array[7]))
				if not info['building_number'].building_number.filter(number=int(array[8])).exists():
					info['error_info'] = '宿舍楼内不存在该宿舍'
					print(info['error_info'])
					return render(request, 'dorm/student_search.html', info)
				info['room_number'] = info['building_number'].building_number.get(number=int(array[8]))
				student = Student.objects.get(number=info['number'])
				if info['building_number']:
					if student.sex != info['building_number'].sex:
						info['error_info'] = '性别不符'
						print(info['error_info'])
				elif not info['room_number']:
					if student.room_number:
						student.room_number = None
						student.save()
						student = Student.objects.get(number=info['number'])
				elif info['room_number'] != student.room_number:
					if info['room_number'].free > 0:
						print('here')
						info['room_number'].free -= 1
						info['room_number'].save()
						info['room_number'] = info['building_number'].building_number.get(number=int(array[8]))
						room = student.room_number
						if room:
							print('before:', room.number, room.free)
							room.free += 1
							print('after:', room.number, room.free)
							room.save()
						student.room_number = info['room_number']
					else:
						info['error_info'] = '宿舍已满'
						print(info['error_info'])
				student.save()
		return redirect(reverse('dorm:StudentSearch'))


class DormSearch(View):
	def get(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if ''.join(request.GET.values()):
			info['building_number'] = request.GET.get('building_number', '')
			info['sex'] = request.GET.get('sex', '')
			info['room_number'] = request.GET.get('room_number', '')
			info['volume_min'] = request.GET.get('volume_min', '0')
			info['volume_max'] = request.GET.get('volume_max', '12')
			info['free_min'] = request.GET.get('free_min', '0')
			info['free_max'] = request.GET.get('free_max', '12')
			if not info['volume_min']:
				info['volume_min'] = '0'
			if not info['volume_max']:
				info['volume_max'] = '12'
			if not info['free_min']:
				info['free_min'] = '0'
			if not info['free_max']:
				info['free_max'] = '12'
			info['volume_min'] = int(info['volume_min'])
			info['volume_max'] = int(info['volume_max'])
			info['free_min'] = int(info['free_min'])
			info['free_max'] = int(info['free_max'])
			if info['building_number'] and info['room_number']:
				if not Building.objects.filter(number=int(info['building_number'])).exists():
					info['error_info'] = '宿舍楼不存在'
					print(info['error_info'])
					return render(request, 'dorm/dorm_search.html', info)
				building = Building.objects.get(number=int(info['building_number']))
				if not Room.objects.filter(number=int(info['room_number'])).exists():
					info['error_info'] = '宿舍楼不存在该宿舍'
					print(info['error_info'])
					return render(request, 'dorm/dorm_search.html', info)
				room = Room.objects.get(number=int(info['room_number']), building_number=building)
				if info['volume_min'] <= room.volume <= info['volume_max'] and \
				info['free_min'] <= room.free <= info['free_max']:
					pass
				else:
					info['error_info'] = '可住人数或剩余容量条件不满足'
					print(info['error_info'])
					return render(request, 'dorm/dorm_search.html', info)
				if info['sex'] not in room.building_number.sex:
					info['error_info'] = '没有符合性别的宿舍楼'
					print(info['error_info'])
					return render(request, 'dorm/dorm_search.html', info)
				info['room_list'] = [room]
				return render(request, 'dorm/dorm_search.html', info)
			elif info['building_number'] and not info['room_number']:
				if not Building.objects.filter(number=int(info['building_number'])).exists():
					info['error_info'] = '宿舍楼不存在'
					print(info['error_info'])
					return render(request, 'dorm/dorm_search.html', info)
				building = Building.objects.get(number=int(info['building_number']))
				if not building.building_number.filter(volume__gte=info['volume_min'], 
				volume__lte=info['volume_max'], free__gte=info['free_min'], 
				free__lte=info['free_max']).exists():
					info['error_info'] = '可住人数或剩余容量条件不满足'
					print(info['error_info'])
					return render(request, 'dorm/dorm_search.html', info)
				room = building.building_number.filter(volume__gte=info['volume_min'],
				volume__lte=info['volume_max'], free__gte=info['free_min'],
				free__lte=info['free_max'])
				room_list = [x for x in room if info['sex'] in x.building_number.sex]
				if not room_list:
					info['error_info'] = '没有符合性别的宿舍楼'
					print(info['error_info'])
					return render(request, 'dorm/dorm_search.html', info)
				info['room_list'] = room_list
				return render(request, 'dorm/dorm_search.html', info)
			elif not info['building_number'] and info['room_number']:
				if Room.objects.filter(number=int(info['room_number']),  
				volume__gte=info['volume_min'], volume__lte=info['volume_max'], 
				free__gte=info['free_min'], free__lte=info['free_max']).exists():
					room = Room.objects.filter(number=int(info['room_number']), 
					volume__gte=info['volume_min'], volume__lte=info['volume_max'], 
					free__gte=info['free_min'], free__lte=info['free_max'])
					room = [x for x in room if info['sex'] in x.building_number.sex]
					info['room_list'] = room
				return render(request, 'dorm/dorm_search.html', info)
			elif not info['building_number'] and not info['room_number']:
				if Room.objects.filter( volume__gte=info['volume_min'], 
				volume__lte=info['volume_max'], free__gte=info['free_min'], 
				free__lte=info['free_max']).exists():
					room = Room.objects.filter(volume__gte=info['volume_min'], 
					volume__lte=info['volume_max'], free__gte=info['free_min'], 
					free__lte=info['free_max'])
					room = [x for x in room if info['sex'] in x.building_number.sex]
					info['room_list'] = room
				return render(request, 'dorm/dorm_search.html', info)
		return render(request, 'dorm/dorm_search.html', info)


	def post(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if request.is_ajax():
			if request.POST.get('option', '') == 'edit':
				array = request.POST.getlist('arr[]', '')
				info['building_number'] = int(array[0])
				info['sex'] = array[1]
				info['room_number'] = int(array[2])
				info['volume'] = int(array[3])
				info['free'] = int(array[4])
				building = Building.objects.get(number=info['building_number'])
				room = building.building_number.get(number=info['room_number'])
				if room.volume != info['volume'] or room.free != info['free']:
					room.volume = info['volume']
					room.free = info['free']
					room.save()
					room = building.building_number.get(number=info['room_number'])
		return render(request, 'dorm/dorm_search.html', info)


class DormSearchDetail(View):
	def get(self, request, building_num, room_num):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		building = Building.objects.get(number=building_num)
		room = building.building_number.get(number=room_num)
		student = room.room_number.all()
		info['student_list'] = student
		return render(request, 'dorm/dorm_search_detail.html', info)

	def post(self, request, building_num, room_num):
		info ={}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if request.is_ajax():
			if request.POST.get('option', '') == 'delete':
				student = Student.objects.get(number=request.POST.get('number', ''))
				room = student.room_number
				room.free += 1
				room.save()
				student.room_number = None
				student.save()
		return redirect(reverse('dorm:DormSearchDetail', args=(building_num, room_num,)))


class RequestView(View):
	def get(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		elif info['kind'] != 'dormadmin':
			print(info['name'])
			return redirect(reverse('dorm:login'))
		student_list = Student.objects.filter(room_number=None)
		info['student_list'] = student_list
		return render(request, 'dorm/request_view.html', info)

	def post(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		if request.is_ajax():
			if request.POST.get('option', '') == 'edit':
				array = request.POST.getlist('arr[]', '')
				info = {}
				info['number'] = array[0]
				info['name'] = array[1]
				info['building_number'] = Building.objects.get(number=int(array[8]))
				info['room_number'] = info['building_number'].building_number.get(number=int(array[7]))
				student = Student.objects.get(number=info['number'])
				if not info['room_number']:
					if student.room_number:
						student.room_number = None
						student.save()
						student = Student.objects.get(number=info['number'])
				elif info['room_number'] != student.room_number:
					if info['room_number'].free > 0:
						info['room_number'].free -= 1
						info['room_number'].save()
						info['room_number'] = info['building_number'].building_number.get(number=int(array[7]))
						room = student.room_number
						if room:
							print('before:', room.number, room.free)
							room.free += 1
							print('after:', room.number, room.free)
							room.save()
						student.room_number = info['room_number']
					else:
						info['error_info': '宿舍已满']
				student.save()
			elif request.POST.get('option', '') == 'auto':
				pass
		return redirect(reverse('dorm:RequestView'))


def auto():
	student = Student.objects.filter(room_number=None)
	boy = student.filter(sex='男')
	print('boy:', boy)
	girl = student.filter(sex='女')
	boy_major = list(set([x.major for x in boy]))
	print('boy_major:', boy_major)

	building = Building.objects.filter(sex='男')
	room_queryset = [x.building_number.filter(free__gt=0).order_by('number') for x in building]
	room = []
	for x in room_queryset:
		for y in x:
			room.append(y)
	print('room:', room)


class PersonView(View):
	def get(self, request):
		info = {}
		info['name'] = request.session.get('name', '')
		info['kind'] = request.session.get('kind', '')
		if not info['name']:
			return redirect(reverse('dorm:login'))
		user = NewUser.objects.get(name=info['name'], kind=info['kind'])
		info['user'] = user
		return render(request, 'dorm/person_view.html', info)
	
	def post(self, request):
		info = {}
		info['name'] = request.POST.get('name', '')
		info['idcard'] = request.POST.get('idcard', '')
		info['sex'] = request.POST.get('sex', '')
		info['phone'] = request.POST.get('phone', '')
		print(info)
		user = NewUser.objects.get(idcard=info['idcard'])
		user.name = info['name']
		user.idcard = info['idcard']
		user.sex = info['sex']
		user.phone = info['phone']
		user.save()
		return redirect(reverse('dorm:PersonView'))

