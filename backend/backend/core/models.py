from django.db import models
from django.utils import timezone


class Branch(models.Model):
    BRANCH_TYPE_CHOICES = [
        ('Main', 'Main'),
        ('Express', 'Express'),
        ('Premium', 'Premium'),
        ('Corporate', 'Corporate'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Temporarily Closed', 'Temporarily Closed'),
        ('Closed', 'Closed'),
    ]

    ZONE_CHOICES = [
        ('Urban', 'Urban'),
        ('Suburban', 'Suburban'),
        ('Rural', 'Rural'),
    ]

    branch_id = models.CharField(max_length=20, primary_key=True, unique=True)
    branch_code = models.CharField(max_length=10, unique=True)
    branch_name = models.CharField(max_length=100)
    branch_type = models.CharField(max_length=30, choices=BRANCH_TYPE_CHOICES)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    geographic_zone = models.CharField(max_length=30, choices=ZONE_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    has_atms = models.BooleanField(default=False)
    atm_count = models.IntegerField(default=0, blank=True, null=True)
    has_teller_windows = models.BooleanField(default=False)
    teller_window_count = models.IntegerField(default=0, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    branch_opening_date = models.DateField()
    branch_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['branch_name']

    def __str__(self):
        return f"{self.branch_name} ({self.branch_id})"


class Customer(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('DNI', 'DNI'),
        ('CURP', 'CURP'),
        ('CC', 'CC'),
        ('CE', 'CE'),
        ('Passport', 'Passport'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    ACCENT_CHOICES = [
        ('mexican', 'Mexican'),
        ('colombian', 'Colombian'),
        ('argentine', 'Argentine'),
    ]

    SEGMENT_CHOICES = [
        ('Premium', 'Premium'),
        ('Plus', 'Plus'),
        ('Basic', 'Basic'),
        ('Student', 'Student'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended'),
        ('Closed', 'Closed'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]

    EDUCATION_CHOICES = [
        ('Primary', 'Primary'),
        ('High School', 'High School'),
        ('University', 'University'),
        ('Postgraduate', 'Postgraduate'),
    ]

    customer_id = models.CharField(max_length=20, primary_key=True, unique=True)
    document_number = models.CharField(max_length=20, unique=True)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    landline_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    detected_accent = models.CharField(max_length=50, choices=ACCENT_CHOICES, blank=True, null=True)
    segment = models.CharField(max_length=50, choices=SEGMENT_CHOICES)
    credit_score = models.IntegerField(blank=True, null=True)
    estimated_monthly_income = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    education_level = models.CharField(max_length=30, choices=EDUCATION_CHOICES, blank=True, null=True)
    registration_date = models.DateTimeField()
    registration_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='registered_customers')
    customer_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    accepts_marketing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-registration_date']
        indexes = [
            models.Index(fields=['customer_id']),
            models.Index(fields=['document_number']),
            models.Index(fields=['segment']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_id})"


class ServiceAgent(models.Model):
    AGENT_TYPE_CHOICES = [
        ('Phone', 'Phone'),
        ('In-Person', 'In-Person'),
        ('Digital', 'Digital'),
        ('Hybrid', 'Hybrid'),
    ]

    EXPERIENCE_CHOICES = [
        ('Junior', 'Junior'),
        ('Mid-Senior', 'Mid-Senior'),
        ('Senior', 'Senior'),
        ('Specialist', 'Specialist'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Vacation', 'Vacation'),
        ('Leave', 'Leave'),
        ('Inactive', 'Inactive'),
    ]

    SHIFT_CHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Night', 'Night'),
        ('Rotating', 'Rotating'),
    ]

    agent_id = models.CharField(max_length=20, primary_key=True, unique=True)
    employee_code = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    native_accent = models.CharField(max_length=50, blank=True, null=True)
    country_of_origin = models.CharField(max_length=50)
    assigned_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='agents')
    agent_type = models.CharField(max_length=30, choices=AGENT_TYPE_CHOICES)
    experience_level = models.CharField(max_length=30, choices=EXPERIENCE_CHOICES)
    languages = models.CharField(max_length=100, blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField()
    avg_csat = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    total_monthly_interactions = models.IntegerField(blank=True, null=True)
    agent_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    work_shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.agent_id})"


class MarketingCampaign(models.Model):
    CAMPAIGN_TYPE_CHOICES = [
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Push', 'Push'),
        ('WhatsApp', 'WhatsApp'),
        ('Voice', 'Voice'),
        ('Mail', 'Mail'),
    ]

    OBJECTIVE_CHOICES = [
        ('Acquisition', 'Acquisition'),
        ('Retention', 'Retention'),
        ('Cross-sell', 'Cross-sell'),
        ('Up-sell', 'Up-sell'),
        ('Reactivation', 'Reactivation'),
    ]

    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('Active', 'Active'),
        ('Paused', 'Paused'),
        ('Completed', 'Completed'),
    ]

    SEGMENT_CHOICES = [
        ('Premium', 'Premium'),
        ('Plus', 'Plus'),
        ('Basic', 'Basic'),
        ('Student', 'Student'),
    ]

    campaign_id = models.CharField(max_length=20, primary_key=True, unique=True)
    campaign_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    campaign_type = models.CharField(max_length=30, choices=CAMPAIGN_TYPE_CHOICES)
    campaign_objective = models.CharField(max_length=30, choices=OBJECTIVE_CHOICES)
    promoted_product = models.CharField(max_length=100, blank=True, null=True)
    target_segment = models.CharField(max_length=50, choices=SEGMENT_CHOICES, blank=True, null=True)
    target_country = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    campaign_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    expected_conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.campaign_name} ({self.campaign_id})"


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('Checking Account', 'Checking Account'),
        ('Savings Account', 'Savings Account'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Personal Loan', 'Personal Loan'),
        ('Mortgage', 'Mortgage'),
        ('Investment', 'Investment'),
    ]

    CURRENCY_CHOICES = [
        ('MXN', 'MXN'),
        ('COP', 'COP'),
        ('ARS', 'ARS'),
        ('USD', 'USD'),
    ]

    CHANNEL_CHOICES = [
        ('Branch', 'Branch'),
        ('Web', 'Web'),
        ('App', 'App'),
        ('Call Center', 'Call Center'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Blocked', 'Blocked'),
        ('Closed', 'Closed'),
        ('Suspended', 'Suspended'),
    ]

    product_id = models.CharField(max_length=20, primary_key=True, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES)
    product_number = models.CharField(max_length=30, unique=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    opening_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    opening_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='opened_products')
    product_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    opening_channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES)
    has_linked_app = models.BooleanField(default=False)
    days_past_due = models.IntegerField(blank=True, null=True)
    last_transaction_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-opening_date']
        indexes = [
            models.Index(fields=['customer', 'product_status']),
            models.Index(fields=['product_number']),
        ]

    def __str__(self):
        return f"{self.product_type} - {self.product_id}"


class Transaction(models.Model):
    CURRENCY_CHOICES = [
        ('MXN', 'MXN'),
        ('COP', 'COP'),
        ('ARS', 'ARS'),
        ('USD', 'USD'),
    ]

    TYPE_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
        ('Payment', 'Payment'),
        ('Purchase', 'Purchase'),
        ('Adjustment', 'Adjustment'),
    ]

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Services', 'Services'),
        ('Entertainment', 'Entertainment'),
        ('Health', 'Health'),
        ('Other', 'Other'),
    ]

    CHANNEL_CHOICES = [
        ('ATM', 'ATM'),
        ('Branch', 'Branch'),
        ('Web', 'Web'),
        ('App', 'App'),
        ('POS', 'POS'),
        ('Transfer', 'Transfer'),
    ]

    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
        ('Pending', 'Pending'),
        ('Reversed', 'Reversed'),
    ]

    transaction_id = models.CharField(max_length=30, primary_key=True, unique=True)
    transaction_date = models.DateTimeField(db_index=True)
    process_date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    transaction_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    amount_usd = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    merchant_name = models.CharField(max_length=150, blank=True, null=True)
    merchant_category = models.CharField(max_length=50, blank=True, null=True)
    transaction_country = models.CharField(max_length=50)
    transaction_city = models.CharField(max_length=100, blank=True, null=True)
    transaction_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response_code = models.CharField(max_length=10, blank=True, null=True)
    is_fraud = models.BooleanField(default=False)
    fraud_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_date']
        indexes = [
            models.Index(fields=['customer', 'transaction_date']),
            models.Index(fields=['transaction_date']),
            models.Index(fields=['is_fraud']),
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.amount} {self.currency}"


