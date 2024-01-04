from .models import Tag, Profile

def top_users_and_tags(request):
    context = {'users': Profile.objects.get_popular_profiles(), 'all_tags': Tag.objects.get_popular_tags()}
    return context
