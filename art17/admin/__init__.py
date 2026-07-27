from flask import abort
from flask_admin import Admin, AdminIndexView, expose

from art17.admin.base import FileUploadView
from art17.admin.config import ConfigModelView
from art17.admin.dataset import DatasetModelView
from art17.admin.etc_data import (
    EtcDataHcoveragePressureModelView,
    EtcDataHcoverageThreatModelView,
    EtcDataSpopulationPressureModelView,
    EtcDataSpopulationThreatModelView,
)
from art17.admin.etc_data_automatic_assessment import (
    EtcDataHabitattypeAutomaticAssessmentModelView,
    EtcDataSpeciesAutomaticAssessmentModelView,
)
from art17.admin.etc_data_region import (
    EtcDataHabitattypeRegionModelView,
    EtcDataSpeciesRegionModelView,
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
from art17.admin.manual_assessment import (
    HabitattypesManualAssessmentModelView,
    SpeciesManualAssessmentModelView,
)
from art17.admin.manual_assessments_comments import (
    CommentModelView,
    HabitatCommentModelView,
)
from art17.admin.user import RegisteredUserModelView, RoleModelView
from art17.admin.wiki_trail import (
    WikiTrailChangeCombinedWithWikiModelView,
    WikiTrailChangeModelView,
    WikiTrailCommentModelView,
    WikiTrailModelView,
)
from art17.common import admin_perm
from art17.models import (
    Comment,
    Config,
    Dataset,
    DicCountryCode,
    EtcDataHabitattypeAutomaticAssessment,
    EtcDataHabitattypeRegion,
    EtcDataHcoveragePressure,
    EtcDataHcoverageThreat,
    EtcDataSpeciesAutomaticAssessment,
    EtcDataSpeciesRegion,
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
    HabitattypesManualAssessment,
    RegisteredUser,
    Role,
    SpeciesManualAssessment,
    WikiTrail,
    WikiTrailChange,
    WikiTrailComment,
    db,
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
        index_view=CustomAdminIndexView(),
    )
    admin.add_view(WikiTrailModelView(WikiTrail, db, category="AuditTrail"))
    admin.add_view(
        WikiTrailChangeModelView(
            WikiTrailChange,
            db,
            category="AuditTrail",
            name="WikiTrailChange (standalone)",
            endpoint="wikitrailchange",
        )
    )
    admin.add_view(
        WikiTrailChangeCombinedWithWikiModelView(
            WikiTrailChange,
            db,
            category="AuditTrail",
            name="WikiTrailChange (with Wiki)",
            endpoint="wikitrailchange_combined",
        )
    )
    admin.add_view(
        WikiTrailCommentModelView(WikiTrailComment, db, category="AuditTrail")
    )
    admin.add_view(DatasetModelView(Dataset, db))
    admin.add_view(DicCountryCodeModelView(DicCountryCode, db))
    admin.add_view(
        EtcDataSpeciesRegionModelView(EtcDataSpeciesRegion, db, category="RegionsData")
    )
    admin.add_view(
        EtcDataHabitattypeRegionModelView(
            EtcDataHabitattypeRegion, db, category="RegionsData"
        )
    )
    admin.add_view(
        EtcDataSpeciesAutomaticAssessmentModelView(
            EtcDataSpeciesAutomaticAssessment, db, category="AutomaticData"
        )
    )
    admin.add_view(
        EtcDataHabitattypeAutomaticAssessmentModelView(
            EtcDataHabitattypeAutomaticAssessment, db, category="AutomaticData"
        )
    )
    admin.add_view(
        SpeciesManualAssessmentModelView(
            SpeciesManualAssessment, db, category="ManualData"
        )
    )
    admin.add_view(
        HabitattypesManualAssessmentModelView(
            HabitattypesManualAssessment, db, category="ManualData"
        )
    )

    admin.add_view(
        EtcDataHcoveragePressureModelView(
            EtcDataHcoveragePressure, db, category="EtcData"
        )
    )
    admin.add_view(
        EtcDataHcoverageThreatModelView(EtcDataHcoverageThreat, db, category="EtcData")
    )
    admin.add_view(
        EtcDataSpopulationPressureModelView(
            EtcDataSpopulationPressure, db, category="EtcData"
        )
    )
    admin.add_view(
        EtcDataSpopulationThreatModelView(
            EtcDataSpopulationThreat, db, category="EtcData"
        )
    )
    admin.add_view(EtcDicBiogeoregModelView(EtcDicBiogeoreg, db, category="EtcDic"))
    admin.add_view(EtcDicConclusionModelView(EtcDicConclusion, db, category="EtcDic"))
    admin.add_view(EtcDicDecisionModelView(EtcDicDecision, db, category="EtcDic"))
    admin.add_view(EtcDicHdHabitatModelView(EtcDicHdHabitat, db, category="EtcDic"))
    admin.add_view(EtcDicMethodModelView(EtcDicMethod, db, category="EtcDic"))
    admin.add_view(
        EtcDicPopulationUnitModelView(EtcDicPopulationUnit, db, category="EtcDic")
    )
    admin.add_view(EtcDicSpeciesTypeModelView(EtcDicSpeciesType, db, category="EtcDic"))
    admin.add_view(EtcDicTrendModelView(EtcDicTrend, db, category="EtcDic"))
    admin.add_view(
        EtcQaErrorsHabitattypeManualCheckedModelView(
            EtcQaErrorsHabitattypeManualChecked, db, category="EtcQA"
        )
    )
    admin.add_view(
        EtcQaErrorsSpeciesManualCheckedModelView(
            EtcQaErrorsSpeciesManualChecked, db, category="EtcQA"
        )
    )
    admin.add_view(ConfigModelView(Config, db))
    # register non-model upload view
    admin.add_view(
        FileUploadView(name="Upload File", endpoint="file_upload", category="Utilities")
    )
    admin.add_view(CommentModelView(Comment, db, category="ManualData"))
    admin.add_view(HabitatCommentModelView(HabitatComment, db, category="ManualData"))
    admin.add_view(RegisteredUserModelView(RegisteredUser, db, category="Users"))
    admin.add_view(RoleModelView(Role, db, category="Users"))
