from datetime import datetime
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    flash,
)
from werkzeug.datastructures import MultiDict
from werkzeug.utils import redirect
from art17.auth import current_user
from art17.common import get_default_period, admin_perm
from art17.forms import CommentForm
from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import Dataset, db


DATE_FORMAT = '%Y-%m-%d'


comments = Blueprint('comments', __name__)


def mark_read(comment, user):
    comment.readers.append(user)
    db.session.commit()


def mark_unread(comment, user):
    comment.readers.remove(user)
    db.session.commit()


@comments.app_template_global('can_post_comment')
def can_post_comment(record):
    if not current_user.is_authenticated():
        return False
    can_add = False
    if current_user.has_role('stakeholder') or current_user.has_role('nat'):
        if record.user.has_role('stakeholder') or \
            (record.user.has_role('nat')
             and record.user_id == current_user.id):
                can_add = True
    else:
        can_add = True

    if can_add:
        authors = [c.author_id for c in record.comments]
        if current_user.id in authors:
            return False

    return not record.deleted and can_add


@comments.app_template_global('can_edit_comment')
def can_edit_comment(comment):
    if not comment or not current_user.is_authenticated():
        return False
    return (
        not comment.record.deleted and not comment.deleted
        and (comment.author_id == current_user.id or admin_perm.can())
    )


@comments.app_template_global('can_toggle_read')
def can_toggle_read(comment):
    if not comment or not current_user.is_authenticated():
        return False

    if comment.author_id == current_user.id:
        return False

    return True


@comments.app_template_global('can_delete_comment')
def can_delete_comment(comment):
    if not comment or not current_user.is_authenticated():
        return False

    if comment.author_id == current_user.id:
        return True

    return admin_perm.can()


class CommentsList(views.View):

    methods = ['GET', 'POST']

    def toggle_delete(self, comment):
        if not can_delete_comment(comment):
            flash('You are not allowed here', 'error')
            return False

        if comment.deleted is None:
            comment.deleted = 0
        comment.deleted = 1 - comment.deleted
        db.session.commit()

    def toggle_read(self, comment):
        if not can_toggle_read(comment):
            flash('You are not allowed here', 'error')
            return False
        if comment.read_for(current_user):
            mark_unread(comment, current_user)
        else:
            mark_read(comment, current_user)

    def process_form(self, form, edited_comment):
        if form.validate():
            if edited_comment:
                if not can_edit_comment(edited_comment):
                    flash('You are not allowed here', 'error')
                    return False
                edited_comment.comment = form.comment.data
                edited_comment.post_date = datetime.now().strftime(DATE_FORMAT)
            else:
                if not can_post_comment(self.record):
                    flash('You are not allowed here', 'error')
                    return False
                comment = self.model_comment_cls(
                    subject=self.record.subject,
                    region=self.record.region,
                    user=self.record.user_id,
                    MS=self.record.MS,
                    comment=form.comment.data,
                    author_id=current_user.id,
                    post_date=datetime.now().strftime(DATE_FORMAT),
                    dataset_id=self.record.dataset_id,
                )
                db.session.add(comment)
            db.session.commit()
            if not edited_comment:
                mark_read(comment, current_user)
            return True
        else:
            flash('The form has errors', 'error')
            return False

    def dispatch_request(self, subject, region, user, MS):
        self.record = self.get_manual_record(subject, region, user, MS)
        edited_comment = None
        if request.args.get('edit'):
            edit_id = request.args.get('edit')
            edited_comment = self.model_comment_cls.query.get(
                (edit_id, self.record.dataset_id))
            if not can_edit_comment(edited_comment):
                flash('You are not allowed to edit this comment', 'error')
                edited_comment = None
        if request.args.get('toggle'):
            comment = self.model_comment_cls.query.get(
                (request.args['toggle'], self.record.dataset_id)
            )
            self.toggle_read(comment)
        if request.args.get('delete'):
            comment = self.model_comment_cls.query.get(
                (request.args['delete'], self.record.dataset_id)
            )
            self.toggle_delete(comment)

        if request.method == 'POST':
            form = CommentForm(request.form)
            if self.process_form(form, edited_comment):
                if edited_comment:
                    hash = '#comment-%s' % edited_comment.id
                else:
                    hash = '#theform'
                return redirect(request.base_url + hash)
        else:
            if edited_comment:
                form_data = MultiDict({'comment': edited_comment.comment})
            else:
                form_data = MultiDict({})
            form = CommentForm(form_data)

        return render_template(
            'comments/list.html',
            record=self.record,
            form=form,
            edited_comment=edited_comment,
        )


class SpeciesCommentsList(SpeciesMixin, CommentsList):

    pass


class HabitatCommentsList(HabitatMixin, CommentsList):

    pass


comments.add_url_rule('/species/comments/<subject>/<region>/<user>/<MS>/',
                      view_func=SpeciesCommentsList.as_view('species-comments'))

comments.add_url_rule('/habitat/comments/<subject>/<region>/<user>/<MS>/',
                      view_func=HabitatCommentsList.as_view('habitat-comments'))


class UserSummary(views.View):

    template = 'history/history.html'

    def dispatch_request(self):
        if not current_user.is_authenticated():
            return redirect('/')
        period = request.args.get('period') or get_default_period()
        period_obj = Dataset.query.get(period)
        history = self.get_history(period)
        return render_template(
            self.template,
            history=history,
            subject_name=self.subject_name,
            summary_endpoint=self.summary_endpoint,
            period=period_obj,
        )

    def get_history(self, period):
        conclusions = (
            self.model_manual_cls.query
            .filter_by(dataset_id=period)
            .order_by('-last_update').limit(100)
        )
        comments_qs = (
            self.model_comment_cls.query
            .join(self.model_comment_cls.record)
            .filter(self.model_manual_cls.dataset_id == period)
            .order_by('-post_date').all()
        )
        return {'conclusions': conclusions, 'comments': comments_qs}


class SpeciesUserSummary(SpeciesMixin, UserSummary):

    summary_endpoint = 'summary.species-summary'


class HabitatUserSummary(HabitatMixin, UserSummary):

    summary_endpoint = 'summary.habitat-summary'


comments.add_url_rule('/history/species/',
                      view_func=SpeciesUserSummary.as_view('species-history'))
comments.add_url_rule('/history/habitat/',
                      view_func=HabitatUserSummary.as_view('habitat-history'))
