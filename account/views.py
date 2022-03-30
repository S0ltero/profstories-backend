from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from djoser.permissions import CurrentUserOrAdmin
from djoser.signals import user_registered

from helper.serializers import StudentMissionSerializer, StudentMissionCreateSerializer
from helper.models import StudentMission, SkillScope, StudentEvent
from events.serializers import EventSerialzier
from events.models import Event

from .permissions import (
    IsEmployer,
    IsProfessional,
    IsNPO,
    IsCollege,
    IsEmploymentAgency,
    IsStudent,
)
from .models import (
    User,
    Employer,
    Professional,
    NPO,
    College,
    EmploymentAgency,
    Teacher,
    Student,
    StudentEmployer,
    StudentProfessional,
    Upload,
    Callback
)
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    EmployerSerializer,
    EmployerCreateSerializer,
    EmployerDetailSerializer,
    ProfessionalSerialzier,
    ProfessionalCreateSerializer,
    ProfessionalDetailSerializer,
    NPOSerializer,
    NPOCreateSerializer,
    NPODetailSerializer,
    CollegeSerializer,
    CollegeCreateSerializer,
    CollegeDetailSerializer,
    EmploymentAgencySerializer,
    TeacherSerializer,
    StudentSerializer,
    StudentEmployerSerializer,
    CallbackSerializer,
)


