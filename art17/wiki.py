from flask import (
    Blueprint,
    views,
    render_template,
    request,
    flash,
    url_for,
    abort,
    redirect)
from flask_principal import PermissionDenied
from datetime import datetime
from sqlalchemy import or_

from art17.common import admin_perm, etc_perm, sta_cannot_change
from art17.models import (
    Wiki,
    WikiChange,
    WikiComment,
    WikiTrail,
    WikiTrailChange,
    RegisteredUser,
    Dataset,
    db,
)
from art17.forms import WikiEditForm, CommentForm, RevisedForm
from art17.auth import current_user
from instance.settings import EU_ASSESSMENT_MODE


wiki = Blueprint('wiki', __name__)

DATE_FORMAT_CMNT = '%B %d, %Y'
TIME_FORMAT_CMNT = '%H:%M:%S'


def format_datetime(value, format):
    if not value:
        return ''
    date = datetime.strftime(value, format)
    return date


@wiki.app_template_filter('format_date_cmnt')
def format_date_cmnt(value):
    return format_datetime(value, DATE_FORMAT_CMNT)


@wiki.app_template_filter('format_time_cmnt')
def format_time_cmnt(value):
    return format_datetime(value, TIME_FORMAT_CMNT)


@wiki.app_template_filter('hide_adm_etc_username')
def hide_adm_etc_username(name):
    name = name or ''
    author = (
        RegisteredUser.query
        .filter(or_(
            RegisteredUser.name == name,
            RegisteredUser.id == name,
        ))
        .first()
    )
    if not (current_user.has_role('etc') or current_user.has_role('admin')):
        if author:
            if author.has_role('etc'):
                name = 'EEA-ETC/BD'
            elif author.has_role('admin'):
                name = 'Admin'
    if author:
        if  author.has_role('stakeholder') or author.has_role('nat'):
            if not current_user.has_role('admin'):
                name = author.institution
    return name

@wiki.app_template_global('is_name_changed')
def is_name_changed(name):
    is_changed = False
    author = (
        RegisteredUser.query
        .filter(or_(
            RegisteredUser.name == name,
            RegisteredUser.id == name,
        ))
        .first()
    )
    if not (current_user.has_role('etc') or current_user.has_role('admin')):
        if author:
            if author.has_role('etc'):
                is_changed = True
            elif author.has_role('admin'):
                is_changed = True
    if author:
        if  author.has_role('stakeholder') or author.has_role('nat'):
            if not current_user.has_role('admin'):
                is_changed = True
    return is_changed

@wiki.app_template_global('is_read')
def is_read(comment):
    return current_user in comment.readers


@wiki.app_template_global('get_css_class')
def get_css_class(comment):
    if comment.deleted:
        return 'cmnt-deleted'
    elif comment.author == current_user:
        return 'cmnt-owned'
    elif current_user in comment.readers:
        return 'cmnt-read'
    else:
        return 'cmnt-notread'


@wiki.app_template_global('can_edit_page')
def can_edit_page(dataset):
    if not dataset or dataset.is_readonly:
        return False
    return admin_perm.can() or etc_perm.can() or EU_ASSESSMENT_MODE


@wiki.app_template_global('can_manage_revisions')
def can_manage_revisions():
    return admin_perm.can() or etc_perm.can() or EU_ASSESSMENT_MODE


@wiki.app_template_global('can_change_revision')
def can_change_revision(revision):
    if not revision.dataset or revision.dataset.is_readonly or revision.active:
        return False
    return admin_perm.can() or etc_perm.can()


@wiki.app_template_global('can_add_comment')
def can_add_comment(comments, revisions, dataset):
    if not dataset or dataset.is_readonly or sta_cannot_change():
        return False
    is_author = current_user in [cmnt.author for cmnt in comments]
    return not (current_user.is_anonymous or is_author) and revisions


@wiki.app_template_global('can_edit_comment')
def can_edit_comment(comment):
    if current_user == comment.author and not comment.deleted and \
            not sta_cannot_change():
        return True
    return False


@wiki.app_template_global('can_manage_comment')
def can_manage_comment(dataset):
    if not dataset or dataset.is_readonly:
        return False
    return not current_user.is_anonymous


