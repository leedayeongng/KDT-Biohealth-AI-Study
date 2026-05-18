from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import Member


def get_current_member(request: HttpRequest):
    member_id = request.session.get("member_id")
    if not member_id:
        return None
    return Member.objects.filter(id=member_id).first()


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "members/home.html", {"member": get_current_member(request)})


@require_POST
def signup(request: HttpRequest) -> HttpResponse:
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    if not username or not password:
        messages.error(request, "아이디와 비밀번호를 모두 입력해주세요.")
        return redirect("home")
    if Member.objects.filter(username=username).exists():
        messages.error(request, "이미 존재하는 아이디입니다.")
        return redirect("home")
    member = Member.objects.create(username=username, password=make_password(password))
    request.session["member_id"] = member.id
    messages.success(request, "회원가입과 세션 로그인이 완료되었습니다.")
    return redirect("profile")


@require_POST
def login(request: HttpRequest) -> HttpResponse:
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    member = Member.objects.filter(username=username).first()
    if member is None or not check_password(password, member.password):
        messages.error(request, "로그인 정보가 올바르지 않습니다.")
        return redirect("home")
    request.session["member_id"] = member.id
    messages.success(request, "세션 로그인이 완료되었습니다.")
    return redirect("profile")


@require_POST
def logout(request: HttpRequest) -> HttpResponse:
    request.session.flush()
    messages.success(request, "세션 로그아웃이 완료되었습니다.")
    return redirect("home")


@require_GET
def profile(request: HttpRequest) -> HttpResponse:
    member = get_current_member(request)
    if member is None:
        messages.error(request, "먼저 세션 로그인해주세요.")
        return redirect("home")
    return render(request, "members/profile.html", {"member": member})
