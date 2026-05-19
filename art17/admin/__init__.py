from flask import abort
from flask_admin import Admin, AdminIndexView, expose
from art17.common import admin_perm
from art17.admin.base import FileUploadView
from art17.admin.config import ConfigModelView
from art17.admin.dataset import DatasetModelView
from art17.admin.etc_data_region import (
    EtcDataSpeciesRegionModelView, 
    EtcDataHabitattypeRegionModelView,
)
from art17.admin.etc_data import (
    EtcDataHcoveragePressureModelView,
    EtcDataHcoverageThreatModelView,
    EtcDataSpopulationPressureModelView,
    EtcDataSpopulationThreatModelView,
)
from art17.admin.etc_dic import (
    DicCountryCodeModelView,
    EtcDicBiogeoregModelView,
    EtcDicConclusionModelView,
    EtcDicDecisionModelView,
    EtcDicHdHabitatModelView,
    EtcDicMethodModelView,
    EtcDicPopulationUnitModelView,
    EtcDicSpeciesTypeModelView,
    EtcDicTrendModelView,
    EtcQaErrorsHabitattypeManualCheckedModelView,
    EtcQaErrorsSpeciesManualCheckedModelView,
)
from art17.admin.etc_data_automatic_assessment import (
    EtcDataSpeciesAutomaticAssessmentModelView,
    EtcDataHabitattypeAutomaticAssessmentModelView,
)
from art17.admin.manual_assessment import (
    SpeciesManualAssessmentModelView,
    HabitattypesManualAssessmentModelView,
)
from art17.admin.wiki_trail import (
    WikiTrailModelView,
    WikiTrailChangeModelView,
    WikiTrailChangeCombinedWithWikiModelView,
    WikiTrailCommentModelView,
)
from art17.models import (
    Comment,
    Config,
    Dataset,
    DicCountryCode,
    EtcDataSpeciesRegion,
    EtcDataHabitattypeRegion,
    EtcDataSpeciesAutomaticAssessment,
    EtcDataHabitattypeAutomaticAssessment,
    SpeciesManualAssessment,
    HabitattypesManualAssessment,
    EtcDataHcoveragePressure,
    EtcDataHcoverageThreat,
    EtcDataSpopulationPressure,
    EtcDataSpopulationThreat,
    EtcDicBiogeoreg,
    EtcDicConclusion,
    EtcDicDecision,
    EtcDicHdHabitat,
    EtcDicMethod,
    EtcDicPopulationUnit,
    EtcDicSpeciesType,
    EtcDicTrend,
    EtcQaErrorsHabitattypeManualChecked,
    EtcQaErrorsSpeciesManualChecked,
    HabitatComment,
    WikiTrail,
    WikiTrailChange,
    WikiTrailComment,
    db,
)

from art17.admin.manual_assessments_comments import (
    CommentModelView,
    HabitatCommentModelView,
)


class CustomAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not admin_perm.can():
            return abort(404)
        return super(CustomAdminIndexView, self).index()


def admin_register(app):
    admin = Admin(
        app,
        name="Article 17",
        template_mode="bootstrap3",
        index_view=CustomAdminIndexView(),
    )
    admin.add_view(WikiTrailModelView(WikiTrail, db.session, category="AuditTrail"))
    admin.add_view(
        WikiTrailChangeModelView(
            WikiTrailChange,
            db.session,
            category="AuditTrail",
            name="WikiTrailChange (standalone)",
            endpoint="wikitrailchange",
        )
    )
    admin.add_view(
        WikiTrailChangeCombinedWithWikiModelView(
            WikiTrailChange,
            db.session,
            category="AuditTrail",
            name="WikiTrailChange (with Wiki)",
            endpoint="wikitrailchange_combined",
        )
    )
    admin.add_view(
        WikiTrailCommentModelView(WikiTrailComment, db.session, category="AuditTrail")
    )
    admin.add_view(DatasetModelView(Dataset, db.session))
    admin.add_view(DicCountryCodeModelView(DicCountryCode, db.session))
    admin.add_view(
        EtcDataSpeciesRegionModelView(
            EtcDataSpeciesRegion, db.session, category="RegionsData"
        )
    )
    admin.add_view(
        EtcDataHabitattypeRegionModelView(
            EtcDataHabitattypeRegion, db.session, category="RegionsData"
        )
    )
    admin.add_view(
        EtcDataSpeciesAutomaticAssessmentModelView(
            EtcDataSpeciesAutomaticAssessment, db.session, category="AutomaticData"
        )
    )
    admin.add_view(
        EtcDataHabitattypeAutomaticAssessmentModelView(
            EtcDataHabitattypeAutomaticAssessment, db.session, category="AutomaticData"
        )
    )
    admin.add_view(
        SpeciesManualAssessmentModelView(
            SpeciesManualAssessment, db.session, category="ManualData"
        )
    )
    admin.add_view(
        HabitattypesManualAssessmentModelView(
            HabitattypesManualAssessment, db.session, category="ManualData"
        )
    )

    admin.add_view(
        EtcDataHcoveragePressureModelView(
            EtcDataHcoveragePressure, db.session, category="EtcData"
        )
    )
    admin.add_view(
        EtcDataHcoverageThreatModelView(
            EtcDataHcoverageThreat, db.session, category="EtcData"
        )
    )
    admin.add_view(
        EtcDataSpopulationPressureModelView(
            EtcDataSpopulationPressure, db.session, category="EtcData"
        )
    )
    admin.add_view(
        EtcDataSpopulationThreatModelView(
            EtcDataSpopulationThreat, db.session, category="EtcData"
        )
    )
    admin.add_view(
        EtcDicBiogeoregModelView(EtcDicBiogeoreg, db.session, category="EtcDic")
    )
    admin.add_view(
        EtcDicConclusionModelView(EtcDicConclusion, db.session, category="EtcDic")
    )
    admin.add_view(
        EtcDicDecisionModelView(EtcDicDecision, db.session, category="EtcDic")
    )
    admin.add_view(
        EtcDicHdHabitatModelView(EtcDicHdHabitat, db.session, category="EtcDic")
    )
    admin.add_view(EtcDicMethodModelView(EtcDicMethod, db.session, category="EtcDic"))
    admin.add_view(
        EtcDicPopulationUnitModelView(
            EtcDicPopulationUnit, db.session, category="EtcDic"
        )
    )
    admin.add_view(
        EtcDicSpeciesTypeModelView(EtcDicSpeciesType, db.session, category="EtcDic")
    )
    admin.add_view(EtcDicTrendModelView(EtcDicTrend, db.session, category="EtcDic"))
    admin.add_view(
        EtcQaErrorsHabitattypeManualCheckedModelView(
            EtcQaErrorsHabitattypeManualChecked, db.session, category="EtcQA"
        )
    )
    admin.add_view(
        EtcQaErrorsSpeciesManualCheckedModelView(
            EtcQaErrorsSpeciesManualChecked, db.session, category="EtcQA"
        )
    )
    admin.add_view(ConfigModelView(Config, db.session))
    # register non-model upload view
    admin.add_view(
        FileUploadView(name="Upload File", endpoint="file_upload", category="Utilities")
    )
    admin.add_view(CommentModelView(Comment, db.session, category="ManualData"))
    admin.add_view(HabitatCommentModelView(HabitatComment, db.session, category="ManualData"))
