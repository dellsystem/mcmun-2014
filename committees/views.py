import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.static import serve

from committees.models import Committee, position_paper_upload_path
from committees.forms import AdHocAppForm, DEFCONAppForm, ICCAppForm, \
     CEAAppForm, UFCAppForm, GreatEmpireAppForm, AwardAssignmentFormset
from committees.utils import get_committee_from_email


def view(request, slug):
    committee = get_object_or_404(Committee, slug=slug)
    if not (committee.is_visible or committee.is_assignable):
        raise Http404

    # If the committee is assignable but not visible, it's a subcommittee
    # for a joint committee. Just show a link to the umbrella committee, whose
    # slug should be entered in the description field.
    is_subcommittee = committee.is_assignable and not committee.is_visible
    show_manage_link = (committee.allow_manager(request.user) and
                        committee.is_assignable)

    data = {
        'title': committee.name,
        'is_subcommittee': is_subcommittee,
        'committee': committee,
        'dais_template': 'dais_photos/%s.html' % committee.slug,
        'DAIS_PHOTO_URL': '%simg/dais/%s/' % (settings.STATIC_URL, committee.slug),
        'show_manage_link': show_manage_link,
    }

    return render(request, 'committee.html', data)


def application(request, slug):
    # Hard-coding the list of committees with applications for now
    # This should really be a field on the committee (for next year)
    committee = get_object_or_404(Committee, slug=slug)

    app_forms = {
        'ad-hoc': AdHocAppForm,
        'defcon': DEFCONAppForm,
        'ufc': UFCAppForm,
        'cea': CEAAppForm,
        'icc': ICCAppForm,
        'great-empire': GreatEmpireAppForm,
    }

    if slug in app_forms:
        app_form = app_forms[slug]
    else:
        return redirect(committee)

    if request.method == 'POST':
        form = app_form(request.POST)

        if form.is_valid():
            form.save()

            data = {
                'committee': committee,
                'title': 'Successful application for %s' % committee.name,
            }

            return render(request, 'committee_app_success.html', data)
    else:
        form = app_form

    data = {
        'deadline': 'November 18th',
        'title': 'Application for %s' % committee.name,
        'intro_template': 'committee_apps/%s.md' % slug,
        'committee': committee,
        'form': form,
    }

    return render(request, 'committee_app.html', data)


@login_required
def serve_papers(request, file_name):
    # Check if user is an admin/mod OR if the user uploaded the file OR dais
    is_authorised = False
    full_path = os.path.join(position_paper_upload_path, file_name)

    if request.user.is_staff:
        is_authorised = True
    elif request.user.username.endswith('@mcmun.org'):
        # Check the dais
        committee = get_committee_from_email(request.user.username)
        if committee and committee.committeeassignment_set.filter(position_paper=full_path):
            is_authorised = True
    else:
        user_schools = request.user.registeredschool_set.filter(is_approved=True)
        if user_schools.count() == 1:
            school = user_schools[0]
            if school.committeeassignment_set.filter(position_paper=full_path):
                is_authorised = True

    if is_authorised:
        return serve(request, file_name, os.path.join(settings.MEDIA_ROOT, position_paper_upload_path))
    else:
        raise PermissionDenied


def timer(request, slug):
    committee = get_object_or_404(Committee, slug=slug)
    context = {
        'committee': committee,
    }

    return render(request, 'timer.html', context)


@login_required
def manage(request, slug):
    committee = get_object_or_404(Committee, slug=slug)

    # Disable the dashboard for umbrella committees.
    if not committee.is_assignable:
        raise Http404

    if not committee.allow_manager(request.user):
        raise PermissionDenied

    context = {
        'committee': committee,
        'title': 'Committee dashboard for %s' % committee.name,
    }

    return render(request, 'committee_manage.html', context)


@login_required
def awards(request, slug):
    committee = get_object_or_404(Committee, slug=slug)
    if not committee.allow_manager(request.user):
        raise PermissionDenied

    awards = committee.awards.all()
    if request.method == 'POST':
        formset = AwardAssignmentFormset(request.POST, queryset=awards)
        if formset.is_valid():
            formset.save()
    else:
        formset = AwardAssignmentFormset(queryset=awards)

    context = {
        'committee': committee,
        'title': 'Awards dashboard for %s' % committee.name,
        'formset': formset,
        'positions': committee.committeeassignment_set.all(),
    }

    return render(request, 'committee_awards.html', context)


@login_required
def list_papers(request, slug):
    committee = get_object_or_404(Committee, slug=slug)

    # Only the dais for this committee and other admins can access this
    if (get_committee_from_email(request.user.username) == committee
        or request.user.is_staff):
        assignments = committee.committeeassignment_set.order_by('assignment')
        data = {
            'title': 'Position papers for %s' % committee.name,
            'committee': committee,
            'assignments': assignments,
        }

        return render(request, 'list_papers.html', data)
    else:
        raise PermissionDenied
