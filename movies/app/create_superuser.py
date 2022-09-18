from django.contrib.auth.models import User

count_superusers = User.objects.filter(is_superuser=True).count()
if count_superusers == 0:
    User.objects.create_superuser('admin', 'admin@movies_admin.com', 'admin')