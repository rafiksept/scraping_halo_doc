import requests
import gspread
import json
import os 
from google.oauth2.service_account import Credentials
import pandas as pd
import time


load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_info(
    json.loads(SERVICE_ACCOUNT_FILE),
    scopes=scopes
)

gc = gspread.authorize(credentials)

sh = gc.open("data nama halodoc").sheet1

last_update = 0

categories = ["disfungsi-ereksi", "hormon-wanita", "disfungsi-ereksi",
              "kondom-dan-pelumas-1", "perawatan-kewanitaan-2", "supplement-pria",
              "test-pack","orang-dewasa", "lansia", "susu-khusus-1","susu-medis-khusus",
              "susu-formula-bayi", "susu-formula-anak","obat-12", "inhaler", "perangkat-dan-aksesoris",
              "kaleng-oksigen-1", "perlengkapan-mandi", "perawatan-kulit-1", "krim-ruam", "lainnya-22", "telon-dan-kayu-putih",
              "popok","tisu-basah","makanan-dan-snack","peralatan-makan","susu-2","susu-khusus","plester-penurun-panas",
              "dekongestan-dan-minyak", "hidung-tersumbat","perawatan-ibu","nutrisi-bersalin", "perlengkapan-menyusui",
              "perlengkapan-pembersih", "sanitizer-dan-antiseptik-1", "lainnya-14", "batuk-dan-flu-5", "nasal-spray-dan-dekongestan",
              "balsem-dan-minyak-esensial", "untuk-bayi-dan-anak", "perawatan-herbal" , "pereda-demam-dan-nyeri","untuk-bayi-dan-anak-1",
              "perawatan-herbal", "asam-lambung-dan-gerd","mual-dan-muntah", "diare-1", "infeksi-cacing", "sembelit-dan-wasir",
              "obat-alergi", "pereda-gatal","sariawan-dan-herpes-mulut","obat-tetes-telinga","obat-kumur-antiseptik","kebersihan-hidung",
              "pelega-tenggorokan","gatal-kering-dan-merah","lainnya-1","jerawat","dermatitis-dan-eksim","infeksi-kulit",
              "lainnya-2","antibiotik-3", "antijamur","antivirus", "tulang-dan-osteoporosis", "asam-urat-dan-radang-sendi",
              "relaksan-otot", "balsem-dan-minyak","kandung-kemih-dan-ginjal","pria","wanita-1","pil-kontrasepsi","lainnya-3",
              "perawatan-wajah","perawatan-tubuh", "perawatan-kulit-berjerawat","perawatan","acne-patch-dan-gel","sun-care",
              "badan-gigi-rambut", "perawatan-kewanitaan-1","deodoran-dan-pewangi","produk-sekali-pakai", "lainnya-15", "wajah",
              "bibir","kuku","aksesoris-2","perawatan-wajah-1","perawatan-tubuh-1","perawatan-rambut","deodoran-dan-pewangi-1",
              "pisau-cukur","lainnya-16","vitamin-a-b-dan-e","vitamin-c","vitamin-d","multivitamin","mineral","imunitas-dan-antioksidan",
              "kehamilan-dan-menyusui","anemia","menopause","multivitamin-3","imun-booster","anemia-1","penambah-nafsu-makan",
              "rambut-kulit-dan-kuku","vitamin-e","antioksidan","kesehatan-prostat","vitalitas-dan-stamina","probiotik","enzim-pencernaan",
              "serat","tulang-dan-gigi","persendian","penurun-berat-badan","penambah-berat-dan-otot","nutrisi-lainnya","snack-sehat",
              "produk-minuman","minyak-ikan","mata-1","jantung-dan-hati","ginjal-dan-kandung-kemih","otak","obat-herbal","habbatussauda-dan-zaitun",
              "madu-dan-kurma","lainnya-5","dewasa","anak","pengobatan-covid","suplemen-dan-herbal","masker-dan-pelindung","sanitizer-dan-antiseptik",
              "alat-tes-mandiri","kaleng-oksigen","termometer","oximeter","asma-2","diabetes-6","penyakit-jantung-1", "pelindung","antiseptik-dan-disinfektan",
              "kesuburan-dan-kehamilan","covid-19-3","lainnya-8","termometer-1","oksimeter","pengukur-tekanan-darah","tes-gula-darah",
              "timbangan","lainnya-9","jarum-tes","swab-alkohol","jarum-insulin","antiseptik-2","perban","perawatan-luka","pelindung-lutut",
              "stoking-kompresi","penyangga-tangan","alat-bantu-dengar-2","aksesoris","celana-sunat","urinal","perlak-dan-popok-dewasa",
              "alat-bantu-mobilitas","lainnya-10","obat","vitamin-dan-herbal","gula-diabetes","nutrisi-diabetes","alat-monitoring-3","lainnya-11",
              "lanset-jarum-dan-swab","insulin","hipertensi-1","kolesterol","penyakit-jantung","vitamin-dan-herbal-2","makanan-dan-nutrisi",
              "alat-monitoring-4","lanset-jarum-dan-swab-1","lensa-kontak-minus","lensa-kontak-plano","cairan-lensa-kontak", "aksesoris"

              ]


name_obat = []
category_array = []
slug_array = []


for category in categories : 
    print(category)
    for i in range(1, 100):
        url = f'https://magneto.api.halodoc.com/api/v1/buy-medicine/categories/{category}/products?page={i}&size=20'


        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print("berhasil")
            if "result" in data:
                leng_data = len(data["result"])
                for j in range(0 , leng_data) :
                    last_update = last_update + 1
                    name_obat.append(data["result"][j]["name"])
                    slug_array.append(data["result"][j]["slug"])
                    category_array.append(category)
            else :
                print("tidak ada data")
                break

        else :
            print("gagal")
            break

    time.sleep(3) # Sleep for 3 seconds



df = pd.DataFrame({
    "name" : name_obat,
    "category" : category_array,
    "slug" : slug_array
})

df.to_csv("data_nama_obat4.csv")