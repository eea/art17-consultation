from flask import (
    Blueprint,
    views,
    render_template,
    request,
    flash,
    url_for,
    abort)
from datetime import datetime

from models import Wiki, WikiChange, WikiComment, db
from forms import DataSheetInfoForm
from auth import current_user


wiki = Blueprint('wiki', __name__)

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


@wiki.app_template_filter('format_date_ph')
def format_date_ph(value):
    if not value:
        return ''
    date = datetime.strftime(value, DATE_FORMAT)
    return date


class WikiView(views.View):
    methods = ['GET', 'POST']

    def dispatch_request(self, page):
        self.page = page

        if request.method == 'POST':
            self.process_post_request()

        context = self.get_context()

        context.update({'user_logged_in': not current_user.is_anonymous()})
        return render_template(self.template_name, **context)


class DataSheetInfo(WikiView):
    template_name = 'wiki/datasheetinfo.html'
    wiki_form_cls = DataSheetInfoForm

    def get_wiki_changes(self):
        period = request.args.get('period')
        subject = request.args.get('subject')
        region = request.args.get('region')

        if self.page == 'species':
            column = 'assesment_speciesname'
        elif self.page == 'habitat':
            column = 'habitatcode'
        else:
            abort(404)

        wiki = Wiki.query.filter(getattr(Wiki, column) == subject,
                                 Wiki.region == region,
                                 Wiki.dataset_id == period).first()

        wiki_changes = WikiChange.query.filter_by(wiki=wiki)

        return wiki_changes

    def get_active_change(self):
        return self.get_wiki_changes().filter_by(active=1).first()

    def get_context(self):
        active_change = self.get_active_change()

        request_args = {arg: request.args.get(arg) for arg in
                        ['subject', 'region', 'period']}

        return {'wiki_body': active_change.body if active_change else None,
                'page_history_url': url_for('.data-sheet-info-page-history',
                                            page=self.page,
                                            **request_args),
                'add_comment_url': url_for('.data-sheet-info-add-comment',
                                           page=self.page,
                                           **request_args),
                'edit_page_url': url_for('.data-sheet-info-edit-page',
                                         page=self.page,
                                         **request_args)
                }


class DataSheetInfoPageHistory(DataSheetInfo):

    def process_post_request(self):
        wiki_changes = self.get_wiki_changes()
        active_change = self.get_active_change()

        new_change_id = request.form.get('hist_page')
        new_active_change = wiki_changes.filter(
            WikiChange.id == new_change_id).first()

        active_change.active = 0
        new_active_change.active = 1

        db.session.commit()

        flash("Active data sheet changed.")

    def get_context(self):
        context = super(DataSheetInfoPageHistory, self).get_context()
        wiki_changes = self.get_wiki_changes()

        all_changes = wiki_changes.order_by(WikiChange.changed.desc()).all()
        page_history = [{'changed': c.changed,
                         'editor': c.editor,
                         'active': c.active,
                         'id': c.id}
                        for c in all_changes]

        context.update({'page_history': page_history})

        return context


class DataSheetInfoAddComment(DataSheetInfo):

    def process_post_request(self):
        active_change = self.get_active_change()

        comment_attrs = {'wiki_id': active_change.wiki_id,
                         'comment': request.form.get('text'),
                         'author': current_user.name,
                         'posted': datetime.now()}

        comment = WikiComment(**comment_attrs)

        db.session.add(comment)
        db.session.commit()

        flash("Comment successfully added.")

    def get_context(self):
        context = super(DataSheetInfoAddComment, self).get_context()

        context.update({'add_comm_form': self.wiki_form_cls()})

        return context


class DataSheetInfoEditPage(DataSheetInfo):

    def process_post_request(self):
        active_change = self.get_active_change()
        active_change.active = 0

        new_change_attrs = {'wiki_id': active_change.wiki_id,
                            'body': request.form.get('text'),
                            'editor': current_user.name,
                            'changed': datetime.now(),
                            'active': 1}

        new_change = WikiChange(**new_change_attrs)

        db.session.add(new_change)
        db.session.commit()

        flash("New data sheet saved.")

    def get_context(self):
        context = super(DataSheetInfoEditPage, self).get_context()

        wiki_edit_page_form = self.wiki_form_cls()
        wiki_edit_page_form.text.data = context['wiki_body']

        context.update({'edit_page_form': wiki_edit_page_form})

        return context


wiki.add_url_rule('/<page>/summary/wiki/',
                  view_func=DataSheetInfo.as_view('data-sheet-info'))

wiki.add_url_rule('/<page>/summary/wiki/page_history',
                  view_func=DataSheetInfoPageHistory
                  .as_view('data-sheet-info-page-history'))

wiki.add_url_rule('/<page>/summary/wiki/add_comment',
                  view_func=DataSheetInfoAddComment
                  .as_view('data-sheet-info-add-comment'))

wiki.add_url_rule('/<page>/summary/wiki/edit_page',
                  view_func=DataSheetInfoEditPage
                  .as_view('data-sheet-info-edit-page'))