class EmployerViewset(viewsets.GenericViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Employer.objects.filter(user__verification=User.Verifiaction.VERIFIED)

        if "video" in self.request.query_params.keys():
            queryset = queryset.filter(company_video__isnull=False)

        if "training" in self.request.query_params.keys():
            queryset = queryset.filter(has_corporate_training=True)

        if "pwd" in self.request.query_params.keys():
            queryset = queryset.filter(has_pwd=True)

        if "adaptation" in self.request.query_params.keys():
            queryset = queryset.filter(has_adaptation=True)

        type = self.request.query_params.get("type")
        if type:
            queryset = queryset.filter(company_count_employees=type)

        wage = self.request.query_params.get("wage")
        if wage:
            queryset = queryset.filter(company_avg_wage__gte=wage)

        scope = self.request.query_params.get("scope")
        if scope:
            queryset = queryset.filter(company_scope=scope)

        region = self.request.query_params.get("region")
        if region:
            region = region.split(",")
            queryset = queryset.filter(company_region__contained_by=region)

        professions = self.request.query_params.get("professions")
        if professions:
            professions = professions.split(",")
            queryset = queryset.filter(company_professions__contained_by=professions)

        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return EmployerCreateSerializer
        else:
            return EmployerSerializer

    def get_object(self):
        queryset = self.queryset
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsEmployer]
        elif self.action == "update":
            self.permission_classes = [CurrentUserOrAdmin]
        return super().get_permissions()

    def retrieve(self, request, pk):
        employer = self.get_object()
        serializer = self.serializer_class(employer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(instance=request.user, data=data, partial=True)
        if not user_serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer.update(request.user, user_serializer.validated_data)
        serializer.save(user_id=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        employer = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(employer, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(employer, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            employers = self.get_queryset()
        except Employer.DoesNotExist:
            return Response("Работодатели не найдены", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(employers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_path="detail",
        url_name="detail",
        serializer_class=EmployerDetailSerializer,
    )
    def qdetail(self, request, pk=None):
        employer = self.get_object()
        serializer = self.serializer_class(employer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
    )
    def random(self, request):
        employers = self.queryset.filter(user__verification=User.Verifiaction.VERIFIED).order_by("?")[:3]
        serializer = self.serializer_class(employers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfessionalViewset(viewsets.GenericViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerialzier
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Professional.objects.filter(user__verification=User.Verifiaction.VERIFIED)

        scope = self.request.query_params.get("scope")
        if scope:
            scope = scope.split(",")
            queryset = queryset.filter(scope__contained_by=scope)

        region = self.request.query_params.get("region")
        if region:
            queryset = queryset.filter(region=region)

        timetable = self.request.query_params.get("timetable")
        if timetable:
            queryset = queryset.filter(timetable=timetable)

        employment = self.request.query_params.get("employment")
        if employment:
            queryset = queryset.filter(employment_type=employment)

        trips = self.request.query_params.get("trips")
        if trips:
            queryset = queryset.filter(business_trips=trips)

        if "pwd" in self.request.query_params.keys():
            queryset = queryset.filter(has_pwd=True)

        wage = self.request.query_params.get("wage")
        if wage:
            queryset = queryset.filter(wage=wage)

        skils = self.request.query_params.get("skils")
        if skils:
            skils = skils.split(",")
            queryset = queryset.filter(soft_skils__contained_by=skils)

        hobbies = self.request.query_params.get("hobbies")
        if hobbies:
            hobbies = hobbies.split(",")
            queryset = queryset.filter(profession_hobbies__contained_by=hobbies)

        school_subjects = self.request.query_params.get("school-subjects")
        if school_subjects:
            school_subjects = school_subjects.split(",")
            queryset = queryset.filter(favorite_school_subjects__contained_by=school_subjects)

        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return ProfessionalCreateSerializer
        else:
            return ProfessionalSerialzier

    def get_object(self):
        queryset = self.queryset
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsProfessional]
        elif self.action == "update":
            self.permission_classes = [CurrentUserOrAdmin]
        return super().get_permissions()

    def retrieve(self, request, pk):
        professional = self.get_object()
        serializer = self.serializer_class(professional)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(instance=request.user, data=data, partial=True)
        if not user_serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        bulk_inserts = []
        for file in request.FILES.getlist("workplace"):
            bulk_inserts.append(Upload(user_id=request.user.id, file=file, type="workplace"))

        user_serializer.update(request.user, user_serializer.validated_data)
        serializer.save(user_id=request.user.id)
        Upload.objects.bulk_create(bulk_inserts)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        professional = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(professional, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(professional, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            professionals = self.get_queryset()
        except Professional.DoesNotExist:
            return Response("Профессионалы не найдены", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(professionals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_path="detail",
        url_name="detail",
        serializer_class=ProfessionalDetailSerializer,
    )
    def qdetail(self, request, pk=None):
        professional = self.get_object()
        serializer = self.serializer_class(professional)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NPOViewset(viewsets.GenericViewSet):
    queryset = NPO.objects.all()
    serializer_class = NPOSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return NPOCreateSerializer
        else:
            return NPOSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsNPO]
        elif self.action == "update":
            self.permission_classes = [CurrentUserOrAdmin]
        return super().get_permissions()

    def retrieve(self, request, pk):
        npo = self.get_object()
        serializer = self.serializer_class(npo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(instance=request.user, data=data, partial=True)
        if not user_serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer.update(request.user, user_serializer.validated_data)
        serializer.save(user_id=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        npo = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(npo, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(npo, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            npo = self.queryset.all()
        except NPO.DoesNotExist:
            return Response("Работодатели не найдены", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(npo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_path="detail",
        url_name="detail",
        serializer_class=NPODetailSerializer,
    )
    def qdetail(self, request, pk=None):
        npo = self.get_object()
        serializer = self.serializer_class(npo)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeViewset(viewsets.GenericViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CollegeCreateSerializer
        else:
            return CollegeSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsCollege]
        elif self.action == "update":
            self.permission_classes = [CurrentUserOrAdmin]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(instance=request.user, data=data, partial=True)
        if not user_serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        bulk_inserts = []
        for file in request.FILES.getlist("images"):
            bulk_inserts.append(Upload(user_id=request.user.id, file=file, type="images"))

        user_serializer.update(request.user, user_serializer.validated_data)
        serializer.save(user_id=request.user.id)
        Upload.objects.bulk_create(bulk_inserts)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        college = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(college, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(college, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmploymentAgencyViewset(viewsets.GenericViewSet):
    queryset = EmploymentAgency.objects.all()
    serializer_class = EmploymentAgencySerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsEmploymentAgency]
        elif self.action == "update":
            self.permission_classes = [CurrentUserOrAdmin]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(instance=request.user, data=data, partial=True)
        if not user_serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer.update(request.user, user_serializer.validated_data)
        serializer.save(user_id=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        employment_agency = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(employment_agency, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(employment_agency, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherViewset(viewsets.GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        user_serializer = UserSerializer(data=data)
        if not user_serializer.is_valid(raise_exception=False):
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = user_serializer.save()
        data["user"] = user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            user_registered.send(
                sender=self.__class__, user=user, request=self.request
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentViewset(viewsets.GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        elif self.action == "update":
            self.permission_classes = [CurrentUserOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def retrieve(self, request, pk):
        student = self.get_object()
        serializer = self.serializer_class(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        user_serializer = CreateUserSerializer(data=data)
        if not user_serializer.is_valid(raise_exception=False):
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = user_serializer.save()
        data["user"] = user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        student = self.get_object()

        if request.data.get("employers"):
            employer_ids = request.data["employers"]
            employers_bulk = []
            for id in employer_ids:
                employers_bulk.append(
                    StudentEmployer(student_id=student.pk, employer_id=id)
                )
            StudentEmployer.objects.bulk_create(employers_bulk)

        if request.data.get("professionals"):
            professional_ids = request.data["professionals"]
            professionals_bulk = []
            for id in professional_ids:
                professionals_bulk.append(
                    StudentProfessional(student_id=student.pk, professional_id=id)
                )
            StudentProfessional.objects.bulk_create(professionals_bulk)

        serializer = self.serializer_class(student, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(student, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        url_path="missions",
        url_name="missions",
        serializer_class=StudentMissionSerializer
    )
    def missions(self, request, pk=None):
        student = self.get_object()
        serializer = self.serializer_class(student.missions.order_by("mission__order"), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get", "patch"],
        detail=True,
        url_path=r"missions/(?P<mission_id>[^/.]+)",
        url_name="mission-detail",
        serializer_class=StudentMissionCreateSerializer
    )
    def mission(self, request, pk=None, mission_id=None):
        student = self.get_object()
        try:
            mission = student.missions.get(pk=mission_id)
        except StudentMission.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = self.serializer_class(mission)
        elif request.method == "PATCH":
            serializer = self.serializer_class(mission, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=False):
                serializer.update(mission, serializer.validated_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_path="professionals",
        url_name="professionals",
        serializer_class=ProfessionalSerialzier
    )
    def professionals(self, request, pk=None):
        student = self.get_object()
        skill = student.skills.order_by("-points").first()
        scope = SkillScope.objects.get(object=skill.object).scope

        professionals = Professional.objects.filter(
            scope__contained_by=scope,
            whitelist=True
        )[:6]
        serializer = self.serializer_class(professionals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_path="employers",
        url_name="employers",
        serializer_class=StudentEmployerSerializer
    )
    def employers(self, request, pk=None):
        student = self.get_object()
        skill = student.skills.order_by("-points").first()
        scope = SkillScope.objects.get(object=skill.object).scope

        employers = Employer.objects.filter(
            company_region__contained_by=[student.region],
            company_scope__in=scope,
            whitelist=True
        )[:6]
        serializer = self.serializer_class(employers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get", "post"],
        detail=True,
        url_path="events",
        url_name="events",
        serializer_class=EventSerialzier,
        permission_classes=(CurrentUserOrAdmin,)
    )
    def events(self, request, pk=None):
        student = self.get_object()
        if request.method == "GET":
            events = Event.objects.filter(pk__in=student.events.values("event"))
            serializer = self.serializer_class(events, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "POST":
            event_id = request.data["event_id"]
            StudentEvent.objects.create(student=student, event_id=event_id)
            return Response(status=status.HTTP_201_CREATED)


class CallbackCreateView(CreateAPIView):
    queryset = Callback
    serializer_class = CallbackSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
