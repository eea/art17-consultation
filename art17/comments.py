from flask import (
    Blueprint,
    views,
    render_template,
    request,
)
from werkzeug.utils import redirect
from art17.auth import current_user
from art17.common import get_default_period
from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import Dataset


comments = Blueprint('comments', __name__)


class CommentsList(views.View):

    def dispatch_request(self, subject, region, user, MS):
        record = self.get_manual_record(subject, region, user, MS)
        return render_template('comments/list.html', record=record)


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
