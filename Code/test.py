# -*- coding: utf-8 -*-
# Narzędzie:
# Autor: Wojciech Skoczeń
# Wersja
# Opis
import pandas as pd
import geopandas as gpd
import shapely as shly
########################################################################################################################
########################################################################################################################
def otworz_pl_gis(n_pl,n_warstwy='',sc='C:\\Temp\\Geokoder'):
    '''Funkcja otwierająca popularne formaty GIS i zwracająca wynik jako ramka geopandasa'''
    sc_p=sc+'\\'+n_pl
    try:
        if (n_pl.split('.')[-1]=='json' or n_pl.split('.')[-1]=='shp'
        or n_pl.split('.')[-1]=='geojson'):
            ramka=gpd.read_file(sc_p)
        elif n_pl.split('.')[-1]=='gpkg':
            ramka = gpd.read_file(sc_p, layer=n_warstwy,encoding='utf-8')
        return ramka
    except(UnboundLocalError):
        print('Niewłaściwy format pliku. Funkcja otwiera pliki .json, .geojson, .shp, .gpkg')
########################################################################################################################
########################################################################################################################
def zapisz_gpkg(grd, n_pl, n_bazy, sc='C:\\Temp\\Geokoder',driver='GPKG'):
    '''Funkcja zapisująca ramkę geopandasa do plikowej geobazy '''
    try:
        if isinstance(grd,gpd.geodataframe.GeoDataFrame)==False:
            print('Próbujesz zapisać niedozwolony obiekt.')
        else:
            n_bazy=n_bazy+'.gpkg'
            return grd.to_file(sc+'\\'+n_bazy,layer=n_pl,driver='GPKG',)
    except:
        print('Coś poszło nie tak. Nie mogłem zapisać danych')
########################################################################################################################
########################################################################################################################
def wybierz_geometrie(grd,geom):
    '''Funkcja wybierająca określony typ geometrii z ramki geopandasa'''
    try:
        if isinstance(grd, gpd.geodataframe.GeoDataFrame) == True:
            wyb_geom=grd[grd.geom_type==geom]
        else:
            print('Próbujesz wybrać geometrie z niewłaściwego obiektu')
    except:
        print('Coś poszło nie tak')
    else:
            return wyb_geom
########################################################################################################################
########################################################################################################################
def rozpakuj_xy_pkt(grd):
    try:
        if isinstance(grd, gpd.geodataframe.GeoDataFrame) == True:
            koor = list(zip([kx for kx in grd.geometry.x], [ky for ky in grd.geometry.y]))
            return koor
        else:
            print('Brak właściwego obiektu z którego mogę pobrać współrzędne x,y')
    except:
        print('Coś poszło nie tak. Nie znalazłem obiektów z geometrią')
########################################################################################################################
########################################################################################################################
def rozpakuj_xy_lin_pol(grd):
    try:
        if isinstance(grd,gpd.geodataframe.GeoDataFrame)==True:
            list_ob=[ob.coords for ob in grd.boundary]
            koor= [list(k) for k in list_ob ]
            return koor
        else:
            print('Brak właściwego obiektu z którego mogę pobrać współrzędne x,y')
    except:
        print('Coś poszło nie tak. Nie znalazłem obiektów z geometrią.')
########################################################################################################################
########################################################################################################################
def rozpakuj_xy_ob_geom(grd):
    koordynaty=[]
    try:
        if isinstance(grd, gpd.geodataframe.GeoDataFrame) == True:
            ob_typ_koor=list(zip([typ for typ in grd.geom_type],[ob for ob in grd.geometry]))
            for ob in ob_typ_koor:
                if ob[0]=='Point':
                    k=list(ob[1].coords[0])
                    koordynaty.append(k)
                elif ob[0] in ('Polygon', 'LineString'):
                    k=list(zip(ob[1].boundary.coords.xy[0],ob[1].boundary.coords.xy[1]))
                    koordynaty.append(k)
                else:
                    print('Obiekt jest pusty lub posiada obiekty nieobsługiwane')
        else:
            print('Brak właściwego obiektu z którego mogę pobrać współrzędne x,y')
    except:
        print('Coś poszło nie tak. Nie znalazłem obiektów z geometrią.')
    else:
        return koordynaty
########################################################################################################################
#######################################################################################################################

if __name__=='__main__':
    a_pkt=otworz_pl_gis('PKt.shp')
    b_pol=otworz_pl_gis('Dzielnice.shp')
    c_zmiesz=b_pol.append(a_pkt)
    r=pd.DataFrame()
    print(r)
    rg=gpd.GeoDataFrame()
    rg['geometry']=None
    wynik=rozpakuj_xy_ob_geom(c_zmiesz)
    c_zmiesz['Kolumn_wyn']=wynik
    c_zmiesz.to_excel('C:\\Temp\\Geokoder\\Ostat.xlsx',encoding='utf-8')


