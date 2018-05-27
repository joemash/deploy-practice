from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse


class BaseView(TemplateView):
	template_name = 'payrol.html'


	

	def post(self,request,*args,**kwargs):
	    myitems = []
	    import locale
	    locale.setlocale(locale.LC_ALL, '')

	    if request.is_ajax():
	        salary = float(request.POST.get("salary"))

	        net_salary = self.calculate_net_salary(salary)
	        net_paye =  self.calculate_net_paye(salary)
	        nhif = self.calculate_nhif(salary)
	        #convert the json string to a python object
	        #json1_data = json.loads(line_items)


	        data = {
	           'url':'http://127.0.0.1:8000/',
	           'salary':net_salary,
	           'net_paye':net_paye,
	           'nhif':nhif,

	        }
	        return JsonResponse(data)
	    return super(BaseView,self).get(request)




	def calculate_gross_paye(self,gross_pay):
	    gross_paye = 0.0
	    nssf = 200
	    taxable_pay = gross_pay - nssf

	    if taxable_pay >= 11181 and taxable_pay <= 21713:
	        gross_paye = 1118.03 + (taxable_pay - 11180) * 0.15

	    elif taxable_pay >= 21714 and taxable_pay <= 32247:
	        gross_paye = 2698.07 + (taxable_pay - 21713) * 0.2

	    elif taxable_pay >= 32248 and taxable_pay <= 42780:
	        gross_paye = 4804.79 + (taxable_pay - 32247) * 0.25

	    elif taxable_pay >= 42781:
	        gross_paye = 7438.18 + (taxable_pay - 42781) * 0.3

	    return round(gross_paye,1)

	def calculate_net_paye(self,gross_pay):
	    net_paye = 0.0
	    personal_relief = 1280

	    if gross_pay > 0:
	        gross_paye = self.calculate_gross_paye(gross_pay)

	        if gross_paye > 0:
	            net_paye = gross_paye -  personal_relief

	    return net_paye

	def calculate_nhif(self,salary):
	    nhif = 0.0

	    if salary >= 1000 and salary <= 5999:
	        nhif = 150

	    elif  salary >= 6000 and salary <= 7999:
	        nhif = 300

	    elif salary >= 8000 and salary <= 11999:
	        nhif = 400

	    elif  salary >= 12000 and salary <= 14999:
	        nhif = 500

	    elif  salary >= 15000 and salary <= 19999:
	        nhif = 600

	    elif  salary >= 20000 and salary <= 24999:
	        nhif = 750

	    elif  salary >= 25000 and salary <= 29999:
	        nhif = 850

	    elif  salary>=30000 and salary <= 34999:
	        nhif = 900

	    elif  salary >= 35000 and salary <= 39999:
	        nhif = 950

	    elif  salary>= 40000 and salary <= 44999:
	        nhif = 1000

	    elif  salary >= 45000 and salary <= 49999:
	        nhif = 1100

	    elif  salary >= 50000 and salary <= 59999:
	        nhif = 1200

	    elif  salary >= 60000  and salary <= 69999:
	        nhif = 1300

	    elif  salary >= 70000 and salary <= 79999:
	        nhif = 1400

	    elif  salary >= 80000 and salary <= 89999:
	        nhif = 1500

	    elif  salary >= 90000 and salary <= 99999:
	        nhif = 1600

	    elif  salary >= 100000:
	        nhif = 1700

	    return nhif

	def calculate_net_salary(self,gross_pay):
	    net_pay = 0.0
	    nssf = 200
	    if type(gross_pay) != str:
	        net_pay = gross_pay - nssf

	        if net_pay > 0:
	            net_pay -= self.calculate_net_paye(gross_pay) + self.calculate_nhif(gross_pay)
	        else:
	            return gross_pay
	    else:
	        net_pay = 0.0

	    return round(net_pay,0)