class CommonSection(object):

    def set_attrs(self, page):
        self.page = page
        if self.page == 'species':
            self.subject_field = 'assesment_speciesname'
        elif self.page == 'habitat':
            self.subject_field = 'habitatcode'

    def get_req_args(self):
        return {arg: request.args.get(arg, '') for arg in
                ['subject', 'region', 'period']}

    def get_wiki(self):
        r = self.get_req_args()

        return (self.wiki_cls.query
                .filter(
                    getattr(self.wiki_cls, self.subject_field) == r['subject'],
                    self.wiki_cls.region_code == r['region'],
                    self.wiki_cls.dataset_id == r['period'])
                .first())

    def get_wiki_changes(self):
        return self.wiki_change_cls.query.filter_by(wiki=self.get_wiki())

    def get_active_change(self):
        return self.get_wiki_changes().filter_by(active=1).first()

    def get_context(self):
        active_change = self.get_active_change()

        revisions = (
            self.get_wiki_changes()
            .order_by(self.wiki_change_cls.changed.desc())
            .all()
        )

        request_args = self.get_req_args()
        period = request_args.get('period')
        dataset = Dataset.query.get(period) if period else None

        return {
            'wiki_body': [('', '', active_change.body)]
            if active_change else [],
            'wiki_revised': getattr(active_change,'revised', None),
            'wiki_revised_form': RevisedForm(),
            'revisions': revisions,
            'page': self.page,
            'dataset': dataset,
            'home_url': url_for(self.home_endpoint,
                                page=self.page,
                                **request_args),
            'page_history_url': url_for(self.pagehist_endpoint,
                                        page=self.page,
                                        **request_args),
            'edit_page_url': url_for(self.editpage_endpoint,
                                     page=self.page,
                                     **request_args),
            'get_rvs_endpoint': self.getrevision_endpoint,
            'page_title': self.page_title
        }

    def insert_inexistent_wiki(self):
        if not self.get_wiki():
            wiki_attrs = {
                'region_code': request.args.get('region', ''),
                self.subject_field: request.args.get('subject'),
                'dataset_id': request.args.get('period')
            }
            if self.wiki_cls == WikiTrail and wiki_attrs['region_code'] == '':
                raise PermissionDenied
            new_wiki = self.wiki_cls(**wiki_attrs)
            db.session.add(new_wiki)
            db.session.commit()
            return True

        return False


class DataSheetSection(CommonSection):
    wiki_cls = Wiki
    wiki_change_cls = WikiChange
    wiki_comment_cls = WikiComment
    page_title = 'Data Sheet Info'
    home_endpoint = '.datasheet'
    pagehist_endpoint = '.ds-page-history'
    addcmnt_endpoint = '.ds-add-comment'
    editpage_endpoint = '.ds-edit-page'
    editcmnt_endpoint = '.ds-edit-comment'
    getrevision_endpoint = '.ds-get-revision'

    def get_context(self):
        context = super(DataSheetSection, self).get_context()

        wiki = self.get_wiki()
        comments = [c for c in wiki.comments if not
                    (c.deleted and c.author != current_user)] if wiki else []
        request_args = self.get_req_args()
        context.update({
            'comments': comments,
            'add_comment_url': url_for(
                self.addcmnt_endpoint,
                page=self.page,
                **request_args)
        })
        return context


class AuditTrailSection(CommonSection):
    wiki_cls = WikiTrail
    wiki_change_cls = WikiTrailChange
    page_title = 'Audit Trail'
    home_endpoint = '.audittrail'
    pagehist_endpoint = '.at-page-history'
    editpage_endpoint = '.at-edit-page'
    getrevision_endpoint = '.at-get-revision'

    def get_context(self):
        context = super(AuditTrailSection, self).get_context()

        if request.args.get('merged') == 'merged':
            request_args = self.get_req_args()
            request_args['region'] = ''
            context.update({
                'back_url': url_for(
                    '.audittrail-merged',
                    page=self.page,
                    **request_args)
            })
        return context


