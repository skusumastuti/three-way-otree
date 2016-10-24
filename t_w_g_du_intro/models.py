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
Behavioral cyber 3 way game intro
"""


class Constants(BaseConstants):
    name_in_url = 't_w_g_du_intro'
    players_per_group = 3
    num_rounds = 2
    total_rounds = 20
    game_rounds = 20
    paid_rounds = 5
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
    APayoff_DefFAbs = c(abs(APayoff_DefF))
    APayoff_UseS = c(1)
    APayoff_UseF = c(0)
    APayoff_No = c(0)
    DPayoff_DefS = c(-2)
    DPayoff_DefSAbs = c(abs(DPayoff_DefS))
    DPayoff_DefF = c(3)
    DPayoff_UseS = c(-0.5)
    DPayoff_UseSAbs = c(abs(DPayoff_UseS))
    DPayoff_UseF = c(2)
    DPayoff_No = c(1)
    UPayoff_DefS = c(0)
    UPayoff_DefF = c(0)
    UPayoff_UseS = c(-0.5)
    UPayoff_UseSAbs = c(abs(UPayoff_UseS))
    UPayoff_UseF = c(3)
    UPayoff_No = c(0.5)
    ACostD = c(2)
    ACostU = c(0.5)
    ACostNo = c(0)
    DCostHS = c(2)
    DCostLS = c(0.5)
    UCostHS = c(1.4)
    UCostLS = c(0)

    a_instr = 't_w_g_du_intro/Ainstr.html'
    d_instr = 't_w_g_du_intro/Dinstr.html'
    u_instr = 't_w_g_du_intro/Uinstr.html'

    success_msg = 'attack successful'
    fail_msg = 'attack failed'
    no_atk_msg = 'no attack'

    q3a = 'Attacking the user where both user and defender have standard security'
    q3b = 'Attacking the defender where both user and defender have standard security'
    q3c = 'Attacking the user where both user and defender have enhanced security'

    q4a = 'Attacker attacks the user and fails'
    q4b = 'Attacker attacks the defender and fails'
    q4c = 'Attacker attacks the defender and succeeds'

    c2a = [('No attack'), ('Attack Defender'), ('Attack User')]
    c2du = [('Having standard security'), ('Having enhanced security')]

    def_train1_correct = 'Defender'
    user_train1_correct = 'User'
    att_train1_correct = 'Attacker'

    def_train2_correct = 'Having an enhanced security against the attacker'
    user_train2_correct = 'Having an enhanced security against the attacker'
    att_train2_correct = 'Attack Defender'

    def_train3_correct = 'Attacking the user where both user and defender have standard security'
    user_train3_correct = 'Attacking the user where both user and defender have standard security'
    att_train3_correct = 'Attacking the user where both user and defender have standard security'

    def_train4_correct = 'Attacker attacks the defender and fails'
    user_train4_correct = 'Attacker attacks the user and fails'
    att_train4_correct = 'Attacker attacks the defender and succeeds'


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

    message = models.CharField(doc="""message displayed to all""")

    a_cost = models.CurrencyField()
    d_cost = models.CurrencyField()
    u_cost = models.CurrencyField()

    att_rand = models.BooleanField(
        doc="""Is the move is randomly generated"""
    )

    def_rand = models.BooleanField(
        doc="""Is the move is randomly generated"""
    )

    user_rand = models.BooleanField(
        doc="""Is the move is randomly generated"""
    )

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


class Player(BasePlayer):

    def role(self):
        if self.id_in_group == 1:
            return 'attacker'
        elif self.id_in_group == 2:
            return 'defender'
        elif self.id_in_group == 3:
            return 'user'

    consent = models.CharField(choices=[
        'I have read the above information, am 18 years of age or older, and I wish to continue with the game.',
        'I am under 18 years of age, and/or do not wish to continue the game'],verbose_name='After having read the above information, please select your preference from the options below:',
        widget=widgets.RadioSelect())

    training1 = models.CharField(choices=[
        ('Attacker'),
        ('Defender'),
        ('User')],
        verbose_name='Your role is',
        widget=widgets.RadioSelect())

    training2a = models.CharField(choices=[('No attack'), ('Attack Defender'), ('Attack User')], widget=widgets.RadioSelect(), blank=True)
    training2du = models.CharField(choices=[('Having standard security'), ('Having enhanced security')], widget=widgets.RadioSelect(), blank=True)

    training3 = models.CharField(choices=[
        Constants.q3a, Constants.q3b, Constants.q3c],
        widget=widgets.RadioSelect())

    training4 = models.CharField(choices=[
        Constants.q4a, Constants.q4b, Constants.q4c],
        widget=widgets.RadioSelect())

    def is_training1_correct(self):
        if self.id_in_group == 1:
            return self.training1 == Constants.att_train1_correct
        if self.id_in_group == 2:
            return self.training1 == Constants.def_train1_correct
        if self.id_in_group == 3:
            return self.training1 == Constants.user_train1_correct

    def is_training2_correct(self):
        if self.id_in_group == 1:
            return self.training2a == Constants.att_train2_correct
        if self.id_in_group == 2:
            return self.training2du == Constants.def_train2_correct
        if self.id_in_group == 3:
            return self.training2du == Constants.user_train2_correct

    def is_training3_correct(self):
        if self.id_in_group == 1:
            return self.training3 == Constants.att_train3_correct
        if self.id_in_group == 2:
            return self.training3 == Constants.def_train3_correct
        if self.id_in_group == 3:
            return self.training3 == Constants.user_train3_correct

    def is_training4_correct(self):
        if self.id_in_group == 1:
            return self.training4 == Constants.att_train4_correct
        if self.id_in_group == 2:
            return self.training4 == Constants.def_train4_correct
        if self.id_in_group == 3:
            return self.training4 == Constants.user_train4_correct