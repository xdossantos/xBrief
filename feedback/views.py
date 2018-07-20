from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()


class FeedbackList(SelectRelatedMixin, generic.ListView):
    model = models.Feedback
    select_related = ("user", "project")


class UserFeedback(generic.ListView):
    model = models.Feedback
    template_name = "feedback/user_feedback_list.html"

    def get_queryset(self):
        try:
            self.feedback_user = User.objects.prefetch_related("feedback").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.feedback_user.feedback.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_user"] = self.feedback_user
        return context


class FeedbackDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Feedback
    select_related = ("user", "project")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreateFeedback(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','project') #the fields we want people to be able to edit
    model = models.Feedback

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form): #This connects the post to the user
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteFeedback(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Feedback
    select_related = ("user", "project")
    success_url = reverse_lazy("feedback:all")#once you have deleted a post it will show you all remaining feedback

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Feedback Deleted")
        return super().delete(*args, **kwargs)
