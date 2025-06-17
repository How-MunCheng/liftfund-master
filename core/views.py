from django.db.models import Q, Sum, FloatField, ExpressionWrapper, F, Count
from django.db.models.functions import Cast
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from accounts.models import User
from campaign.models import Campaign, Donation
from core.models import Category


class HomeView(ListView):
    model = Campaign
    template_name = "home.html"
    context_object_name = "campaigns"

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = (
            Campaign.objects
            .prefetch_related("user")
            .filter(is_active=True)
            .annotate(
                annotated_total_raised=Sum('donation__donation', filter=Q(donation__approved=True)),
                annotated_progress_percentage=ExpressionWrapper(
                    100 * (Sum('donation__donation', filter=Q(donation__approved=True)) /
                    Cast(F('goal'), FloatField())),
                    output_field=FloatField()
                ),
            )
            .order_by("-date")
        )
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(category__name__icontains=query)
            )

        return qs  # Or your preferred limit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_campaigns"] = Campaign.objects.filter(is_active=True).count()
        context["fund_raised"] = Donation.objects.filter(approved=True).aggregate(Sum("donation"))
        context["members"] = User.objects.count()
        context["search_term"] = self.request.GET.get("q", "")
        context["categories"] = (
            Category.objects.annotate(
                num_campaigns=Count('campaign', filter=Q(campaign__is_active=True))
            ).order_by('-num_campaigns', 'name')[:4]
        )
        return context

class CategoryListView(ListView):
    model = Category
    template_name = "categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.annotate(
            active_campaign_count=Count('campaign', filter=Q(campaign__is_active=True))
        ).order_by('name')




class CampaignCategoryListView(ListView):
    model = Campaign
    template_name = "campaigns/campaigns-by-category.html"
    context_object_name = "campaigns"

    def get_queryset(self):
        category_id = self.kwargs.get("pk")
        query = self.request.GET.get('q')
        qs = (
            Campaign.objects.filter(category_id=category_id, is_active=True)
            .annotate(
                annotated_total_raised=Sum(
                    'donation__donation', filter=Q(donation__approved=True)
                ),
                annotated_progress_percentage=ExpressionWrapper(
                    100 * (
                        Sum('donation__donation', filter=Q(donation__approved=True)) /
                        Cast(F('goal'), FloatField())
                    ),
                    output_field=FloatField()
                ),
            )
            .order_by('-date')
        )
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(pk=self.kwargs["pk"])
        return context


class HowItWorksView(TemplateView):
    template_name = "how-it-works.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["steps"] = [
            {
                "icon": "fa fa-lightbulb-o",
                "title": "1. Start with an Idea",
                "description": "Have a creative project, cause, or dream? Start by crafting your campaign story."
            },
            {
                "icon": "fa fa-edit",
                "title": "2. Create Your Campaign",
                "description": "Set up your fundraising goal, deadline, and rewards. Add compelling images and videos."
            },
            {
                "icon": "fa fa-share-alt",
                "title": "3. Share with Everyone",
                "description": "Launch your campaign and share it with your network through social media and email."
            },
            {
                "icon": "fa fa-users",
                "title": "4. Engage Supporters",
                "description": "Keep your backers updated and engaged throughout your campaign journey."
            }
        ]
        return context

class AboutUsView(TemplateView):
    template_name = "about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add extra context variables here if needed in the future
        # context["team"] = [ ... ]  # example
        return context