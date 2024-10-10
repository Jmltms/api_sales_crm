from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Account(models.Model):
    ACTIVE = 1
    SUSPENDED = 2
    DELETED = 3

    MALE = 1
    FEMALE = 2

    ADMIN = 1
    MANAGER = 2
    STAFF = 3
    EXTERNAL = 4
    GENMANAGER = 5

    STATUS = [
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
        (DELETED, 'Deleted'),
    ]

    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    TYPE = [
        (ADMIN, "admin"),
        (MANAGER, "manager"),
        (STAFF, "staff"),
        (EXTERNAL, "external"),
        (GENMANAGER, "general manager")
    ]

    user = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True
    )
    type = models.IntegerField(
        choices=TYPE,
        null=True,
        blank=True
    )
    employee_id = models.IntegerField(
        null=True,
        blank=True
    )
    gender = models.IntegerField(
        choices=GENDER,
        null=True,
        blank=True
    )
    date_hired = models.DateField(
        null=True,
        blank=True
    )
    address = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    job_title = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    phone_num = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.employee_id)


class Industry(models.Model):
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    field = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class CompanyInformation(models.Model):
    industry = models.ForeignKey(
        'Industry',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    address = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    company_size = models.IntegerField(
        null=True,
        blank=True
    )

    # def __str__(self):
    #     return self.name


class Client(models.Model):
    company = models.ForeignKey(
        'CompanyInformation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    phone_num = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    tel_num = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True
    )
    job_title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    department = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class LeadInformation(models.Model):
    UNTOUCHED = 1
    QUALIFICATION = 2
    FOLLOW_UP = 3
    COLD_L = 4
    PRESENTATION = 5
    PROPOSAL = 6
    NEGOTIATION = 7
    CLOSE_DEAL = 8
    LOST_DEAL = 9
    REASSIGN = 10
    DO_NOT_CALL = 11

    UNCONTACTED = 1
    CONTACTED = 2
    PIPELINE = 3
    CLOSE_DEAL = 4
    REASSIGN = 5

    B2B = 1
    B2C = 2

    ACTIVE = 1
    DELETED = 2

    STATUS = [
        (1, "untouched"),
        (2, "qualification"),
        (3, "follow up"),
        (4, "cold leads"),
        (5, "presentation"),
        (6, "proposal"),
        (7, "negotiation"),
        (8, "close deal"),
        (9, "lost deal"),
        (10, "reassign"),
        (11, "do not call")
    ]

    STATUS_LABEL = [
        (1, "uncontacted"),
        (2, "contacted"),
        (3, "pipeline"),
        (4, "close deal"),
        (5, "reassign")
    ]

    TYPE = [
        (B2B, "b2b"),
        (B2C, "b2c")
    ]

    CONDITION = [
        (ACTIVE, "active"),
        (DELETED, "deleted")
    ]

    client = models.ForeignKey(
        'Client',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS,
        default=1,
    )
    lead_score = models.IntegerField(
        null=True,
        blank=True
    )
    status_label = models.IntegerField(
        choices=STATUS_LABEL,
        default=1,
    )
    type = models.IntegerField(
        choices=TYPE,
        null=True,
        blank=True
    )
    source = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    date_contacted = models.DateField(
        null=True,
        blank=True
    )
    date_close_deal = models.DateField(
        null=True,
        blank=True
    )
    remarks = models.TextField(
        null=True,
        blank=True
    )
    condition = models.IntegerField(
        choices=CONDITION,
        default=ACTIVE
    )

    def __str__(self):
        return "%s %s %s" % (
            self.id,
            self.client.first_name,
            self.client.last_name
        )


class LeadOwner(models.Model):
    ON_PROGRESS = 1
    DONE_DEAL = 2

    STATUS = [
        (ON_PROGRESS, "on progress"),
        (DONE_DEAL, "done deal")
    ]
    account = models.ForeignKey(
        'Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    lead = models.ForeignKey(
        'LeadInformation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS,
        default=ON_PROGRESS
    )
    date_handle = models.DateField(
        null=True,
        blank=True
    )
    date_completed = models.DateField(null=True, blank=True)

    # def __str__(self):
    #     return f"{self.id}-{self.account.user.first_name}"
    def __str__(self):
        if self.id:
            lead_info = str(self.id)
        else:
            lead_info = "Lead info not available"
        if self.account:
            user_info = str(self.account.user.first_name)
        else:
            user_info = "User info not available"
        return f"{lead_info} - {user_info}"


class OwnerHistory(models.Model):
    ACTIVE = 1
    INACTIVE = 2

    STATUS = [
        (ACTIVE, "active"),
        (INACTIVE, "inactive")
    ]
    last_owner = models.ForeignKey(
        'Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    lead_owner = models.ForeignKey(
        'LeadOwner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS,
        default=ACTIVE
    )
    date_handle = models.DateField(null=True, blank=True)
    date_transfer = models.DateField(null=True, blank=True)


class Notes(models.Model):
    ACTIVE = 1
    DELETED = 2

    STATUS = [
        (ACTIVE, 'active'),
        (DELETED, 'deleted')
    ]

    lead_info = models.ForeignKey(
        'LeadInformation',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    message = models.TextField(
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS,
        default=ACTIVE
    )
    date_noted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s %s" % (
            self.lead_info.client.first_name,
            self.lead_info.client.last_name
        )


class Activity(models.Model):
    ACTIVE = 1
    DELETED = 2

    NEWLEADS = 1
    UPDATESTATUS = 2
    UPDATEINFO = 3

    STATUS = [
        (ACTIVE, 'active'),
        (DELETED, 'deleted')
    ]
    TYPE = [
        (NEWLEADS, 'new leads'),
        (UPDATESTATUS, "update status"),
        (UPDATEINFO, 'update info')
    ]

    lead_info = models.ForeignKey(
        'LeadInformation',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    message = models.TextField(
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS,
        default=ACTIVE
    )
    type = models.IntegerField(
        choices=TYPE,
        null=True,
        blank=True
    )
    date_generated = models.DateTimeField(null=True, blank=True)
    owner = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return "%s %s" % (
            self.lead_info.client.first_name,
            self.lead_info.client.last_name
        )


class ServiceOffered(models.Model):
    ACTIVE = 1
    INACTIVE = 2

    STATUS = [
        (ACTIVE, "active"),
        (INACTIVE, "inactive")
    ]
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name


class LeadServices(models.Model):
    ONGOING = 1
    DONE = 2
    HOLD = 3

    STATUS = [
        (ONGOING, "ongoing"),
        (DONE, "done"),
        (HOLD, "hold"),
    ]

    service = models.ForeignKey(
        'ServiceOffered',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    lead_info = models.ForeignKey(
        'LeadInformation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    otf = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=True,
        blank=True
    )
    msf = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS,
        default=ONGOING
    )
    revenue = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=True,
        blank=True
    )
    otf_payment = models.DateField(
        null=True,
        blank=True
    )


class MonthlyTerms(models.Model):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    MONTHS = [
        (JANUARY, "january"),
        (FEBRUARY, "february"),
        (MARCH, "march"),
        (APRIL, "april"),
        (MAY, "may"),
        (JUNE, "june"),
        (JULY, "july"),
        (AUGUST, "august"),
        (SEPTEMBER, "september"),
        (OCTOBER, "october"),
        (NOVEMBER, "november"),
        (DECEMBER, "december")
    ]

    lead_service = models.ForeignKey(
        'LeadServices',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    month_start = models.IntegerField(
        choices=MONTHS,
        null=True,
        blank=True
    )
    month_end = models.IntegerField(
        choices=MONTHS,
        null=True,
        blank=True
    )
    date_start = models.DateField(
        null=True,
        blank=True
    )
    date_end = models.DateField(
        null=True,
        blank=True
    )


class TermStatus(models.Model):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    DEFAULT = 1
    PAID = 2
    UNPAID = 3

    MONTHS = [
        (JANUARY, "january"),
        (FEBRUARY, "february"),
        (MARCH, "march"),
        (APRIL, "april"),
        (MAY, "may"),
        (JUNE, "june"),
        (JULY, "july"),
        (AUGUST, "august"),
        (SEPTEMBER, "september"),
        (OCTOBER, "october"),
        (NOVEMBER, "november"),
        (DECEMBER, "december")
    ]

    STATUS = [
        (PAID, "paid"),
        (UNPAID, "unpaid"),
        (DEFAULT, "default")
    ]
    lead_service = models.ForeignKey(
        'LeadServices',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    months = models.IntegerField(
        choices=MONTHS,
        null=True,
        blank=True
    )
    date_pay = models.DateField(
        null=True,
        blank=True
    )
    date_unpay = models.DateField(
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS,
        blank=True,
        null=True
    )
    year = models.IntegerField(
        null=True,
        blank=True
    )
    msf = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=True,
        blank=True
    )


class ServiceHistory(models.Model):
    lead_service = models.ForeignKey(
        'LeadServices',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    projected_revenue = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    projected_otf = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    projected_msf = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )


class Archive(models.Model):
    lead_info = models.ForeignKey(
        'LeadInformation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date_deleted = models.DateField(
        null=True,
        blank=True
    )
    deleted_by = models.ForeignKey(
        'Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return "%s %s" % (
            self.id,
            self.lead_info.client.first_name
        )


class Attachment(models.Model):
    ACTIVE = 1
    DELETED = 2

    status = [
        {ACTIVE, "active"},
        {DELETED, "deleted"}
    ]

    lead_info = models.ForeignKey(
        'LeadInformation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date_inserted = models.DateField(
        null=True,
        blank=True
    )
    label = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    status = models.IntegerField(
        default=ACTIVE,
        null=True,
        blank=True
    )
    file = models.FileField(
        upload_to='files',
        null=True,
        blank=True
    )
    uploaded_by = models.ForeignKey(
        'Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class Notification(models.Model):
    NEW_LEADS = 1

    SUBJECT = [
        (NEW_LEADS, "new leads")
    ]

    ACTIVE = 1
    DELETED = 2

    STATUS = [
        (ACTIVE, "active"),
        (DELETED, "deleted")
    ]

    sender = models.ForeignKey(
        'Account',
        related_name="sender",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    receiver = models.ForeignKey(
        'Account',
        related_name="receiver",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    subject = models.IntegerField(
        default=NEW_LEADS,
        choices=SUBJECT,
    )
    message = models.TextField(
        null=True,
        blank=True
    )
    status = models.IntegerField(
        default=ACTIVE,
        choices=STATUS
    )
    is_seen = models.BooleanField(default=False)
    date_deliver = models.DateTimeField(
        null=True,
        blank=True
    )
    date_seen = models.DateTimeField(
        null=True,
        blank=True
    )

    # def __str__(self):
    #     return self.u.employee_id