class CallCenterInteraction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ('Inbound Call', 'Inbound Call'),
        ('Outbound Call', 'Outbound Call'),
        ('Chat', 'Chat'),
        ('Email', 'Email'),
        ('Video', 'Video'),
    ]

    CHANNEL_CHOICES = [
        ('Phone', 'Phone'),
        ('Web Chat', 'Web Chat'),
        ('WhatsApp', 'WhatsApp'),
        ('Email', 'Email'),
        ('App', 'App'),
    ]

    REASON_CATEGORY_CHOICES = [
        ('Transactional', 'Transactional'),
        ('Product', 'Product'),
        ('Technical', 'Technical'),
        ('Commercial', 'Commercial'),
        ('Complaint', 'Complaint'),
    ]

    SENTIMENT_CHOICES = [
        ('Positive', 'Positive'),
        ('Neutral', 'Neutral'),
        ('Negative', 'Negative'),
        ('Very Negative', 'Very Negative'),
    ]

    interaction_id = models.CharField(max_length=30, primary_key=True, unique=True)
    interaction_date = models.DateTimeField(db_index=True)
    process_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    agent = models.ForeignKey(ServiceAgent, on_delete=models.SET_NULL, null=True, blank=True, related_name='interactions')
    interaction_type = models.CharField(max_length=30, choices=INTERACTION_TYPE_CHOICES)
    channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES)
    contact_reason = models.CharField(max_length=100)
    reason_category = models.CharField(max_length=50, choices=REASON_CATEGORY_CHOICES)
    duration_seconds = models.IntegerField(blank=True, null=True)
    wait_time_seconds = models.IntegerField(blank=True, null=True)
    was_resolved = models.BooleanField(default=False)
    requires_followup = models.BooleanField(default=False)
    detected_sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, blank=True, null=True)
    sentiment_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    customer_detected_accent = models.CharField(max_length=50, blank=True, null=True)
    agent_used_accent = models.CharField(max_length=50, blank=True, null=True)
    was_escalated = models.BooleanField(default=False)
    mentioned_products = models.CharField(max_length=200, blank=True, null=True)
    has_transcript = models.BooleanField(default=False)
    has_recording = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-interaction_date']
        indexes = [
            models.Index(fields=['customer', 'interaction_date']),
            models.Index(fields=['agent', 'interaction_date']),
            models.Index(fields=['was_resolved']),
        ]

    def __str__(self):
        return f"{self.interaction_id} - {self.interaction_type}"


