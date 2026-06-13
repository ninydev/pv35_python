from django.shortcuts import render

from feedback.forms import FeedbackForm


# Create your views here.
def feedback_page(request):
    form = FeedbackForm()
    return render(request, 'forms/feedback_page.html', {'form': form})