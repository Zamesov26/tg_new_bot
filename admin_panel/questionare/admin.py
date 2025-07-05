from django.contrib import admin

from .models import Answer, FormInstance, Question, Questionnaire


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    readonly_fields = ("id",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "questionnaire", "function_name")
    list_filter = ("questionnaire",)

    readonly_fields = ("id",)


@admin.register(FormInstance)
class FormInstanceAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "questionnaire", "created_at")
    list_filter = ("questionnaire", "created_at")

    readonly_fields = ("id",)
    search_fields = ("user_id",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "question",
        "form_instance",
        "value",
        "created_at",
    )
    list_filter = ("created_at", "form_instance__questionnaire")

    readonly_fields = ("id",)
    search_fields = ("user_id", "value")
