# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

import random

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

def vars_for_all_templates(self):

    return {'total_rounds': Constants.total_rounds,
            'num_rounds': Constants.num_rounds,
            'round_number': self.subsession.round_number,
            'player.role': self.player.role(),
            'minimal_bonus': Constants.minimal_bonus,
            'paid_rounds': Constants.paid_rounds,
            'participation': Constants.participation,
            'game_rounds': Constants.game_rounds,
            'adefs': Constants.APayoff_DefS,
            'adeff': Constants.APayoff_DefFAbs,
            'ausers': Constants.APayoff_UseS,
            'auserf': Constants.APayoff_UseF,
            'ddefs': Constants.DPayoff_DefSAbs,
            'ddeff': Constants.DPayoff_DefF,
            'dusers': Constants.DPayoff_UseSAbs,
            'duserf': Constants.DPayoff_UseF,
            'udefs': Constants.UPayoff_DefS,
            'udeff': Constants.UPayoff_DefF,
            'uusers': Constants.UPayoff_UseSAbs,
            'uuserf': Constants.UPayoff_UseF,
            'dno': Constants.DPayoff_No,
            'uno': Constants.UPayoff_No,
            'acostd': Constants.ACostD,
            'acostu': Constants.ACostU,
            'dcosts': Constants.DCostLS,
            'dcoste': Constants.DCostHS,
            'ucosts': Constants.UCostLS,
            'ucoste': Constants.UCostHS,}


class WaitIntroPage(WaitPage):

    body_text = "Please wait for other players to arrive. This page will automatically refresh when all participants have joined"

    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1


class CustomWait(WaitPage):

    template_name = "t_w_g_du_intro/CustomWait.html"

    def vars_for_template(self):
        return { "alt_title_text":"Please wait while other participants arrive. Once enough have accepted the HIT, a chime will sound if you have autoplay enabled for audio. If you would like a browser notification when it is time to begin, please granted this site permission to send you a notification.",
                "body_text":"Once the experiments begins, the whole process should take less than 30 minutes."
                }
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1

class Infosheet(Page):

    template_name = "t_w_g_du_intro/Infosheet.html"

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['consent']


class No(Page):

    def is_displayed(self):
        return self.player.consent == 'I am under 18 years of age, and/or do not wish to continue the game'


class Introduction1(Page):

    def is_displayed(self):
        return {self.subsession.round_number == 1,
                self.player.consent == 'I have read the above information, am 18 years of age or older, and I wish to continue with the game.'}

    timeout_seconds = 60


class Introduction2(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    timeout_seconds = 60


class Introduction3(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    timeout_seconds = 60


class Introduction4(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    timeout_seconds = 60


class Introduction5(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    timeout_seconds = 60


class Introduction6(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    timeout_seconds = 60


class AChoice(Page):

    def is_displayed(self):
        return self.player.role() == 'attacker'

    form_model = models.Group
    form_fields = ['a_choice']

    timeout_seconds = 45

    def before_next_page(self):
        if self.timeout_happened:
            self.group.a_choice = random.choice(['Attack Defender','Attack User','No Attack'])
            self.group.a_skipped = True
        else:
            self.group.a_skipped = False


class DChoice(Page):

    def is_displayed(self):
        return self.player.role() == 'defender'

    form_model = models.Group
    form_fields = ['d_choice']

    timeout_seconds = 45

    def before_next_page(self):
        if self.timeout_happened:
            self.group.d_choice = random.choice(['Standard Security','Enhanced Security'])
            self.group.d_skipped = True
        else:
            self.group.d_skipped = False


class UWait(WaitPage):
    body_text = "Waiting for the defender to make a decision"


class UChoice(Page):

    def vars_for_template(self):
        return {
            'd_choice': self.group.d_choice,
        }

    def is_displayed(self):
        return self.player.role() == 'user'

    form_model = models.Group
    form_fields = ['u_choice']

    timeout_seconds = 45

    def before_next_page(self):
        if self.timeout_happened:
            self.group.u_choice = random.choice(['Standard Security','Enhanced Security'])
            self.group.u_skipped = True
        else:
            self.group.u_skipped = False


class ResultsWaitPage(WaitPage):

    body_text = "Waiting for the other participants to decide."

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    def vars_for_template(self):

        return {
            'a_choice': self.group.a_choice,
            'd_choice': self.group.d_choice,
            'u_choice': self.group.u_choice,
            'acost': self.group.a_cost,
            'dcost': self.group.d_cost,
            'ucost': self.group.u_cost,
            'result': self.group.message,
            'payoff': self.player.payoff
        }

    timeout_seconds = 30


class Question(Page):

    template_name = 't_w_g_du_intro/Question.html'

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    form_model = models.Player
    form_fields = ['training1']

    timeout_seconds = 30


class Answer(Page):

    template_name = 't_w_g_du_intro/Answer.html'

    def vars_for_template(self):
        return {
            'is_correct': self.player.is_training1_correct(),
            'training1': self.player.training1,
            'att_ans': Constants.att_train1_correct,
            'def_ans': Constants.def_train1_correct,
            'user_ans': Constants.user_train1_correct
        }

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    timeout_seconds = 30


class Question2(Page):

    template_name = 't_w_g_du_intro/Question2.html'

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    form_model = models.Player
    form_fields = ['training2a', 'training2du']

    timeout_seconds = 30


class Answer2(Page):

    template_name = 't_w_g_du_intro/Answer2.html'

    def vars_for_template(self):
        return {
            'is_correct': self.player.is_training2_correct(),
            'training2a': self.player.training2a(),
            'training2du': self.player.training2du(),
            'att_ans': Constants.att_train2_correct,
            'def_ans': Constants.def_train2_correct,
            'user_ans': Constants.user_train2_correct
        }

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    timeout_seconds = 30


class Question3(Page):

    template_name = 't_w_g_du_intro/Question3.html'

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    form_model = models.Player
    form_fields = ['training3']

    timeout_seconds = 30


class Answer3(Page):

    template_name = 't_w_g_du_intro/Answer3.html'

    def vars_for_template(self):
        return {
            'is_correct': self.player.is_training3_correct(),
            'training3': self.player.training3,
            'att_ans': Constants.att_train3_correct,
            'def_ans': Constants.def_train3_correct,
            'user_ans': Constants.user_train3_correct
        }

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    timeout_seconds = 30


class Question4(Page):

    template_name = 't_w_g_du_intro/Question4.html'

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    form_model = models.Player
    form_fields = ['training4']

    timeout_seconds = 30


class Answer4(Page):

    template_name = 't_w_g_du_intro/Answer4.html'

    def vars_for_template(self):
        return {
            'is_correct': self.player.is_training4_correct(),
            'training4': self.player.training4,
            'att_ans': Constants.att_train4_correct,
            'def_ans': Constants.def_train4_correct,
            'user_ans': Constants.user_train4_correct
        }

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    timeout_seconds = 30


page_sequence = [
    CustomWait,
    Infosheet,
    No,
    Introduction1,
    Introduction2,
    Introduction3,
    Introduction4,
    Introduction5,
    Introduction6,
    AChoice,
    DChoice,
    UWait,
    UChoice,
    ResultsWaitPage,
    Results,
    Question,
    Answer,
    Question3,
    Answer3,
    Question4,
    Answer4
]
