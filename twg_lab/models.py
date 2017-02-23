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
    name_in_url = 'twg_lab'
    players_per_group = 3
    num_rounds = 20
    participation = 1
    minimal_bonus = 1
    max_bonus = 7

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
    DPayoff_DefS = c(-1.5)
    DPayoff_DefF = c(2.5)
    DPayoff_UseS = c(-1)
    DPayoff_UseF = c(1)
    DPayoff_No = c(0.5)
    UPayoff_DefS = c(0)
    UPayoff_DefF = c(0)
    UPayoff_UseS = c(-1.5)
    UPayoff_UseF = c(2.5)
    UPayoff_No = c(0.5)
    ACostD = c(3)
    ACostU = c(1)
    ACostNo = c(0)
    DCostHS = c(2)
    DCostLS = c(0.8)
    UCostHS = c(1.4)
    UCostLS = c(0)

    a_instr = 'twg_lab/Ainstr.html'
    d_instr = 'twg_lab/Dinstr.html'
    u_instr = 'twg_lab/Uinstr.html'

    success_msg = 'attack successful'
    fail_msg = 'attack failed'
    no_atk_msg = 'no attack'

    atk_train_ans = '2'
    def_train_ans = '0.5'
    user_train_ans = '0'


class Subsession(BaseSubsession):
	pass

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

    p_success = models.FloatField(default=0)

    atk_success = models.BooleanField(
        doc="""Whether an attack was successful"""
    )

    no_atk = models.BooleanField(
        doc="""Whether there is no attack"""
    )

    a_skipped = models.BooleanField()
    d_skipped = models.BooleanField()
    u_skipped = models.BooleanField()

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
""""
        if self.subsession.round_number in self.session.vars['paying_rounds']:
            if self.a_skipped:
                self.a_cum = 0
            else:
                self.a_cum = attacker.payoff
            if self.d_skipped:
                self.d_cum = 0
            else:
                self.d_cum = defender.payoff
            if self.u_skipped:
                self.u_cum = 0
            else:
                self.u_cum = user.payoff
        else:
            self.a_cum = 0
            self.d_cum = 0
            self.u_cum = 0
"""

class Player(BasePlayer):

    turk_id = models.CharField(verbose_name='Please enter your Mechanical Turk ID', widget=widgets.TextInput())

    email = models.CharField(verbose_name='Please enter the e-mail address where we can send you the reward should you obtain the highest score across all the groups', widget=widgets.TextInput())

    clear = models.PositiveIntegerField(choices=[
        [1,'Very clear'],
        [2,'Somewhat clear'],
        [3,'Neither clear nor unclear'],
        [4,'Somewhat unclear'],
        [5,'Very unclear']
        ],
        verbose_name='How clear were the instructions to play the game?',
        widget=widgets.RadioSelectHorizontal())

    timing_instr = models.PositiveIntegerField(choices=[
        [1,'Very long'],
        [2,'Somewhat long'],
        [3,'Just right'],
        [4,'Somewhat short'],
        [5,'Very short'],
        ],
        verbose_name='How was the allocated timing to read the instructions? i.e. Did you have enough time to read the instructions before the page automatically forwards?',
        widget=widgets.RadioSelectHorizontal())

    timing_dec = models.PositiveIntegerField(choices=[
        [1,'Very fast'],
        [2,'Somewhat fast'],
        [3,'Just right'],
        [4,'Somewhat slow'],
        [5,'Very slow']
        ],
        verbose_name='How was the allocated timing for the decision making page? (The page each round that asks for your decision) i.e. Did you have enough time to make an informed decision before the page automatically forwards?',
        widget=widgets.RadioSelectHorizontal())

    timing_res = models.PositiveIntegerField(choices=[
        [1,'Very fast'],
        [2,'Somewhat fast'],
        [3,'Just right'],
        [4,'Somewhat slow'],
        [5,'Very slow']
        ],
        verbose_name='How was the allocated timing for the page displaying the results of the game? (The page that shows the outcome for each round) i.e. Did you have enough time to read the results of each round before the page automatically forwards?',
        widget=widgets.RadioSelectHorizontal())

    diff = models.PositiveIntegerField(choices=[
        [1,'Very easy'],
        [2,'Somewhat easy'],
        [3,'Neither easy nor difficult'],
        [4,'Somewhat difficult'],
        [5,'Very difficult']
         ],
        verbose_name='How easy was it to understand the goal of the game?',
        widget=widgets.RadioSelectHorizontal())

    comment = models.CharField(verbose_name='Please write any comments or suggestions about the game', widget=widgets.Textarea())

    def role(self):
        if self.id_in_group == 1:
            return 'attacker'
        if self.id_in_group == 2:
            return 'defender'
        if self.id_in_group == 3:
            return 'user'

