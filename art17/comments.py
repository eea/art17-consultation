from datetime import datetime
from werkzeug.datastructures import MultiDict
from werkzeug.utils import redirect
from sqlalchemy import or_, func
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    url_for,
)
from flask.ext.principal import PermissionDenied

from art17.auth import current_user
from art17.common import get_default_period, admin_perm
from art17.forms import CommentForm
from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import (
    Dataset, db,
    Comment, t_comments_read, HabitatComment, t_habitat_comments_read,
    Wiki, WikiComment, t_wiki_comments_read,
)


DATE_FORMAT = '%Y-%m-%d'


comments = Blueprint('comments', __name__)


def mark_read(comment, user):
    comment.readers.append(user)


def mark_unread(comment, user):
    comment.readers.remove(user)


@comments.app_template_global('can_post_comment')
def can_post_comment(record):
    if not current_user.is_authenticated():
        return False
    if record.dataset and record.dataset.is_readonly:
        return False
    can_add = False
    if current_user.has_role('stakeholder') or current_user.has_role('nat'):
        if not record.user or record.user.has_role('stakeholder') or \
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
    if comment and comment.record and comment.record.dataset and \
            comment.record.dataset.is_readonly:
        return False
    return (not comment.record.deleted and not comment.deleted
            and comment.author_id == current_user.id)


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
            raise PermissionDenied

        if comment.deleted is None:
            comment.deleted = 0
        comment.deleted = 1 - comment.deleted
        db.session.commit()

    def toggle_read(self, comment):
        if not can_toggle_read(comment):
            raise PermissionDenied
        if comment.read_for(current_user):
            mark_unread(comment, current_user)
        else:
            mark_read(comment, current_user)
        db.session.commit()

    def process_form(self, form, edited_comment):
        if form.validate():
            if edited_comment:
                if not can_edit_comment(edited_comment):
                    raise PermissionDenied
                edited_comment.comment = form.comment.data
                edited_comment.readers = []
                edited_comment.post_date = datetime.now().strftime(DATE_FORMAT)
            else:
                if not can_post_comment(self.record):
                    raise PermissionDenied
                comment = self.model_comment_cls(
                    subject=self.record.subject,
                    region=self.record.region,
                    user_id=self.record.user_id,
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
                db.session.commit()
            return True
        else:
            raise PermissionDenied

    def dispatch_request(self, period, subject, region, user):
        MS = request.args.get('MS')
        self.record = self.get_manual_record(period, subject, region, user, MS)
        edited_comment = None
        if request.args.get('edit'):
            edit_id = request.args.get('edit')
            edited_comment = self.model_comment_cls.query.get(edit_id)
            if not can_edit_comment(edited_comment):
                raise PermissionDenied
        if request.args.get('toggle'):
            comment = self.model_comment_cls.query.get(request.args['toggle'])
            self.toggle_read(comment)
        if request.args.get('delete'):
            comment = self.model_comment_cls.query.get(request.args['delete'])
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
            home_url=self.get_home_url(subject=subject, region=region,
                                       user=user, MS=MS, period=period)
        )


class SpeciesCommentsList(SpeciesMixin, CommentsList):

    def get_home_url(self, **kwargs):
        return url_for('.species-comments', **kwargs)


class HabitatCommentsList(HabitatMixin, CommentsList):

    def get_home_url(self, **kwargs):
        return url_for('.habitat-comments', **kwargs)


comments.add_url_rule(
    '/species/comments/<period>/<subject>/<region>/<user>/',
    view_func=SpeciesCommentsList.as_view('species-comments')
)
comments.add_url_rule(
    '/habitat/comments/<period>/<subject>/<region>/<user>/',
    view_func=HabitatCommentsList.as_view('habitat-comments')
)


class UserSummary(views.View):

    template = 'history/history.html'

    def dispatch_request(self):
        if not current_user.is_authenticated():
            raise PermissionDenied
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
            .order_by(self.model_manual_cls.last_update.desc()).limit(100)
        )
        comments_list = (
            self.model_comment_cls.query
            .join(self.model_comment_cls.record)
            .filter(self.model_manual_cls.dataset_id == period)
            .order_by(self.model_comment_cls.post_date.desc()).all()
        )
        return {'conclusions': conclusions, 'comments': comments_list}


class SpeciesUserSummary(SpeciesMixin, UserSummary):
    pass


class HabitatUserSummary(HabitatMixin, UserSummary):
    pass


comments.add_url_rule('/history/species/',
                      view_func=SpeciesUserSummary.as_view('species-history'))
comments.add_url_rule('/history/habitat/',
                      view_func=HabitatUserSummary.as_view('habitat-history'))


class _CommentCounterBase(object):

    def __init__(self, dataset_id, user_id):
        self.dataset_id = dataset_id
        self.user_id = user_id

    def _get_comments_query(self):
        return (
            db.session.query(
                self.subject_column,
                self.comment_cls.region,
                func.count('*'),
            )
            .filter(self.comment_cls.dataset_id == self.dataset_id)
            .filter(or_(
                self.comment_cls.deleted == 0,
                self.comment_cls.deleted == None,
            ))
            .filter(WikiComment.author_id != self.user_id)
            .group_by(
                self.subject_column,
                self.comment_cls.region,
            )
        )

    def _get_comments_for_me_query(self):
        return (
            self._get_comments_query()
            .join(self.comment_cls.record)
            .filter_by(user_id=self.user_id)
        )

    def _get_wiki_comments_query(self):
        return (
            db.session.query(
                self.wiki_subject_column,
                Wiki.region_code,
                func.count(WikiComment.id),
            )
            .join(WikiComment.wiki)
            .filter(Wiki.dataset_id == self.dataset_id)
            .filter(or_(
                WikiComment.deleted == 0,
                WikiComment.deleted == None,
            ))
            .filter(WikiComment.author_id != self.user_id)
            .filter(self.wiki_subject_column != None)
            .group_by(
                self.wiki_subject_column,
                Wiki.region_code,
            )
        )

    def _count_unread(self, comments_query, read_table, reader_col):
        rv = {(row[0], row[1]): row[2] for row in comments_query}

        read_comments_query = (
            comments_query
            .join(read_table)
            .filter(getattr(read_table.c, reader_col) == self.user_id)
        )
        for row in read_comments_query:
            count = row[2]
            rv[row[0], row[1]] -= count

        return rv

    def get_counts(self):
        return {
            'user': self._count_unread(
                self._get_comments_for_me_query(),
                self.read_table, 'reader_user_id',
            ),
            'all': self._count_unread(
                self._get_comments_query(),
                self.read_table, 'reader_user_id',
            ),
            'wiki': self._count_unread(
                self._get_wiki_comments_query(),
                t_wiki_comments_read, 'reader_id',
            ),
        }

    def get_wiki_unread_count(self, subject, region):
        count_rv = self._count_unread(
            self._get_wiki_comments_query(),
            t_wiki_comments_read, 'reader_id',
        )
        return count_rv.get((subject, region), 0)


class SpeciesCommentCounter(_CommentCounterBase):

    comment_cls = Comment
    subject_column = property(lambda self: Comment.assesment_speciesname)
    read_table = t_comments_read
    wiki_subject_column = property(lambda self: Wiki.assesment_speciesname)


class HabitatCommentCounter(_CommentCounterBase):

    comment_cls = HabitatComment
    subject_column = property(lambda self: HabitatComment.habitat)
    read_table = t_habitat_comments_read
    wiki_subject_column = property(lambda self: Wiki.habitatcode)
