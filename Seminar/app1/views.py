from collections import UserDict
from .models import CustomUser,Dokument,StudentDokument
from django.db.models import Count
from collections import Counter
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render,redirect,get_object_or_404
from collections import Counter
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from .decorators import unauthenticated_user,allowd_users

def is_admin(user):
    return user.role == 'admin'


def is_professor(user):
     return user.role == 'profesor'


def is_student(user):
     return user.role == 'student'


# Create your views here.
@user_passes_test(is_admin)
def reg(request):
    form=CreateUserForm()
     
    if request.method=="POST":
        
        form=CreateUserForm(request.POST)
       
        
        if form.is_valid():
            form.save()
            
            
            user=form.cleaned_data.get('username')
            messages.success(request,'Profile details updated for '+ user)
            
            return redirect('domaa')
        
            
    context={'form':form}

    return render(request,'app1/reg.html',context)

def log(request):
    

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        

        user=authenticate(request,username=username ,password=password)

        if user is not None:
            login(request,user)
            
            return redirect('domaa')
        else:
            messages.info(request, 'Username or Password are WRONG')
            


    context={}
    return render(request,'app1/log.html',context)



#@allowd_users(allowd_roles=['admin','student','profesor'])
@login_required
def nov(request):
    if request.method == 'GET':
        username=request.user.username
        

        messages.warning(request, 'Nebi smija bit odi '+ username )
        
    return render(request,"app1/nov.html",{})


#@allowd_users(allowd_roles=['admin','student','profesor'])
@login_required
def doma(request):
    if request.method == 'GET':
        username=request.user.username
        user_role = request.user.role  


        ##messages.success(request, 'Profile details updated '+ username )
    
        
        messages.warning(request, 'Ti si '+ user_role)

    return render(request,"app1/doma.html",{})
@login_required
def domaa(request):
    user = request.user
    if user.role == 'admin':
        return render(request, 'app1/sucess_admin.html', {'user': user})

    elif user.role == 'student':
        return render(request, 'app1/sucess_student.html', {'user': user})
    elif user.role == 'profesor':
        return render(request, 'app1/sucess_prof.html', {'user': user})   
    else:
        return redirect('/accounts/log/')

@login_required
def admin_users(request):
    all_users = CustomUser.objects.all()
    


    students = CustomUser.objects.filter(role='student').order_by('username')
    professors = CustomUser.objects.filter(role='profesor').order_by('username')
    
    all_users = list(students) + list(professors)
    sort_by = request.GET.get('sort_by', 'username')  # Default sorting by username

    if sort_by == 'username':
        all_users.sort(key=lambda user: user.username)
    elif sort_by == 'student':
        all_users.sort(key=lambda user: (user.role != 'student', user.username))
    elif sort_by == 'profesor':
        all_users.sort(key=lambda user: (user.role != 'profesor', user.username))

    user_data = [{'username': user.username, 'role': user.role} for user in all_users]
    return render(request, 'app1/admin_users.html', {'users': user_data, 'sort_by': sort_by})

 

@login_required    
def admin_users_delete(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
        return redirect('admin_users')  # Redirect to the users list page

    users = CustomUser.objects.all()
    return render(request, 'app1/admin_users_delete.html', {'users': users})
@login_required
def admin_users_edit_2(request):
    users = CustomUser.objects.all()
    selected_user = None
    form = None

    if request.method == 'POST':
        
        user_id = request.POST.get('user_id')
        
        if user_id:
            student = get_object_or_404(CustomUser, id=user_id)
            form = UserChangeForm(request.POST or None, instance=student)
            if form.is_valid():
                form.save()
                return redirect('domaa')  # Redirect to the users list page
  

    return render(request, 'app1/admin_users_edit.html', {'users': users, 'selected_user': selected_user, 'form': form})
            
        
##def edit_student(request, student_id):
    student = get_object_or_404(Korisnici, id=student_id)
    form = KorisniciForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'edit_student.html', {'form': form})

    



from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import UserChangeForm
@login_required
def admin_users_edit(request):
    users = CustomUser.objects.all()
    selected_user = None
    form = None

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            selected_user = CustomUser.objects.get(id=user_id)
            form = UserChangeForm(request.POST, instance=selected_user)

            if form.is_valid():
                form.save()
                return redirect('domaa')  # Redirect to the users list page
    else:
        user_id_to_edit = request.GET.get('edit_user_id')
        if user_id_to_edit:
            selected_user = CustomUser.objects.get(id=user_id_to_edit)
            form = UserChangeForm(instance=selected_user)
    
    return render(request, 'app1/admin_users_edit.html', {'users': users, 'selected_user': selected_user, 'form': form})


