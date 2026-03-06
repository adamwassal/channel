from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

from .models import Episode, Question, Section


def _is_admin(user) -> bool:
    return user.is_authenticated and user.is_superuser


def home(request):
    if request.method == "POST" and _is_admin(request.user):
        title = request.POST.get("title", "").strip()
        mode = request.POST.get("mode", "").strip()
        if title and mode in {Episode.MODE_PODCAST, Episode.MODE_VIDEO}:
            episode = Episode.objects.create(title=title, mode=mode)
            return redirect("episode-detail", episode_id=episode.id)
    episodes = Episode.objects.all().order_by("-created_at")
    return render(request, "home.html", {"episodes": episodes})


def episode_detail(request, episode_id: int):
    episode = get_object_or_404(Episode, id=episode_id)
    questions = list(episode.questions.all())
    sections = list(episode.sections.all())
    section_map = {}
    section_groups = []
    for index, question in enumerate(questions):
        name = (question.section or "عام").strip() or "عام"
        if name not in section_map:
            section_map[name] = {"name": name, "questions": []}
            section_groups.append(section_map[name])
        section_map[name]["questions"].append(
            {
                "id": question.id,
                "index": index,
                "text": question.text,
                "section": name,
            }
        )
    return render(
        request,
        "episode_detail.html",
        {
        "episode": episode,
        "questions": questions,
        "section_groups": section_groups,
        "sections": sections,
    },
    )


@require_POST
@login_required
@user_passes_test(_is_admin)
def add_question(request, episode_id: int):
    episode = get_object_or_404(Episode, id=episode_id)
    text = request.POST.get("question", "").strip()
    section_id = request.POST.get("section_id", "").strip()
    section_name = "عام"
    if section_id:
        section = Section.objects.filter(id=section_id, episode=episode).first()
        if section:
            section_name = section.name
    if text:
        max_pos = episode.questions.aggregate(Max("position"))["position__max"] or 0
        Question.objects.create(
            episode=episode,
            text=text,
            position=max_pos + 1,
            section=section_name,
        )
    return redirect("episode-detail", episode_id=episode.id)


@require_POST
@login_required
@user_passes_test(_is_admin)
def add_section(request, episode_id: int):
    episode = get_object_or_404(Episode, id=episode_id)
    name = request.POST.get("section_name", "").strip()
    if name:
        Section.objects.get_or_create(episode=episode, name=name)
    return redirect("episode-detail", episode_id=episode.id)


@require_POST
@login_required
@user_passes_test(_is_admin)
def update_question(request, episode_id: int, question_id: int):
    episode = get_object_or_404(Episode, id=episode_id)
    question = get_object_or_404(Question, id=question_id, episode=episode)
    text = request.POST.get("question_text", "").strip()
    section_id = request.POST.get("section_id", "").strip()
    section_name = "عام"
    if section_id:
        section = Section.objects.filter(id=section_id, episode=episode).first()
        if section:
            section_name = section.name
    if text:
        question.text = text
        question.section = section_name
        question.save(update_fields=["text", "section"])
    return redirect("episode-detail", episode_id=episode.id)


@require_POST
@login_required
@user_passes_test(_is_admin)
def update_script(request, episode_id: int):
    episode = get_object_or_404(Episode, id=episode_id)
    if episode.mode == Episode.MODE_VIDEO:
        episode.script = request.POST.get("script", "")
        episode.save(update_fields=["script"])
    return redirect("episode-detail", episode_id=episode.id)
