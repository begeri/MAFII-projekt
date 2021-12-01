# MAFII-projekt
A 2021/22es tanév őszi félévében MAF2 tárgy nagybeadandója. 

A projekt célja egy algoritmus létrehozása, amely képes értelmes döntéseket hozni, ha van elég gondolkodási ideje. Ezt egy Monte Carlo Tree Search eljárásra alapozva csináljuk.

Az algoritmus egy adott játékállásból felépít egy fát, ami a lehetséges játékfolytatásokat reprezentálja. Minden ciklusban hozzávesz egy új lépést a fához, és onnan egy véletlen játékot lejátsszva nyerő, semleges vagy vesztes állásnak könyveli el.
Az UCB (Upper Confidence Bound) gondoskodik az ígéretes játékállások boncolgatása és a felfedezetlen ágak felderítése közötti egyensúlyról.
