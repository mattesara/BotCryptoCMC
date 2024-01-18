import requests
import time
from datetime import datetime
import schedule
import json

class Bot:                              #classe Bot per connettersi a CMC e ricavare i dati necessari sul mercato delle criptovalute
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'f05c2e94-765e-4aa7-a271-0e424399e9ae',
        }

    def __init__(self, params):
            self.params = params


    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return r['data']

BestCurrencybot = Bot({                         #parametri per ricavare le prime 20 criptovalute nella classifica di CMC
            'start': '1',
            'limit': '20',
            'convert': 'USD'})

Bestbot = Bot({'start': '1',                    #parametri per ricavare le prime 10 criptovalute per movimento percentuale giornaliero
            'limit': '10',
            'convert': 'USD',
            'sort': 'percent_change_24h'})

Worstbot = Bot({                                #parametri per ricavare le ultime 10 criptovalute per movimento percentuale giornaliero
            'start': '1',
            'limit': '10',
            'convert': 'USD',
            'sort': 'percent_change_24h',
            'sort_dir': 'asc'})

Volumebot = Bot({                               #parametri per ricavare tra le prime 100 crypto, quelle con volume superiore a 76000000$
            'start': '1',
            'limit': '100',
            'convert': 'USD',
            'volume_24h_min': '76000000'})

def report():                                                       #funzione per attivare  il Bot, permettendo la pianificazione di esso
    currencies = BestCurrencybot.fetchCurrenciesData()              #utilizzando schedule
    BestVolumeCurrency = currencies[0]
    BestCurrency = currencies[0]
    for currency in currencies:                                                                           #ricerca della cypto con maggior volume di scambio nella classica di CMC
        if currency['quote']['USD']['volume_24h'] > BestVolumeCurrency['quote']['USD']['volume_24h']:     #in seguito stamparla insieme al suo volume in dollari
            BestVolumeCurrency = currency
    print('La criptovaluta con il volume maggiore, tra le prime 20, nelle ultime 24 ore è ' + (BestVolumeCurrency['symbol']))
    print(BestVolumeCurrency['quote']['USD']['volume_24h'], '$')
    for currency in currencies:                                                                                     #ricerca della crypto con maggior incremento percentuale
        if currency['quote']['USD']['percent_change_24h'] > BestCurrency['quote']['USD']['percent_change_24h']:     #nella classifica di CMC
            BestCurrency = currency
    print("La criptovaluta con l'incremento percentuale maggiore, tra le prime 20, nelle ultime 24 ore è " + (BestCurrency['symbol']))
    print(BestCurrency['quote']['USD']['percent_change_24h'], '%')

    BestCurrencies = Bestbot.fetchCurrenciesData()
    BestCrypto= []

    for BestCurrencies in BestCurrencies:                                               #dopo aver creato la lista per contenere le top 10 crypto per incremento percentuale
        BestCrypto.append(BestCurrencies['name'])                                       #la utlizzo per ordinare e stamparne i nomi
    print('Le migliori 10 criptovalute per incremento percentuale giornaliero sono:')
    print(BestCrypto)

    WorstCurrencies = Worstbot.fetchCurrenciesData()
    WorstCrypto = []

    for WorstCurrencies in WorstCurrencies:
        WorstCrypto.append(WorstCurrencies['name'])
    print('Le peggiori 10 criptovalute per incremento percentuale giornaliero sono:')
    print(WorstCrypto)

    Values = []
    WeekDifference = []
    YesterdayPrice = []
    for currencies in currencies:
        Values.append(currencies['quote']['USD']['price'])               #lista creata per contenere i prezzi di ciascuna top 20 crypto nella classifica CMC
        WeekDifferenceValues = 1000 * currencies['quote']['USD']['percent_change_7d'] / 100
        WeekDifference.append(WeekDifferenceValues)
        PercentChange = 100 + (currencies['quote']['USD']['percent_change_24h'])
        InversePercent = (currencies['quote']['USD']['price']) * 100 / PercentChange
        YesterdayPrice.append(InversePercent)


    TotPrice = sum(Values)                                                               # somma dei prezzi delle crypto contenuti nella lista Values
    print("Il denaro necessario per acquistare un'unità di ciascuna delle prime 20 criptovalute è " + str(TotPrice),
          "$")

    VolumeCurrencies = Volumebot.fetchCurrenciesData()
    VolumeValues = []


    for VolumeCurrencies in VolumeCurrencies:
        VolumeValues.append(VolumeCurrencies['quote']['USD']['price'])                   #lista creata per contenere i prezzi crypto con volume
                                                                                         #superiore a 76.000.000$
    VolumeTotPrice = sum(VolumeValues)                                                   #somma dei prezzi delle crypto contenute nella lista VolumeValues
    print("Il denaro necessario per acquistare un'unità di tutte le criptovalute con volume giornaliero superiore a 76.000.000 $ è " + str(
            VolumeTotPrice), "$")

    TotYesterdayPrice = sum(YesterdayPrice)
    print('Il prezzo totale delle crypto Top 20 del giorno prima è: ' + str(TotYesterdayPrice) + '$')
    Percent = (((TotPrice - TotYesterdayPrice) / TotYesterdayPrice) * 100)                     #con Percent calcolo la percentuale da YesterdayPrice
    if Percent > 0:
        print("La percentuale di guadagno sulle prime 20 criptovalaute è: " + str(Percent) + '%')
    else:
        print("La percentuale di perdita sulle prime 20 criptovalaute è: " + str(Percent) + '%')

    TotWeekDifference = sum(WeekDifference)                                              #trovo il guadagno/perdita totale delle crypto Top 20 della settimana prima,
    OneWeekPrice = 20000 + (TotWeekDifference)                                            #che questa volta viene sommato al mio investimento totale di 20000$ (1000$ su ciascuna crypto Top 20)
    print('Se la settimana scorsa, avessi investito 1000$ su ciascuna delle prime 20 criptovalute, ora avresti: ' + str(OneWeekPrice) + '$')


    data = {'Crypto con maggior volume(Crypto Top 20)': BestVolumeCurrency['symbol'],    #codice per salvare i dati in un file json
            'Crypto con maggior incremento percentuale giornaliero(Crypto Top 20)': BestCurrency['symbol'],
            'Top 10 crypto con maggior incremento giornaliero': BestCrypto,
            'Top 10 crypto con minor incremento giornaliero': WorstCrypto,
            "Somma dei prezzi di ogni crypto top 20": TotPrice,
            "Somma dei prezzi di ogni crypto con volume superiore a 76.000.000": VolumeTotPrice,
            "Differenza in percentuale totale dal giorno prima su l'acquisto di ciascuna crypto Top 20": Percent,
            "Valore dell' investimento iniziale di 1000$ nella settimana precedente su ciascuna crypto Top 20": OneWeekPrice}
    with open('report.json', 'w') as file:
        json.dump(data, file, indent=7)

schedule.every().day.at('14:30').do(report)

while True:
    schedule.run_pending()
    time.sleep(1)