class WikiView(views.View):
    methods = ['GET', 'POST']
    wiki_form_cls = WikiEditForm
    cmnt_form_cls = CommentForm
    template_name = 'wiki/wiki.html'

    def __init__(self, section):
        self.section = section()

    def process_post_request(self):
        form = RevisedForm(request.form)
        if not form.validate():
            flash("Something went wrong.")
            return False
        wiki_change = self.section.get_wiki_changes().filter_by(
            active=True).first()
        wiki_change.revised = form.revised.data
        wiki_change.editor = current_user.id
        db.session.commit()

        flash("Data sheet revised!")

        return True

    def get_context(self):
        return {}

    def dispatch_request(self, page):
        self.section.set_attrs(page)

        context = self.section.get_context()
        context.update(self.get_context())

        if request.method == 'POST':
            if self.process_post_request():
                return redirect(context['home_url'])

        return render_template(self.template_name, **context)


class MergedRegionsView(views.View):
    methods = ['GET']
    template_name = 'wiki/wiki.html'

    def __init__(self, section):
        self.section = section()

    def dispatch_request(self, page):
        self.section.set_attrs(page)
        rq = self.section.get_req_args()

        wikis = (
            self.section.wiki_cls.query
            .filter(getattr(self.section.wiki_cls, self.section.subject_field)
                    == rq['subject'],
                    self.section.wiki_cls.dataset_id == rq['period']).all())
        wiki_body = []

        for wiki in wikis:
            change = (
                self.section.wiki_change_cls.query
                .filter_by(
                    wiki=wiki,
                    active=1,
                ).first()
            )
            if change:
                region_change_url = url_for(
                    self.section.home_endpoint,
                    page=self.section.page,
                    region=wiki.region.reg_code,
                    subject=rq['subject'],
                    period=rq['period'])
                wiki_body.append(
                    (wiki.region.reg_name, region_change_url, change.body))

        return render_template(self.template_name,
                               page_title=self.section.page_title,
                               wiki_body=wiki_body,
                               merged=True)


class PageHistory(WikiView):

    def process_post_request(self):
        wiki_changes = self.section.get_wiki_changes()
        active_change = self.section.get_active_change()

        new_change_id = request.form.get('revision_id')
        new_active_change = (
            wiki_changes
            .filter_by(id=new_change_id)
            .first_or_404()
        )

        if not can_change_revision(new_active_change):
            raise PermissionDenied

        if active_change:
            active_change.active = 0
        new_active_change.active = 1

        db.session.commit()

        flash("Active revision changed.")
        return True


class AddComment(WikiView):

    def process_post_request(self):
        wiki = self.section.get_wiki()
        wiki_changes = self.section.get_wiki_changes().all()
        comments = wiki.comments if wiki else []

        dataset = Dataset.query.get(request.args.get('period'))

        if not can_add_comment(comments, wiki_changes, dataset):
            raise PermissionDenied

        form = CommentForm(request.form)
        if not form.validate():
            flash("Please enter a valid comment.")
            return False

        comment = self.section.wiki_comment_cls(
            wiki_id=wiki.id,
            comment=form.comment.data,
            author_id=current_user.id,
            posted=datetime.now(),
            dataset_id=dataset.id,
        )
        db.session.add(comment)
        db.session.commit()

        flash("Comment successfully added.")
        return True

    def get_context(self):
        return {'add_cmnt_form': self.cmnt_form_cls()}


class EditPage(WikiView):

    def process_post_request(self):
        dataset = Dataset.query.get(request.args.get('period'))

        if not can_edit_page(dataset):
            raise PermissionDenied

        form = WikiEditForm(request.form)
        if not form.validate():
            flash("Please enter a non-empty text.")
            return False

        active_change = self.section.get_active_change()
        if active_change:
            if active_change.body == form.text.data:
                flash('No changes were made.')
                return False
            active_change.active = 0
        else:
            self.section.insert_inexistent_wiki()

        wiki = self.section.get_wiki()
        new_change = self.section.wiki_change_cls(
            wiki_id=wiki.id,
            body=form.text.data,
            editor=current_user.id,
            changed=datetime.now(),
            active=1,
            dataset_id=dataset.id,
        )
        db.session.add(new_change)
        db.session.commit()

        flash("Saved changes.")
        return True

    def get_context(self):
        wiki_edit_page_form = self.wiki_form_cls()
        wiki = self.section.get_active_change()
        wiki_edit_page_form.text.process_data(wiki.body if wiki else '')

        return {'edit_page_form': wiki_edit_page_form}


