""" Formes Quasi Affines et Calendriers.
    Les formes quasi affines sont des fonctions f définies par :
    
        f(x) = [(ax + r) / b]
    
    où a, b et c sont des entiers avec a > r >= 0 et [x] désigne la 
    valeur entière (floor) de x.
    
    Entre autres, les formes quasi affines sont utiles dans les calculs de
    calendriers.
    Dans son livre 'La saga des calendriers ou le frisson millénariste'
    (Bibliothèque pour la Science, 1998), Jean Lefort en donne une illustration 
    intéressante.
    Cette utilisation des droites discrètes a été proposée en 1992 par A. Troesch :
    
    'Droites discrètes et calendriers' (Albert Troesch)
    https://mathinfo.unistra.fr/websites/math-info/irem/Publications/L_Ouvert/n071/o_71_27-42.pdf

    Bibliographie.
    [1] 'La saga des calendriers' (Jean LEFORT, Pour la Science, 1998).
    [2] 'Calendrical Calculations'
    (Nachum Dershowitz et Edward M. Reingold, Cambridge University Press, 1997).
    [3] 'Droites discrètes et calendriers'
    (Albert TROESCH, Mathématiques et sciences humaines, tome 141, 1998, p. 11-41)
        disponible sur http://www.numdam.org/article/MSH_1998__141__11_0.pdf
    [4] 'Calculs astronomiques à l'usage des amateurs'
    (Jean MEEUS, Société Astronomique de France, Paris, 2014).
"""

# import .outils
# import .fqa
# import .calendrier
#
__all__ = ["fqa", "calendrier", "calendar", "outils"]
