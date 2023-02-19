#!/usr/bin/env python
# - *- coding: utf-8 -*-

import spade
import time
import string
string.letters
import random
from random import randint

class AgentAutomat(spade.Agent.Agent):

#NAKON N-TOG KRUGA POSLATI NA KRAJ
    class OdabirPojma(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            if self.myAgent.agent1 == 1:
                self.myAgent.prvi = 'Agent 1'
                self.myAgent.drugi = 'Agent 2'
            else:
                self.myAgent.prvi = 'Agent 2'
                self.myAgent.drugi = 'Agent 1'

            # self.myAgent.brojac = 1

            print "--------------------------------------"
            print "Brojač krugova: {}".format(self.myAgent.brojac)
            print "Odabran broj KRUGOVA: {}".format(self.myAgent.brojKrugova)

            print "Bodovi Agenta 1: {}".format(self.myAgent.bodoviAgent1)
            print "Bodovi Agenta 2: {}".format(self.myAgent.bodoviAgent2)

            print "--------------------------------------"

            if (self.myAgent.brojac != self.myAgent.brojKrugova):
                if (self.myAgent.brojac == 0):
                    print "Papir - Kamen - Škare .... prvi je..."
                    self.myAgent.prviIgra = randint(0,99)
                    if(self.myAgent.prviIgra % 2 == 1):
                        self.myAgent.agent1 = 1
                        self.myAgent.agent2 = 0
                        self.myAgent.prvi = 'Agent 1'
                        self.myAgent.drugi = 'Agent 2'
                    else:
                        self.myAgent.agent1 = 0
                        self.myAgent.agent2 = 1
                        self.myAgent.prvi = 'Agent 2'
                        self.myAgent.drugi = 'Agent 1'

                    self.myAgent.brojac = self.myAgent.brojac + 1
                    time.sleep(2)
                    print self.myAgent.prvi
                    #self._exitcode = self.myAgent.PRIJELAZ_U_POGADJAJ1
                else:
                    print "Igru započinje {}".format(self.myAgent.prvi)
                    time.sleep(1)
                    self.myAgent.brojac = self.myAgent.brojac + 1

                print "--------------------------------------"

                print "Stanje ODABIRA POJMA!"
                time.sleep(1)
                #print "lista Biranih slova: {}".format(self.myAgent.biranaSlova)
                self.myAgent.biranaSlova[:] = {}
                print "lista Biranih slova: {}".format(self.myAgent.biranaSlova)
                time.sleep(1)
                #print "lista Asocijacija: {}".format(self.myAgent.asocijacije)
                self.myAgent.asocijacije[:] = {}
                print "lista Asocijacija: {}".format(self.myAgent.asocijacije)
                time.sleep(1)
                #print "INDEX ASOCIJACIJE: {}".format(self.myAgent.asocind)
                self.myAgent.asocind = 4
                #print "INDEX ASOCIJACIJE: {}".format(self.myAgent.asocind)

                self.myAgent.bodovi = 5
                self.myAgent.slucajniBroj = randint(0, 19)
                self.myAgent.slucajniPojam = self.myAgent.odaberi[self.myAgent.slucajniBroj]

                #print "Odabran je broj: {}".format(self.myAgent.slucajniBroj)
                #print "...koji odgovara slučajnom pojmu: {}".format( self.myAgent.slucajniPojam)
                #time.sleep(2)
                print "{}: Zamišljam pojam...".format(self.myAgent.prvi)
                time.sleep(1)

                print "Zamislio sam pojam. Pogodi što se krije iza upitnika :D..."
                self.myAgent.skriveniPojam = len(self.myAgent.slucajniPojam) * "? "
                print(self.myAgent.skriveniPojam)
                self._exitcode = self.myAgent.PRIJELAZ_U_POGADJAJ1

            else:
                print "Agenti su odigrali {} kruga/ova, što je jednako odabranom broju izmjena Agenata.".format(self.myAgent.brojac)
                self._exitcode = self.myAgent.PRIJELAZ_KRAJ
                #print("bla")


        def _process(self):
            pass
#POGADANJE SLOVA U ZAMISLJENOM POJMU
    class Pogadjaj(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            #print "-------------------broj dostupnih asocijacija: {}".format(self.myAgent.asocind)
            if self.myAgent.bodovi == 0:
                print "{}: Potrošio si sve pokušaje, gubiš bodove iz ovog kruga. Sad ja pogađam.".format(self.myAgent.prvi)
                self._exitcode = self.myAgent.PRIJELAZ_U_ZAMJENA_AS
            else:
                print "---------------------------------------------------"
                time.sleep(1)
                print "Stanje POGAĐAJ !!!"

                print "Lista biranih slova: {}".format(self.myAgent.biranaSlova)

                print self.myAgent.drugi + " pogađa pojam...odabir slova.. "
                self.myAgent.slovo = random.choice(string.ascii_lowercase)
                time.sleep(2)
                print "Biram slovo: {}".format(self.myAgent.slovo)
                self._exitcode = self.myAgent.PRIJELAZ_U_PROVJERI

        def _process(self):
            pass
#PROVJERA PONUDENOG SLOVA
    class Provjeri(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            print "--------------------------------------"
            print "Stanje PROVJERA !!"

            if (self.myAgent.slovo not in self.myAgent.slucajniPojam):
                print self.myAgent.prvi + ":Izabrano slovo se ne nalazi u zamišljenom pojmu."
                if (self.myAgent.slovo not in self.myAgent.biranaSlova):
                    self.myAgent.biranaSlova.append(self.myAgent.slovo)
                    self.myAgent.asocijacije.append(self.myAgent.dictionary[self.myAgent.slucajniPojam][self.myAgent.bodovi - 1])
                    self.myAgent.bodovi = self.myAgent.bodovi - 1
                    print self.myAgent.prvi + ":Gubiš 1 bod, nudim asocojaciju na pojam: {}".format(self.myAgent.asocijacije)
                else:
                    time.sleep(2)
                    print"Odabrano slovo je već bilo ponuđeno, {} ponovno bira slovo.".format(self.myAgent.drugi)
                    self._exitcode = self.myAgent.PRIJELAZ_U_POGADJAJ3
            else:
                print("Odabrno slovo nalazi se u zamišljenom pojmu")


            self.myAgent.pogadjam = ''
            for s in list(self.myAgent.slucajniPojam):
                if (s == self.myAgent.slovo):
                    self.myAgent.pogadjam = self.myAgent.pogadjam + self.myAgent.slovo
                elif (s == '_'):
                    self.myAgent.pogadjam = self.myAgent.pogadjam + '_'
                else:
                    self.myAgent.pogadjam = self.myAgent.pogadjam + '?'
            a = self.myAgent.pogadjam
            b = self.myAgent.skriveniPojam.replace(" ","")
            self.myAgent.skriveniPojam = ''
            for x, y in zip(a, b):
                if x != '?':
                    self.myAgent.skriveniPojam = self.myAgent.skriveniPojam + x
                else:
                    self.myAgent.skriveniPojam = self.myAgent.skriveniPojam + y
            print(self.myAgent.skriveniPojam)
            self.myAgent.slucajniBroj = randint(0, 19)
            #print "odabran je slučajni broj : {}".format(self.myAgent.slucajniBroj)
            time.sleep(1)
            if (self.myAgent.slucajniBroj % 2) == 1:
                print self.myAgent.drugi + ": Želim ponuditi riješenje"
                self._exitcode = self.myAgent.PRIJELAZ_U_POGODI_POJAM
            else:
                print self.myAgent.drugi + ": Nemam moguće riješenje, biram novo slovo."
                self._exitcode = self.myAgent.PRIJELAZ_U_POGADJAJ3

        def _process(self):
            pass
#PROVJERA PONUDENOG ODGOVORA
    class PogodiPojam(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            print "--------------------------------------"
            print("STANJE POGODI POJAM !!!!")
            time.sleep(1)
            asocijacijaPojma = self.myAgent.dictionary[self.myAgent.slucajniPojam][self.myAgent.asocind]
            print "Poznajem asocijaciju: {}".format(asocijacijaPojma)
            for k,v in self.myAgent.dictionary.items():
                #print v[self.myAgent.asocind]
                if v[self.myAgent.asocind] == asocijacijaPojma:
                    #print(self.myAgent.asocind)
                    #print(k)
                    self.myAgent.pokusajPogotka = k
                    break
                    #return self.myAgent.pokusajPogotka
            print self.myAgent.drugi + ": Zamislio si pojam {}".format(self.myAgent.pokusajPogotka)
            self.myAgent.asocind = self.myAgent.asocind - 1
            if self.myAgent.pokusajPogotka == self.myAgent.slucajniPojam:
                print "Pojam je pogodjen, Agenti se mijenjaju"
                time.sleep(2)
                self._exitcode = self.myAgent.PRIJELAZ_U_ZAMJENA
            else:
                print "Pojam nije pogodjen,{} pogadja ponovno".format(self.myAgent.drugi)
                time.sleep(2)
                self._exitcode = self.myAgent.PRIJELAZ_U_POGADJAJ4

        def _process(self):
            pass
# ZAMJENA
    class Zamjena(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            print "--------------------------------------"
            print "STANJE ZAMJENA !!!!!"
            if self.myAgent.agent1 == 0:
                self.myAgent.bodoviAgent1 = self.myAgent.bodoviAgent1 + self.myAgent.bodovi
            else:
                self.myAgent.bodoviAgent2 = self.myAgent.bodoviAgent2 + self.myAgent.bodovi
            self.myAgent.agent1 = (self.myAgent.agent1 + 1) % 2
            self._exitcode = self.myAgent.PRIJELAZ_U_ODABIR_POJMA

        def _process(self):
            pass
# KRAJ
    class Kraj(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            print "--------------------------------------"
            print "STANJE KRAJ !!! IGRA ZAVRŠENA !!!"
            if (self.myAgent.bodoviAgent1 == self.myAgent.bodoviAgent2):
                print "Agenti imaju jednak broj bodova. Izjednačeno !!"
            elif(self.myAgent.bodoviAgent1 > self.myAgent.bodoviAgent2):
                print "Pobijedio je Agent 1, broj ostvarenih bodova: {}".format(self.myAgent.bodoviAgent1)
            else:
                print "Pobijedio je Agent 2, broj ostvarenih bodova: {}".format(self.myAgent.bodoviAgent2)
            self.myAgent._kill()

        def _process(self):
            pass

    def _setup(self):

        time.sleep(2)
        print "Igra se pokreće . . ."
        time.sleep(2)
        print "Agent 1 i Agent 2 su budni, postavi igru..."
        time.sleep(2)

        #Zanje agenata
        self.dictionary = {'struja':['more','golf','svijetlo','Tesla','koristi se za napajanje'],
                        'balerina':['ples','Labudje jezero','Mija Corak Slavenska','Crni Labud','baletan'],
                        'izbor':['parlament','alternativa','birati','imati mogucnost','hocu ili necu'],
                        'pogon':['tvornica','pusti radnike u..','auto moze imati prednji i zadnji..','mlazni..','motorni..'],
                        'parobrod':['pramac','dimnjak','para','plovi','more'],
                        'alpinizam':[ 'sport','alternativa','puno opreme','penjanje','visoko'],
                        'dijeta':['izgubiti kile','vaga','linija','ljeto','more'],
                        'dinamo':['Zagreb','klub','Vatreni','struja','koristi se za napajanje'],
                        'kanarski_otoci':['kanari','otočje od sedam otoka','brod','posjetitit','putovanje..'],
                        'monte_carlo':['neslužbeni glavni grad','svjetska prvenstvima u boksu i backgammonu','Monako','posjetiti','putovanje..'],
                        'srcani_udar':['puls','bol','srce','napor','more'],
                        'grinch':['ne voli Bozic','zeleno','zlocest','malen','bozic'],
                        'morske_orgulje':['Zadar','glazba','pozdrav suncu','posjetiti','more'],
                        'kucanice':['pas','postar','ljubavnica','serija','zena'],
                        'virginia_wolf':['konjanik','mjesec','djevica','vuk','zena'],
                        'partenon':['antički hram','Darius','Atena','božica','povijest'],
                        'petar_zrinski':['supruga Ana Katarina Zrinski','roden je 6. lipnja 1621. u Vrbovcu','vojskovoda i pjesnik','ban','povijest'],
                        'sljivovica':['moze se praviti od vise sorti iste vocke','bistrice','rakija','ljuto','slavonija'],
                        'neptun':['8 kamencic od sunca','rimski bog mora','nebo','malen','visoko'],
                        'katastar':['linija','ral','hektar','cestice','vaga']}

        self.odaberi = ['struja', 'balerina', 'izbor', 'pogon', 'parobrod', 'alpinizam', 'dijeta', 'dinamo', 'kanarski_otoci', 'monte_carlo', 'srcani_udar', 'grinch', 'morske_orgulje', 'kucanice', 'virginia_volf', 'partenon', 'petar_zrinski', 'sljivovica', 'neptun', 'katastar']


        
        self.brojac = 0  #brojac krugova

        #self.slucajniPojam = "pojam{}".format(self.slucajniBroj)
        #self.slucajniPojam = self.odaberi[self.slucajniBroj]
        #print self.slucajniPojam
        #self.odabrano = ''
        self.slucajniPojam = ''
        self.asocijacije = [] #lista ponuđenih asocijacija
        self.asocind = 4
        self.skriveniPojam = '' # pojam koji se prikazuje, umjesto slova ??? koje drugi igrač otkriva redom
        self.slovo = ''  # slovo koje bira drugi igrač
        self.biranaSlova = []  #lista biranih slova po jednom krugu
        self.pogadjam= ''  #pojam koji želim saznati  i otkrivam slovo po slovo
        self.pokusajPogotka = '' #STANJE POGOTKA pogađamo skriveni pojam
        #self.duzinaPogadjam = len(self.pogadjam)
        #self.brojac = 0
        self.brojKrugova = raw_input("Koliko krugova igramo :) ?")
        self.brojKrugova = int(self.brojKrugova)
        self.bodoviAgent1 = 0
        self.bodoviAgent2 = 0
        self.agent1 = 1
        self.prvi = ''
        self.drugi = ''
        #self.agent2 = 0

        time.sleep(1)

        self.STANJE_ODABIR_POJMA = 1
        self.STANJE_POGADJAJ = 2
        self.STANJE_PROVJERI = 3
        self.STANJE_POGODI_POJAM = 4
        self.STANJE_ZAMJENA = 5
        self.STANJE_KRAJ = 6

        self.PRIJELAZ_PRETPOSTAVLJENI = 0
        self.PRIJELAZ_U_POGADJAJ1 = 100
        self.PRIJELAZ_U_PROVJERI = 200
        self.PRIJELAZ_U_ZAMJENA_AS = 201
        self.PRIJELAZ_U_POGADJAJ3 = 300
        self.PRIJELAZ_U_POGODI_POJAM = 301
        self.PRIJELAZ_U_POGADJAJ4 = 400
        self.PRIJELAZ_U_ZAMJENA = 401
        self.PRIJELAZ_U_ODABIR_POJMA = 500
        self.PRIJELAZ_U_KRAJ = 600
        self.PRIJELAZ_KRAJ = 601

        self.p = spade.Behaviour.FSMBehaviour()
        self.p.registerFirstState(self.OdabirPojma(), self.STANJE_ODABIR_POJMA)
        self.p.registerState(self.Pogadjaj(), self.STANJE_POGADJAJ)
        self.p.registerState(self.Provjeri(), self.STANJE_PROVJERI)
        self.p.registerState(self.PogodiPojam(), self.STANJE_POGODI_POJAM)
        self.p.registerState(self.Zamjena(), self.STANJE_ZAMJENA)
        self.p.registerState(self.Kraj(), self.STANJE_KRAJ)

        self.p.registerTransition(self.STANJE_ODABIR_POJMA, self.STANJE_POGADJAJ, self.PRIJELAZ_U_POGADJAJ1)
        self.p.registerTransition(self.STANJE_ODABIR_POJMA, self.STANJE_KRAJ, self.PRIJELAZ_KRAJ)
        self.p.registerTransition(self.STANJE_POGADJAJ, self.STANJE_PROVJERI, self.PRIJELAZ_U_PROVJERI)
        self.p.registerTransition(self.STANJE_POGADJAJ, self.STANJE_ZAMJENA, self.PRIJELAZ_U_ZAMJENA_AS)
        self.p.registerTransition(self.STANJE_PROVJERI, self.STANJE_POGADJAJ, self.PRIJELAZ_U_POGADJAJ3)
        self.p.registerTransition(self.STANJE_PROVJERI, self.STANJE_POGODI_POJAM, self.PRIJELAZ_U_POGODI_POJAM)
        self.p.registerTransition(self.STANJE_POGODI_POJAM, self.STANJE_ZAMJENA, self.PRIJELAZ_U_ZAMJENA)
        self.p.registerTransition(self.STANJE_POGODI_POJAM, self.STANJE_POGADJAJ, self.PRIJELAZ_U_POGADJAJ4)
        self.p.registerTransition(self.STANJE_ZAMJENA, self.STANJE_ODABIR_POJMA, self.PRIJELAZ_U_ODABIR_POJMA)

        # p.registerTransition()
        self.addBehaviour(self.p, None)


if __name__ == '__main__':
    a = AgentAutomat("ka@127.0.0.1", "tajna")
    a.start()