from django.shortcuts import render

from feedback.forms import FeedbackForm


# Create your views here.
def feedback_page(request):

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()


    form = FeedbackForm()
    return render(request, 'forms/feedback_page.html', {'form': form})