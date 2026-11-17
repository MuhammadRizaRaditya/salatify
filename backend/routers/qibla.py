"""Router arah kiblat."""

from fastapi import APIRouter
from backend.schemas import QiblaRequest, QiblaResponse
from backend.services.qibla_service import QiblaService
from backend.utils.constants import KAABAH_LATITUDE, KAABAH_LONGITUDE

router = APIRouter(prefix="/qibla", tags=["Arah Kiblat"])
service = QiblaService()


def arah_teks(derajat: float) -> str:
    arah = ["Utara", "Timur Laut", "Timur", "Tenggara", "Selatan", "Barat Daya", "Barat", "Barat Laut"]
    index = int(((derajat + 22.5) % 360) / 45)
    return arah[index]


@router.post("/hitung", response_model=QiblaResponse)
def hitung_kiblat(payload: QiblaRequest):
    derajat = service.bearing_kiblat(payload.latitude, payload.longitude)
    if derajat is None:
        derajat = 0.0
    return QiblaResponse(
        derajat=derajat,
        arah=arah_teks(derajat),
        kaabah_latitude=KAABAH_LATITUDE,
        kaabah_longitude=KAABAH_LONGITUDE,
    )