class CallTranscript(models.Model):
    LANGUAGE_CHOICES = [
        ('Spanish', 'Spanish'),
        ('English', 'English'),
        ('Portuguese', 'Portuguese'),
    ]

    TRANSCRIPTION_MODEL_CHOICES = [
        ('Whisper', 'Whisper'),
        ('Google STT', 'Google STT'),
        ('Manual', 'Manual'),
    ]

    AUDIO_QUALITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    transcript_id = models.CharField(max_length=30, primary_key=True, unique=True)
    interaction = models.OneToOneField(CallCenterInteraction, on_delete=models.CASCADE, related_name='transcript')
    process_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transcripts')
    agent = models.ForeignKey(ServiceAgent, on_delete=models.SET_NULL, null=True, blank=True, related_name='transcripts')
    full_text = models.TextField()
    customer_text = models.TextField(blank=True, null=True)
    agent_text = models.TextField(blank=True, null=True)
    detected_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    detected_accent = models.CharField(max_length=50, blank=True, null=True)
    accent_confidence = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    detected_keywords = models.CharField(max_length=500, blank=True, null=True)
    mentioned_entities = models.TextField(blank=True, null=True)
    detected_intents = models.CharField(max_length=300, blank=True, null=True)
    main_topics = models.CharField(max_length=300, blank=True, null=True)
    transcription_model = models.CharField(max_length=50, choices=TRANSCRIPTION_MODEL_CHOICES)
    audio_quality = models.CharField(max_length=20, choices=AUDIO_QUALITY_CHOICES, blank=True, null=True)
    duration_seconds = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-process_date']

    def __str__(self):
        return f"{self.transcript_id}"


