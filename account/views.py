from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from djoser.permissions import CurrentUserOrAdmin

from .permissions import (
    IsEmployer,
    IsProfessional,
    IsNPO,
    IsCollege,
    IsEmploymentAgency,
)
from .models import (
    User,
    Employer,
    Professional,
    NPO,
    College,
    EmploymentAgency,
    Upload,
    Callback
)
from .serializers import (
    UserSerializer,
    EmployerSerialzier,
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
    CallbackSerializer,
)


class EmployerViewset(viewsets.GenericViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerialzier
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
            return EmployerSerialzier

    def retrieve(self, request, pk):
        try:
            employer = self.queryset.objects.get(user_id=pk)
        except Employer.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)

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
        try:
            employer = self.queryset.objects.get(user_id=pk)
        except Employer.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)

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
            page = self.paginate_queryset(employers)
        except Employer.DoesNotExist:
            return Response("Работодатели не найдены", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        url_path="detail",
        url_name="detail",
        serializer_class=EmployerDetailSerializer,
    )
    def qdetail(self, request, pk=None):
        try:
            employer = self.queryset.objects.get(user_id=pk)
        except Employer.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(employer)
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

    def retrieve(self, request, pk):
        try:
            professional = self.queryset.objects.get(user_id=pk)
        except Employer.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)

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
        try:
            professional = self.queryset.objects.get(user_id=pk)
        except Professional.DoesNotExist:
            return Response(f"Профессионал {pk} не найден", status=status.HTTP_404_NOT_FOUND)

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
        try:
            professional = self.queryset.objects.get(user_id=pk)
        except Professional.DoesNotExist:
            return Response(f"Профессионал {pk} не найден", status=status.HTTP_404_NOT_FOUND)

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

    def retrieve(self, request, pk):
        try:
            npo = self.queryset.objects.get(user_id=pk)
        except NPO.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)

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
        try:
            npo = self.queryset.objects.get(user_id=pk)
        except NPO.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)

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
            page = self.paginate_queryset(npo)
        except NPO.DoesNotExist:
            return Response("Работодатели не найдены", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        url_path="detail",
        url_name="detail",
        serializer_class=NPODetailSerializer,
    )
    def qdetail(self, request, pk=None):
        try:
            npo = self.queryset.objects.get(user_id=pk)
        except NPO.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)

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
        try:
            college = self.queryset.objects.get(user_id=pk)
        except College.DoesNotExist:
            return Response(f"Колледж {pk} не найден", status=status.HTTP_404_NOT_FOUND)

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
        try:
            employment_agency = self.queryset.objects.get(user_id=pk)
        except EmploymentAgency.DoesNotExist:
            return Response(f"Орган занятости {pk} не найден", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer_class()
        serializer = serializer(employment_agency, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(employment_agency, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
