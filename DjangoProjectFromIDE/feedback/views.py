from django.shortcuts import render

from djangopv35_v1 import settings
from feedback.forms import FeedbackForm


# Create your views here.
def feedback_page(request):

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if request.user.is_authenticated:
            form.user = request.user
        if form.is_valid():
            form.save()
            form.send_email()

    form = FeedbackForm()
    return render(request, 'forms/feedback_page.html', {'form': form})