class SatisfactionSurvey(models.Model):
    SURVEY_TYPE_CHOICES = [
        ('CSAT', 'CSAT'),
        ('NPS', 'NPS'),
        ('CES', 'CES'),
    ]

    CHANNEL_CHOICES = [
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('IVR', 'IVR'),
        ('App', 'App'),
        ('Web', 'Web'),
    ]

    NPS_CATEGORY_CHOICES = [
        ('Promoter', 'Promoter'),
        ('Passive', 'Passive'),
        ('Detractor', 'Detractor'),
    ]

    SENTIMENT_CHOICES = [
        ('Positive', 'Positive'),
        ('Neutral', 'Neutral'),
        ('Negative', 'Negative'),
    ]

    survey_id = models.CharField(max_length=30, primary_key=True, unique=True)
    survey_date = models.DateTimeField(db_index=True)
    process_date = models.DateField()
    interaction = models.ForeignKey(CallCenterInteraction, on_delete=models.SET_NULL, null=True, blank=True, related_name='surveys')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='surveys')
    agent = models.ForeignKey(ServiceAgent, on_delete=models.SET_NULL, null=True, blank=True, related_name='surveys')
    survey_type = models.CharField(max_length=20, choices=SURVEY_TYPE_CHOICES)
    send_channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES)
    main_score = models.IntegerField()
    nps_category = models.CharField(max_length=20, choices=NPS_CATEGORY_CHOICES, blank=True, null=True)
    question_1_text = models.TextField(blank=True, null=True)
    question_1_response = models.IntegerField(blank=True, null=True)
    question_2_text = models.TextField(blank=True, null=True)
    question_2_response = models.IntegerField(blank=True, null=True)
    question_3_text = models.TextField(blank=True, null=True)
    question_3_response = models.IntegerField(blank=True, null=True)
    open_comments = models.TextField(blank=True, null=True)
    comment_sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, blank=True, null=True)
    response_time_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    campaign_response_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-survey_date']
        indexes = [
            models.Index(fields=['customer', 'survey_date']),
            models.Index(fields=['survey_type']),
        ]

    def __str__(self):
        return f"{self.survey_id} - Score: {self.main_score}"


class DigitalEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('PageView', 'PageView'),
        ('Click', 'Click'),
        ('FormSubmit', 'FormSubmit'),
        ('Login', 'Login'),
        ('Logout', 'Logout'),
        ('Error', 'Error'),
        ('Transaction', 'Transaction'),
    ]

    CATEGORY_CHOICES = [
        ('Navigation', 'Navigation'),
        ('Transaction', 'Transaction'),
        ('Authentication', 'Authentication'),
        ('Product', 'Product'),
        ('Error', 'Error'),
    ]

    CHANNEL_CHOICES = [
        ('Android App', 'Android App'),
        ('iOS App', 'iOS App'),
        ('Desktop Web', 'Desktop Web'),
        ('Mobile Web', 'Mobile Web'),
    ]

    PLATFORM_CHOICES = [
        ('Android', 'Android'),
        ('iOS', 'iOS'),
        ('Windows', 'Windows'),
        ('macOS', 'macOS'),
        ('Linux', 'Linux'),
    ]

    event_id = models.CharField(max_length=30, primary_key=True, unique=True)
    event_date = models.DateTimeField(db_index=True)
    process_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='digital_events')
    session_id = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    event_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES)
    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES, blank=True, null=True)
    browser = models.CharField(max_length=50, blank=True, null=True)
    app_version = models.CharField(max_length=20, blank=True, null=True)
    page_url = models.CharField(max_length=300, blank=True, null=True)
    page_title = models.CharField(max_length=300, blank=True, null=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    element_id = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='digital_events')
    event_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    duration_seconds = models.IntegerField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    ip_country = models.CharField(max_length=50, blank=True, null=True)
    ip_city = models.CharField(max_length=100, blank=True, null=True)
    is_mobile = models.BooleanField(default=False)
    referrer = models.CharField(max_length=300, blank=True, null=True)
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']
        indexes = [
            models.Index(fields=['customer', 'event_date']),
            models.Index(fields=['session_id']),
            models.Index(fields=['event_type']),
        ]

    def __str__(self):
        return f"{self.event_id} - {self.event_type}"


