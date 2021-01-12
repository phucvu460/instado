import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Profile, FriendRequest, User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        f = UserRegisterForm(request.POST)
        if f.is_valid():
            f.save()
            # username = f.cleaned_data['username']
            messages.success(request, f'Your account has been created! You can now login!')
            return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "Failed to create new account. Please check again the information")
            return render(request, "accounts/register.html", {
                "form": f
            })


    return render(request, "accounts/register.html", {
        "form": UserRegisterForm()
    })

@login_required
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)

    friends = []
    sent_to = []

    my_friends = request.user.profile.friends.all()
    for u in users:
        if u not in my_friends:
            friends.append(u)
    
    for se in sent_friend_requests:
        sent_to.append(se.to_user)


    return render(request, "accounts/users_list.html", {
        "users": friends,
        "sent": sent_to
    })


@login_required
def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return HttpResponseRedirect(reverse("profile_view", 
                                args=[request.user.profile.slug]))

    return render(request, "accounts/edit_profile.html", {
        "u_form": UserUpdateForm(instance=request.user),
        "p_form": ProfileUpdateForm(instance=request.user.profile)
    })



@login_required
def friend_list(request):
    p = request.user.profile
    friends = p.friends.all()
    return render(request, "accounts/friend_list.html", {
        "friends": friends
    })


@login_required
def send_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user,
                                                                    to_user=user)
    friend_request.save()
    # return HttpResponseRedirect(reverse("profile_view", args=[user.profile.slug]))


@login_required
def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    friend_request = FriendRequest.objects.filter(from_user=request.user,
                                                    to_user=user).first()
    friend_request.delete()
    # return HttpResponseRedirect(reverse("profile_view", args=[user.profile.slug]))


@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    to_user = request.user
    friend_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first()

    from_user.profile.friends.add(to_user.profile)
    to_user.profile.friends.add(from_user.profile)
    friend_request.delete()
    # return HttpResponseRedirect(reverse("my_profile"))


@login_required
def reject_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    friend_request = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    friend_request.delete()
    # return HttpResponseRedirect(reverse("my_profile"))


@login_required
def unfriend(request, id):
    friend_profile = get_object_or_404(Profile, id=id)
    my_profile = request.user.profile

    friend_profile.friends.remove(my_profile)
    my_profile.friends.remove(friend_profile)
    # return HttpResponseRedirect(reverse("profile_view", args=[friend_profile.slug]))


actions = {
    'send_friend_request': send_friend_request,
    'cancel_friend_request': cancel_friend_request,
    'accept_friend_request': accept_friend_request,
    'reject_friend_request': reject_friend_request,
    'unfriend': unfriend
}

@csrf_exempt
@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    u = p.user

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        if action in actions:
            actions[action](request, u.id)
            return JsonResponse({
                "message": "Success",
                'is_friend': True if p in request.user.profile.friends.all() else False,
                'check_friend_request': True if FriendRequest.objects.filter(from_user=request.user, to_user=u) else False
                })
        else:
            return JsonResponse({'error': 'Failed action'})

    
    sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
    friends = p.friends.all()

    button_status = 'none' # 'none' means being friends already
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        if len(FriendRequest.objects.filter(from_user=request.user, to_user=u)) > 0:
            button_status = 'friend_request_sent'

    return render(request, "accounts/profile.html", {
        'u': u,
        'button_status': button_status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
    })


@login_required
def my_profile(request):
    p = request.user.profile
    you = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=you)
    rec_friend_requests = FriendRequest.objects.filter(to_user=you)
    friends = p.friends.all()

    button_status = 'none'
    if p not in request.user.profile.friends.all():
	    button_status = 'not_friend'

		# if we have sent him a friend request
	    if len(FriendRequest.objects.filter(from_user=request.user).filter(to_user=you)) == 1:
		    button_status = 'friend_request_sent'

    return render(request, "accounts/profile.html", {
        'u': you,
        'button_status': button_status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
    })