@login_required
def prof_create_document(request):
   
    if request.method == 'POST':
        naslov = request.POST.get('naslov')
        putanja = request.FILES.get('putanja')
        kreator = request.user  # Trenutno prijavljeni korisnik, pretpostavka da je profesor

        # Stvaranje novog dokumenta
        novi_dokument = Dokument(naslov=naslov, putanja=putanja, kreator=kreator)
        novi_dokument.save()

        return redirect('prof_view_document')  #  za prikaz popisa dokumenata

    return render(request, 'app1/prof_create_document.html')



@login_required    
def prof_view_document(request):
 
    
    sortiranje = request.GET.get('sortiranje', 'vrijeme_kreiranja')  # Default sortiranje po vremenu kre
    dokumenti = Dokument.objects.filter(kreator_id=request.user.id).order_by(sortiranje)##kreator_id=request.user.id uvjet da u dokument kreator_id treba biti isti ka id usera

    return render(request, 'app1/prof_view_document.html', {'dokumenti': dokumenti, 'sortiranje': sortiranje})





@login_required
def prof_delete_document(request):
    if request.method == 'POST':
        dokument_id = request.POST.get('dokument_id')
        dokument = get_object_or_404(Dokument, pk=dokument_id)##dohvacanje 1og dok iz baze

        # Provjera korisnika da li je on kreator dokumenta ili ima prava za brisanje
        if dokument.kreator == request.user:
            dokument.delete()
            return redirect('domaa')

    dokumenti = Dokument.objects.filter(kreator_id=request.user.id)##dohvacanje svig iz baze
    return render(request, 'app1/prof_delete_document.html', {'dokumenti': dokumenti})
@login_required
def prof_share_document(request):
    if request.method == 'POST':
        dokument_id = request.POST.get('dokument_id')
        studenti_ids = request.POST.getlist('studenti')
        
        dokument = get_object_or_404(Dokument, pk=dokument_id)

        for student_id in studenti_ids:
            student = get_object_or_404(CustomUser, pk=student_id)

            # Provjeri je li dokument već podijeljen s trenutnim korisnikom
            if StudentDokument.objects.filter(dokument=dokument, student=student).exists():
                messages.error(request, f"Dokument je već podijeljen s korisnikom {student.username}.")
                return redirect('prof_share_document')

            # Ako dokument nije podijeljen s trenutnim korisnikom, podijeli ga
            StudentDokument.objects.create(dokument=dokument, student=student)

        return redirect('domaa')

    dokumenti = Dokument.objects.filter(kreator_id=request.user.id)
    studenti = CustomUser.objects.filter(role='student')
    return render(request, 'app1/prof_share_document.html', {'dokumenti': dokumenti, 'studenti': studenti})



@login_required
def prof_share_document_list(request):
    if request.method == 'POST':
        student_dokument_id = request.POST.get('student_dokument_id')
        student_dokument = get_object_or_404(StudentDokument, pk=student_dokument_id)
        
        # Provjera da li je korisnik (profesor) kreator dokumenta prije nego što se poništi dijeljenje
        if student_dokument.dokument.kreator == request.user:
            student_dokument.delete()
            return redirect('domaa')

    student_dokumenti = StudentDokument.objects.all()

    # Filtriranje student_dokumenti da sadrži samo one gdje je korisnik (profesor) kreator dokumenta
    student_dokumenti = [sd for sd in student_dokumenti if sd.dokument.kreator == request.user]##prolazi kroz svaki el u listi i gleda uvjet

    return render(request, 'app1/prof_share_document_list.html', {'student_dokumenti': student_dokumenti})





##def prof_share_document_lisst(request):
    if request.method == 'POST':
        student_dokument_id = request.POST.get('student_dokument_id')
        student_dokument = get_object_or_404(StudentDokument, pk=student_dokument_id)
        
        # Provjera da li je korisnik (profesor) kreator dokumenta prije nego što se poništi dijeljenje
        if student_dokument.dokument.kreator == request.user:
            student_dokument.delete()
            return redirect('domaa')

    student_dokumenti = StudentDokument.objects.all()
    return render(request, 'app1/prof_share_document_list.html', {'student_dokumenti': student_dokumenti})

