# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

import random

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


def vars_for_all_templates(self):

    return {'total_rounds': Constants.num_rounds,
            'round_number': self.subsession.round_number,
            'role': self.player.role(),
            'minimal_bonus': Constants.minimal_bonus,
            'paid_rounds': Constants.paid_rounds,
            'participation': Constants.participation,
            }


class WaitIntroPage(WaitPage):

    body_text = "Waiting for other players to start the game"

    wait_for_all_groups = True


class AChoice(Page):

    def is_displayed(self):
        return self.player.role() == 'attacker'

    form_model = models.Group
    form_fields = ['a_choice']

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.group.a_choice = random.choice(['Attack Defender','Attack User','No Attack'])
            self.group.att_rand = True


class DChoice(Page):

    def is_displayed(self):
        return self.player.role() == 'defender'

    form_model = models.Group
    form_fields = ['d_choice']

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.group.d_choice = random.choice(['Standard Security','Enhanced Security'])
            self.group.def_rand = True

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

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.group.u_choice = random.choice(['Standard Security','Enhanced Security'])
            self.group.user_rand = True


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

class FinalResults(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        group_in_all_rounds = self.group.in_all_rounds()

        a_total = sum([g.a_cum for g in self.group.in_all_rounds()])
        d_total = sum([g.d_cum for g in self.group.in_all_rounds()])
        u_total = sum([g.u_cum for g in self.group.in_all_rounds()])

        return {
            'player_in_all_rounds': player_in_all_rounds,
            'group_in_all_rounds': group_in_all_rounds,
            'a_total': a_total,
            'd_total': d_total,
            'u_total': u_total,
            'paying_rounds': self.session.vars['paying_rounds']
        }

    timeout_seconds = 120


page_sequence = [
    AChoice,
    DChoice,
    UWait,
    UChoice,
    ResultsWaitPage,
    Results,
    FinalResults
]