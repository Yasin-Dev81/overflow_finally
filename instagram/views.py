from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from instagrapi import Client, exceptions as insta_except

from . import models
from . import tasks
from .forms import NewInstaUserForm


# finished
@staff_member_required
def add_user_view(request):
    request_method = request.method
    if request_method == 'POST':
        # add data in data-base with forms
        new_insta_user_form = NewInstaUserForm(request.POST)
        if new_insta_user_form.is_valid():
            print('---valid.')
            new_insta_user = new_insta_user_form.save(commit=False)
            cl = Client(settings=models.MyInstaPage.objects.order_by('?').first().settings)
            new_insta_user.user_id = str(cl.user_id_from_username(str(new_insta_user)))
            new_insta_user.save()
            return redirect(reverse('user_list_url'))
        else:
            print('---not valid!')
            insta_user_form = NewInstaUserForm()
    else:
        insta_user_form = NewInstaUserForm()  # send forms to templates
    return render(request, "instagram/add_user.html", context={'form': insta_user_form})


# finished
@staff_member_required
def add_pk_view(request, userid):
    my_page = get_object_or_404(models.InstaUserForCopy, user_id=userid).user_pub
    tasks.GetPk(my_page, target_userid=userid).start()
    return HttpResponse('adding pk started...')


# finished
@staff_member_required
def user_list_view(request):
    return render(
        request,
        'instagram/user_list_view.html',
        context={
            'instagram_user': models.InstaUserForCopy.objects.all(),
        }
    )


# finished
@staff_member_required
def user_pub_list_view(request):
    return render(
        request,
        'instagram/user_pub_list_view.html',
        context={
            'instagram_user': models.MyInstaPage.objects.all(),
        }
    )


def posting_view(request, password, user_pub):
    if password == 'poolooshk':
        try:
            user_pub = get_object_or_404(models.MyInstaPage, user_key=user_pub)
            random_pk = models.InstaPkForCopy.objects.filter(user_pub=user_pub).order_by('?').first()
            print(random_pk, user_pub)
            cl = tasks.InstaPosting(
                pk=random_pk.insta_pk,
                my_username=user_pub.username,
                my_settings=user_pub.settings,
            )
            cl.get_data()
            print('---data got.')
            cl.start()
            random_pk.status = 'pub'
            random_pk.save()
            return HttpResponse('started...')
        except insta_except.UnknownError:
            return redirect(reverse('posting_url', args=['poolooshk', ]))
        except insta_except.MediaNotFound:
            return redirect(reverse('posting_url', args=['poolooshk', ]))
    else:
        return HttpResponse('password is incorrect!')


@staff_member_required
def get_settings(request, user_pub):
    cl = Client()
    user = get_object_or_404(models.MyInstaPage, user_key=user_pub)
    cl.login(user.username, user.password)
    user.settings = cl.get_settings()
    user.save()
    return HttpResponse('login process finished...')
