from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home/hero.html"


class AboutView(TemplateView):
    template_name = "home/about.html"


class ContactView(TemplateView):
    template_name = "home/contact.html"


class ServicesView(TemplateView):
    template_name = "home/services.html"