class EditComment(WikiView):

    def process_post_request(self):
        comment_id = request.args.get('comment_id')
        comment = (
            self.section.wiki_comment_cls.query
            .filter_by(id=comment_id)
            .first_or_404()
        )

        if not can_edit_comment(comment):
            raise PermissionDenied

        form = CommentForm(request.form)
        if not form.validate():
            flash("Please enter a valid comment.")
            return False

        comment.comment = form.comment.data
        comment.readers = []
        db.session.commit()

        flash("Comment successfully modified.")

        return True

    def get_context(self):
        comment_id = request.args.get('comment_id')
        comment = (
            self.section.wiki_comment_cls.query
            .filter_by(id=comment_id)
            .first_or_404()
        )

        wiki_edit_cmnt_form = self.cmnt_form_cls()
        wiki_edit_cmnt_form.comment.process_data(comment.comment)

        return {'edit_comment_form': wiki_edit_cmnt_form}


class ManageComment(WikiView):
    methods = ['GET']

    def dispatch_request(self, page):
        dataset = Dataset.query.get(request.args.get('period'))

        if not can_manage_comment(dataset):
            raise PermissionDenied

        comment_id = request.args.get('comment_id')
        comment = (
            self.section.wiki_comment_cls.query
            .filter_by(id=comment_id)
            .first_or_404()
        )

        toggle = request.args.get('toggle')
        if toggle == 'del':
            if comment.author != current_user or sta_cannot_change():
                raise PermissionDenied
            if comment.deleted is None:
                comment.deleted = 0
            comment.deleted = 1 - comment.deleted
            db.session.commit()

        elif toggle == 'read':
            if comment.author == current_user:
                raise PermissionDenied
            if is_read(comment):
                comment.readers.remove(current_user)
            else:
                comment.readers.append(current_user)
            db.session.commit()
        else:
            abort(404)

        return ''


class GetRevision(WikiView):
    methods = ['GET']

    def dispatch_request(self, page):
        if not can_manage_revisions():
            raise PermissionDenied

        revision_id = request.args.get('revision_id')
        revision = (
            self.section.wiki_change_cls.query
            .filter_by(id=revision_id)
            .first_or_404()
        )

        return revision.body


wiki.add_url_rule('/<page>/summary/datasheet/',
                  view_func=WikiView
                  .as_view('datasheet', section=DataSheetSection))

wiki.add_url_rule('/<page>/summary/datasheet/page_history/',
                  view_func=PageHistory
                  .as_view('ds-page-history', section=DataSheetSection))

wiki.add_url_rule('/<page>/summary/datasheet/add_comment/',
                  view_func=AddComment
                  .as_view('ds-add-comment', section=DataSheetSection))

wiki.add_url_rule('/<page>/summary/datasheet/edit_page/',
                  view_func=EditPage
                  .as_view('ds-edit-page', section=DataSheetSection))

wiki.add_url_rule('/<page>/summary/datasheet/edit_comment/',
                  view_func=EditComment
                  .as_view('ds-edit-comment', section=DataSheetSection))

wiki.add_url_rule('/<page>/summary/datasheet/manage_comment/',
                  view_func=ManageComment
                  .as_view('ds-manage-comment', section=DataSheetSection))

wiki.add_url_rule('/<page>/summary/datasheet/get_revision/',
                  view_func=GetRevision
                  .as_view('ds-get-revision', section=DataSheetSection))

wiki.add_url_rule('/<page>/summary/audittrail/',
                  view_func=WikiView
                  .as_view('audittrail', section=AuditTrailSection))

wiki.add_url_rule('/<page>/summary/audittrail-merged/',
                  view_func=MergedRegionsView
                  .as_view('audittrail-merged', section=AuditTrailSection))

wiki.add_url_rule('/<page>/summary/audittrail/page_history/',
                  view_func=PageHistory
                  .as_view('at-page-history', section=AuditTrailSection))

wiki.add_url_rule('/<page>/summary/audittrail/edit_page/',
                  view_func=EditPage
                  .as_view('at-edit-page', section=AuditTrailSection))

wiki.add_url_rule('/<page>/summary/audittrail/get_revision/',
                  view_func=GetRevision
                  .as_view('at-get-revision', section=AuditTrailSection))
