from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from config.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("team/", TemplateView.as_view(template_name="pages/team.html"), name="team"),
    path("planning/", TemplateView.as_view(template_name="pages/planning.html"), name="planning"),
    path("resources/", TemplateView.as_view(template_name="pages/resources.html"), name="resources"),
    # Django Admin, use {% url 'admin:index' %}
    path("sitemap.xml/", sitemap, kwargs={"sitemaps": sitemaps}, name="sitemap"),
    path("jet/", include("jet.urls", "jet")),  # Django JET URLS
    path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "robots.txt/",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    # User management
    path("users/", include("rahulgupta.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
