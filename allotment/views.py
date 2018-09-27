from django.shortcuts import render, render_to_response
from .models import Shift, Department, Staff, TimeTable, Exam
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def index(request):
	"""View Function of Home Page"""
	StaffListCount=Staff.objects.count()
	StaffNamesList=Staff.objects.filter(department__shift=1).order_by('name')

	return render(request,'index.html')

#____________________
#_____TimeTable _____

class TimeTableList(generic.ListView):
	model = TimeTable

class TimeTableCreate(CreateView):
	model=TimeTable
	fields = '__all__'
	success_url = reverse_lazy('timetableList')

class TimeTableUpdate(UpdateView):
	model=TimeTable
	fields = '__all__'
	success_url = reverse_lazy('timetableList')

class TimeTableDelete(DeleteView):
	model=TimeTable
	success_url = reverse_lazy('timetableList')

def timetable_detail(request, pk):
	queryset1=TimeTable.objects.filter(id=pk)
	timetableName=queryset1.get().longName
	examDateList=Exam.objects.filter(timetable_id=pk).order_by('dateOfExam')
	context={
	'examDateList':examDateList,
	'timetableName':timetableName,
	'pk':pk,
	}
	request.session['timetableSession'] = pk
	request.session['timetableName'] = timetableName
	return render(request,'allotment/timetable_detail.html',context=context)

#_____________________
#_______ Exam ________
class ExamCreate(CreateView):
	model=Exam
	fields=['timetable_id','dateOfExam','noOfStudents']
	HEADING="Add Exams"
	def get_initial(self):
		timetable_id=self.request.session['timetableSession']
		return { 'timetable_id':timetable_id }
	def get_context_data(self, **kwargs):
		ctx = super(ExamCreate,self).get_context_data(**kwargs)
		ctx['HEADING'] = self.HEADING
		return ctx
	def get_success_url(self):
		timetable_id=self.request.session['timetableSession']
		return reverse_lazy('timetable_detail',args=[str(timetable_id)])

class ExamDelete(DeleteView):
	model = Exam

	def get_context_data(self, **kwargs):
		ctx = super(ExamDelete,self).get_context_data(**kwargs)
		ctx['timetableName'] = self.request.session['timetableName']
		return ctx

	def get_success_url(self):
		timetable_id=self.request.session['timetableSession']
		return reverse_lazy('timetable_detail',args=[str(timetable_id)])

from django.forms.models import modelform_factory
from django import forms

class ExamAllotStaff(UpdateView):
	""" Used to select staff names with a multi choice tick box """
	model = Exam

	form_class =  modelform_factory(Exam,fields=['timetable_id','dateOfExam','noOfStudents','staffs'],
		widgets={"staffs": forms.CheckboxSelectMultiple()})

	def get_form(self, form_class=form_class):
		form = super(ExamAllotStaff,self).get_form(form_class) #instantiate using parent
		form.fields['staffs'].queryset = Staff.objects.all().filter(department__shift=1).order_by('-dateofJoining')
		form.fields['timetable_id'].disabled=True
		form.fields['dateOfExam'].disabled=True
		form.fields['noOfStudents'].disabled=True
		return form

	def get_success_url(self):
		timetable_id=self.request.session['timetableSession']
		return reverse_lazy('timetable_detail',args=[str(timetable_id)])

class ExamEdit(UpdateView):
	""" Used to Edit no of students attending for this exam """
	model = Exam
	form_class =  modelform_factory(Exam,fields=['timetable_id','dateOfExam','noOfStudents'])
	def get_form(self, form_class=form_class):
		form = super(ExamEdit,self).get_form(form_class) #instantiate using parent
		form.fields['timetable_id'].disabled=True
		form.fields['dateOfExam'].disabled=True
		return form
	def get_success_url(self):
		timetable_id=self.request.session['timetableSession']
		return reverse_lazy('timetable_detail',args=[str(timetable_id)])

"""def selectExamsForStaffsForATimeTable(request,pk):
	#Getting Staff Name
	querysetStaff = Staff.objects.filter(id=pk)
	staffName = querysetStaff.get().name
	#Get Timetable id from Sessions
	timetable_id = request.session['timetableSession']
	timetableName = request.session['timetableName'] 
	#Exam query Set
	qs = Exam.objects.filter(timetable_id=timetable_id)
	qs2 = Exam.objects.filter(staffs=pk)

	exam_instance = get_object_or_404(Exam, pk=pk)

	# If this is a POST request then process the Form data
	if request.method == 'POST':
		form = SelectExamsForm(request.POST)

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			examdates = form.cleaned_data['Exams']
			for e in examdates:
				e.staffs.add(pk)
				e.save()
			# redirect to a new URL:
			return HttpResponseRedirect(reverse('staff_list') )
	else:
		#Declaring Form
		form = SelectExamsForm(qs,qs2)
		context = {'form':form, 'staffName':staffName, 'timetableName':timetableName}
	return render_to_response('allotment/exam_form.html', context=context)"""

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

def report(request,pk):
	
	queryset=Exam.objects.filter(id=pk)
	
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

	c = canvas.Canvas(response)
	c.setPageSize(A4)
	c.setFont("Helvetica", 14)

	i=10
	j=750
	for s in queryset:
		c.drawString(i,j,str(s.staffs__name))
		j=j-10

	c.showPage()
	c.save()
	return response