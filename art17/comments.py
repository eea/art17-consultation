from flask import (
    Blueprint,
    views,
    render_template,
)
from art17.mixins import SpeciesMixin, HabitatMixin


comments = Blueprint('comments', __name__)


class CommentsList(views.View):

    def dispatch_request(self, subject, region, user, MS):
        record = self.get_manual_record(subject, region, user, MS)
        return render_template('comments/list.html', record=record)

    @classmethod
    def get_manual_record(cls, subject, region, user, MS):
        filters = {cls.subject_field: subject, 'region': region,
                   'user_id': user, 'MS': MS}
        return cls.model_manual_cls.query.filter_by(**filters).first()


class SpeciesCommentsList(SpeciesMixin, CommentsList):

    pass


class HabitatCommentsList(HabitatMixin, CommentsList):

    pass


comments.add_url_rule('/species/comments/<subject>/<region>/<user>/<MS>/',
                      view_func=SpeciesCommentsList.as_view('species-comments'))

comments.add_url_rule('/habitat/comments/<subject>/<region>/<user>/<MS>/',
                      view_func=HabitatCommentsList.as_view('habitat-comments'))
