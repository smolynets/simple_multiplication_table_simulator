import random
from datetime import datetime, timedelta

from django.db import models
from solo.models import SingletonModel


class FinishPerDay(models.Model):
    finish_time = models.CharField(max_length=50)
    score = models.CharField(max_length=10)
    spended_time = models.CharField(max_length=1000)

    @classmethod
    def how_many_seconds_until_midnight(cls):
        """
        Get the number of seconds until midnight.
        """
        tomorrow = datetime.now() + timedelta(1)
        midnight = datetime(
            year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=0, minute=0, second=0
        )
        return (midnight - datetime.now()).seconds


    @classmethod
    def get_spent_time(cls, request):
        """
        Get difference bettwen current time and saved in session start time
        """
        if request.session.get("start_time") and request.session.get("finish_time"):
            start_time = datetime.strptime(request.session["start_time"], "%Y-%m-%d %H:%M:%S")
            now = datetime.strptime(request.session["finish_time"], "%Y-%m-%d %H:%M:%S")
            time_delta = now - start_time
            return time_delta.seconds
        seconds = None
        return seconds


    @classmethod
    def get_correct_aswers_str(cls, correct_aswers):
        """
        Different question words
        """
        if correct_aswers == 0 or correct_aswers >= 5:
            return f"{correct_aswers} питань"
        return f"{correct_aswers} питання"


    @classmethod
    def create_finish_per_day(cls, score, finish_time, spended_time):
        """
        Create FinishPerDay when finish studing per day
        """
        if not FinishPerDay.objects.filter(finish_time=finish_time).exists():
            FinishPerDay.objects.create(
                finish_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                score=score,
                spended_time=spended_time,
            )


    @classmethod
    def prepare_sessions(cls, request):
        """
        Check question_number and correct_aswers variables in request.session
        """
        seconds_until_midnight = cls.how_many_seconds_until_midnight()
        request.session.set_expiry(seconds_until_midnight)
        if not request.session.get("question_number"):
            request.session["question_number"] = 0
        if not request.session.get("correct_aswers"):
            request.session["correct_aswers"] = 0


    @classmethod
    def index_post_logic(cls, request):
        """
        Logic for POST method
        """
        template_name = None
        template_params = None
        choice = int(request.POST["choice"])
        form_multiplication_result = int(request.POST["result"])
        if request.session["question_number"] == 10 and not request.session.get("finish_time"):
            request.session["finish_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if choice != form_multiplication_result:
            if request.session["question_number"] == 10:
                seconds = cls.get_spent_time(request)
                cls.create_finish_per_day(
                    request.session["correct_aswers"], request.session.get("finish_time"), seconds
                )
                template_name = "negative_limit_per_day.html"
                template_params = {
                                    "form_multiplication_result": form_multiplication_result,
                                    "correct_aswers_str": cls.get_correct_aswers_str(
                                        request.session["correct_aswers"]
                                    ),
                                    "seconds": seconds,
                                }
            else:
                template_name = "negative_answer.html"
                template_params = {"form_multiplication_result": form_multiplication_result}
        else:
            if request.session["question_number"] <= 10 and not request.session.get("finish_time"):
                request.session["correct_aswers"] += 1
            else:
                if request.session["question_number"] == 10 and not request.session.get(
                    "finish_last_question"
                ):
                    request.session["correct_aswers"] += 1
                    request.session["finish_last_question"] = True
                seconds = cls.get_spent_time(request)
                cls.create_finish_per_day(
                    request.session["correct_aswers"], request.session.get("finish_time"), seconds
                )
                template_name = "positive_limit_per_day.html"
                template_params = {
                        "correct_aswers_str": cls.get_correct_aswers_str(
                            request.session["correct_aswers"]
                        ),
                        "seconds": seconds,
                    }
        return template_name, template_params


    @classmethod
    def index_get_logic(cls, request):
        """
        Logic for GET method
        """
        template_name = None
        template_params = None
        if not request.session.get("start_page"):
            request.session["start_page"] = True
            template_name = "start.html"
            template_params = {}
        else:
            first_number = random.randint(1, 10)
            second_number = random.randint(1, 10)
            # first_number = random.randint(-10, 10)
            # second_number = random.randint(-10, 10)
            multiplication_result = first_number * second_number
            random_answers = random.sample(range(1, 100), 3)
            random_insert_index = random.randint(0, 3)
            random_answers.insert(random_insert_index, multiplication_result)
            request.session["question_number"] += 1
            if request.session["question_number"] == 1:
                request.session["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if request.session["question_number"] > 10:
                seconds = cls.get_spent_time(request)
                template_name = "limit_per_day.html"
                template_params = {
                        "correct_aswers_str": cls.get_correct_aswers_str(request.session["correct_aswers"]),
                        "seconds": seconds,
                    }
            else:
                template_name = "question_form.html"
                template_params = {
                        "first_number": first_number,
                        "second_number": second_number,
                        "first_question": random_answers[0],
                        "second_question": random_answers[1],
                        "third_question": random_answers[2],
                        "fourth_question": random_answers[3],
                        "multiplication_result": multiplication_result,
                        "current_question_number": request.session["question_number"],
                    }
        return template_name, template_params


class SiteConfiguration(SingletonModel):
    greeting_text = models.TextField()

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
