"""Konstanta shared backend SALATIFY."""

API_PRAYER_TIMES = "https://api.aladhan.com/v1/timings"
API_QURAN_SURAH = "https://equran.id/api/v2/surah"
KAABAH_LATITUDE = 21.4225
KAABAH_LONGITUDE = 39.8262
DEFAULT_CALC_METHOD = "mwml"
CALCULATION_METHODS = {
    "mwml": "Kementerian Agama RI",
    "isna": "ISNA (Amerika)",
    "makkah": "Majlis Ugama Makkah",
    "karachi": "Majlis Ugama Karachi",
    "tehran": "Institut Geofisik Tehran",
}
