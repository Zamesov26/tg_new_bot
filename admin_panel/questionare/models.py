import uuid

from django.db import models


class Questionnaire(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)

    class Meta:
        db_table = "questionnaire"
        managed = False

    def __str__(self):
        return self.title


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    questionnaire = models.ForeignKey(
        "Questionnaire", on_delete=models.DO_NOTHING
    )
    text = models.TextField()
    function_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "question"
        managed = False

    def __str__(self):
        return self.text


class FormInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.BigIntegerField()
    questionnaire = models.ForeignKey(
        "Questionnaire", on_delete=models.DO_NOTHING
    )
    created_at = models.DateTimeField()

    class Meta:
        db_table = "form_instance"
        managed = False

    def __str__(self):
        return f"{self.user_id} ({self.created_at:%Y-%m-%d})"


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey("Question", on_delete=models.DO_NOTHING)
    user_id = models.BigIntegerField()
    value = models.TextField()
    created_at = models.DateTimeField()
    form_instance = models.ForeignKey(
        "FormInstance", on_delete=models.DO_NOTHING
    )

    class Meta:
        db_table = "answer"
        managed = False

    def __str__(self):
        return f"Answer {self.id} — Q{self.question_id} by {self.user_id}"
