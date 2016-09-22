# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Sarah A Kusumastuti'

doc = """
Behavioral cyber 3 way game
"""


class Constants(BaseConstants):
    name_in_url = 't_w_g_ud'
    players_per_group = 3
    num_rounds = 5
    paid_rounds = 3
    participation = 1
    minimal_bonus = 1

    U_SProb_UHDH = .2
    U_SProb_ULDH = .4
    U_SProb_UHDL = .6
    U_SProb_ULDL = .8
    D_SProb_UHDH = .55
    D_SProb_ULDH = .55
    D_SProb_UHDL = .85
    D_SProb_ULDL = .85
    No_SProb = 1
    APayoff_DefS = c(8)
    APayoff_DefF = c(-2)
    APayoff_UseS = c(1)
    APayoff_UseF = c(0)
    APayoff_No = c(0)
    DPayoff_DefS = c(-2)
    DPayoff_DefF = c(3)
    DPayoff_UseS = c(-0.5)
    DPayoff_UseF = c(2)
    DPayoff_No = c(1)
    UPayoff_DefS = c(0)
    UPayoff_DefF = c(0)
    UPayoff_UseS = c(-0.5)
    UPayoff_UseF = c(3)
    UPayoff_No = c(0.5)
    ACostD = c(2)
    ACostU = c(0.5)
    ACostNo = c(0)
    DCostHS = c(2)
    DCostLS = c(0.5)
    UCostHS = c(1.4)
    UCostLS = c(0)

    success_msg = 'attack successful'
    fail_msg = 'attack failed'
    no_atk_msg = 'no attack'

    atk_train_ans = '2'
    def_train_ans = '0.5'
    user_train_ans = '0'


class Subsession(BaseSubsession):

    def before_session_starts(self):
        if self.round_number == 1:
            paying_rounds = random.sample(range(1,Constants.num_rounds), Constants.paid_rounds)
            self.session.vars['paying_rounds'] = paying_rounds


class Group(BaseGroup):

    # attacker
    a_choice = models.CharField(choices=[
        'Attack Defender',
        'Attack User',
        'No Attack'],
        verbose_name='Please select your action', doc = """Attacker choice""",
        widget=widgets.RadioSelect())
    # defender
    d_choice = models.CharField(choices=[
        'Standard Security',
        'Enhanced Security'],
        verbose_name='Please select your action', doc = """Defender choice""",
        widget=widgets.RadioSelect())

    # user
    u_choice = models.CharField(choices=[
        'Standard Security',
        'Enhanced Security'],
        verbose_name='Please select your action', doc = """User choice""",
        widget=widgets.RadioSelect())

    p_success = models.FloatField()

    atk_success = models.BooleanField(
        doc="""Whether an attack was successful"""
    )

    no_atk = models.BooleanField(
        doc="""Whether there is no attack"""
    )

    message = models.CharField(doc="""message displayed to all""")

    a_cost = models.CurrencyField()
    d_cost = models.CurrencyField()
    u_cost = models.CurrencyField()

    a_pay = models.CurrencyField()
    d_pay = models.CurrencyField()
    u_pay = models.CurrencyField()

    a_cum = models.CurrencyField()
    d_cum = models.CurrencyField()
    u_cum = models.CurrencyField()

    def set_payoffs(self):

        attacker = self.get_player_by_role('attacker')
        defender = self.get_player_by_role('defender')
        user = self.get_player_by_role('user')

        #rand=random.random()

        if self.a_choice == 'Attack Defender':
            self.a_cost = Constants.ACostD
        elif self.a_choice == 'Attack User':
            self.a_cost = Constants.ACostU
        elif self.a_choice == 'No Attack':
            self.a_cost = Constants.ACostNo

        if self.d_choice == 'Standard Security':
            self.d_cost = Constants.DCostLS
        elif self.d_choice == 'Enhanced Security':
            self.d_cost = Constants.DCostHS

        if self.u_choice == 'Standard Security':
            self.u_cost = Constants.UCostLS
        elif self.u_choice == 'Enhanced Security':
            self.u_cost = Constants.UCostHS

        """if self.a_choice == 'Attack Defender':
            attacker.payoff = c(1)
            defender.payoff = c(2)
            user.payoff = c(3)
        elif self.a_choice == 'No Attack':
            attacker.payoff = c(7)
            defender.payoff = c(8)
            user.payoff = c(9)"""

        if self.a_choice == 'Attack Defender':
            if self.d_choice == 'Standard Security':
                self.p_success = Constants.D_SProb_UHDH
        elif self.a_choice == 'Attack User':
            if self.u_choice == 'Standard Security':
                if self.d_choice == 'Standard Security':
                    self.p_success = Constants.U_SProb_ULDL
                elif self.d_choice == 'Enhanced Security':
                    self.p_success = Constants.U_SProb_ULDH
            elif self.u_choice == 'Enhanced Security':
                if self.d_choice == 'Standard Security':
                    self.p_success = Constants.U_SProb_UHDL
                elif self.d_choice == 'Enhanced Security':
                    self.p_success = Constants.U_SProb_UHDH
        elif self.a_choice == 'No Attack':
            self.no_atk = True
            self.p_success = 0

        rand=random.random()
        if self.a_choice == 'No Attack':
            self.message = Constants.no_atk_msg
            attacker.payoff = Constants.APayoff_No
            defender.payoff = Constants.DPayoff_No
            user.payoff = Constants.UPayoff_No
        else:
            if rand < self.p_success:
                self.atk_success = True
                self.message = Constants.success_msg
            elif rand > self.p_success:
                self.atk_success = False
                self.message = Constants.fail_msg

        if self.atk_success is True:
            if self.a_choice == 'Attack Defender':
                attacker.payoff = Constants.APayoff_DefS
                defender.payoff = Constants.DPayoff_DefS
                user.payoff = Constants.UPayoff_DefS
            elif self.a_choice == 'Attack User':
                attacker.payoff = Constants.APayoff_UseS
                defender.payoff = Constants.DPayoff_UseS
                user.payoff = Constants.UPayoff_UseS
        elif self.atk_success is False:
            if self.a_choice == 'Attack Defender':
                attacker.payoff = Constants.APayoff_DefF
                defender.payoff = Constants.DPayoff_DefF
                user.payoff = Constants.UPayoff_DefF
            elif self.a_choice == 'Attack User':
                attacker.payoff = Constants.APayoff_UseF
                defender.payoff = Constants.DPayoff_UseF
                user.payoff = Constants.UPayoff_UseF

        self.a_pay = attacker.payoff
        self.d_pay = defender.payoff
        self.u_pay = user.payoff

        if self.subsession.round_number in self.session.vars['paying_rounds']:
            self.a_cum = attacker.payoff
            self.d_cum = defender.payoff
            self.u_cum = user.payoff
        else:
            self.a_cum = 0
            self.d_cum = 0
            self.u_cum = 0


class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'attacker'
        if self.id_in_group == 2:
            return 'defender'
        if self.id_in_group == 3:
            return 'user'