@login_required
def student_shared_document(request):
    current_user=request.user
    Lista=[]
    student_dokumenti = StudentDokument.objects.filter(student_id=current_user)##sve dok sa useron trenutnin
    Dokument_ids = [student_dokument.dokument_id for student_dokument in student_dokumenti] ##spreman dok ids
    dokumenti = Dokument.objects.filter(id__in=Dokument_ids)##nalazin sve dok sa tin id
    Kreator_idss = [dokument.kreator_id for dokument in dokumenti] ##iz njih vadin kreator id
    
    for x in Dokument_ids:
        Stud_Dok = StudentDokument.objects.get(dokument_id=x,student_id=current_user)
        Lista.append(Stud_Dok)




    

    professors1 = CustomUser.objects.filter(role='profesor', id__in=Kreator_idss)   #uzima sve profesore -6-      



    ##student_dokument_id = request.POST.get('student_dokument_id')##uzme sve kjuceve
   ## student_dokument=StudentDokument.objects.filter(pk__in=student_dokument_id_list)##uzima sve iz baze sa tin kljucen


    sortiranje = request.GET.get('sortiranje', 'vrijeme_kreiranja')
    student_dokumenti = StudentDokument.objects.filter(student_id=request.user.id)##uzima sve uz uvijet da je shersno sa userom -6-
    selected_prof_id = request.POST.get('kreator_id') ##trenutni id vata za sortiranje
    selected_prof = CustomUser.objects.get(id=selected_prof_id) if selected_prof_id else None ##uzima 


    # Sortiraj student_dokumenti prema odabranom kriteriju
    if sortiranje == 'vrijeme_kreiranja':
        student_dokumenti = student_dokumenti.order_by('dokument__vrijeme_kreiranja')
    elif sortiranje == 'naslov':
        student_dokumenti = student_dokumenti.order_by('dokument__naslov')
        

    return render(request, 'app1/student_shared_document.html', {'Stud_Dok':Stud_Dok,'student_dokumenti': student_dokumenti, 'sortiranje': sortiranje,'dokumenti':dokumenti,'Kreator_idss':Kreator_idss,'professors1':professors1,'selected_prof': selected_prof, 'student_dokumenti': student_dokumenti})


    
def ispis_studenata(request):
    studenti = CustomUser.objects.filter(role='student').values_list('id', flat=True)

    student_dokumenti = StudentDokument.objects.all() ##medutablica
    Studenti_ids = [student_dokument.student_id for student_dokument in student_dokumenti] ##da uzmen sve id iz medutablice
    nova_lista = list(set(Studenti_ids)) ## bez duplikata

    brojac = Counter(Studenti_ids)
    rezultati = []
    for broj, broj_ponavljanja in brojac.items():
        rezultati.append(f"Broj {broj} se pojavljuje {broj_ponavljanja} puta.")

    



    
  




    Dokumentii=Dokument.objects.all().count()  
    

  

    




    



    return render(request, 'app1/ispis_studenata.html', {'rezultati': rezultati,'nova_lista':nova_lista,'Studenti_ids':Studenti_ids, 'studenti':studenti,'Dokumentii':Dokumentii,'student_dokumenti':student_dokumenti})






        








##def student_shared_document1(request):
    
    
    Kreator_idss=[]
    professors = CustomUser.objects.filter(role='profesor')
   
    Dokument_ids=StudentDokument.objects.values_list('dokument_id')       #uzme sve id od tablice -1-
    dokumenti=Dokument.objects.all()       #uzme sve instance dokumenata -2-
    ##Student_id_list = list(set(Dokument_ids.split(',')))##sredi kljuce
    #kreator_id = Dokument.objects.filter(studentdokument__dokument=Dokument_ids)
    Dokument_ids = [x[0] for x in Dokument_ids] ##imam dokumente podiljenje al to mi netriba
      
    for dok_id in Dokument_ids:
        student_dokument = StudentDokument.objects.get(dokument_id=dok_id)   ##uzimamo instance priko id -3-
        dokument = student_dokument.dokument #da pristupi dokumentima
        kreator_id = dokument.kreator_id ## uzima sve idjeve koji postojwe u dokumentima -4-
        Kreator_idss.append(kreator_id) #sprema ih -5-
        

    Kreator_idss = list(set(Kreator_idss))

    professors1 = CustomUser.objects.filter(role='profesor', id__in=Kreator_idss)   #uzima sve profesore -6-      



    ##student_dokument_id = request.POST.get('student_dokument_id')##uzme sve kjuceve
   ## student_dokument=StudentDokument.objects.filter(pk__in=student_dokument_id_list)##uzima sve iz baze sa tin kljucen


    sortiranje = request.GET.get('sortiranje', 'vrijeme_kreiranja')
    student_dokumenti = StudentDokument.objects.filter(student_id=request.user.id)##uzima sve uz uvijet da je shersno sa userom -6-
    selected_prof_id = request.POST.get('kreator_id') ##trenutni id vata za sortiranje
    selected_prof = CustomUser.objects.get(id=selected_prof_id) if selected_prof_id else None ##uzima 


    # Sortiraj student_dokumenti prema odabranom kriteriju
    if sortiranje == 'vrijeme_kreiranja':
        student_dokumenti = student_dokumenti.order_by('dokument__vrijeme_kreiranja')
    elif sortiranje == 'naslov':
        student_dokumenti = student_dokumenti.order_by('dokument__naslov')
        

    return render(request, 'app1/student_shared_document.html', {'student_dokumenti': student_dokumenti, 'sortiranje': sortiranje,'dokumenti':dokumenti,'Kreator_idss':Kreator_idss,'professors1':professors1,'selected_prof': selected_prof, 'student_dokumenti': student_dokumenti})
