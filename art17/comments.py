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
from art17.models import Dataset, Comment, db


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


comments = Blueprint('comments', __name__)


@comments.app_template_global('can_post_comment')
def can_post_comment(record):
    return not record.deleted and admin_perm.can()


class CommentsList(views.View):

    methods = ['GET', 'POST']

    def dispatch_request(self, subject, region, user, MS):
        record = self.get_manual_record(subject, region, user, MS)
        if request.method == 'POST':
            if not can_post_comment(record):
                flash('You are not allowed here', 'error')
            else:
                form = CommentForm(request.form)
                if form.validate():
                    comment = Comment(
                        subject=subject, region=region, user=user,
                        MS=MS, comment=form.comment.data,
                        author_id=current_user.id,
                        post_date=datetime.now().strftime(DATE_FORMAT)
                    )
                    db.session.add(comment)
                    db.session.commit()
                    flash('Comment successfully added')
                    form = CommentForm(MultiDict({}))
                else:
                    flash('The form has errors', 'error')
        else:
            form = CommentForm()
        return render_template('comments/list.html', record=record, form=form)


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
            .filter(self.model_manual_cls.dataset_id==period)
            .order_by('-post_date')
        )
        return {'conclusions': conclusions, 'comments': comments_qs}


class SpeciesUserSummary(SpeciesMixin, UserSummary):

    summary_endpoint = 'summary.species-summary'


class HabitatUserSummary(HabitatMixin, UserSummary):

    summary_endpoint = 'summary.habitat-summary'


comments.add_url_rule('/usersummary/species/',
                      view_func=SpeciesUserSummary.as_view('species-history'))
comments.add_url_rule('/usersummary/habitat/',
                      view_func=HabitatUserSummary.as_view('habitat-history'))