class Complaint(models.Model):
    CASE_TYPE_CHOICES = [
        ('Complaint', 'Complaint'),
        ('Claim', 'Claim'),
        ('Request', 'Request'),
        ('Suggestion', 'Suggestion'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Process', 'In Process'),
        ('Escalated', 'Escalated'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
        ('Rejected', 'Rejected'),
    ]

    RECEPTION_CHANNEL_CHOICES = [
        ('Call Center', 'Call Center'),
        ('Email', 'Email'),
        ('Web', 'Web'),
        ('App', 'App'),
        ('Branch', 'Branch'),
        ('Regulatory', 'Regulatory'),
    ]

    complaint_id = models.CharField(max_length=30, primary_key=True, unique=True)
    creation_date = models.DateTimeField(db_index=True)
    process_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='complaints')
    case_type = models.CharField(max_length=30, choices=CASE_TYPE_CHOICES)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    reception_channel = models.CharField(max_length=30, choices=RECEPTION_CHANNEL_CHOICES)
    affected_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    related_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    origin_interaction = models.ForeignKey(CallCenterInteraction, on_delete=models.SET_NULL, null=True, blank=True, related_name='originated_complaints')
    description = models.TextField()
    claimed_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    claimed_currency = models.CharField(max_length=3, blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    assigned_agent = models.ForeignKey(ServiceAgent, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    assignment_date = models.DateTimeField(blank=True, null=True)
    first_response_date = models.DateTimeField(blank=True, null=True)
    resolution_date = models.DateTimeField(blank=True, null=True)
    closing_date = models.DateTimeField(blank=True, null=True)
    sla_breached = models.BooleanField(default=False)
    resolution_days = models.IntegerField(blank=True, null=True)
    resolution_text = models.TextField(blank=True, null=True)
    compensation_granted = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    resolution_satisfaction_score = models.IntegerField(blank=True, null=True)
    is_repeat_complainer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creation_date']
        indexes = [
            models.Index(fields=['customer', 'creation_date']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f"{self.complaint_id} - {self.case_type}"


class CampaignSend(models.Model):
    CHANNEL_CHOICES = [
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Push', 'Push'),
        ('WhatsApp', 'WhatsApp'),
        ('Voice', 'Voice'),
    ]

    STATUS_CHOICES = [
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
        ('Bounced', 'Bounced'),
        ('Blocked', 'Blocked'),
    ]

    DEVICE_CHOICES = [
        ('Desktop', 'Desktop'),
        ('Mobile', 'Mobile'),
        ('Tablet', 'Tablet'),
    ]

    send_id = models.CharField(max_length=30, primary_key=True, unique=True)
    send_date = models.DateTimeField(db_index=True)
    process_date = models.DateField()
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, related_name='sends')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='campaign_sends')
    send_channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES)
    template_used = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    send_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    was_delivered = models.BooleanField(default=False)
    was_opened = models.BooleanField(default=False)
    was_clicked = models.BooleanField(default=False)
    open_date = models.DateTimeField(blank=True, null=True)
    click_date = models.DateTimeField(blank=True, null=True)
    click_count = models.IntegerField(default=0, blank=True, null=True)
    had_conversion = models.BooleanField(default=False)
    conversion_date = models.DateTimeField(blank=True, null=True)
    conversion_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    open_device = models.CharField(max_length=30, choices=DEVICE_CHOICES, blank=True, null=True)
    open_country = models.CharField(max_length=50, blank=True, null=True)
    failure_reason = models.CharField(max_length=200, blank=True, null=True)
    send_cost = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-send_date']
        indexes = [
            models.Index(fields=['customer', 'send_date']),
            models.Index(fields=['campaign', 'send_date']),
            models.Index(fields=['send_status']),
        ]

    def __str__(self):
        return f"{self.send_id} - {self.send_channel}"


class DailyExchangeRate(models.Model):
    CURRENCY_CHOICES = [
        ('MXN', 'MXN'),
        ('COP', 'COP'),
        ('ARS', 'ARS'),
        ('USD', 'USD'),
    ]

    date = models.DateField(db_index=True)
    source_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    target_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=6)
    buy_rate = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    sell_rate = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('date', 'source_currency', 'target_currency')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date', 'source_currency', 'target_currency']),
        ]

    def __str__(self):
        return f"{self.source_currency}/{self.target_currency} - {self.date}"
